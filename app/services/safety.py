class SafetyService:
    URGENT_TERMS = ("chest pain", "difficulty breathing", "can't breathe", "cannot breathe", "severe bleeding", "unconscious", "stroke", "suicide", "overdose")
    def is_urgent(self, message: str) -> bool:
        return any(term in message.lower() for term in self.URGENT_TERMS)
    def safety_message(self, message: str) -> str | None:
        if self.is_urgent(message):
            return "This may involve an urgent health situation. Please seek appropriate emergency or professional medical care rather than relying on a chatbot or home remedy."
        return None
