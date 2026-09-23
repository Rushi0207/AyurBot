from google import genai
from google.genai import types
from app.llm.interface import LLMProvider
from app.llm.types import LLMRequest, LLMResponse
class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, default_model: str):
        self.client = genai.Client(api_key=api_key)
        self.default_model = default_model
    def generate(self, request: LLMRequest) -> LLMResponse:
        system_instruction = None
        contents = []
        for message in request.messages:
            if message.role == "system":
                system_instruction = f"{system_instruction}\n{message.content}".strip() if system_instruction else message.content
            else:
                contents.append(types.Content(role="user" if message.role == "user" else "model", parts=[types.Part.from_text(text=message.content)]))
        response = self.client.models.generate_content(
            model=request.model or self.default_model,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=system_instruction, temperature=request.temperature, max_output_tokens=request.max_tokens),
        )
        usage = getattr(response, "usage_metadata", None)
        return LLMResponse(content=response.text or "", model=request.model or self.default_model, input_tokens=getattr(usage, "prompt_token_count", None), output_tokens=getattr(usage, "candidates_token_count", None), total_tokens=getattr(usage, "total_token_count", None))
