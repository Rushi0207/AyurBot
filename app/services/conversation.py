from app.llm.service import LLMService
from app.llm.types import LLMRequest, Message, LLMResponse
from app.prompts.ayurveda import SYSTEM_PROMPT
from app.services.safety import SafetyService
class ConversationService:
    def __init__(self, llm: LLMService, safety: SafetyService, max_history: int = 20):
        self.llm, self.safety, self.max_history = llm, safety, max_history
        self.history: list[Message] = []
    def chat(self, user_message: str) -> LLMResponse:
        user_message = user_message.strip()
        if not user_message: raise ValueError("Message cannot be empty.")
        if len(user_message) > 4000: raise ValueError("Message is too long. Maximum length is 4000 characters.")
        safety_message = self.safety.safety_message(user_message)
        if safety_message:
            response = LLMResponse(safety_message, "safety-layer")
        else:
            messages = [Message("system", SYSTEM_PROMPT), *self.history[-self.max_history:], Message("user", user_message)]
            response = self.llm.generate(LLMRequest(messages=messages, temperature=0.4, max_tokens=1024))
        self.history.extend([Message("user", user_message), Message("assistant", response.content)])
        self.history = self.history[-self.max_history:]
        return response
    def clear(self): self.history.clear()
