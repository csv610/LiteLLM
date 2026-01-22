"""Module docstring - Surgery Information Generator.

Generate comprehensive, evidence-based surgical procedure information using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and patient education purposes.
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

from surgery_info_models import SurgeryInfo

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for surgical procedure information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for surgical procedure information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are an expert surgical information specialist with comprehensive knowledge of surgical procedures and perioperative care.

Your responsibilities include:
- Providing accurate, evidence-based information about surgical procedures
- Explaining indications, contraindications, and procedural steps
- Describing risks, complications, and expected outcomes
- Outlining preoperative preparation and postoperative care requirements
- Emphasizing patient safety and current best practices

Guidelines:
- Base all information on current medical evidence and established surgical standards
- Present information clearly for both healthcare professionals and patients
- Include relevant anatomical considerations and technical details
- Highlight critical safety considerations and risk factors
- Maintain professional medical terminology while ensuring comprehension"""

    @staticmethod
    def create_user_prompt(surgery: str) -> str:
        """
        Create the user prompt for surgical procedure information.

        Args:
            surgery: The name of the surgical procedure

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive information for the surgical procedure: {surgery}."


@final
class SurgeryInfoGenerator:
    """Generates comprehensive surgery information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.info(f"Initialized SurgeryInfoGenerator")

    def generate_text(self, surgery: str) -> SurgeryInfo:
        """Generates comprehensive surgery information."""
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        logger.info(f"Starting surgical procedure information generation for: {surgery}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(surgery)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=SurgeryInfo,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated surgery information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgery information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> SurgeryInfo:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, surgery_info: SurgeryInfo, output_path: Path) -> Path:
        """Saves the surgery information to a JSON file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving surgery information to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(surgery_info.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved surgery information to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving surgery information to {output_path}: {e}")
            raise

    @property
    def logger(self):
        return logger


def print_result(result: SurgeryInfo) -> None:
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
        description="Generate comprehensive surgical procedure information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python surgery_info_cli.py -i "appendectomy"
  python surgery_info_cli.py -i "coronary bypass" -o output.json -v 3
  python surgery_info_cli.py -i "knee replacement" -d outputs/surgeries
        """
    )
    parser.add_argument(
        "-i", "--surgery",
        required=True,
        help="The name of the surgical procedure to generate information for."
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
        log_file="surgery_info.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("SURGERY INFO CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Surgery: {args.surgery}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = SurgeryInfoGenerator(model_config)
        surgery_info = generator.generate_text(surgery=args.surgery)

        if surgery_info is None:
            logger.error("✗ Failed to generate surgery information.")
            sys.exit(1)

        # Display formatted result
        print_result(surgery_info)

        if args.output:
            generator.save(surgery_info, Path(args.output))
        else:
            default_path = output_dir / f"{args.surgery.lower().replace(' ', '_')}_info.json"
            generator.save(surgery_info, default_path)

        logger.info("="*80)
        logger.info("✓ Surgery information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Surgery information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(app_cli())
