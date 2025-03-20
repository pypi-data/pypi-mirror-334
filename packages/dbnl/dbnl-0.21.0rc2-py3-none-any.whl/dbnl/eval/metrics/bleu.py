from __future__ import annotations

from abc import ABC
from typing import Literal, Optional

import pandas as pd
from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu  # type: ignore[import-untyped]
from typing_extensions import override

from .metric import Metric


class Bleu(Metric, ABC):
    def __init__(
        self,
        prediction: str,
        target: str,
    ):
        """
        Initializes a Bleu metric.

        :param prediction: prediction column name
        :param target: target column name
        """
        self._prediction = prediction
        self._target = target

    @override
    def metric(self) -> str:
        return "bleu"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._prediction}__{self._target}"

    @override
    def type(self) -> Literal["float"]:
        return "float"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the BLEU score between the '{self._prediction}' and '{self._target}' columns."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return True

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._prediction}, {self._target})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[float]:
        if self._target not in df:
            raise ValueError(f"Missing target column {self._target} in {df}")
        targets = df[self._target]

        if self._prediction not in df:
            raise ValueError(f"Missing prediction column {self._prediction} in {df}")
        predictions = df[self._prediction]

        scores = []
        for target, prediction in zip(targets, predictions):
            scores.append(
                sentence_bleu(
                    [target.split()],
                    prediction.split(),
                    smoothing_function=SmoothingFunction().method1,
                )
            )

        return pd.Series(scores, dtype="float32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return f"{self._prediction}__{self._target}"
