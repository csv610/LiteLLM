"""
bookchapters_gradio.py - Gradio interface for the BookChaptersGenerator application.
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

# Add project root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / f"{Path(__file__).stem}.log"))
logger = logging.getLogger(__name__)

from lite.config import ModelConfig
from .bookchapters_generator import BookChaptersGenerator
from .bookchapters_models import BookInput


def generate_chapters_gradio(
    subject: str,
    level: str = None,
    num_chapters: int = 12,
    model_name: str = "ollama/gemma3",
):
    """Generate book chapters for Gradio interface - browser output only."""
    if not subject.strip():
        logger.warning("Empty subject provided")
        return "Please provide a subject or topic."

    try:
        # Create ModelConfig and BookChaptersGenerator
        model_config = ModelConfig(model=model_name, temperature=0.2)
        generator = BookChaptersGenerator(model_config)

        # Create BookInput
        book_input = BookInput(
            subject=subject.strip(),
            level=level.strip() if level and level.strip() else None,
            num_chapters=num_chapters,
        )

        # Generate curriculum (but don't save to file - just return result)
        result = generator.generate(book_input)

        level_display = level if level and level.strip() else "All Levels"
        logger.info(
            f"Generated chapters for subject: {subject}, level: {level_display}"
        )
        return f"""# Chapter Suggestions Generated Successfully

**Subject:** {subject}
**Education Level:** {level_display}
**Number of Chapters:** {num_chapters}
**Model Used:** {model_name}

---

## Generated Content

{result}

---
*Results displayed in browser only (not saved to file per Gradio interface requirements).*"""

    except Exception as e:
        logger.error(f"Error generating chapters: {str(e)}", exc_info=True)
        return f"Error generating chapters: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating BookChaptersGenerator Gradio interface")
    # Import level codes for the dropdown
    try:
        from .bookchapters_prompts import LEVEL_CODES

        level_choices = [""] + list(LEVEL_CODES.keys())  # Empty option for "All Levels"
    except ImportError:
        # Fallback if we can't import
        level_choices = [
            "",
            "Early Childhood",
            "Elementary School",
            "Middle School",
            "High School",
            "Undergraduate",
            "Post-Graduate",
            "General Public",
        ]

    with gr.Blocks(
        title="BookChaptersGenerator - Educational Curriculum Generator"
    ) as interface:
        gr.Markdown("# 📚 BookChaptersGenerator")
        gr.Markdown(
            "Generate educational curriculum chapters for any subject across education levels."
        )

        with gr.Row():
            with gr.Column():
                subject_input = gr.Textbox(
                    label="📖 Subject or Topic",
                    placeholder="Enter the subject or topic to create curriculum for...",
                    lines=1,
                )
                level_dropdown = gr.Dropdown(
                    label="🎓 Education Level (Optional)",
                    choices=level_choices,
                    value="",
                    allow_custom_value=True,
                )
                num_chapters_slider = gr.Slider(
                    label="📖 Number of Chapters per Level",
                    minimum=1,
                    maximum=50,
                    value=12,
                    step=1,
                )
                model_dropdown = gr.Dropdown(
                    label="🤖 LLM Model",
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
                generate_btn = gr.Button(
                    "Generate Chapter Suggestions", variant="primary"
                )

            with gr.Column():
                output_display = gr.Markdown(
                    label="📄 Generated Content",
                    value="Generated content will appear here...",
                )

        generate_btn.click(
            fn=generate_chapters_gradio,
            inputs=[subject_input, level_dropdown, num_chapters_slider, model_dropdown],
            outputs=output_display,
            api_name="generate_chapters",
        )

        gr.Markdown("""
        ### How to Use
        1. Enter the subject or topic you want to create curriculum for
        2. Optionally select an education level (leave empty for all levels)
        3. Specify the number of chapters to generate per level
        4. Select the LLM model to use for generation
        5. Click "Generate Chapter Suggestions" to create the curriculum
        6. The generated chapters will appear in the output box (browser only)
        
        ### Education Levels
        - **Early Childhood**: Preschool and kindergarten levels
        - **Elementary School**: Grades 1-5
        - **Middle School**: Grades 6-8
        - **High School**: Grades 9-12
        - **Undergraduate**: College/bachelor's degree level
        - **Post-Graduate**: Master's, PhD, and advanced studies
        - **General Public**: Popular science/literature level for adults
        
        ### About BookChaptersGenerator
        This tool uses AI to generate structured educational curriculum:
        - Creates logically sequenced chapter suggestions
        - Adapts content complexity to the specified education level
        - Generates comprehensive outlines for complete learning paths
        - Note: Gradio interface displays results in browser only (no file saving)
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting BookChaptersGenerator Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7866, share=False)
