from typing import Dict, List

from vajra._native.scheduler import KvpStateTracker as KvpStateTracker
from vajra.datatypes import (
    SchedulerOutput,
    Sequence,
    SequenceScheduleMetadata,
)


class BatchFormationTracker:
    """
    Batch formation tracker for the current scheduling cycle
    """

    def __init__(
        self,
        schedule_id: int,
        max_micro_batch_size: int,
        kvp_state_tracker: KvpStateTracker,
    ):
        self.schedule_id: int = schedule_id
        self.max_micro_batch_size: int = max_micro_batch_size
        self.kvp_state_tracker = kvp_state_tracker

        # Start a new batch formation cycle in the KVP manager
        self.kvp_state_tracker.start_batch_formation()

        # Basic batch formation tracking
        self.num_sequences: int = 0
        self.sequences: List[Sequence] = []
        self.ignored_sequence_ids: List[str] = []
        self.preempted_sequence_ids: List[str] = []

        # Metadata for building the scheduler output
        self.batch_num_q_tokens: List[int] = []
        self.batch_group_mapping: List[Dict[int, int]] = []
        self.batch_active_group_ids: List[List[int]] = []

    def add_sequence(
        self,
        seq: Sequence,
        num_q_tokens: int,
    ) -> None:
        self.num_sequences += 1
        active_kvp_group_ids = self.kvp_state_tracker.get_active_kvp_group_ids(seq)

        self.sequences.append(seq)
        self.batch_num_q_tokens.append(num_q_tokens)
        self.batch_group_mapping.append(
            self.kvp_state_tracker.get_kvp_group_block_counter(seq.seq_id)
        )
        self.batch_active_group_ids.append(active_kvp_group_ids)

        num_processed_tokens = seq.get_num_tokens_stage_processed()

        # Update prefill work tracking in the KVP manager
        self.kvp_state_tracker.update_prefill_work(
            seq, num_processed_tokens, num_q_tokens
        )
        # Add sequence to the KVP manager's batch tracker
        self.kvp_state_tracker.add_sequence_to_batch(
            seq, num_q_tokens, active_kvp_group_ids
        )

    def add_ignored_sequence(self, seq: Sequence) -> None:
        self.ignored_sequence_ids.append(seq.seq_id)

    def add_preempted_sequence(self, seq: Sequence) -> None:
        self.preempted_sequence_ids.append(seq.seq_id)

    def can_add_sequences(self) -> bool:
        return self.num_sequences < self.max_micro_batch_size

    def get_batch(self) -> SchedulerOutput:
        seq_schedule_metadata_list: List[SequenceScheduleMetadata] = []

        for i, seq in enumerate(self.sequences):
            seq_schedule_metadata_list.append(
                SequenceScheduleMetadata(
                    schedule_id=self.schedule_id,
                    seq_id=seq.seq_id,
                    num_q_tokens=self.batch_num_q_tokens[i],
                    kvp_group_block_counter=self.batch_group_mapping[i],
                    kvp_group_ids=self.batch_active_group_ids[i],
                )
            )

        return SchedulerOutput(
            self.schedule_id,
            self.ignored_sequence_ids,
            self.preempted_sequence_ids,
            seq_schedule_metadata_list,
        )
