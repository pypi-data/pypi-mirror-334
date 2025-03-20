//==============================================================================
// Copyright 2025 Vajra Team; Georgia Institute of Technology
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//==============================================================================
#include "native/scheduler/replica_schedulers/trackers/KvpStateTracker.h"

#include <algorithm>
#include <cmath>

using vajra::KvpStateTracker;

KvpStateTracker::KvpStateTracker(const ModelConfig& model_config,
                                 const CacheConfig& cache_config,
                                 const ParallelConfig& parallel_config)
    : model_config_(model_config),
      cache_config_(cache_config),
      parallel_config_(parallel_config),
      kvp_size_(parallel_config.kv_parallel_size) {
  // Initialize max tokens per KVP group
  if (kvp_size_ == 1) {
    max_num_tokens_per_kvp_group_ = model_config_.max_model_len;
  } else {
    ASSERT_VALID_ARGUMENTS(parallel_config_.max_num_tokens_per_kvp_group > 0,
                           "max_num_tokens_per_kvp_group must be positive");
    ASSERT_VALID_ARGUMENTS(
        static_cast<int>(parallel_config_.max_num_tokens_per_kvp_group) >
            static_cast<int>(cache_config_.block_size),
        "max_num_tokens_per_kvp_group must be greater than block_size");
    ASSERT_VALID_ARGUMENTS(
        parallel_config_.max_num_tokens_per_kvp_group %
                cache_config_.block_size ==
            0,
        "max_num_tokens_per_kvp_group must be a multiple of block_size");
    max_num_tokens_per_kvp_group_ =
        parallel_config_.max_num_tokens_per_kvp_group;
  }

  // Calculate max blocks per KVP group
  max_num_blocks_per_kvp_group_ = static_cast<int>(
      std::ceil(static_cast<double>(max_num_tokens_per_kvp_group_) /
                cache_config_.block_size));
  max_num_blocks_per_kvp_group_ =
      std::min(max_num_blocks_per_kvp_group_, cache_config_.num_gpu_blocks);

  // Calculate max sequence length
  max_seq_len_ =
      kvp_size_ * max_num_blocks_per_kvp_group_ * cache_config_.block_size;

  // Initialize block managers for each KVP group
  for (int i = 0; i < kvp_size_; ++i) {
    block_managers_map_[i] = std::make_unique<BlockSpaceManager>(
        cache_config_.block_size, cache_config_.num_gpu_blocks,
        model_config_.max_model_len);
  }

  // Initialize prefill work tracker
  kvp_group_pending_prefill_work_.resize(kvp_size_, 0);

  // Initialize batch tracker
  current_batch_tracker_ = nullptr;
}

void KvpStateTracker::StartBatchFormation() {
  current_batch_tracker_ = std::make_unique<KvpBatchTracker>(kvp_size_);
}

std::vector<int> KvpStateTracker::GetBatchTrackerQTokens(
    const std::shared_ptr<vajra::Sequence> seq) const {
  const_cast<KvpStateTracker*>(this)->EnsureBatchTracker();
  std::vector<int> active_kvp_group_ids = GetActiveKvpGroupIds(seq);
  return current_batch_tracker_->GetQTokensForKvpGroups(active_kvp_group_ids);
}

std::vector<int> KvpStateTracker::GetBatchTrackerFreeGroups() const {
  const_cast<KvpStateTracker*>(this)->EnsureBatchTracker();
  return current_batch_tracker_->GetFreeKvpGroups();
}

void KvpStateTracker::AddSequenceToBatch(
    const std::shared_ptr<vajra::Sequence> seq, int num_q_tokens,
    const std::vector<int>& active_kvp_group_ids) {
  EnsureBatchTracker();
  auto [num_processed_tokens, kv_token_info] =
      GetSequenceKvTokenInfo(seq, active_kvp_group_ids);
  current_batch_tracker_->AddSequence(seq, num_q_tokens, active_kvp_group_ids,
                                      kv_token_info, num_processed_tokens);
}

std::tuple<std::vector<std::shared_ptr<vajra::Sequence>>, std::vector<int>,
           std::vector<int>, std::vector<int>, std::vector<int>>
KvpStateTracker::GetBatchTrackerPerGroupInfo(int kvp_group_id) const {
  const_cast<KvpStateTracker*>(this)->EnsureBatchTracker();
  return std::make_tuple(
      current_batch_tracker_->GetPerGroupSequences(kvp_group_id),
      current_batch_tracker_->GetPerGroupQTokens(kvp_group_id),
      current_batch_tracker_->GetPerGroupKvTokens(kvp_group_id),
      current_batch_tracker_->GetPerGroupActiveKvpGroups(kvp_group_id),
      current_batch_tracker_->GetPerGroupLastKvpGroupIds(kvp_group_id));
}

