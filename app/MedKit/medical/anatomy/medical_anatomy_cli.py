"""Module docstring - Medical Anatomy Information Generator.

Generate comprehensive, evidence-based anatomical information using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and education purposes.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional, final

from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from medical_anatomy_models import MedicalAnatomy

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for anatomical information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for anatomical information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are an expert anatomist with comprehensive knowledge of human anatomy and related medical sciences.

Your responsibilities include:
- Providing accurate, detailed anatomical information about body structures
- Describing location, structure, function, and clinical significance
- Explaining anatomical relationships and variations
- Detailing blood supply, innervation, and lymphatic drainage
- Correlating anatomy with clinical applications and pathology

Guidelines:
- Use precise anatomical terminology while ensuring clarity
- Base all information on established anatomical knowledge and evidence
- Include relevant embryological development when applicable
- Highlight clinically important anatomical features and variations
- Organize information systematically for educational and clinical reference
- Emphasize anatomical relationships critical for medical practice"""

    @staticmethod
    def create_user_prompt(structure: str) -> str:
        """
        Create the user prompt for anatomical information.

        Args:
            structure: The name of the anatomical structure

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive anatomical information for: {structure}."


@final
class MedicalAnatomyGenerator:
    """Generates comprehensive anatomical information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.info(f"Initialized MedicalAnatomyGenerator")

    def generate_text(self, structure: str) -> MedicalAnatomy:
        """Generates comprehensive anatomical information."""
        if not structure or not str(structure).strip():
            raise ValueError("Structure name cannot be empty")

        logger.info(f"Starting anatomical information generation for: {structure}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(structure)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=MedicalAnatomy,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated anatomical information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating anatomical information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> MedicalAnatomy:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, anatomy_info: MedicalAnatomy, output_path: Path) -> Path:
        """Saves the anatomical information to a JSON file."""
        try:
            logger.info(f"Saving anatomical information to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(anatomy_info.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved anatomical information to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving anatomical information to {output_path}: {e}")
            raise

    @property
    def logger(self):
        return logger


def print_result(result: MedicalAnatomy) -> None:
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


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical anatomy information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_anatomy_cli.py -i "heart"
  python medical_anatomy_cli.py -i "femur" -o output.json -v 3
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
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use for generation (default: ollama/gemma3)."
    )
    parser.add_argument(
        "-v", "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2)."
    )

    return parser.parse_args()


def app_cli() -> int:
    """CLI entry point."""
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file="medical_anatomy.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL ANATOMY CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Structure: {args.structure}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate anatomical information
    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalAnatomyGenerator(model_config)
        anatomy_info = generator.generate_text(structure=args.structure)

        if anatomy_info is None:
            logger.error("✗ Failed to generate anatomical information.")
            sys.exit(1)

        # Display formatted result
        print_result(anatomy_info)

        # Save if output path is specified
        if args.output:
            generator.save(anatomy_info, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.structure.lower().replace(' ', '_')}_anatomy.json"
            generator.save(anatomy_info, default_path)

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
    sys.exit(app_cli())
