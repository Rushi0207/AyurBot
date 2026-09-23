# 🌿 AyurBot V1

AyurBot is an Ayurveda-focused conversational assistant built with Python, Gradio, and Gemini.

## V1 includes
- Ayurveda-focused system prompt
- Gemini API through an LLM provider wrapper
- Conversation memory for the current session
- Herbs, Dinacharya, Ayurveda Basics, and Doshas quick prompts
- Lightweight urgent-symptom safety routing
- Educational disclaimer
- Gradio UI

## Setup
Use Python 3.12.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key.

```powershell
python app.py
```

## Architecture
```text
Gradio UI -> ConversationService -> SafetyService + LLMService -> LLMProvider -> GeminiProvider -> Gemini API
```

This is an educational wellness assistant, not a diagnostic or prescribing system.