void KvpStateTracker::EnsureBatchTracker() {
  if (current_batch_tracker_ == nullptr) {
    StartBatchFormation();
  }
}

int KvpStateTracker::GetMaxSeqLen() const { return max_seq_len_; }

std::vector<int> KvpStateTracker::GetAllocationOrder(
    const std::vector<int>& kvp_group_ids) const {
  std::vector<int> ordered_groups = kvp_group_ids;
  std::sort(ordered_groups.begin(), ordered_groups.end(), [this](int a, int b) {
    return kvp_group_pending_prefill_work_[a] <
           kvp_group_pending_prefill_work_[b];
  });
  return ordered_groups;
}

std::pair<bool, int> KvpStateTracker::Allocate(
    const std::shared_ptr<vajra::Sequence> seq) {
  std::vector<int> filter_kvp_group_ids = GetBatchTrackerFreeGroups();

  int num_blocks = static_cast<int>(seq->GetLogicalTokenBlocks().size());

  // If sequence is too large, return false
  if (num_blocks > kvp_size_ * max_num_blocks_per_kvp_group_) {
    LOG_WARNING(
        "Ignoring seq_id: {} due to max num blocks per kvp group limit.",
        seq->seq_id);
    return {false, num_blocks};
  }

  // Determine available KVP groups
  std::vector<int> available_kvp_group_ids;
  if (!filter_kvp_group_ids.empty()) {
    available_kvp_group_ids = filter_kvp_group_ids;
  } else {
    for (int i = 0; i < kvp_size_; ++i) {
      available_kvp_group_ids.push_back(i);
    }
  }

  if (available_kvp_group_ids.empty()) {
    return {false, num_blocks};
  }

  // If sequence fits in one KVP group, allocate to first available
  if (num_blocks < max_num_blocks_per_kvp_group_) {
    std::vector<int> ordered_groups =
        GetAllocationOrder(available_kvp_group_ids);
    for (int kvp_group_id : ordered_groups) {
      if (block_managers_map_[kvp_group_id]->CanAllocateBlocks(num_blocks)) {
        block_managers_map_[kvp_group_id]->Allocate(seq, num_blocks);
        seq_kvp_group_block_counter_[seq->seq_id][kvp_group_id] = num_blocks;
        return {true, num_blocks};
      }
    }
    return {false, num_blocks};
  }

  // If sequence requires multiple KVP groups
  int num_kv_parallel_groups = static_cast<int>(std::ceil(
      static_cast<double>(num_blocks) / max_num_blocks_per_kvp_group_));
  int last_group_num_blocks =
      num_blocks - max_num_blocks_per_kvp_group_ * (num_kv_parallel_groups - 1);

  int num_groups_found = 0;
  bool last_group_found = false;
  std::vector<int> kvp_group_ids;
  int last_kvp_group_id = -1;

  std::vector<int> ordered_groups = GetAllocationOrder(available_kvp_group_ids);
  for (int kvp_group_id : ordered_groups) {
    auto& block_manager = block_managers_map_[kvp_group_id];
    if (block_manager->CanAllocateBlocks(max_num_blocks_per_kvp_group_)) {
      num_groups_found++;
      kvp_group_ids.push_back(kvp_group_id);
    } else if (last_group_num_blocks > 0 && !last_group_found &&
               block_manager->CanAllocateBlocks(last_group_num_blocks)) {
      last_group_found = true;
      num_groups_found++;
      last_kvp_group_id = kvp_group_id;
    }

    if (num_groups_found == num_kv_parallel_groups) {
      break;
    }
  }

  if (num_groups_found != num_kv_parallel_groups) {
    return {false, num_blocks};
  }

  if (last_kvp_group_id != -1) {
    kvp_group_ids.push_back(last_kvp_group_id);
  } else {
    last_kvp_group_id = kvp_group_ids.back();
  }

  for (int kvp_group_id : kvp_group_ids) {
    if (kvp_group_id == last_kvp_group_id) {
      block_managers_map_[kvp_group_id]->Allocate(seq, last_group_num_blocks);
      seq_kvp_group_block_counter_[seq->seq_id][kvp_group_id] =
          last_group_num_blocks;
    } else {
      block_managers_map_[kvp_group_id]->Allocate(
          seq, max_num_blocks_per_kvp_group_);
      seq_kvp_group_block_counter_[seq->seq_id][kvp_group_id] =
          max_num_blocks_per_kvp_group_;
    }

    // Use GetPromptLength() to access the prompt length
    size_t prompt_len = seq->GetPromptLength();
    kvp_group_pending_prefill_work_[kvp_group_id] +=
        static_cast<int>(prompt_len * prompt_len);
  }

  return {true, num_blocks};
}

