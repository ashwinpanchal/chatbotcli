from pydantic import BaseModel
from typing import Literal
from abc import ABC, abstractmethod

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ProviderResponse(BaseModel):
    response : str
    input_token : int
    output_token : int

class BaseProvider(ABC):
    name: str
    pricing: dict[str, dict[str, float]] = {}

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def complete(self, messages: list[Message]) -> ProviderResponse:
        ...

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        rates = self.pricing.get(self.model, {"input": 0.0, "output": 0.0})
        return (input_tokens * rates["input"]) + (output_tokens * rates["output"])