import argparse
import json
import logging
import sys

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from medical_test_devices_models import MedicalDeviceInfo

logger = logging.getLogger(__name__)


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

    def generate_text(self, device_name: str) -> MedicalDeviceInfo:
        """
        Generate comprehensive medical device information.

        Args:
            device_name: Name of the medical device.

        Returns:
            The generated MedicalDeviceInfo object.
        """
        logger.info(f"Generating medical device information for: {device_name}...")
        
        # Build prompt and create ModelInput
        prompt = self.build_user_prompt(device_name)
        model_input = ModelInput(
            user_prompt=prompt, 
            response_format=MedicalDeviceInfo
        )
        
        try:
            result = self.ask_llm(model_input)
            logger.info(f"Successfully generated medical device information for: {device_name}.")
            return result
        except (ValueError, RuntimeError) as e:
            logger.error(f"Error generating device information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> MedicalDeviceInfo:
        """
        Call the LLM client to generate information.

        Args:
            model_input: ModelInput object.

        Returns:
            The generated MedicalDeviceInfo object.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, device_info: MedicalDeviceInfo, output_path: Path) -> Path:
        """
        Save the generated device information to a JSON file.

        Args:
            device_info: The MedicalDeviceInfo object to save.
            output_path: Path where the JSON file should be saved.

        Returns:
            The output path where the file was saved.

        Raises:
            OSError: If directory creation or file writing fails.
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(device_info.model_dump(), f, indent=2)
            logger.info(f"Saved device information to: {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"Error saving device information to {output_path}: {e}")
            raise

def print_result(result: MedicalDeviceInfo) -> None:
    """Print medical device information in a formatted manner using rich."""
    console = Console()

    # Extract main fields from the result model
    result_dict = result.model_dump()

    # Create a formatted panel showing the result
    for section_name, section_value in result_dict.items():
        if section_value is not None:
            if isinstance(section_value, dict):
                formatted_text = "\n".join([f"  [bold]{k}:[/bold] {v}" for k, v in section_value.items()])
            else:
                formatted_text = str(section_value)

            console.print(Panel(
                formatted_text,
                title=section_name.replace('_', ' ').title(),
                border_style="cyan",
            ))

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

# Helper functions removed - CLI-only operation

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
        result = generator.generate_text(args.input)

        # Save to file
        if args.output:
            output_path = Path(args.output)
        else:
            output_dir = Path("outputs")
            output_path = output_dir / f"{args.input.lower().replace(' ', '_')}_device_info.json"
        
        generator.save(result, output_path)

        # Display results
        print_result(result)

    except Exception as e:
        logger.error(f"CLI execution failed: {e}")

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app_cli()