void KvpStateTracker::FreeSeq(const std::shared_ptr<vajra::Sequence> seq) {
  if (seq_kvp_group_block_counter_.find(seq->seq_id) ==
      seq_kvp_group_block_counter_.end()) {
    return;
  }

  for (const auto& [kvp_group_id, _] :
       seq_kvp_group_block_counter_[seq->seq_id]) {
    block_managers_map_[kvp_group_id]->Free(seq);
  }

  seq_kvp_group_block_counter_.erase(seq->seq_id);
}

int KvpStateTracker::GetLastKvGroupId(
    const std::shared_ptr<vajra::Sequence> seq) const {
  auto it = seq_kvp_group_block_counter_.find(seq->seq_id);
  ASSERT_VALID_ARGUMENTS(it != seq_kvp_group_block_counter_.end(),
                         "Sequence not found in block counter");

  const auto& group_map = it->second;
  ASSERT_VALID_ARGUMENTS(!group_map.empty(), "Empty group map for sequence");

  // Get the last element in the ordered map
  return group_map.rbegin()->first;
}

bool KvpStateTracker::CanAppendSlot(
    const std::shared_ptr<vajra::Sequence> seq) const {
  int last_kvp_group_id = GetLastKvGroupId(seq);
  return block_managers_map_.at(last_kvp_group_id)->CanAppendSlot();
}

bool KvpStateTracker::AppendSlot(const std::shared_ptr<vajra::Sequence> seq,
                                 int num_total_blocks) {
  int last_kvp_group_id = GetLastKvGroupId(seq);
  // Pass num_total_blocks to AppendSlot as required by BlockSpaceManager
  bool has_appended =
      block_managers_map_[last_kvp_group_id]->AppendSlot(seq, num_total_blocks);

  if (has_appended) {
    seq_kvp_group_block_counter_[seq->seq_id][last_kvp_group_id]++;
  }

  return has_appended;
}

std::vector<int> KvpStateTracker::GetActiveKvpGroupIds(
    const std::shared_ptr<vajra::Sequence> seq) const {
  auto it = seq_kvp_group_block_counter_.find(seq->seq_id);
  if (it == seq_kvp_group_block_counter_.end()) {
    return {};
  }

  std::vector<int> active_kvp_group_ids;
  for (const auto& [kvp_group_id, _] : it->second) {
    active_kvp_group_ids.push_back(kvp_group_id);
  }

  return active_kvp_group_ids;
}

void KvpStateTracker::UpdatePrefillWork(
    const std::shared_ptr<vajra::Sequence> seq, int current_tokens,
    int new_tokens) {
  for (int kvp_group_id : GetActiveKvpGroupIds(seq)) {
    int delta = new_tokens * new_tokens - current_tokens * current_tokens;
    kvp_group_pending_prefill_work_[kvp_group_id] += delta;
  }
}

std::map<int, int> KvpStateTracker::GetKvpGroupBlockCounter(
    const std::string& seq_id) const {
  auto it = seq_kvp_group_block_counter_.find(seq_id);
  if (it == seq_kvp_group_block_counter_.end()) {
    return {};
  }

  return it->second;
}

std::pair<int, std::vector<std::tuple<int, int, bool>>>
KvpStateTracker::GetSequenceKvTokenInfo(
    const std::shared_ptr<vajra::Sequence> seq,
    const std::vector<int>& active_kvp_group_ids) const {
  // Get the number of processed tokens using the accessor method
  int num_processed_tokens =
      static_cast<int>(seq->GetNumTokensStageProcessed());

  // Prepare KV token info
  std::vector<std::tuple<int, int, bool>> kv_token_info;

  for (size_t i = 0; i < active_kvp_group_ids.size(); ++i) {
    int kvp_group_id = active_kvp_group_ids[i];
    bool is_last_group = i == active_kvp_group_ids.size() - 1;

    int num_kv_tokens;
    if (is_last_group) {
      // For the last group, calculate remaining tokens
      int num_kv_tokens_in_other_groups =
          static_cast<int>(active_kvp_group_ids.size() - 1) *
          max_num_tokens_per_kvp_group_;
      num_kv_tokens = num_processed_tokens - num_kv_tokens_in_other_groups;
    } else {
      // For non-last groups, use maximum tokens per group
      num_kv_tokens = max_num_tokens_per_kvp_group_;
    }

    // Ensure we don't have negative token counts
    ASSERT_VALID_ARGUMENTS(num_kv_tokens >= 0,
                           "Negative KV token count calculated: {}",
                           num_kv_tokens);

    // Add the token info with is_last_group flag
    kv_token_info.emplace_back(kvp_group_id, num_kv_tokens, is_last_group);
  }

  return {num_processed_tokens, kv_token_info};
}

int KvpStateTracker::GetMaxNumTokensPerKvpGroup() const {
  return max_num_tokens_per_kvp_group_;
}
