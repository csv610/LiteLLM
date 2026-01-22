"""Module docstring - Medical Decision Guide Generator.

Generate medical decision trees for symptom assessment using structured data models
and the LiteClient with schema-aware prompting for clinical decision support.
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

from medical_decision_guide_models import MedicalDecisionGuide

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for medical decision guide generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medical decision guide generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a clinical decision support specialist expert in diagnostic reasoning and symptom assessment algorithms.

Your responsibilities include:
- Creating systematic, evidence-based decision trees for symptom evaluation
- Structuring logical pathways from initial presentation to differential diagnoses
- Identifying critical decision points and red flag symptoms
- Recommending appropriate diagnostic tests and assessments
- Prioritizing urgent versus routine evaluations
- Guiding appropriate triage and referral decisions

Guidelines:
- Base decision algorithms on current clinical evidence and best practices
- Structure decision trees with clear, actionable steps
- Emphasize patient safety and timely identification of serious conditions
- Include warning signs requiring immediate medical attention
- Provide context for when to seek emergency care versus routine evaluation
- Consider common presentations while recognizing atypical cases
- Ensure decision points are practical and clinically relevant
- Focus on supporting clinical judgment, not replacing it"""

    @staticmethod
    def create_user_prompt(symptom: str) -> str:
        """
        Create the user prompt for medical decision guide generation.

        Args:
            symptom: The symptom to create a decision guide for

        Returns:
            str: Formatted user prompt
        """
        return f"Generate a comprehensive medical decision tree for: {symptom}."


@final
class MedicalDecisionGuideGenerator:
    """Generates medical decision guides based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.info(f"Initialized MedicalDecisionGuideGenerator")

    def generate_text(self, symptom: str) -> MedicalDecisionGuide:
        """Generates a medical decision guide for symptom assessment."""
        if not symptom or not str(symptom).strip():
            raise ValueError("Symptom name cannot be empty")

        logger.info(f"Starting decision guide generation for: {symptom}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(symptom)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=MedicalDecisionGuide,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated decision guide")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating decision guide: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> MedicalDecisionGuide:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, guide: MedicalDecisionGuide, output_path: Path) -> Path:
        """Saves the decision guide to a JSON file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving decision guide to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(guide.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved decision guide to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving decision guide to {output_path}: {e}")
            raise

    @property
    def logger(self):
        return logger


def print_result(result: MedicalDecisionGuide) -> None:
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
        description="Generate medical decision trees for symptom assessment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_decision_guide_cli.py -i fever
  python medical_decision_guide_cli.py -i "sore throat" -o output.json -v 3
  python medical_decision_guide_cli.py -i cough -d outputs/guides
        """
    )
    parser.add_argument(
        "-i", "--symptom",
        required=True,
        help="The name of the symptom to generate a decision tree for."
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
        log_file="medical_decision_guide.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL DECISION GUIDE CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Symptom: {args.symptom}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate decision guide
    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalDecisionGuideGenerator(model_config)
        guide = generator.generate_text(symptom=args.symptom)

        if guide is None:
            logger.error("✗ Failed to generate decision guide.")
            sys.exit(1)

        # Display formatted result
        print_result(guide)

        # Save if output path is specified
        if args.output:
            generator.save(guide, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.symptom.lower().replace(' ', '_')}_decision_tree.json"
            generator.save(guide, default_path)

        logger.info("="*80)
        logger.info("✓ Decision guide generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Decision guide generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(app_cli())
