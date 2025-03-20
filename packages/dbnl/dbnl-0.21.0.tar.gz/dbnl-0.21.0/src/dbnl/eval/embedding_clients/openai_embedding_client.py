from __future__ import annotations

from typing import Any

from openai import OpenAI
from typing_extensions import override

from .embedding_client import (
    EmbeddingClient,
    EmbeddingResponse,
    rate_limit_call_wrapper,
    replace_empty_string_with_space_wrapper,
)

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class OpenAIEmbeddingClient(EmbeddingClient):
    """Embedding client that wraps the OpenAI client."""

    def __init__(self, api_key: str, embedding_model: str = DEFAULT_EMBEDDING_MODEL):
        """
        Initialize the OpenAIEmbeddingClient with the provided API key and embedding model

        :param api_key: Azure OpenAI API key.
        :param api_version: Azure OpenAI API version.
        :param azure_endpoint: Azure OpenAI endpoint.
        :param llm_model: LLM model.
        """
        self._client = OpenAI(api_key=api_key)
        self._embedding_model = embedding_model

    @classmethod
    def from_existing_client(
        cls, client: OpenAI, embedding_model: str = DEFAULT_EMBEDDING_MODEL
    ) -> OpenAIEmbeddingClient:
        """
        :param client: Existing OpenAI client.
        :param embedding_model: Embedding model.
        :return: An instance of OpenAIEmbeddingClient.
        """
        return OpenAIEmbeddingClient(api_key=client.api_key, embedding_model=embedding_model)

    @override
    def id(self) -> str:
        """
        Returns a unique identifier for the OpenAI Embedding client.

        :return: OpenAI Embedding client id.
        """
        return f"openai:/{self._embedding_model}"

    @override
    @replace_empty_string_with_space_wrapper
    @rate_limit_call_wrapper
    def call(self, texts: list[str]) -> list[EmbeddingResponse]:
        """
        Calls the OpenAI Embedding provider with the provided texts.

        """
        response = self._client.embeddings.create(input=texts, model=self._embedding_model)
        res = []
        for r in response.data:
            response_dict: dict[str, Any] = r.to_dict()
            embedding_response = EmbeddingResponse(embedding=response_dict["embedding"])
            res.append(embedding_response)
        return res
