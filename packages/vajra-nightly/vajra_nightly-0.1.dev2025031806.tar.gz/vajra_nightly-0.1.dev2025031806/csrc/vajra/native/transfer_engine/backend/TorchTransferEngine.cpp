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
#include "native/transfer_engine/backend/TorchTransferEngine.h"

#include "commons/Logging.h"
#include "commons/StdCommon.h"
#include "native/transfer_engine/backend/TorchTransferWork.h"
//==============================================================================
using vajra::ReplicaResourceMapping;
using vajra::TorchTransferEngine;
using vajra::TorchTransferWork;
using vajra::TransferWork;
//==============================================================================
TorchTransferEngine::TorchTransferEngine(
    std::size_t global_rank, ReplicaResourceMapping replica_mapping,
    const c10::intrusive_ptr<c10d::ProcessGroup> global_process_group)
    : global_rank_(global_rank),
      replica_mapping_(replica_mapping),
      global_process_group_(global_process_group) {
  std::size_t curr_num_gpus_seen = 0;
  bool found_replica_id = false;

  for (std::size_t current_replica_index = 0;
       current_replica_index < replica_mapping.size();
       current_replica_index++) {
    const auto& replica_resource_config =
        replica_mapping[current_replica_index];
    replica_global_offsets_.emplace_back(curr_num_gpus_seen);
    curr_num_gpus_seen += replica_resource_config.world_size;
    if (!found_replica_id && curr_num_gpus_seen > global_rank) {
      replica_id_ = current_replica_index;
      found_replica_id = true;
    }
  }
  ASSERT_VALID_RUNTIME(found_replica_id, "Unable to find a replica id for {}",
                       global_rank);
  local_rank_ = global_rank_ - replica_global_offsets_[replica_id_];
}
// TODO(Kasra): Transfer Engine implementation
std::unique_ptr<TransferWork> TorchTransferEngine::AsyncSend(
    std::size_t dst_replica_id, torch::Tensor const& page_tensor,
    const std::vector<std::size_t>& page_list, std::size_t layer_id) {
  return std::make_unique<TorchTransferWork>();
}

std::unique_ptr<TransferWork> TorchTransferEngine::AsyncRecv(
    std::size_t src_replica_id, torch::Tensor const& page_tensor,
    const std::vector<std::size_t>& page_list, std::size_t layer_id) {
  return std::make_unique<TorchTransferWork>();
}

std::vector<std::size_t> TorchTransferEngine::GetMatchingOtherGlobalRanks(
    std::size_t other_replica_id, std::size_t layer_id) {
  std::vector<std::size_t> matching_other_global_ranks;
  const auto& replica_resource_config = replica_mapping_[replica_id_];
  const auto& other_replica_resource_config =
      replica_mapping_[other_replica_id];

  std::size_t local_tp_rank =
      GetLocalTPRank(local_rank_, replica_resource_config);
  std::size_t local_pp_rank =
      GetLocalPPRank(local_rank_, replica_resource_config);

  std::size_t expected_local_pp_rank =
      std::floor((static_cast<double>(layer_id) /
                  replica_resource_config.total_num_layers) *
                 replica_resource_config.pipeline_parallel_size);
  ASSERT_VALID_ARGUMENTS(
      expected_local_pp_rank == local_pp_rank,
      "Expected local pp rank {} did not match the actual pp rank of {} "
      "for parameter layer id {} and total num layers {}.",
      expected_local_pp_rank, local_pp_rank, layer_id,
      replica_resource_config.total_num_layers);

  std::size_t other_local_tp_rank_start =
      local_tp_rank *
      (static_cast<double>(other_replica_resource_config.tensor_parallel_size) /
       replica_resource_config.tensor_parallel_size);

  // exclusive end
  std::size_t other_local_tp_rank_end = std::ceil(
      (local_tp_rank + 1) *
      (static_cast<double>(other_replica_resource_config.tensor_parallel_size) /
       replica_resource_config.tensor_parallel_size));

  std::size_t other_local_pp_rank =
      std::floor((static_cast<double>(layer_id) /
                  other_replica_resource_config.total_num_layers) *
                 other_replica_resource_config.pipeline_parallel_size);

  for (std::size_t other_local_tp_rank = other_local_tp_rank_start;
       other_local_tp_rank < other_local_tp_rank_end; other_local_tp_rank++) {
    std::size_t other_local_rank =
        other_local_tp_rank +
        other_replica_resource_config.tensor_parallel_size *
            other_local_pp_rank;
    std::size_t other_global_rank =
        other_local_rank + replica_global_offsets_[other_replica_id];
    matching_other_global_ranks.emplace_back(other_global_rank);
  }

  return matching_other_global_ranks;
}

inline std::size_t TorchTransferEngine::GetLocalPPRank(
    std::size_t local_rank, const ReplicaResourceConfig& replica_config) {
  return std::floor(
      (static_cast<double>(local_rank) / replica_config.world_size) *
      replica_config.pipeline_parallel_size);
}

inline std::size_t TorchTransferEngine::GetLocalTPRank(
    std::size_t local_rank, const ReplicaResourceConfig& replica_config) {
  return (local_rank) % replica_config.tensor_parallel_size;
}
//==============================================================================
