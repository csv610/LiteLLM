"""
feynman_tutor_gradio.py - Gradio interface for the FeynmanTutor application.
"""

import gradio as gr
import sys
from pathlib import Path
import logging
from lite.logging_config import configure_logging

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / f"{Path(__file__).stem}.log"))
logger = logging.getLogger(__name__)

from app.DigiTeacher.FeynmanTutor.feynman_tutor import (
    FeynmanTutorQuestionGenerator,
    ModelConfig,
)


def run_feynman_tutor_gradio(topic: str, level: str):
    """Run the Feynman tutor for Gradio interface - browser output only."""
    if not topic.strip():
        logger.warning("Empty topic provided")
        return "Please provide a topic to learn about.", "", None

    if not level.strip():
        level = "beginner"  # Default level

    try:
        logger.info(f"Starting Feynman tutor for topic: {topic}, level: {level}")
        config = ModelConfig(topic=topic, level=level)
        tutor = FeynmanTutorQuestionGenerator(config)

        # Start the tutoring session
        response = tutor.start_tutoring()

        # For Gradio, we just return the response to display in browser (no file saving)
        output = f"""# 🧠 Feynman-Style AI Tutor

**Topic:** {topic}
**Level:** {level}

---

{response}

---

**Instructions:**
- Enter your explanation or response in the text box below
- Click "Submit Response" to continue the learning loop
- Type "exit", "quit", or "goodbye" to end the session
- The tutor will guide you until you can explain the concept simply
"""
        logger.info(f"Feynman tutor initialized for topic: {topic}")
        return output, "", None  # No tutor state needed for browser-only version
    except Exception as e:
        logger.error(f"Error initializing tutor: {str(e)}", exc_info=True)
        return f"Error initializing tutor: {str(e)}", "", None


def process_response_gradio(topic, level, user_input):
    """Process student response for Gradio interface - browser output only."""
    if not user_input.strip():
        logger.warning("Empty user input provided")
        return "Please enter a response."

    if user_input.lower() in ["exit", "quit", "goodbye"]:
        logger.info("User ended tutoring session")
        return """👋 Keep exploring! The more you simplify, the more you understand."""

    # For simplicity in browser version, we'll provide a generic response
    # In a full implementation, we'd maintain state, but for browser-only we simplify
    return f"""🧠 Feynman: Thank you for your explanation. Let me help you refine it further.

To improve your explanation:
1. Try to use simpler language
2. Use analogies or everyday examples
3. Explain as if teaching to a 12-year-old
4. Identify the core concept and build from there

Please try again or type "exit" to end the session."""


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating FeynmanTutor Gradio interface")
    with gr.Blocks(title="FeynmanTutor - Learn by Teaching") as interface:
        gr.Markdown("# 🧠 Feynman-Style AI Tutor")
        gr.Markdown("Learn any topic by attempting to teach it to an AI tutor.")

        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(
                    label="📌 Topic",
                    placeholder="Enter the topic you want to learn about...",
                    lines=1,
                )
                level_input = gr.Dropdown(
                    label="📊 Your Current Understanding",
                    choices=["beginner", "intermediate", "advanced"],
                    value="beginner",
                )
                start_btn = gr.Button("Start Learning Session", variant="primary")

            with gr.Column():
                # We'll use a chatbot-like interface for the conversation
                chatbot = gr.Chatbot(
                    label="Tutoring Session", height=400, show_label=True
                )
                msg_input = gr.Textbox(
                    label="👤 Your Response",
                    placeholder="Enter your explanation or response here...",
                    lines=2,
                )
                send_btn = gr.Button("Submit Response", variant="secondary")
                clear_btn = gr.Button("Clear Session")

        # Event handlers
        start_btn.click(
            fn=run_feynman_tutor_gradio,
            inputs=[topic_input, level_input],
            outputs=[chatbot, msg_input],
        )

        send_btn.click(
            fn=process_response_gradio,
            inputs=[topic_input, level_input, msg_input],
            outputs=[chatbot],
        ).then(
            lambda: "",  # Clear the input after sending
            None,
            msg_input,
        )

        # Allow pressing Enter to submit
        msg_input.submit(
            fn=process_response_gradio,
            inputs=[topic_input, level_input, msg_input],
            outputs=[chatbot],
        ).then(
            lambda: "",  # Clear the input after sending
            None,
            msg_input,
        )

        clear_btn.click(
            lambda: ([], None),  # Clear chatbot
            None,
            [chatbot],
        )

        gr.Markdown("""
        ### How to Use
        1. Enter the topic you want to learn about
        2. Select your current understanding level (beginner/intermediate/advanced)
        3. Click "Start Learning Session" to begin
        4. The tutor will ask you to explain the concept
        5. Enter your explanation in the response box and click "Submit Response"
        6. Continue the dialogue by refining your explanation based on feedback
        7. Type "exit", "quit", or "goodbye" to end the session early
        
        ### About the Feynman Technique
        The Feynman Technique is a learning method where you:
        - Choose a concept to learn
        - Attempt to explain it in simple terms
        - Identify gaps in your explanation
        - Review and simplify further
        - Repeat until you can explain it clearly
        
        Note: Gradio interface displays results in browser only (no file saving or state persistence).
        For persistent tutoring sessions, use the CLI version.
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting FeynmanTutor Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7863, share=False)
