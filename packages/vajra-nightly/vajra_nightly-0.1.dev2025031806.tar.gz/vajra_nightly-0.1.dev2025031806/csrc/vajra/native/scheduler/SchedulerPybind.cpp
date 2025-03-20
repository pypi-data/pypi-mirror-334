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
#include "native/scheduler/SchedulerPybind.h"

#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "native/configs/CacheConfig.h"
#include "native/configs/ModelConfig.h"
#include "native/configs/ParallelConfig.h"
#include "native/scheduler/replica_schedulers/trackers/KvpBatchTracker.h"
#include "native/scheduler/replica_schedulers/trackers/KvpStateTracker.h"

void InitKvpBatchTrackerPybind(py::module& m) {
  py::class_<vajra::KvpBatchTracker>(m, "KvpBatchTracker")
      .def(py::init<int>())
      .def("add_sequence", &vajra::KvpBatchTracker::AddSequence, py::arg("seq"),
           py::arg("num_q_tokens"), py::arg("active_kvp_group_ids"),
           py::arg("kv_token_info"), py::arg("num_processed_tokens"))
      .def("_get_q_tokens_for_kvp_groups",
           &vajra::KvpBatchTracker::GetQTokensForKvpGroups,
           py::arg("active_kvp_group_ids"))
      .def("get_free_kvp_groups", &vajra::KvpBatchTracker::GetFreeKvpGroups,
           py::arg("token_threshold") = vajra::ALLOCATION_MAX_TOKEN_THRESHOLD)
      .def("get_per_group_sequences",
           &vajra::KvpBatchTracker::GetPerGroupSequences,
           py::arg("kvp_group_id"))
      .def("get_per_group_q_tokens",
           &vajra::KvpBatchTracker::GetPerGroupQTokens, py::arg("kvp_group_id"))
      .def("get_per_group_kv_tokens",
           &vajra::KvpBatchTracker::GetPerGroupKvTokens,
           py::arg("kvp_group_id"))
      .def("get_per_group_active_kvp_groups",
           &vajra::KvpBatchTracker::GetPerGroupActiveKvpGroups,
           py::arg("kvp_group_id"))
      .def("get_per_group_last_kvp_group_ids",
           &vajra::KvpBatchTracker::GetPerGroupLastKvpGroupIds,
           py::arg("kvp_group_id"));
}

void InitKvpStateTrackerPybind(py::module& m) {
  py::class_<vajra::KvpStateTracker>(m, "KvpStateTracker")
      .def(py::init<const vajra::ModelConfig&, const vajra::CacheConfig&,
                    const vajra::ParallelConfig&>(),
           py::arg("model_config"), py::arg("cache_config"),
           py::arg("parallel_config"))
      .def("start_batch_formation",
           &vajra::KvpStateTracker::StartBatchFormation)
      .def("get_batch_tracker_q_tokens",
           &vajra::KvpStateTracker::GetBatchTrackerQTokens, py::arg("seq"))
      .def("get_batch_tracker_free_groups",
           &vajra::KvpStateTracker::GetBatchTrackerFreeGroups)
      .def("add_sequence_to_batch", &vajra::KvpStateTracker::AddSequenceToBatch,
           py::arg("seq"), py::arg("num_q_tokens"),
           py::arg("active_kvp_group_ids"))
      .def("get_batch_tracker_per_group_info",
           &vajra::KvpStateTracker::GetBatchTrackerPerGroupInfo,
           py::arg("kvp_group_id"))
      .def("get_max_seq_len", &vajra::KvpStateTracker::GetMaxSeqLen)
      .def("get_allocation_order", &vajra::KvpStateTracker::GetAllocationOrder,
           py::arg("kvp_group_ids"))
      .def("allocate", &vajra::KvpStateTracker::Allocate, py::arg("seq"))
      .def("free_seq", &vajra::KvpStateTracker::FreeSeq, py::arg("seq"))
      .def("get_last_kv_group_id", &vajra::KvpStateTracker::GetLastKvGroupId,
           py::arg("seq"))
      .def("can_append_slot", &vajra::KvpStateTracker::CanAppendSlot,
           py::arg("seq"))
      .def("append_slot", &vajra::KvpStateTracker::AppendSlot, py::arg("seq"),
           py::arg("num_total_blocks"))
      .def("get_active_kvp_group_ids",
           &vajra::KvpStateTracker::GetActiveKvpGroupIds, py::arg("seq"))
      .def("update_prefill_work", &vajra::KvpStateTracker::UpdatePrefillWork,
           py::arg("seq"), py::arg("current_tokens"), py::arg("new_tokens"))
      .def("get_kvp_group_block_counter",
           &vajra::KvpStateTracker::GetKvpGroupBlockCounter, py::arg("seq_id"))
      .def("get_sequence_kv_token_info",
           &vajra::KvpStateTracker::GetSequenceKvTokenInfo, py::arg("seq"),
           py::arg("active_kvp_group_ids"))
      .def("get_max_num_tokens_per_kvp_group",
           &vajra::KvpStateTracker::GetMaxNumTokensPerKvpGroup);
}

void InitSchedulerPybindSubmodule(py::module& m) {
  auto scheduler_module = m.def_submodule("scheduler");
  InitKvpBatchTrackerPybind(scheduler_module);
  InitKvpStateTrackerPybind(scheduler_module);
}
