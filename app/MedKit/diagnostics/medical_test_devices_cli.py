import argparse
import json
import logging
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

# ==============================================================================
# LITECLIENT SETUP
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from medical_test_devices_models import MedicalDeviceInfo

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTS
# ==============================================================================

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class Config:
    """Configuration for the medical test device generator."""
    enable_cache: bool = True
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING (default), 3=INFO, 4=DEBUG
    output_dir: Path = Path("outputs")
    model: str = "ollama/gemma3:12b"

# ==============================================================================
# MAIN CLASS: MEDICAL TEST DEVICE GENERATOR
# ==============================================================================

class MedicalTestDeviceGenerator:
    """Generate comprehensive information for medical test devices."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator."""
        self.config = config or Config()
        self.client = LiteClient(ModelConfig(model=self.config.model, temperature=0.7))

        # Apply verbosity level to logger
        verbosity_levels = {
            0: "CRITICAL",
            1: "ERROR",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG"
        }
        log_level = verbosity_levels.get(self.config.verbosity, "WARNING")
        logger.setLevel(log_level)

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

    def generate(self, device_name: str, output_path: Optional[Path] = None) -> MedicalDeviceInfo:
        """
        Generate and save comprehensive medical device information.

        Args:
            device_name: Name of the medical device.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalDeviceInfo object.

        Raises:
            ValueError: If device_name is empty.
        """
        if not device_name or not device_name.strip():
            logger.error("Device name cannot be empty")
            raise ValueError("Device name cannot be empty")

        if output_path is None:
            output_path = self.config.output_dir / f"{device_name.lower().replace(' ', '_')}_device_info.json"

        logger.info(f"Starting medical device information generation for: {device_name}")

        try:
            device_info = self._generate_info(device_name)
            self.save(device_info, output_path)
            logger.info(f"Successfully generated all device information for: {device_name}")
            self.print_summary(device_info, output_path)
            return device_info
        except (ValueError, OSError, IOError) as e:
            logger.error(f"Failed to generate device information for {device_name}: {e}")
            raise

    def _generate_info(self, device_name: str) -> MedicalDeviceInfo:
        """
        Generate the device information.

        Args:
            device_name: Name of the medical device.

        Returns:
            The generated MedicalDeviceInfo object.
        """
        logger.info(f"Generating comprehensive information for {device_name}...")
        try:
            prompt = self.build_user_prompt(device_name)
            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=MedicalDeviceInfo,
                )
            )
            logger.info(f"Successfully generated comprehensive information for {device_name}.")
            return result
        except (ValueError, RuntimeError) as e:
            logger.error(f"Error generating information for {device_name}: {e}")
            raise

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

    def print_summary(self, device_info: MedicalDeviceInfo, output_path: Path) -> None:
        """
        Print a summary of the generated device information.

        Args:
            device_info: The generated MedicalDeviceInfo object.
            output_path: Path where the device information was saved.
        """
        print("\n" + "="*70)
        print(f"MEDICAL DEVICE INFORMATION SUMMARY: {device_info.basic_info.device_name}")
        print("="*70)
        print(f"  - Category: {device_info.basic_info.device_category}")
        print(f"  - Intended Use: {device_info.basic_info.intended_use}")
        print(f"  - Manufacturer: {device_info.manufacturer_and_support.manufacturer_name}")
        print(f"\n✓ Generation complete. Saved to {output_path}")

# ==============================================================================
# DISPLAY/OUTPUT FUNCTIONS
# ==============================================================================

def print_result(result: MedicalDeviceInfo, verbose: bool = False) -> None:
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

def get_device_info(device_name: str, output_path: Optional[Path] = None) -> MedicalDeviceInfo:
    """
    High-level function to generate and optionally save device information.
    """
    generator = MedicalTestDeviceGenerator()
    return generator.generate(device_name, output_path)

# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================

def argument_parser():
    """
    Parse command-line arguments for the medical test device generator CLI.

    Returns:
        argparse.Namespace: Parsed arguments with 'input' and 'output' attributes.
    """
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical device.")
    parser.add_argument("-i", "--input", type=str, required=True, help="The name of the medical device to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")

    return parser.parse_args()


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    Main CLI entry point for the medical test device generator.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        args = argument_parser()
        generator = MedicalTestDeviceGenerator()
        output_file_path = Path(args.output) if args.output else None
        result = generator.generate(device_name=args.input, output_path=output_file_path)
        if result:
            print_result(result)
        return 0
    except Exception as e:
        logger.error(f"CLI execution failed: {e}")
        return 1

# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
