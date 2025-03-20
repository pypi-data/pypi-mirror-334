from __future__ import annotations

from abc import ABC
from enum import Enum
from typing import Literal, Optional

import pandas as pd
from rouge_score.rouge_scorer import RougeScorer  # type: ignore[import-untyped]
from typing_extensions import override

from .metric import Metric


class RougeScoreType(Enum):
    PRECISION = "precision"
    RECALL = "recall"
    FMEASURE = "fmeasure"


class RougeMetricType(Enum):
    ROUGE1 = "rouge1"
    ROUGE2 = "rouge2"
    ROUGEL = "rougeL"
    ROUGELSUM = "rougeLsum"


class Rouge(Metric, ABC):
    def __init__(
        self,
        metric_type: RougeMetricType,
        prediction: str,
        target: str,
        score_type: RougeScoreType = RougeScoreType.FMEASURE,
    ):
        """
        Initializes a rouge metric.

        :param metric: name of rouge metric to compute (e.g. rouge1, rouge2, etc.)
        :param prediction: prediction column name
        :param target: target column name
        """
        self._metric = _get_rouge_metric_string(metric_type.value, score_type)
        self._metric_type = metric_type.value
        self._prediction = prediction
        self._target = target
        self._score_type = score_type

    @override
    def metric(self) -> str:
        return self._metric

    @override
    def name(self) -> str:
        return f"{self._metric}__{self._prediction}__{self._target}"

    @override
    def type(self) -> Literal["float"]:
        return "float"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the {self._metric} score between the '{self._prediction}' and '{self._target}' columns as defined in the \"ROUGE: A Package for Automatic Evaluation of Summaries\" paper."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return True

    @override
    def expression(self) -> str:
        return f"{self._metric}({self._prediction}, {self._target})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[float]:
        if not self._target in df:
            raise ValueError(f"Missing target column {self._target} in {df}")
        targets = df[self._target]

        if not self._prediction in df:
            raise ValueError(f"Missing prediction column {self._prediction} in {df}")
        predictions = df[self._prediction]

        scorer = RougeScorer([self._metric_type])
        scores = []
        for prediction, target in zip(predictions, targets):
            score = scorer.score(target, prediction)
            scores.append(getattr(score[self._metric_type], self._score_type.value))

        return pd.Series(scores, dtype="float32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return f"{self._prediction}__{self._target}"


def _get_rouge_metric_string(metric_type: str, score_type: RougeScoreType) -> str:
    """This function returns the rouge metric string.

    The current implementation is a simple string concatenation of the metric and score type.
    If the score type is FMEASURE, only the metric is returned, which would looke like:
    eg, "rouge1" or "rouge2" rather than "rouge1_fmeasure" or "rouge2_fmeasure".
    """
    if score_type == RougeScoreType.FMEASURE:
        return f"{metric_type}"
    return f"{metric_type}_{score_type.value}"
