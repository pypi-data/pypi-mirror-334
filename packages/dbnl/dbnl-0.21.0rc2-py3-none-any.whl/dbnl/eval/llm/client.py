from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI, OpenAI
from typing_extensions import override


@dataclass
class LLMResponse:
    content: Optional[str]


class LLMClient(ABC):
    """Abstract interface to be implemented by all LLM providers."""

    @abstractmethod
    def id(self) -> str:
        """
        Returns a unique identifier for the LLM client. For example, an LLM client for the OpenAPI
        GPT-4 model might have an id of `openai:gpt4`. Used to uniquely identify the client.

        :return: LLM client id.
        """
        raise NotImplementedError()

    @abstractmethod
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the underlying LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        raise NotImplementedError()


class OpenAILLMClient(LLMClient):
    """LLM client that wraps the OpenAI client."""

    def __init__(self, api_key: str, llm_model: str):
        """
        Initialize the AzureOpenAILLMClient with the provided API key, API version, Azure endpoint, and LLM model.

        :param api_key: Azure OpenAI API key.
        :param api_version: Azure OpenAI API version.
        :param azure_endpoint: Azure OpenAI endpoint.
        :param llm_model: LLM model.
        """
        self.client = OpenAI(api_key=api_key)
        self.temperature = 0.0
        self.llm_model = llm_model

    @classmethod
    def from_existing_client(cls, client: OpenAI, llm_model: str) -> LLMClient:
        """
        Alternative constructor that initializes the AzureOpenAILLMClient with an existing AzureOpenAI client and LLM model.

        :param client: Existing AzureOpenAI client.
        :param llm_model: LLM model.
        :return: An instance of AzureOpenAILLMClient.
        """
        instance = cls.__new__(cls)
        instance.client = client
        instance.llm_model = llm_model
        instance.temperature = 0.0
        return instance

    @override
    def id(self) -> str:
        """
        Returns a unique identifier for the Azure OpenAI LLM client.

        :return: Azure OpenAI LLM client id.
        """
        return f"openai:/{self.llm_model}"

    @override
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the OpenAI LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        if not system_prompt:
            system_prompt = "You are a helpful AI assistant"

        response = self.client.chat.completions.create(
            model=self.llm_model,
            temperature=self.temperature,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        )

        return LLMResponse(content=response.choices[0].message.content)


class AzureOpenAILLMClient(LLMClient):
    """LLM client that wraps the AzureOpenAI client."""

    def __init__(self, api_key: str, api_version: str, azure_endpoint: str, llm_model: str):
        """
        Initialize the AzureOpenAILLMClient with the provided API key, API version, Azure endpoint, and LLM model.

        :param api_key: Azure OpenAI API key.
        :param api_version: Azure OpenAI API version.
        :param azure_endpoint: Azure OpenAI endpoint.
        :param llm_model: LLM model.
        """
        self.client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)
        self.temperature = 0.0
        self.llm_model = llm_model

    @classmethod
    def from_existing_client(cls, client: AzureOpenAI, llm_model: str) -> LLMClient:
        """
        Alternative constructor that initializes the AzureOpenAILLMClient with an existing AzureOpenAI client and LLM model.

        :param client: Existing AzureOpenAI client.
        :param llm_model: LLM model.
        :return: An instance of AzureOpenAILLMClient.
        """
        instance = cls.__new__(cls)
        instance.client = client
        instance.llm_model = llm_model
        instance.temperature = 0.0
        return instance

    @override
    def id(self) -> str:
        """
        Returns a unique identifier for the Azure OpenAI LLM client.

        :return: Azure OpenAI LLM client id.
        """

        # at the moment this is id tightly coupled to model name checking behavior in mlflow
        # https://github.com/mlflow/mlflow/blob/e6c7d6e0362c92d6145d59b83534162cb0e8913f/mlflow/metrics/genai/model_utils.py#L13

        return f"openai:/{self.llm_model}"

    @override
    def call(self, prompt: str, system_prompt: Optional[str] = None) -> LLMResponse:
        """
        Calls the Azure OpenAI LLM provider with the provided prompt.

        :param prompt: Prompt text.
        :return: LLMResponse.
        """
        if not system_prompt:
            system_prompt = "You are a helpful AI assistant"

        response = self.client.chat.completions.create(
            model=self.llm_model,
            temperature=self.temperature,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        )

        return LLMResponse(content=response.choices[0].message.content)
