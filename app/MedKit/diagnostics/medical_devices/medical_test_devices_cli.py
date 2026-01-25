import argparse
import json
import logging
import sys

from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_test_devices_models import MedicalDeviceInfo

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for constructing prompts for medical device information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for the medical device information generator.

        Returns:
            The system prompt string.
        """
        return """You are a medical device information specialist with extensive knowledge of medical diagnostic and therapeutic equipment. Your role is to provide comprehensive, accurate, and evidence-based information about medical devices.

When generating medical device information, you must:

1. Provide technically accurate specifications and classifications based on FDA, CE, or other relevant regulatory standards
2. Include detailed information about device functionality, intended use, and clinical applications
3. Describe physical and operational specifications with precision
4. Address safety considerations, contraindications, and regulatory compliance
5. Include information about maintenance, servicing, and quality assurance requirements
6. Discuss cost considerations, availability, and market positioning where applicable
7. Present both advantages and limitations objectively
8. Use appropriate medical and technical terminology
9. Structure information in a clear, organized manner following the requested categories

Your responses should be comprehensive yet concise, suitable for healthcare professionals, biomedical engineers, and procurement specialists. Maintain a professional, objective tone and base all information on established medical device standards and clinical evidence."""

    @staticmethod
    def build_user_prompt(device_name: str) -> str:
        """
        Build the prompt for generating comprehensive medical device information.

        Args:
            device_name: Name of the medical device.

        Returns:
            The formatted prompt string.
        """
        return f"""Generate comprehensive medical device information for: {device_name}

Include detailed information about:
1. Device name and classification
2. Intended use and applications
3. Technical specifications and principles
4. Physical specifications
5. Operational requirements and specifications
6. Safety and regulatory information
7. Clinical applications and benefits
8. Maintenance and servicing requirements
9. Cost and availability information
10. Advantages and limitations

Provide accurate, evidence-based medical device information."""


class MedicalTestDeviceGenerator:
    """Generate comprehensive information for medical test devices."""

    def __init__(
        self,
        model_config: ModelConfig
    ):
        """Initialize the generator.

        Args:
            model_config: ModelConfig object containing model settings.
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def generate_text(self, device_name: str, structured: bool = False) -> Union[MedicalDeviceInfo, str]:
        """
        Generate comprehensive medical device information.

        Args:
            device_name: Name of the medical device.
            structured: Whether to use structured output mode (default: False)

        Returns:
            Union[MedicalDeviceInfo, str]: The generated MedicalDeviceInfo object or raw string.
        """
        logger.debug(f"Generating medical device information for: {device_name}...")

        # Build prompts and create ModelInput
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.build_user_prompt(device_name)

        response_format=None
        if structured:
           response_format = MedicalDeviceInfo

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format
        )

        try:
            result = self.ask_llm(model_input)
            logger.debug(f"Successfully generated medical device information for: {device_name}.")
            return result
        except (ValueError, RuntimeError) as e:
            logger.error(f"Error generating device information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[MedicalDeviceInfo, str]:
        """
        Call the LLM client to generate information.

        Args:
            model_input: ModelInput object.

        Returns:
            The generated results (MedicalDeviceInfo or str).
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, device_info: Union[MedicalDeviceInfo, str], output_path: Path) -> Path:
        """Save the generated device information to a JSON or MD file."""
        if isinstance(device_info, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(device_info, output_path)


def get_user_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments for the medical test device generator CLI.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical device.")
    parser.add_argument("-i", "--input", type=str, required=True, help="The name of the medical device to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-m", "--model", type=str, default="ollama/gemma3", help="Model to use for generation (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, help="Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). Default: 2.")
    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()


def app_cli():
    """
    Main CLI entry point for the medical test device generator.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = get_user_arguments()

    # Apply logging configuration at the entry point
    configure_logging(
        log_file="medical_test_devices.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalTestDeviceGenerator(model_config)

        # Generate the device information
        result = generator.generate_text(args.input, structured=args.structured)
        
        # Save to file
        if args.output:
            output_path = Path(args.output)
        else:
            output_dir = Path("outputs")
            output_path = output_dir / f"{args.input.lower().replace(' ', '_')}_device_info.json"
        
        generator.save(result, output_path)

        # Display results
        print_result(result, title="Medical Device Information")

    except Exception as e:
        logger.error(f"CLI execution failed: {e}")

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app_cli()
