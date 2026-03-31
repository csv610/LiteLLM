"""
hadamard_tutor_gradio.py - Gradio interface for the HadamardTutor application.
"""

import gradio as gr
import sys
from pathlib import Path
import logging
# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from lite.logging_config import configure_logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / f"{Path(__file__).stem}.log"))
logger = logging.getLogger(__name__)

from .hadamard_tutor import HadamardTutorQuestionGenerator


def run_hadamard_tutor_gradio(topic: str, level: str):
    """Run the Hadamard tutor for Gradio interface."""
    if not topic.strip():
        logger.warning("Empty topic provided")
        return "Please provide a topic or problem to explore.", None

    if not level.strip():
        level = "beginner"  # Default level

    try:
        logger.info(f"Starting Hadamard tutor for topic: {topic}, level: {level}")
        tutor = HadamardTutorQuestionGenerator(topic, level)

        # Start with preparation phase
        response = tutor.get_preparation_phase()

        output = f"""# 🧠 Hadamard Discovery Tutor

**Topic/Problem:** {topic}
**Context/Level:** {level}

---

{response}

---

**Instructions:**
- Enter your thoughts or response in the text box below
- Click "Submit Response" to continue through the discovery phases
- The tutor will guide you through Preparation → Incubation → Illumination → Verification
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
        logger.info("User ended tutoring session")
        return """👋 Hadamard: May your intuition stay sharp!""", None

    if tutor_state is None:
        logger.error("Tutor state is None")
        return "Please start a new tutoring session first.", None

    try:
        # Determine which phase we're in based on tutor state
        # For simplicity, we'll track phase internally in the tutor
        response = tutor_state.process_student_response(user_input)

        output = f"""🧠 Hadamard: {response}

---
"""

        if tutor_state.is_convinced:
            output += f"""--- [Discovery Complete] ---
📊 Summary of Breakthrough: {tutor_state.summary}

🎉 Hadamard: Brilliant! You have navigated the psychological path to invention.
"""
            logger.info(f"Discovery completed for topic: {topic}")
            return output, None  # End session
        else:
            output += """👤 Your turn to respond:"""
            logger.debug(f"Continuing tutoring session for topic: {topic}")
            return output, tutor_state  # Continue session

    except Exception as e:
        logger.error(f"Error processing response: {str(e)}", exc_info=True)
        return f"Error processing response: {str(e)}", tutor_state


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating HadamardTutor Gradio interface")
    with gr.Blocks(title="HadamardTutor - Discovery Through Four Phases") as interface:
        gr.Markdown("# 🧠 Hadamard Discovery Tutor")
        gr.Markdown(
            "Guiding you through Preparation, Incubation, Illumination, and Verification."
        )

        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(
                    label="📌 Topic or Problem",
                    placeholder="Enter the topic or problem you want to explore...",
                    lines=1,
                )
                level_input = gr.Dropdown(
                    label="📊 Your Current Level/Context",
                    choices=[
                        "beginner",
                        "intermediate",
                        "advanced",
                        "researching",
                        "stuck",
                    ],
                    value="beginner",
                )
                start_btn = gr.Button("Start Discovery Session", variant="primary")

            with gr.Column():
                chatbot = gr.Chatbot(
                    label="Discovery Session", height=400, show_label=True
                )
                msg_input = gr.Textbox(
                    label="👤 Your Response",
                    placeholder="Enter your thoughts or response here...",
                    lines=2,
                )
                send_btn = gr.Button("Submit Response", variant="secondary")
                clear_btn = gr.Button("Clear Session")

        # State to store the tutor instance
        tutor_state = gr.State(None)

        # Event handlers
        start_btn.click(
            fn=run_hadamard_tutor_gradio,
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
        1. Enter the topic or problem you want to explore
        2. Select your current level/context (beginner/intermediate/advanced/researching/stuck)
        3. Click "Start Discovery Session" to begin
        4. The tutor will guide you through the four phases of discovery:
           - **Preparation**: Gather information and explore the problem
           - **Incubation**: Let ideas simmer subconsciously
           - **Illumination**: Experience the "aha!" moment
           - **Verification**: Test and refine your solution
        5. Enter your thoughts in the response box and click "Submit Response"
        6. Continue through the phases until the tutor confirms your discovery
        7. Type "exit", "quit", or "goodbye" to end the session early
        
        ### About the Hadamard Method
        Based on Jacques Hadamard's study of mathematical invention, this method involves:
        - **Preparation**: Conscious work on the problem
        - **Incubation**: Unconscious processing while focusing on other things
        - **Illumination**: Sudden insight or "aha!" moment
        - **Verification**: Conscious verification and elaboration of the insight
        
        This AI tutor guides you through these phases, helping you discover breakthroughs in your thinking.
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting HadamardTutor Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7864, share=False)
