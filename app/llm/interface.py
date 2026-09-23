from abc import ABC, abstractmethod
from app.llm.types import LLMRequest, LLMResponse
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError
