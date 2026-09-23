import os
import gradio as gr

from config import GEMINI_API_KEY, GEMINI_MODEL
from app.llm.providers.gemini import GeminiProvider
from app.llm.service import LLMService
from app.services.conversation import ConversationService
from app.services.safety import SafetyService
from app.ui.theme import build_theme


provider = GeminiProvider(GEMINI_API_KEY, GEMINI_MODEL)

conversation = ConversationService(
    LLMService(provider),
    SafetyService()
)

WELCOME = (
    "🌿 **Namaste! I'm AyurBot.**\n\n"
    "I can help you explore Ayurveda concepts, traditional terminology, "
    "herbs, daily routines, and general wellness information.\n\n"
    "Choose a topic below or ask me a question."
)


def respond(message, history):
    history = history or []

    if not message or not message.strip():
        return "", history

    try:
        answer = conversation.chat(message)

        history += [
            {
                "role": "user",
                "content": message.strip()
            },
            {
                "role": "assistant",
                "content": answer.content
            }
        ]

    except Exception as exc:
        history += [
            {
                "role": "user",
                "content": message.strip()
            },
            {
                "role": "assistant",
                "content": f"⚠️ I couldn't process that request.\n\n`{exc}`"
            }
        ]

    return "", history


def clear_chat():
    conversation.clear()

    return [
        {
            "role": "assistant",
            "content": WELCOME
        }
    ], ""


def quick(text, history):
    return respond(text, history)


with gr.Blocks(
    title="AyurBot — Ayurveda Knowledge Assistant",
    theme=build_theme(),
    css="""
    .hero {
        text-align: center;
        padding: 10px;
    }

    .disclaimer {
        text-align: center;
        font-size: 12px;
        opacity: 0.7;
        padding: 8px;
    }
    """
) as demo:

    gr.HTML(
        """
        <div class="hero">
            <h1>🌿 AyurBot</h1>
            <p>Ayurveda Knowledge & Wellness Assistant</p>
        </div>
        """
    )

    chatbot = gr.Chatbot(
        value=[
            {
                "role": "assistant",
                "content": WELCOME
            }
        ],
        type="messages",
        allow_tags=False,
        height=520,
        label="Conversation"
    )

    gr.Markdown("### Explore Ayurveda")

    with gr.Row():
        herbs = gr.Button("🌿 Herbs")
        routine = gr.Button("🧘 Daily Routine")
        basics = gr.Button("📚 Ayurveda Basics")
        doshas = gr.Button("🪷 Doshas")

    with gr.Row():
        message = gr.Textbox(
            placeholder="Ask about Ayurveda...",
            show_label=False,
            lines=2,
            scale=8
        )

        send = gr.Button(
            "Send ➤",
            variant="primary",
            scale=1
        )

    clear = gr.Button("Clear Chat")

    gr.Markdown(
        """
        <div class="disclaimer">
            AyurBot provides educational information about Ayurveda.
            It does not diagnose conditions or provide personalized treatment.
        </div>
        """
    )

    send.click(
        respond,
        inputs=[message, chatbot],
        outputs=[message, chatbot]
    )

    message.submit(
        respond,
        inputs=[message, chatbot],
        outputs=[message, chatbot]
    )

    herbs.click(
        lambda h: quick(
            "Explain the traditional Ayurvedic understanding of herbs and how herbs are generally discussed in Ayurveda.",
            h
        ),
        inputs=[chatbot],
        outputs=[message, chatbot]
    )

    routine.click(
        lambda h: quick(
            "What is Dinacharya in Ayurveda? Explain the concept and common traditional practices.",
            h
        ),
        inputs=[chatbot],
        outputs=[message, chatbot]
    )

    basics.click(
        lambda h: quick(
            "Give me a beginner-friendly introduction to Ayurveda and its major concepts.",
            h
        ),
        inputs=[chatbot],
        outputs=[message, chatbot]
    )

    doshas.click(
        lambda h: quick(
            "Explain Vata, Pitta, and Kapha in Ayurveda and clearly describe them as traditional Ayurvedic concepts.",
            h
        ),
        inputs=[chatbot],
        outputs=[message, chatbot]
    )

    clear.click(
        clear_chat,
        inputs=[],
        outputs=[chatbot, message]
    )

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )