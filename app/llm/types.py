from dataclasses import dataclass
from typing import Literal
Role = Literal["system", "user", "assistant"]
@dataclass
class Message:
    role: Role
    content: str
@dataclass
class LLMRequest:
    messages: list[Message]
    model: str | None = None
    temperature: float = 0.4
    max_tokens: int = 1024
@dataclass
class LLMResponse:
    content: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
