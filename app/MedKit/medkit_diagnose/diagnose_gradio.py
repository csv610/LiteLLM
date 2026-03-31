"""
diagnose_gradio.py - Gradio interface for the MedKit Diagnose application.
"""

import gradio as gr
import os
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

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / f"{Path(__file__).stem}.log"))
logger = logging.getLogger(__name__)

from lite.config import ModelConfig

# Import generators from diagnostics package
try:
    from medkit_diagnose.med_devices.medical_test_devices import MedicalTestDeviceGuide
    from medkit_diagnose.med_images.med_images import MedImageClassifier
    from medkit_diagnose.med_tests.medical_test_info import MedicalTestInfoGenerator
except (ImportError, ValueError):
    try:
        from .med_devices.medical_test_devices import MedicalTestDeviceGuide
        from .med_images.med_images import MedImageClassifier
        from .med_tests.medical_test_info import MedicalTestInfoGenerator
    except (ImportError, ValueError):
        from med_devices.medical_test_devices import MedicalTestDeviceGuide
        from med_images.med_images import MedImageClassifier
        from med_tests.medical_test_info import MedicalTestInfoGenerator


def get_medical_test_info(test_name: str, model_name: str, structured: bool):
    """Get information about a medical laboratory test."""
    if not test_name.strip():
        logger.warning("Empty test name provided")
        return "Please enter a medical test name."

    try:
        model_config = ModelConfig(model=model_name, temperature=0.2)
        gen = MedicalTestInfoGenerator(model_config)
        result = gen.generate_text(test_name=test_name.strip(), structured=structured)

        if result:
            # Save result to outputs directory
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            output_file = (
                output_dir / f"medical_test_{test_name.replace(' ', '_').lower()}.txt"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)

            logger.info(f"Medical test info retrieved for: {test_name}")
            return f"""## Medical Test Information: {test_name}

{result}

---
*Information saved to: {output_file}*"""
        else:
            logger.warning(f"No information found for test: {test_name}")
            return f"No information found for test: {test_name}"

    except Exception as e:
        logger.error(
            f"Error retrieving medical test information: {str(e)}", exc_info=True
        )
        return f"Error retrieving medical test information: {str(e)}"


def get_medical_device_info(device_name: str, model_name: str, structured: bool):
    """Get information about a medical diagnostic device."""
    if not device_name.strip():
        logger.warning("Empty device name provided")
        return "Please enter a medical device name."

    try:
        model_config = ModelConfig(model=model_name, temperature=0.2)
        gen = MedicalTestDeviceGuide(model_config)
        result = gen.generate_text(
            device_name=device_name.strip(), structured=structured
        )

        if result:
            # Save result to outputs directory
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            output_file = (
                output_dir
                / f"medical_device_{device_name.replace(' ', '_').lower()}.txt"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)

            logger.info(f"Medical device info retrieved for: {device_name}")
            return f"""## Medical Device Information: {device_name}

{result}

---
*Information saved to: {output_file}*"""
        else:
            logger.warning(f"No information found for device: {device_name}")
            return f"No information found for device: {device_name}"

    except Exception as e:
        logger.error(
            f"Error retrieving medical device information: {str(e)}", exc_info=True
        )
        return f"Error retrieving medical device information: {str(e)}"


