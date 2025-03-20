from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from dbnl.print_logging import dbnl_logger
from dbnl.tqdm import tqdm

T = TypeVar("T")
CHUNK_SIZE = 100
SECONDS_BETWEEN_REQUESTS = 5


@dataclass
class EmbeddingResponse:
    """
    Dataclass to hold the response from an Embedding provider.

    :param embedding: Embedding vector.
    :param prompt: Prompt used to generate the embedding.
    """

    embedding: list[float]


class EmbeddingClient(ABC):
    """Abstract interface to be implemented by all Embedding providers."""

    _embedding_model: Any

    @abstractmethod
    def id(self) -> str:
        """
        Returns a unique identifier for the Embedding client.

        :return: Embedding client id.
        """
        raise NotImplementedError()

    @abstractmethod
    def call(self, texts: list[str]) -> list[EmbeddingResponse]:
        """
        Calls the underlying Embedding provider with the provided prompt.

        :param texts: List of strings to created embeddings for
        :return: List of EmbeddingResponse objects.
        """
        raise NotImplementedError()


def replace_empty_string_with_space_wrapper(
    func: Callable[[T, list[str]], list[EmbeddingResponse]],
) -> Callable[[T, list[str]], list[EmbeddingResponse]]:
    """
    Decorator to replace None values in the input list with empty strings.

    :param func: Function to decorate.
    :return: Decorated function.
    """

    def wrapper(self: T, texts: list[str]) -> list[EmbeddingResponse]:
        updated_texts = []
        for text in texts:
            if type(text) != str:
                raise TypeError(f"Expected text to be of type str, got {type(text)}")
            if text == "":
                updated_texts.append(" ")
            else:
                updated_texts.append(text)
        return func(self, updated_texts)

    return wrapper


def rate_limit_call_wrapper(
    func: Callable[[T, list[str]], list[EmbeddingResponse]],
    chunk_size: int = CHUNK_SIZE,
    seconds_between_requests: int = SECONDS_BETWEEN_REQUESTS,
) -> Callable[[T, list[str]], list[EmbeddingResponse]]:
    """
    Decorator to rate limit the calls to the underlying function.

    :param func: Function to decorate.
    :return: Decorated function.
    """

    def wrapper(self: T, texts: list[str]) -> list[EmbeddingResponse]:
        embeddings = []
        for chunk in _chunk_list(texts, chunk_size, chunk_name="texts"):
            embeddings.extend(func(self, chunk))
            time.sleep(seconds_between_requests)
        return embeddings

    return wrapper


def _chunk_list(lst: list[str], chunk_size: int, chunk_name: str) -> Generator[list[Any], None, None]:
    dbnl_logger.info(f"Chunking {chunk_name} column, total length: {len(lst)}")
    for i in tqdm(
        range(0, len(lst), chunk_size),
        desc=f"Chunking {chunk_name} column (chunk size: {chunk_size})",
        unit="chunk",
        total=(len(lst) + chunk_size - 1) // chunk_size,
    ):
        yield list(lst[i : i + chunk_size])
