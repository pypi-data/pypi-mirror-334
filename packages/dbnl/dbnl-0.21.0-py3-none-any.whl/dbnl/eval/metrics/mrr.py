from __future__ import annotations

from abc import ABC
from typing import Any, Literal, Optional

import pandas as pd
from typing_extensions import override

from .metric import Metric


class Mrr(Metric, ABC):
    def __init__(
        self,
        ground_truth_document_id: str,
        retrieved_document_ids: str,
    ):
        """
        Initializes a Mean Reciprocal Rank (MRR) metric.

        :param ground_truth_document_id: ground_truth_document_id column name
        :param retrieved_document_ids: retrieved_document_ids column name
        """
        self._ground_truth_document_id = ground_truth_document_id
        self._retrieved_document_ids = retrieved_document_ids

    @override
    def metric(self) -> str:
        return "mrr"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._ground_truth_document_id}__{self._retrieved_document_ids}"

    @override
    def type(self) -> Literal["float"]:
        return "float"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the mean reciprocal rank (MRR) between the '{self._ground_truth_document_id}' and '{self._retrieved_document_ids}' columns. The formula is 1 / (i + 1) where i is the index of the ground truth document id in the retrieved document ids."

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
                _get_mrr(ground_truth_document_id, retrieved_document_ids)
                for ground_truth_document_id, retrieved_document_ids in zip(
                    ground_truth_document_id_col, retrieved_document_ids_col
                )
            ],
            dtype="float32[pyarrow]",
        )


def _get_mrr(ground_truth_document_id: str, retrieved_document_ids: list[str]) -> float:
    """
    Returns the mean reciprocal rank (MRR) of the retrieved context_ids.
    """
    for i, retrieved_context_id in enumerate(retrieved_document_ids):
        if ground_truth_document_id == retrieved_context_id:
            return 1 / (i + 1)
    return 0
