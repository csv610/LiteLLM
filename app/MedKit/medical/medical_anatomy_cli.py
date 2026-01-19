"""Module docstring - Medical Anatomy Information Generator.

Generate comprehensive, evidence-based anatomical information using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and education purposes.
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
from medical_anatomy_models import MedicalAnatomy

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
class MedicalAnatomyConfig:
    """Configuration for generating medical anatomy information."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class MedicalAnatomyGenerator:
    """Generates comprehensive anatomical information based on provided configuration."""

    def __init__(self, config: MedicalAnatomyConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized MedicalAnatomyGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        structure: str,
        output_path: Optional[str] = None,
    ) -> MedicalAnatomy:
        """
        Generates comprehensive anatomical information.

        Args:
            structure: Name of the anatomical structure
            output_path: Optional path to save the output JSON file

        Returns:
            MedicalAnatomy: Validated anatomical information object
        """
        # Validate inputs
        if not structure or not str(structure).strip():
            raise ValueError("Structure name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting anatomical information generation")
        logger.info(f"Structure Name: {structure}")

        # Determine output path
        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{structure.lower().replace(' ', '_')}_anatomy.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        # Generate anatomical information
        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate comprehensive anatomical information for: {structure}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=MedicalAnatomy,
                )
            )

            logger.info(f"✓ Successfully generated anatomical information")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating anatomical information: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, anatomy_info: MedicalAnatomy, output_path: str):
        """
        Saves the anatomical information to a JSON file.

        Args:
            anatomy_info: The MedicalAnatomy object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving anatomical information to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(anatomy_info.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved anatomical information")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving anatomical information: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: MedicalAnatomy, verbose: bool = False) -> None:
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


def get_anatomy_info(
    structure: str,
    config: MedicalAnatomyConfig,
    output_path: Optional[str] = None,
) -> Optional[MedicalAnatomy]:
    """
    Get comprehensive anatomical information.

    This is a convenience function that instantiates and runs the
    MedicalAnatomyGenerator.

    Args:
        structure: Name of the anatomical structure
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        MedicalAnatomy: The result of the generation, or None if it fails
    """
    try:
        generator = MedicalAnatomyGenerator(config)
        return generator.generate(structure=structure, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate anatomical information: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating medical anatomy information.
    """
    logger.info("="*80)
    logger.info("MEDICAL ANATOMY CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical anatomy information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_anatomy_cli.py -i "heart"
  python medical_anatomy_cli.py -i "femur" -o output.json -v
  python medical_anatomy_cli.py -i "left ventricle" -d outputs/anatomy
        """
    )
    parser.add_argument(
        "-i", "--structure",
        required=True,
        help="The name of the anatomical structure to generate information for."
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

    # Create configuration
    config = MedicalAnatomyConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Structure: {args.structure}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Generate anatomical information
    try:
        generator = MedicalAnatomyGenerator(config)
        anatomy_info = generator.generate(structure=args.structure, output_path=args.output)

        if anatomy_info is None:
            logger.error("✗ Failed to generate anatomical information.")
            sys.exit(1)

        # Display formatted result
        print_result(anatomy_info, args.verbose)

        # Save if output path is specified
        if args.output:
            generator.save(anatomy_info, args.output)
        else:
            # Save to default location
            default_path = config.output_dir / f"{args.structure.lower().replace(' ', '_')}_anatomy.json"
            generator.save(anatomy_info, str(default_path))

        logger.info("="*80)
        logger.info("✓ Anatomical information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Anatomical information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
