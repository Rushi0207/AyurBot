from app.llm.interface import LLMProvider
from app.llm.types import LLMRequest, LLMResponse
class LLMService:
    def __init__(self, provider: LLMProvider): self.provider = provider
    def generate(self, request: LLMRequest) -> LLMResponse: return self.provider.generate(request)
