"""
deep_deliberation_gradio.py - Gradio interface for the DeepDeliberation application.
"""

import gradio as gr
import asyncio
import sys
import os
import re
from pathlib import Path
from typing import Optional

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from lite import ModelConfig
from .deep_deliberation import DeepDeliberation
from .deep_deliberation_models import KnowledgeSynthesis


async def run_discovery_gradio(
    topic: str, num_rounds: int, num_faqs: int, model: Optional[str] = None
):
    """Run the knowledge discovery mission for Gradio interface."""
    if not topic.strip():
        return "Please provide a topic for discovery."

    try:
        model_name = model or os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")
        model_config = ModelConfig(model=model_name, temperature=0.7)

        engine = DeepDeliberation(model_config=model_config)
        result = engine.run(topic, num_rounds, num_faqs)

        # Format the output
        output = f"""# Strategic Knowledge Map

**Topic:** {result.topic}

## Executive Summary
{result.executive_summary}

## Hidden Connections
"""
        for conn in result.hidden_connections:
            output += f"- {conn}\n"

        output += "\n## Research Frontiers\n"
        for frontier in result.research_frontiers:
            output += f"- {frontier}\n"

        output += f"\n---\n*Discovery mission completed successfully.*"

        return output
    except Exception as e:
        return f"Error during discovery mission: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(title="DeepDeliberation - Knowledge Discovery Engine") as interface:
        gr.Markdown("# DeepDeliberation")
        gr.Markdown(
            "Probing the boundaries of a topic through iterative discovery rounds."
        )

        with gr.Row():
            with gr.Column():
                topic_input = gr.Textbox(
                    label="Topic of Inquiry",
                    placeholder="Enter the field or topic you want to explore...",
                    lines=2,
                )
                num_rounds_slider = gr.Slider(
                    label="Number of Discovery Rounds",
                    minimum=1,
                    maximum=10,
                    value=3,
                    step=1,
                )
                num_faqs_slider = gr.Slider(
                    label="Number of Initial Strategic Probes (FAQs)",
                    minimum=1,
                    maximum=20,
                    value=5,
                    step=1,
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
                discovery_btn = gr.Button("Start Discovery Mission", variant="primary")

            with gr.Column():
                discovery_output = gr.Textbox(
                    label="Discovery Results",
                    lines=25,
                    max_lines=40,
                    show_copy_button=True,
                )

        discovery_btn.click(
            fn=run_discovery_gradio,
            inputs=[topic_input, num_rounds_slider, num_faqs_slider, model_dropdown],
            outputs=discovery_output,
            api_name="discover_knowledge",
        )

        gr.Markdown("""
        ### How to Use
        1. Enter the topic you want to explore in the input box
        2. Configure the number of discovery rounds and initial strategic probes
        3. Select the LLM model to use for the discovery process
        4. Click "Start Discovery Mission" to begin the iterative exploration
        5. The results will appear in the output box showing:
           - Executive summary of findings
           - Hidden connections discovered
           - Research frontiers identified
        
        ### About DeepDeliberation
        DeepDeliberation uses a multi-agent approach to probe the boundaries of knowledge:
        - Generates strategic questions to explore a topic
        - Conducts iterative discovery rounds
        - Identifies hidden connections between concepts
        - Maps out research frontiers and open questions
        """)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7861, share=False)
