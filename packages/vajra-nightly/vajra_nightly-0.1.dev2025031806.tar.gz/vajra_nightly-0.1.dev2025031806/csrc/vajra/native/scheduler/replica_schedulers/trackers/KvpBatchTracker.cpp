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
#include "native/scheduler/replica_schedulers/trackers/KvpBatchTracker.h"

using vajra::KvpBatchTracker;

KvpBatchTracker::KvpBatchTracker(int kvp_size /*[in]*/) : kvp_size_(kvp_size) {
  // Initialize the per KVP group trackers
  per_kvp_group_sequences_.resize(kvp_size);
  per_kvp_group_num_q_tokens_.resize(kvp_size);
  per_kvp_group_num_kv_tokens_.resize(kvp_size);
  per_kvp_group_num_active_kvp_groups_.resize(kvp_size);
  per_kvp_group_last_kvp_group_ids_.resize(kvp_size);
  per_kvp_group_seq_num_processed_tokens_.resize(kvp_size);
  per_kvp_group_total_num_q_tokens_.resize(kvp_size, 0);
}

void KvpBatchTracker::AddSequence(
    const std::shared_ptr<vajra::Sequence> seq /*[in]*/,
    int num_q_tokens /*[in]*/,
    const std::vector<int>& active_kvp_group_ids /*[in]*/,
    const std::vector<std::tuple<int, int, bool>>& kv_token_info /*[in]*/,
    int num_processed_tokens /*[in]*/) {
  // Add the sequence to each active KVP group
  for (int group_id : active_kvp_group_ids) {
    ASSERT_VALID_ARGUMENTS(group_id >= 0 && group_id < kvp_size_,
                           "Invalid KVP group ID: {}", group_id);

    per_kvp_group_sequences_[group_id].push_back(seq);
    per_kvp_group_num_q_tokens_[group_id].push_back(num_q_tokens);
    per_kvp_group_num_active_kvp_groups_[group_id].push_back(
        static_cast<int>(active_kvp_group_ids.size()));
    per_kvp_group_seq_num_processed_tokens_[group_id].push_back(
        num_processed_tokens);

    // Update the total number of Q tokens for this group
    per_kvp_group_total_num_q_tokens_[group_id] += num_q_tokens;

    // Find the last KVP group ID
    int last_kvp_group_id = -1;
    if (!active_kvp_group_ids.empty()) {
      last_kvp_group_id = active_kvp_group_ids.back();
    }
    per_kvp_group_last_kvp_group_ids_[group_id].push_back(last_kvp_group_id);
  }

  // Process the KV token info
  for (const auto& [group_id, num_tokens, is_prefill] : kv_token_info) {
    ASSERT_VALID_ARGUMENTS(group_id >= 0 && group_id < kvp_size_,
                           "Invalid KVP group ID in token info: {}", group_id);

    per_kvp_group_num_kv_tokens_[group_id].push_back(num_tokens);
  }
}

std::vector<int> KvpBatchTracker::GetQTokensForKvpGroups(
    const std::vector<int>& active_kvp_group_ids /*[in]*/) const {
  std::vector<int> q_tokens;
  for (int group_id : active_kvp_group_ids) {
    ASSERT_VALID_ARGUMENTS(group_id >= 0 && group_id < kvp_size_,
                           "Invalid KVP group ID: {}", group_id);

    q_tokens.push_back(per_kvp_group_total_num_q_tokens_[group_id]);
  }
  return q_tokens;
}

std::vector<int> KvpBatchTracker::GetFreeKvpGroups(
    int token_threshold /*[in]*/) const {
  std::vector<int> free_groups;
  for (int group_id = 0; group_id < kvp_size_; ++group_id) {
    if (per_kvp_group_total_num_q_tokens_[group_id] <= token_threshold) {
      free_groups.push_back(group_id);
    }
  }
  return free_groups;
}

std::vector<std::shared_ptr<vajra::Sequence>>
KvpBatchTracker::GetPerGroupSequences(int kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id >= 0 && kvp_group_id < kvp_size_,
                         "Invalid KVP group ID: {}", kvp_group_id);

  return per_kvp_group_sequences_[kvp_group_id];
}

std::vector<int> KvpBatchTracker::GetPerGroupQTokens(
    int kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id >= 0 && kvp_group_id < kvp_size_,
                         "Invalid KVP group ID: {}", kvp_group_id);

  return per_kvp_group_num_q_tokens_[kvp_group_id];
}

std::vector<int> KvpBatchTracker::GetPerGroupKvTokens(
    int kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id >= 0 && kvp_group_id < kvp_size_,
                         "Invalid KVP group ID: {}", kvp_group_id);

  return per_kvp_group_num_kv_tokens_[kvp_group_id];
}

std::vector<int> KvpBatchTracker::GetPerGroupActiveKvpGroups(
    int kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id >= 0 && kvp_group_id < kvp_size_,
                         "Invalid KVP group ID: {}", kvp_group_id);

  return per_kvp_group_num_active_kvp_groups_[kvp_group_id];
}

std::vector<int> KvpBatchTracker::GetPerGroupLastKvpGroupIds(
    int kvp_group_id /*[in]*/) const {
  ASSERT_VALID_ARGUMENTS(kvp_group_id >= 0 && kvp_group_id < kvp_size_,
                         "Invalid KVP group ID: {}", kvp_group_id);

  return per_kvp_group_last_kvp_group_ids_[kvp_group_id];
}
