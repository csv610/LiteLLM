"""
article_reviewer_gradio.py - Gradio interface for the ArticleReviewer application.
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

from lite.config import ModelConfig  # noqa: E402
from app.ArticleReviewer.agentic.article_reviewer_agents import MultiAgentReviewer  # noqa: E402
from app.ArticleReviewer.agentic.article_reviewer_utils import format_review_markdown  # noqa: E402


async def run_review_gradio(article_text, model_name=None):
    """Run the multi-stage review for Gradio interface."""
    if not article_text.strip():
        logger.warning("Empty article text provided")
        return "Please provide an article text to review."

    if model_name is None or model_name == "":
        model_name = "ollama/gemma3"

    try:
        logger.info(f"Starting review with model: {model_name}")
        model_config = ModelConfig(model=model_name, temperature=0.3)
        reviewer = MultiAgentReviewer(model_config=model_config)

        review = await reviewer.review(article_text)

        logger.info("Review completed successfully")
        return format_review_markdown(review)
    except Exception as e:
        logger.error(f"Error during review: {str(e)}", exc_info=True)
        return f"Error during review: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating ArticleReviewer Gradio interface")
    with gr.Blocks(title="Article Reviewer") as interface:
        gr.Markdown("# Article Reviewer")
        gr.Markdown("Multi-stage article review workflow using LiteClient agents.")

        with gr.Row():
            with gr.Column():
                article_input = gr.Textbox(
                    label="Article Text",
                    placeholder="Paste your article text here...",
                    lines=10,
                    max_lines=20,
                )
                model_dropdown = gr.Dropdown(
                    label="Model",
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
                review_btn = gr.Button("Start Review", variant="primary")

            with gr.Column():
                review_output = gr.Markdown(
                    label="Review Results", value="Review results will appear here..."
                )

        review_btn.click(
            fn=run_review_gradio,
            inputs=[article_input, model_dropdown],
            outputs=review_output,
            api_name="review_article",
        )

        gr.Markdown("""
        ### How to Use
        1. Paste your article text in the input box
        2. Select the model you want to use for review
        3. Click "Start Review" to begin the multi-stage review process
        4. The review results will appear in the output box
        
        ### About the Review Process
        The multi-stage reviewer uses multiple AI agents to:
        - Analyze content quality and accuracy
        - Check for logical flow and structure
        - Evaluate engagement and readability
        - Provide constructive feedback and suggestions
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting ArticleReviewer Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
