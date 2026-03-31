"""
deep_intuition_gradio.py - Gradio interface for the DeepIntuition application.
"""

import gradio as gr
import asyncio
import sys
from pathlib import Path
import logging
from lite.logging_config import configure_logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / f"{Path(__file__).stem}.log"))
logger = logging.getLogger(__name__)

from lite.config import ModelConfig
from .deep_intuition import DeepIntuition


async def run_intuition_gradio(problem_statement: str, model_name: str = None):
    """Run the deep intuition process for Gradio interface - browser output only."""
    if not problem_statement.strip():
        logger.warning("Empty problem statement provided")
        return "Please provide a problem statement or question."

    if model_name is None or model_name == "":
        model_name = "ollama/gemma3"

    try:
        logger.info(
            f"Starting intuition process for problem: {problem_statement[:50]}... with model: {model_name}"
        )
        model_config = ModelConfig(model=model_name, temperature=0.7)
        intuition_engine = DeepIntuition(model_config=model_config)

        result = intuition_engine.solve(problem_statement)

        # Format the output for browser display only
        output = f"""# Deep Intuition Solution

**Problem:** {result.problem_statement}

## Executive Summary
{result.executive_summary}

## Key Insights
"""
        for i, insight in enumerate(result.key_insights, 1):
            output += f"{i}. {insight}\n"

        output += "\n## Reasoning Chain\n"
        for i, step in enumerate(result.reasoning_chain, 1):
            output += f"{i}. {step}\n"

        if result.alternative_perspectives:
            output += "\n## Alternative Perspectives\n"
            for perspective in result.alternative_perspectives:
                output += f"- {perspective}\n"

        logger.info(
            f"Intuition process completed for problem: {problem_statement[:50]}..."
        )
        return output
    except Exception as e:
        logger.error(f"Error during deep intuition process: {str(e)}", exc_info=True)
        return f"Error during deep intuition process: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating DeepIntuition Gradio interface")
    with gr.Blocks(title="DeepIntuition - Intuitive Problem Solving") as interface:
        gr.Markdown("# DeepIntuition")
        gr.Markdown(
            "Intuitive problem-solving approach that explores problems from multiple angles."
        )

        with gr.Row():
            with gr.Column():
                problem_input = gr.Textbox(
                    label="Problem Statement or Question",
                    placeholder="Enter the problem you want to solve intuitively...",
                    lines=4,
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
                intuition_btn = gr.Button("Start Intuitive Analysis", variant="primary")

            with gr.Column():
                intuition_output = gr.Markdown(
                    label="Intuition Results",
                    value="Intuition results will appear here...",
                )

        intuition_btn.click(
            fn=run_intuition_gradio,
            inputs=[problem_input, model_dropdown],
            outputs=intuition_output,
            api_name="solve_intuitively",
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
