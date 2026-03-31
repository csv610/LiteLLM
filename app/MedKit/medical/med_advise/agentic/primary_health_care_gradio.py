"""
primary_health_care_gradio.py - Gradio interface for the Primary Health Care Advisor application.
"""

import gradio as gr
import sys
import os
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from lite.config import ModelConfig

try:
    from .primary_health_care import PrimaryHealthCareProvider
except (ImportError, ValueError):
    try:
        from medical.med_advise.agentic.primary_health_care import (
            PrimaryHealthCareProvider,
        )
    except (ImportError, ValueError):
        from medical.med_advise.agentic.primary_health_care import (
            PrimaryHealthCareProvider,
        )


def get_health_advice(query: str, model_name: str, structured: bool):
    """Get primary health care advice for a health concern."""
    if not query.strip():
        return "Please enter a health concern or question."

    try:
        model_config = ModelConfig(model=model_name, temperature=0.2)
        provider = PrimaryHealthCareProvider(model_config)
        result = provider.generate_text(query=query.strip(), structured=structured)

        if result:
            # Save result to outputs directory
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            # Create a safe filename from the query
            safe_query = "".join(c if c.isalnum() else "_" for c in query.strip())[:50]
            output_file = output_dir / f"health_advice_{safe_query.lower()}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)

            return f"""## Primary Health Care Advice

**Your Question:** {query}

{result}

---
*Advice saved to: {output_file}*"""
        else:
            return f"Unable to generate advice for: {query}"

    except Exception as e:
        return f"Error generating health advice: {str(e)}"


def process_health_queries_file(file_path, model_name: str, structured: bool):
    """Process a file containing multiple health queries."""
    if not file_path:
        return "Please upload a file with health queries."

    if not os.path.exists(file_path.name):
        return f"File not found: {file_path.name}"

    try:
        # Read queries from file
        with open(file_path.name, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]

        if not queries:
            return "The file is empty or contains no valid queries."

        model_config = ModelConfig(model=model_name, temperature=0.2)
        provider = PrimaryHealthCareProvider(model_config)

        results = []
        for query in queries:
            result = provider.generate_text(query=query, structured=structured)
            if result:
                results.append(f"**Query:** {query}\n\n{result}\n\n{'-' * 50}\n")

        if results:
            # Save combined results
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / "health_advice_batch.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n\n".join(results))

            return f"""## Batch Health Advice Results

Processed {len(queries)} health queries.

{chr(10).join(results)}

---
*All advice saved to: {output_file}*"""
        else:
            return "Unable to generate advice for any of the queries."

    except Exception as e:
        return f"Error processing health queries file: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(title="Primary Health Care Advisor") as interface:
        gr.Markdown("# 🏥 Primary Health Care Advisor")
        gr.Markdown(
            "Get preliminary health information and advice for common health concerns."
        )

        with gr.Tabs():
            # Single Query Tab
            with gr.TabItem("💬 Single Health Query"):
                with gr.Row():
                    with gr.Column():
                        query_input = gr.Textbox(
                            label="Health Concern or Question",
                            placeholder="Describe your health concern or question (e.g., 'I have a headache and fever', 'What are symptoms of diabetes?')",
                            lines=3,
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
                        structured_checkbox = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        advice_btn = gr.Button("Get Health Advice", variant="primary")

                    with gr.Column():
                        advice_output = gr.Markdown(label="Health Advice")

                advice_btn.click(
                    fn=get_health_advice,
                    inputs=[query_input, model_dropdown, structured_checkbox],
                    outputs=advice_output,
                )

                gr.Markdown("""
                ### About Single Health Queries
                Enter a specific health concern or question to get preliminary information and advice.
                The advisor provides general health information but is not a substitute for professional medical consultation.
                """)

            # Batch Processing Tab
            with gr.TabItem("📄 Multiple Queries from File"):
                with gr.Row():
                    with gr.Column():
                        file_input = gr.File(
                            label="Upload File with Health Queries",
                            file_types=[".txt"],
                            type="filepath",
                        )
                        batch_model_dropdown = gr.Dropdown(
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
                        batch_structured_checkbox = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        batch_btn = gr.Button(
                            "Process Health Queries", variant="primary"
                        )

                    with gr.Column():
                        batch_output = gr.Markdown(label="Batch Results")

                batch_btn.click(
                    fn=process_health_queries_file,
                    inputs=[
                        file_input,
                        batch_model_dropdown,
                        batch_structured_checkbox,
                    ],
                    outputs=batch_output,
                )

                gr.Markdown("""
                ### About Batch Processing
                Upload a text file containing multiple health queries (one per line) to get advice for all of them.
                Each query should be on a separate line in the file.
                """)

        gr.Markdown("""
        ### How to Use
        1. **Single Health Query**: Enter your health concern or question and click "Get Health Advice"
        2. **Multiple Queries**: Upload a text file with health queries (one per line) and click "Process Health Queries"
        3. Select your preferred LLM model
        4. Optionally enable structured output for formatted results
        5. Advice will be displayed and automatically saved to the `outputs` directory
        
        ### Important Disclaimer
        ⚠️ **This tool provides general health information only and is NOT a substitute for professional medical advice, diagnosis, or treatment.**
        - Always consult with a qualified healthcare provider for medical concerns
        - In case of emergency, call emergency services immediately
        - This advisor does not replace professional medical judgment
        """)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7869, share=False)
