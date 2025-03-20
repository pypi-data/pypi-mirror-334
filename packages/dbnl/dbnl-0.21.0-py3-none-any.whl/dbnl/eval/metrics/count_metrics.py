from __future__ import annotations

from abc import ABC
from functools import lru_cache
from typing import Literal, Optional

import pandas as pd
import spacy
from spacy.language import Language
from typing_extensions import override

from dbnl.errors import DBNLError

from .metric import Metric


@lru_cache
def _load_spacy_model() -> Language:
    try:
        return spacy.load("en_core_web_sm", exclude=["tagger", "attribute_ruler", "lemmatizer", "ner"])
    except OSError as ex:
        raise DBNLError(
            "Missing spacy language model. A spacy language model is required to compute count metrics. Please run: python -m spacy download en_core_web_sm"
        ) from ex


class CharacterCount(Metric, ABC):
    def __init__(self, text_col_name: str):
        """
        Initializes a Character Count metric.

        :param text_col_name: text_col_name column name
        """
        self._text_col_name = text_col_name

    @override
    def metric(self) -> str:
        return "character_count"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._text_col_name}"

    @override
    def type(self) -> Literal["int"]:
        return "int"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the character count of the '{self._text_col_name}' column."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return None

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._text_col_name})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[int]:
        if self._text_col_name not in df:
            raise ValueError(f"Missing text_col_name column {self._text_col_name} in {df}")
        texts = df[self._text_col_name].tolist()
        return pd.Series([len(text) for text in texts], dtype="int32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return self._text_col_name


class SentenceCount(Metric, ABC):
    def __init__(self, text_col_name: str):
        """
        Initializes a Sentence Count metric.

        :param text_col_name: text_col_name column name
        """
        self._text_col_name = text_col_name

    @override
    def metric(self) -> str:
        return "sentence_count"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._text_col_name}"

    @override
    def type(self) -> Literal["int"]:
        return "int"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the sentence count of the '{self._text_col_name}' column."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return None

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._text_col_name})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[int]:
        if not self._text_col_name in df:
            raise ValueError(f"Missing text_col_name column {self._text_col_name} in {df}")
        nlp = _load_spacy_model()
        texts = df[self._text_col_name].tolist()
        docs = nlp.pipe(texts)
        return pd.Series([sum(1 for _ in doc.sents) for doc in docs], dtype="int32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return self._text_col_name


class TokenCount(Metric, ABC):
    def __init__(self, text_col_name: str):
        """
        Initializes a Token Count metric.

        :param text_col_name: text_col_name column name
        """
        self._text_col_name = text_col_name

    @override
    def metric(self) -> str:
        return "token_count"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._text_col_name}"

    @override
    def type(self) -> Literal["int"]:
        return "int"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the token count of the '{self._text_col_name}' column."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return None

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._text_col_name})"

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[int]:
        if not self._text_col_name in df:
            raise ValueError(f"Missing text_col_name column {self._text_col_name} in {df}")
        nlp = _load_spacy_model()
        texts = df[self._text_col_name].tolist()
        docs = nlp.pipe(texts, disable=["tok2vec", "parser"])
        return pd.Series([sum(1 for _ in doc) for doc in docs], dtype="int32[pyarrow]")

    @override
    def component(self) -> Optional[str]:
        return self._text_col_name


class WordCount(Metric, ABC):
    def __init__(self, text_col_name: str):
        """
        Initializes a Word Count metric.

        :param text_col_name: text_col_name column name
        """
        self._text_col_name = text_col_name

    @override
    def metric(self) -> str:
        return "word_count"

    @override
    def name(self) -> str:
        return f"{self.metric()}__{self._text_col_name}"

    @override
    def type(self) -> Literal["int"]:
        return "int"

    @override
    def description(self) -> Optional[str]:
        return f"Computes the word count of the '{self._text_col_name}' column."

    @override
    def greater_is_better(self) -> Optional[bool]:
        return None

    @override
    def expression(self) -> str:
        return f"{self.metric()}({self._text_col_name})"

    @override
    def component(self) -> Optional[str]:
        return self._text_col_name

    @override
    def evaluate(self, df: pd.DataFrame) -> pd.Series[int]:
        if not self._text_col_name in df:
            raise ValueError(f"Missing text_col_name column {self._text_col_name} in {df}")
        nlp = _load_spacy_model()
        texts = df[self._text_col_name].tolist()
        docs = nlp.pipe(texts, disable=["tok2vec", "parser"])
        return pd.Series(
            [sum(1 for token in doc if token.is_alpha or token.is_digit) for doc in docs],
            dtype="int32[pyarrow]",
        )
