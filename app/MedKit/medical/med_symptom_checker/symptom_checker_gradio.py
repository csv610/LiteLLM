"""
symptom_checker_gradio.py - Gradio interface for the Medical Symptom Checker application.
"""

import gradio as gr
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to sys.path to access lite module
project_root = Path(__file__).resolve().parents[4]
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
from lite.lite_client import LiteClient
from symptom_detection_qa import MedicalConsultation
from symptom_detection_prompts import PromptBuilder


def start_medical_consultation(
    patient_name: str,
    patient_age: int,
    patient_gender: str,
    patient_occupation: str,
    max_questions: int,
    model_name: str,
):
    """Start a medical consultation session."""
    if not patient_name.strip():
        return "Please enter patient name.", None, None

    if patient_age <= 0:
        return "Please enter a valid age.", None, None

    try:
        # Initialize the consultation system
        config = ModelConfig(model=model_name, temperature=0.7)
        client = LiteClient(model_config=config)
        consultation = MedicalConsultation(model=model_name)

        # Override the client with our configured one
        consultation.client = client

        # We'll simulate the consultation process for Gradio
        # For a real implementation, we'd need to handle the interactive nature differently
        # For now, we'll provide a summary of what would happen

        demographics_text = f"""
Patient Demographics:
- Name: {patient_name}
- Age: {patient_age}
- Gender: {patient_gender}
- Occupation: {patient_occupation or "Not specified"}
"""

        consultation_text = f"""# Medical Consultation Session Started

{demographics_text}

## Consultation Process
A medical consultation would proceed as follows:

1. **Initial Question**: "What is troubling you?"
2. **Follow-up Questions**: Based on your responses, the system would ask targeted questions to narrow down potential conditions
3. **Red Flag Checking**: The system continuously monitors for emergency symptoms requiring immediate attention
4. **Assessment**: After gathering sufficient information, a clinical assessment would be generated
5. **Management Plan**: Recommendations for investigations, treatment, and follow-up would be provided

## To Complete This Consultation:
You would need to run the interactive CLI version:
```
python symptom_detection_cli.py -m {model_name} -n {max_questions}
```

Then follow the prompts to provide information about the patient's symptoms.

## Disclaimer
⚠️ **This is an AI-based consultation system and should NOT be used as a substitute for professional medical advice, diagnosis, or treatment.**
- Cannot perform physical examination
- Cannot order and interpret tests  
- Cannot prescribe medications
- Based on patient self-reporting only
- Always seek professional medical care for any health concerns
"""

        return consultation_text, f"Consultation ready for {patient_name}", None

    except Exception as e:
        return f"Error initializing consultation: {str(e)}", None, None


def create_gradio_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(title="Medical Symptom Checker - Consultation System") as interface:
        gr.Markdown("# 🩺 Medical Symptom Checker")
        gr.Markdown(
            "AI-powered structured medical consultation system using decision tree reasoning."
        )

        with gr.Row():
            with gr.Column():
                gr.Markdown("### Patient Information")
                name_input = gr.Textbox(
                    label="Patient Name",
                    placeholder="Enter patient's full name",
                    lines=1,
                )
                age_input = gr.Number(
                    label="Age", minimum=0, maximum=120, value=30, precision=0
                )
                gender_input = gr.Dropdown(
                    label="Gender",
                    choices=["Male", "Female", "Other", "Prefer not to say"],
                    value="Male",
                )
                occupation_input = gr.Textbox(
                    label="Occupation (Optional)",
                    placeholder="Patient's occupation",
                    lines=1,
                )

                gr.Markdown("### Consultation Settings")
                max_questions_slider = gr.Slider(
                    label="Maximum Follow-up Questions",
                    minimum=5,
                    maximum=30,
                    value=15,
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

                start_btn = gr.Button("Start Consultation", variant="primary")

            with gr.Column():
                consultation_output = gr.Markdown(
                    label="Consultation Information",
                    value="Enter patient information above and click 'Start Consultation' to begin.",
                )
                status_output = gr.Textbox(
                    label="Status", interactive=False, visible=False
                )

        start_btn.click(
            fn=start_medical_consultation,
            inputs=[
                name_input,
                age_input,
                gender_input,
                occupation_input,
                max_questions_slider,
                model_dropdown,
            ],
            outputs=[consultation_output, status_output],
        )

        gr.Markdown("""
        ### About the Medical Symptom Checker
        This system uses a structured decision tree approach to medical consultation:
        
        ## How It Works
        1. **Initial Assessment**: Starts with "What is troubling you?"
        2. **Branching Logic**: Based on responses, follows specific pathways for different symptom categories
        3. **Thinking Process**: Captures internal medical reasoning for transparency
        4. **Red Flag Detection**: Continuously monitors for emergency symptoms
        5. **Clinical Assessment**: Generates differential diagnosis and most likely diagnosis
        6. **Management Plan**: Provides recommendations for investigations, treatment, and follow-up
        
        ## Safety Features
        - Emergency red flag detection for immediate escalation
        - Comprehensive disclaimers about limitations
        - Structured approach to reduce cognitive biases
        - Clear separation between information gathering and diagnosis
        
        ## Limitations
        ⚠️ **Important**: This system has significant limitations:
        - Cannot perform physical examination
        - Cannot order or interpret laboratory tests or imaging
        - Cannot prescribe medications
        - Relies entirely on patient self-reporting
        - Not a substitute for professional medical evaluation
        
        ## When to Use
        - For educational purposes to understand medical reasoning
        - As a tool to help organize thoughts before seeing a healthcare provider
        - To learn about the process of medical diagnosis
        
        ## When NOT to Use
        - In medical emergencies (call 911 or go to ER)
        - For definitive diagnosis or treatment decisions
        - As a replacement for professional medical care
        - For medications prescriptions or medical procedures
        """)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7870, share=False)
