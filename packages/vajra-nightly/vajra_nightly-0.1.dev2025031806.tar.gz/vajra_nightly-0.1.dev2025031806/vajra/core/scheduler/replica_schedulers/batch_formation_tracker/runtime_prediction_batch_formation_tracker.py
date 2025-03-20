from typing import Dict, List

from vidur.entities import Batch as VidurBatch
from vidur.execution_time_predictor.base_execution_time_predictor import (
    BaseExecutionTimePredictor,
)

from vajra._native.scheduler import KvpStateTracker as KvpStateTracker
from vajra.core.scheduler.replica_schedulers.batch_formation_tracker.batch_formation_tracker import (
    BatchFormationTracker,
)
from vajra.datatypes import Sequence

EXECUTION_TIME_PREDICTION_SLACK = 0.1
EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE = 512
EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY = 32


def round_down_to_nearest_multiple(value: int, multiple: int) -> int:
    return (value // multiple) * multiple


def round_up_to_nearest_multiple(value: int, multiple: int) -> int:
    return ((value + multiple - 1) // multiple) * multiple


class BatchFormationTrackerWithRuntimePrediction(BatchFormationTracker):
    def __init__(
        self,
        schedule_id: int,
        max_micro_batch_size: int,
        pipeline_parallel_size: int,
        kvp_state_tracker: KvpStateTracker,
        max_chunk_size: int,
        min_chunk_size: int,
        execution_time_predictor: BaseExecutionTimePredictor,
    ):
        super().__init__(
            schedule_id,
            max_micro_batch_size,
            kvp_state_tracker,
        )
        self.pipeline_parallel_size = pipeline_parallel_size
        self.execution_time_predictor = execution_time_predictor
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size

        self.batch_execution_time_predictions: List[int] = [
            0 for _ in range(kvp_state_tracker.kvp_size)
        ]

    def add_sequence(
        self,
        seq: Sequence,
        num_q_tokens: int,
        active_kvp_group_ids: List[int],
        kvp_group_block_counter: Dict[int, int],
    ) -> None:
        super().add_sequence(
            seq, num_q_tokens, active_kvp_group_ids, kvp_group_block_counter
        )

        if num_q_tokens == 1:
            # Do not update predictions for decode seqs
            # We are assuming that the decode seqs are all added
            # at the beginning and don't need q chunk sizes, so we can just
            # do updates once we start adding prefills
            return

        for kvp_group_id in range(self.kvp_state_tracker.kvp_size):
            self.batch_execution_time_predictions[kvp_group_id] = (
                self._compute_batch_execution_time(kvp_group_id)
            )

    def _compute_batch_execution_time(
        self,
        kvp_group_id: int,
        extra_seqs: List[Sequence] = [],
        extra_num_q_tokens: List[int] = [],
        extra_num_kv_tokens: List[int] = [],
        extra_num_active_kvp_groups: List[int] = [],
        extra_last_kvp_group_ids: List[int] = [],
    ) -> int:
        # Get all current batch info for this KVP group
        seqs, q_tokens, kv_tokens, active_groups, last_group_ids = (
            self.kvp_state_tracker.get_batch_tracker_per_group_info(kvp_group_id)
        )

        if len(seqs) + len(extra_seqs) == 0:
            return 0

        num_seqs = len(seqs) + len(extra_seqs)

        return (
            self.execution_time_predictor.get_execution_time(
                VidurBatch(
                    0,  # replica_id
                    [None] * num_seqs,  # sequences
                    q_tokens + extra_num_q_tokens,
                    kv_tokens + extra_num_kv_tokens,
                    active_groups + extra_num_active_kvp_groups,
                    last_group_ids + extra_last_kvp_group_ids,
                    kvp_group_id,
                ),
                pipeline_stage=0,
            ).total_time
            * self.pipeline_parallel_size
        )

    def get_batch_execution_time(self, kvp_group_id: int) -> int:
        return self.batch_execution_time_predictions[kvp_group_id]

    def get_batch_execution_time_for_kvp_groups(self, kvp_group_ids: List[int]) -> int:
        return [
            self.batch_execution_time_predictions[kvp_group_id]
            for kvp_group_id in kvp_group_ids
        ]

    def get_max_chunk_size_for_seq(
        self,
        seq: Sequence,
        active_kvp_group_ids: List[int],
        target_batch_time: float,
    ) -> int:
        # identify the kvp group with the maximum execution time, and get the execution time and group id
        max_execution_time_group_id = active_kvp_group_ids[0]
        max_execution_time = 0

        for kvp_group_id in active_kvp_group_ids:
            execution_time = self.get_batch_execution_time(kvp_group_id)
            if execution_time > max_execution_time:
                max_execution_time = execution_time
                max_execution_time_group_id = kvp_group_id

        if max_execution_time > target_batch_time * (
            1 - EXECUTION_TIME_PREDICTION_SLACK
        ):
            return 0

        is_last_group = max_execution_time_group_id == active_kvp_group_ids[-1]

        num_processed_tokens = seq.get_num_tokens_stage_processed()

        num_kv_tokens = self._get_num_kv_tokens(
            num_processed_tokens, active_kvp_group_ids, is_last_group
        )
        num_kvp_groups = len(active_kvp_group_ids)
        last_kvp_group_id = active_kvp_group_ids[-1]
        remaining_tokens = max(seq.prompt_len - num_processed_tokens, 0)

        # Get initial bounds for binary search
        if hasattr(seq, "__last_chunk_size"):
            high = seq.__last_chunk_size
        else:
            high = EXECUTION_TIME_PREDICTION_START_CHUNK_SIZE

        # Cap high by remaining tokens
        high = round_down_to_nearest_multiple(
            2 * high, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY
        )
        high = min(remaining_tokens, high)
        low = 0

        # Binary search with 32-token steps except for last chunk
        closest_match = 0
        closest_time = None

        seen_chunk_sizes = set()

        while low <= high:
            mid = (low + high) // 2

            mid = min(self.max_chunk_size, mid)

            if mid < remaining_tokens:
                mid = round_down_to_nearest_multiple(
                    mid, EXECUTION_TIME_PREDICTION_CHUNK_SIZE_GRANULARITY
                )
                if mid == 0:
                    mid = min(self.min_chunk_size, remaining_tokens)
            else:
                mid = remaining_tokens

            if mid in seen_chunk_sizes:
                break

            seen_chunk_sizes.add(mid)

            if mid == 0:
                break

            execution_time = self._compute_batch_execution_time(
                max_execution_time_group_id,
                extra_seqs=[seq],
                extra_num_q_tokens=[mid],
                extra_num_kv_tokens=[num_kv_tokens],
                extra_num_active_kvp_groups=[num_kvp_groups],
                extra_last_kvp_group_ids=[last_kvp_group_id],
            )

            # Check if execution time is within both bounds of slack range
            if execution_time >= target_batch_time * (
                1 - EXECUTION_TIME_PREDICTION_SLACK
            ) and execution_time <= target_batch_time * (
                1 + EXECUTION_TIME_PREDICTION_SLACK
            ):
                # Found a good size within slack range
                closest_match = mid
                closest_time = execution_time
                break
            elif execution_time < target_batch_time * (
                1 - EXECUTION_TIME_PREDICTION_SLACK
            ):
                low = mid
            else:
                high = mid

            if closest_time is None or abs(execution_time - target_batch_time) < abs(
                closest_time - target_batch_time
            ):
                closest_match = mid
                closest_time = execution_time

        if closest_match != 0:
            seq.__last_chunk_size = closest_match

        return closest_match

    def _get_num_kv_tokens(
        self,
        num_processed_tokens: int,
        active_kvp_group_ids: List[int],
        is_last_group: bool,
    ) -> int:
        # This method needs to be implemented - it appears to be missing from the original code
        # Since we don't have the implementation, I'll add a placeholder
        # TODO: Implement the actual logic for getting the number of KV tokens
        return num_processed_tokens
