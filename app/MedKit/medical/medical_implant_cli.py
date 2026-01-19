"""Module docstring - Medical Implant Information Generator.

Generate comprehensive, evidence-based medical implant information using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and patient education purposes.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from rich.console import Console
from rich.panel import Panel

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from medical_implant_models import ImplantInfo

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
console = Console()

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class MedicalImplantConfig:
    """Configuration for generating medical implant information."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class MedicalImplantGenerator:
    """Generates comprehensive medical implant information based on provided configuration."""

    def __init__(self, config: MedicalImplantConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized MedicalImplantGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        implant: str,
        output_path: Optional[str] = None,
    ) -> ImplantInfo:
        """
        Generates comprehensive medical implant information.

        Args:
            implant: Name of the medical implant
            output_path: Optional path to save the output JSON file

        Returns:
            ImplantInfo: Validated implant information object
        """
        if not implant or not str(implant).strip():
            raise ValueError("Implant name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting medical implant information generation")
        logger.info(f"Implant Name: {implant}")

        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{implant.lower().replace(' ', '_')}_info.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate comprehensive information for the medical implant: {implant}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=ImplantInfo,
                )
            )

            logger.info(f"✓ Successfully generated implant information")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating implant information: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, implant_info: ImplantInfo, output_path: str):
        """
        Saves the implant information to a JSON file.

        Args:
            implant_info: The ImplantInfo object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving implant information to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(implant_info.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved implant information")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving implant information: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: ImplantInfo, verbose: bool = False) -> None:
    """Print result in a formatted manner using rich."""
    console = Console()

    # Extract main fields from the result model
    result_dict = result.model_dump()

    # Create a formatted panel showing the result
    # Use semantic formatting: green for success/positive, yellow for warnings, blue for info
    # Display the data in organized sections

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


def get_implant_info(
    implant: str,
    config: MedicalImplantConfig,
    output_path: Optional[str] = None,
) -> Optional[ImplantInfo]:
    """
    Get comprehensive implant information.

    Args:
        implant: Name of the implant
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        ImplantInfo: The result of the generation, or None if it fails
    """
    try:
        generator = MedicalImplantGenerator(config)
        return generator.generate(implant=implant, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate implant information: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating medical implant information.
    """
    logger.info("="*80)
    logger.info("MEDICAL IMPLANT CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical implant information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_implant_cli.py -i "cardiac pacemaker"
  python medical_implant_cli.py -i "hip prosthesis" -o output.json -v
  python medical_implant_cli.py -i "cochlear implant" -d outputs/implants
        """
    )
    parser.add_argument(
        "-i", "--implant",
        required=True,
        help="The name of the medical implant to generate information for."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save the output JSON file."
    )
    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose/debug logging output."
    )

    args = parser.parse_args()

    config = MedicalImplantConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Implant: {args.implant}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    try:
        generator = MedicalImplantGenerator(config)
        implant_info = generator.generate(implant=args.implant, output_path=args.output)

        if implant_info is None:
            logger.error("✗ Failed to generate implant information.")
            sys.exit(1)

        # Display formatted result
        print_result(implant_info, args.verbose)

        if args.output:
            generator.save(implant_info, args.output)
        else:
            default_path = config.output_dir / f"{args.implant.lower().replace(' ', '_')}_info.json"
            generator.save(implant_info, str(default_path))

        logger.info("="*80)
        logger.info("✓ Implant information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Implant information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
