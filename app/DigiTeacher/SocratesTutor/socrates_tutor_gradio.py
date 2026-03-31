"""
socrates_tutor_gradio.py - Gradio interface for the SocratesTutor application.
"""

import gradio as gr
import sys
from pathlib import Path
import logging
from lite.logging_config import configure_logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / f"{Path(__file__).stem}.log"))
logger = logging.getLogger(__name__)

from .socrates_tutor import SocratesTutor


def run_socrates_tutor_gradio(topic: str, level: str):
    """Run the Socrates tutor for Gradio interface."""
    if not topic.strip():
        logger.warning("Empty topic provided")
        return "Please provide a concept or problem to explore.", None

    if not level.strip():
        level = "student"  # Default level

    try:
        logger.info(f"Starting Socrates tutor for topic: {topic}, level: {level}")
        tutor = SocratesTutor(topic, level)

        # Start the inquiry
        response = tutor.begin_inquiry()

        output = f"""# 🏛️ Socrates AI Tutor

**Concept/Problem:** {topic}
**Your Background:** {level}

---

{response}

---

**Instructions:**
- Enter your response or answer in the text box below
- Click "Submit Response" to continue the dialogue
- Socrates will guide you through questioning to discover truth
- Type "exit", "quit", or "goodbye" to end the session
"""
        return output, tutor  # Return initial response and tutor state
    except Exception as e:
        logger.error(f"Error initializing tutor: {str(e)}", exc_info=True)
        return f"Error initializing tutor: {str(e)}", None


def process_response_gradio(topic, level, user_input, tutor_state):
    """Process user response for Gradio interface."""
    if not user_input.strip():
        logger.warning("Empty user input provided")
        return "Please enter a response.", tutor_state

    if user_input.lower() in ["exit", "quit", "goodbye"]:
        logger.info("User ended inquiry session")
        return (
            """👋 Socrates: Farewell, seeker of wisdom. May your questions never cease!""",
            None,
        )

    if tutor_state is None:
        logger.error("Tutor state is None")
        return "Please start a new inquiry session first.", None

    try:
        # Process the user's response
        response = tutor_state.provide_response(user_input)

        output = f"""🧠 Socrates: {response}

---
"""

        if tutor_state.is_convinced:
            output += f"""--- [Inquiry Complete] ---
📊 Summary of Understanding: {tutor_state.summary}

🎉 Socrates: Our dialogue has reached its end. You have discovered the truth through your own reason.
"""
            logger.info(f"Inquiry completed for topic: {topic}")
            return output, None  # End session
        else:
            output += """👤 Your turn to respond:"""
            logger.debug(f"Continuing inquiry session for topic: {topic}")
            return output, tutor_state  # Continue session

    except Exception as e:
        logger.error(f"Error processing response: {str(e)}", exc_info=True)
        return f"Error processing response: {str(e)}", tutor_state


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating SocratesTutor Gradio interface")
    with gr.Blocks(
        title="SocratesTutor - Discover Truth Through Dialogue"
    ) as interface:
        gr.Markdown("# 🏛️ Socrates AI Tutor")
        gr.Markdown("Discover truth through dialectical questioning and dialogue.")

        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(
                    label="📌 Concept or Problem to Explore",
                    placeholder="What concept or problem shall we explore together?",
                    lines=1,
                )
                level_input = gr.Dropdown(
                    label="📊 Your Current Understanding",
                    choices=[
                        "student",
                        "beginner",
                        "intermediate",
                        "advanced",
                        "expert",
                        "confused",
                    ],
                    value="student",
                )
                start_btn = gr.Button("Begin Inquiry", variant="primary")

            with gr.Column():
                chatbot = gr.Chatbot(
                    label="Socratic Dialogue", height=400, show_label=True
                )
                msg_input = gr.Textbox(
                    label="👤 Your Response",
                    placeholder="Enter your response or answer here...",
                    lines=2,
                )
                send_btn = gr.Button("Submit Response", variant="secondary")
                clear_btn = gr.Button("Clear Session")

        # State to store the tutor instance
        tutor_state = gr.State(None)

        # Event handlers
        start_btn.click(
            fn=run_socrates_tutor_gradio,
            inputs=[topic_input, level_input],
            outputs=[chatbot, tutor_state],
        )

        send_btn.click(
            fn=process_response_gradio,
            inputs=[topic_input, level_input, msg_input, tutor_state],
            outputs=[chatbot, tutor_state],
        ).then(
            lambda: "",  # Clear the input after sending
            None,
            msg_input,
        )

        # Allow pressing Enter to submit
        msg_input.submit(
            fn=process_response_gradio,
            inputs=[topic_input, level_input, msg_input, tutor_state],
            outputs=[chatbot, tutor_state],
        ).then(
            lambda: "",  # Clear the input after sending
            None,
            msg_input,
        )

        clear_btn.click(
            lambda: ([], None),  # Clear chatbot and tutor state
            None,
            [chatbot, tutor_state],
        )

        gr.Markdown("""
        ### How to Use
        1. Enter the concept or problem you want to explore
        2. Select your current understanding level
        3. Click "Begin Inquiry" to start the Socratic dialogue
        4. Socrates will ask you probing questions to help you discover truth
        5. Enter your responses in the text box and click "Submit Response"
        6. Continue the dialogue until Socrates indicates you've reached understanding
        7. Type "exit", "quit", or "goodbye" to end the session early
        
        ### About the Socratic Method
        The Socratic method is a form of cooperative argumentative dialogue that:
        - Uses questioning to stimulate critical thinking
        - Helps uncover underlying assumptions
        - Leads to deeper understanding through self-discovery
        - Focuses on asking questions rather than giving answers
        
        This AI tutor embodies Socrates' approach, guiding you to discover truth through your own reasoning rather than simply imparting knowledge.
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting SocratesTutor Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7865, share=False)
