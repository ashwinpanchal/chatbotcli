from openai import OpenAI

from ...config import settings
from .base import BaseProvider, Message, ProviderResponse


class OpenAIProvider(BaseProvider):
    name = "openai"
    pricing = {
        "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
        "gpt-4o": {"input": 5.00 / 1_000_000, "output": 15.00 / 1_000_000},
        "gpt-4-turbo": {"input": 10.00 / 1_000_000, "output": 30.00 / 1_000_000},
    }

    def __init__(self, model: str):
        super().__init__(model)
        self.client = OpenAI(api_key=settings.OPEN_API_SECRET_KEY.get_secret_value())

    def complete(self, messages: list[Message]) -> ProviderResponse:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[message.model_dump() for message in messages],
        )

        usage = response.usage
        return ProviderResponse(
            response=response.choices[0].message.content,
            input_token=usage.prompt_tokens,
            output_token=usage.completion_tokens,
        )