def classify_medical_image(image_path: str, model_name: str, structured: bool):
    """Classify a medical diagnostic image."""
    if not image_path.strip():
        logger.warning("Empty image path provided")
        return "Please provide an image path."

    # Check if file exists
    if not os.path.exists(image_path.strip()):
        logger.error(f"Image file not found: {image_path}")
        return f"Image file not found: {image_path}"

    try:
        model_config = ModelConfig(model=model_name, temperature=0.2)
        gen = MedImageClassifier(model_config)
        result = gen.classify_image(image_path.strip(), structured=structured)

        if result:
            # Save result to outputs directory
            output_dir = Path("outputs")
            output_dir.mkdir(exist_ok=True)
            image_filename = os.path.basename(image_path.strip())
            output_file = (
                output_dir / f"classification_{os.path.splitext(image_filename)[0]}.txt"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result)

            logger.info(f"Medical image classified: {image_filename}")
            return f"""## Medical Image Classification: {image_filename}

{result}

---
*Classification saved to: {output_file}*"""
        else:
            logger.warning(f"Could not classify image: {image_path}")
            return f"Could not classify image: {image_path}"

    except Exception as e:
        logger.error(f"Error classifying medical image: {str(e)}", exc_info=True)
        return f"Error classifying medical image: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    logger.info("Creating MedKit Diagnose Gradio interface")
    with gr.Blocks(
        title="MedKit Diagnose - Medical Information & Image Classification"
    ) as interface:
        gr.Markdown("# 🏥 MedKit Diagnose")
        gr.Markdown(
            "Get information about medical tests, devices, and classify medical images."
        )

        with gr.Tabs():
            # Medical Tests Tab
            with gr.TabItem("🔬 Medical Tests"):
                with gr.Row():
                    with gr.Column():
                        test_input = gr.Textbox(
                            label="Medical Test Name",
                            placeholder="Enter test name (e.g., 'HbA1c', 'Complete Blood Count')",
                            lines=1,
                        )
                        test_model = gr.Dropdown(
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
                        test_structured = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        test_btn = gr.Button("Get Test Information", variant="primary")

                    with gr.Column():
                        test_output = gr.Markdown(label="Test Information")

                test_btn.click(
                    fn=get_medical_test_info,
                    inputs=[test_input, test_model, test_structured],
                    outputs=test_output,
                )

                gr.Markdown("""
                ### About Medical Tests
                Get detailed information about medical laboratory tests including:
                - Purpose and what the test measures
                - Normal ranges and interpretation
                - Preparation requirements
                - Clinical significance
                """)

            # Medical Devices Tab
            with gr.TabItem("💻 Medical Devices"):
                with gr.Row():
                    with gr.Column():
                        device_input = gr.Textbox(
                            label="Medical Device Name",
                            placeholder="Enter device name (e.g., 'MRI Scanner', 'Insulin Pump')",
                            lines=1,
                        )
                        device_model = gr.Dropdown(
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
                        device_structured = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        device_btn = gr.Button(
                            "Get Device Information", variant="primary"
                        )

                    with gr.Column():
                        device_output = gr.Markdown(label="Device Information")

                device_btn.click(
                    fn=get_medical_device_info,
                    inputs=[device_input, device_model, device_structured],
                    outputs=device_output,
                )

                gr.Markdown("""
                ### About Medical Devices
                Get detailed information about medical diagnostic devices including:
                - How the device works
                - Clinical applications
                - Advantages and limitations
                - Safety considerations
                """)

            # Medical Image Classification Tab
            with gr.TabItem("🖼️ Image Classification"):
                with gr.Row():
                    with gr.Column():
                        image_input = gr.Textbox(
                            label="Image Path",
                            placeholder="Path to medical image file (JPG, PNG, etc.)",
                            lines=1,
                        )
                        image_model = gr.Dropdown(
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
                        image_structured = gr.Checkbox(
                            label="Structured Output", value=False
                        )
                        image_btn = gr.Button("Classify Image", variant="primary")

                    with gr.Column():
                        image_output = gr.Markdown(label="Classification Result")

                image_btn.click(
                    fn=classify_medical_image,
                    inputs=[image_input, image_model, image_structured],
                    outputs=image_output,
                )

                gr.Markdown("""
                ### About Medical Image Classification
                Classify medical diagnostic images to identify:
                - Tissue types and abnormalities
                - Potential pathologies
                - Anatomical structures
                - Image quality assessments
                
                **Supported formats:** JPG, JPEG, PNG, GIF, WEBP, BMP, TIFF
                """)

        gr.Markdown("""
        ### How to Use
        1. Select the tab for what you want to do (Tests, Devices, or Image Classification)
        2. Enter the required information (test/device name or image path)
        3. Choose your preferred LLM model
        4. Optionally enable structured output for formatted results
        5. Click the action button to get information or classification
        6. Results will be displayed and automatically saved to the `outputs` directory
        
        ### Output Files
        All results are automatically saved to the `outputs` directory with descriptive filenames:
        - Medical tests: `medical_test_{test_name}.txt`
        - Medical devices: `medical_device_{device_name}.txt`
        - Image classifications: `classification_{image_filename}.txt`
        """)

    return interface


if __name__ == "__main__":
    logger.info("Starting MedKit Diagnose Gradio interface")
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7867, share=False)
