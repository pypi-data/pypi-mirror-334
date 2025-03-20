from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from openai import AzureOpenAI
from typing_extensions import override

from .embedding_client import (
    EmbeddingClient,
    EmbeddingResponse,
    rate_limit_call_wrapper,
    replace_empty_string_with_space_wrapper,
)
from .openai_embedding_client import DEFAULT_EMBEDDING_MODEL


class AzureOpenAIEmbeddingClient(EmbeddingClient):
    """Embedding client that wraps the OpenAI client."""

    def __init__(
        self, api_key: str, api_version: str, azure_endpoint: str, embedding_model: str = DEFAULT_EMBEDDING_MODEL
    ):
        """
        :param api_key: Azure OpenAI API key.
        :param api_version: Azure OpenAI API version.
        :param azure_endpoint: Azure OpenAI endpoint.
        """
        self._client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
        self._embedding_model = embedding_model

    @classmethod
    def from_existing_client(
        cls, client: AzureOpenAI, embedding_model: str = DEFAULT_EMBEDDING_MODEL
    ) -> AzureOpenAIEmbeddingClient:
        """Create an instance of AzureOpenAIEmbeddingClient from an existing AzureOpenAI client."""
        parsed_url = urlparse(str(client._base_url))
        return AzureOpenAIEmbeddingClient(
            api_key=client.api_key,
            api_version=client._api_version,
            azure_endpoint=f"{parsed_url.scheme}://{parsed_url.netloc}",
            embedding_model=embedding_model,
        )

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
