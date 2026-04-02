"""
deep_intuition_gradio.py - Gradio interface for the DeepIntuition application.
"""

import gradio as gr
import asyncio
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

from lite.config import ModelConfig
from app.DeepIntuition.agentic.deep_intuition import DeepIntuition


async def run_intuition_gradio(topic: str, model_name: str = None):
    """Run the deep intuition process for Gradio interface - returns Markdown."""
    if not topic.strip():
        logger.warning("Empty topic provided")
        return "Please provide a topic or idea to explore."

    if model_name is None or model_name == "":
        model_name = "ollama/gemma3"

    try:
        logger.info(
            f"Starting intuition process for topic: {topic[:50]}... with model: {model_name}"
        )
        model_config = ModelConfig(model=model_name, temperature=0.7)
        intuition_engine = DeepIntuition(model_config=model_config)

        # generate_story returns a Markdown string
        result_markdown = intuition_engine.generate_story(topic)

        logger.info(
            f"Intuition process completed for topic: {topic[:50]}..."
        )
        return result_markdown
    except Exception as e:
        logger.error(f"Error during deep intuition process: {str(e)}", exc_info=True)
        return f"Error during deep intuition process: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating DeepIntuition Gradio interface")
    with gr.Blocks(title="DeepIntuition - Uncovering the Human Story") as interface:
        gr.Markdown("# DeepIntuition")
        gr.Markdown(
            "Uncovering the human story and intuitive leaps behind fundamental ideas."
        )

        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(
                    label="Fundamental Idea or Topic",
                    placeholder="e.g., Galois Theory, The Second Law of Thermodynamics...",
                    lines=2,
                )
                model_dropdown = gr.Dropdown(
                    label="LLM Model",
                    choices=[
                        "ollama/gemma3",
                        "ollama/llama3",
                        "ollama/mistral",
                        "gpt-3.5-turbo",
                        "gpt-4",
                        "claude-3-haiku-20240307",
                        "claude-3-sonnet-20240229",
                    ],
                    value="ollama/gemma3",
                )
                intuition_btn = gr.Button("Explore Intuitively", variant="primary")

            with gr.Column():
                intuition_output = gr.Markdown(
                    label="Intuition Results",
                    value="The human story will appear here...",
                )

        intuition_btn.click(
            fn=run_intuition_gradio,
            inputs=[topic_input, model_dropdown],
            outputs=intuition_output,
            api_name="generate_story",
        )

        gr.Markdown("""
        ### How to Use
        1. Enter your problem statement or question in the input box
        2. Select the LLM model to use for the intuitive analysis
        3. Click "Start Intuitive Analysis" to begin the deep intuition process
        4. The results will appear in the output box showing:
           - Executive summary of the solution
           - Key insights discovered
           - Reasoning chain showing the intuitive thought process
           - Alternative perspectives considered
         
        ### About DeepIntuition
        DeepIntuition uses an intuitive approach to problem-solving:
        - Explores problems from multiple cognitive angles
        - Generates insights through pattern recognition and analogy
        - Builds reasoning chains that combine logic with intuition
        - Considers alternative perspectives to avoid cognitive biases
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting DeepIntuition Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7862, share=False)
