from __future__ import annotations

from abc import ABC
from typing import Literal, Optional

import pandas as pd
from textstat import automated_readability_index, flesch_kincaid_grade  # type: ignore[import-untyped]
from typing_extensions import override

from .metric import Metric


class FleschKincaidGrade(Metric, ABC):
    def __init__(
        self,
        text_col_name: str,
    ):
        """
        Initializes a Flesch-Kincaid Grade metric.

        :param text_col_name: text_col_name column name
        """
        self._text_col_name = text_col_name

    @override
    def metric(self) -> str:
        return "flesch_kincaid_grade"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._text_col_name}"

    @override
    def type(self) -> Literal["float"]:
        return "float"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the Flesch-Kincaid Grade of the '{self._text_col_name}' column."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return True

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._text_col_name})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[float]:
        if not self._text_col_name in df:
            raise ValueError(f"Missing text_col_name column {self._text_col_name} in {df}")
        texts = df[self._text_col_name].tolist()
        return pd.Series([flesch_kincaid_grade(text) for text in texts], dtype="float32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return self._text_col_name


class AutomatedReadabilityIndex(Metric, ABC):
    def __init__(
        self,
        text_col_name: str,
    ):
        """
        Initializes an Automated Readability Index metric.

        :param text_col_name: text_col_name column name
        """
        self._text_col_name = text_col_name

    @override
    def metric(self) -> str:
        return "automated_readability_index"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._text_col_name}"

    @override
    def type(self) -> Literal["float"]:
        return "float"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the Automated Readability Index of the '{self._text_col_name}' column."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return True

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._text_col_name})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[float]:
        if not self._text_col_name in df:
            raise ValueError(f"Missing text_col_name column {self._text_col_name} in {df}")
        texts = df[self._text_col_name].tolist()
        return pd.Series([automated_readability_index(text) for text in texts], dtype="float32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return self._text_col_name
