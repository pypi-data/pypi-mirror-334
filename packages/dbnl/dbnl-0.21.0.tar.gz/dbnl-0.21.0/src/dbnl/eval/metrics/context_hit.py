from __future__ import annotations

from abc import ABC
from typing import Any, Literal, Optional

import pandas as pd
from typing_extensions import override

from .metric import Metric


class ContextHit(Metric, ABC):
    def __init__(
        self,
        ground_truth_document_id: str,
        retrieved_document_ids: str,
    ):
        """
        Initializes a Context Hit metric.

        :param ground_truth_document_id: ground_truth_document_id column name
        :param retrieved_document_ids: retrieved_document_ids column name
        """
        self._ground_truth_document_id = ground_truth_document_id
        self._retrieved_document_ids = retrieved_document_ids

    @override
    def metric(self) -> str:
        return "context_hit"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._ground_truth_document_id}__{self._retrieved_document_ids}"

    @override
    def type(self) -> Literal["boolean"]:
        return "boolean"

    @override
    def description(self) -> Optional[str]:
        return "Computes whether the ground truth document id is in the retrieved document ids."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return True

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._ground_truth_document_id}, {self._retrieved_document_ids})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[Any]:
        if self._ground_truth_document_id not in df:
            raise ValueError(f"Missing ground_truth_document_id column {self._ground_truth_document_id} in {df}")
        if self._retrieved_document_ids not in df:
            raise ValueError(f"Missing retrieved_document_ids column {self._retrieved_document_ids} in {df}")
        ground_truth_document_id_col = df[self._ground_truth_document_id]
        retrieved_document_ids_col = df[self._retrieved_document_ids]

        return pd.Series(
            [
                _get_context_hit(ground_truth_document_id, retrieved_document_ids)
                for ground_truth_document_id, retrieved_document_ids in zip(
                    ground_truth_document_id_col, retrieved_document_ids_col
                )
            ],
            dtype="bool[pyarrow]",
        )


def _get_context_hit(ground_truth_document_id: str, retrieved_document_ids: list[str]) -> float:
    """
    Returns the context_hit, boolean value indicating whether the ground truth
    document is in the retrieved documents.
    """
    return ground_truth_document_id in retrieved_document_ids
