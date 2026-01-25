"""Module docstring - Medical FAQ Generator.

Generate comprehensive, patient-friendly FAQs for medical topics using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and patient education purposes.
"""

import argparse
import json
import logging
import sys
from pathlib import Path


from typing import Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_faq_models import ComprehensiveFAQ

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for medical FAQ generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Creates the system prompt for FAQ generation."""
        return (
            "You are a medical information specialist creating patient-friendly FAQs. "
            "Your responses should be accurate, clear, and accessible to non-medical audiences. "
            "Organize information in logical sections with concise, informative answers. "
            "Always encourage users to consult healthcare professionals for medical advice."
        )

    @staticmethod
    def create_user_prompt(topic: str) -> str:
        """Creates the user prompt for FAQ generation."""
        return f"Generate comprehensive patient-friendly FAQs for: {topic}."


class MedicalFAQGenerator:
    """Generates comprehensive FAQ content based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.debug(f"Initialized MedicalFAQGenerator")

    def generate_text(self, topic: str, structured: bool = False) -> Union[ComprehensiveFAQ, str]:
        """Generates comprehensive FAQ content."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        logger.debug(f"Starting FAQ generation for: {topic}")

        user_prompt = PromptBuilder.create_user_prompt(topic)
        logger.debug(f"Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = ComprehensiveFAQ

        model_input = ModelInput(
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated FAQ")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating FAQ: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[ComprehensiveFAQ, str]:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, faq: Union[ComprehensiveFAQ, str], output_path: Path) -> Path:
        """Saves the FAQ to a JSON or MD file."""
        if isinstance(faq, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(faq, output_path)



def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical FAQs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_faq_cli.py -i diabetes
  python medical_faq_cli.py -i "heart disease" -o output.json -v 3
  python medical_faq_cli.py -i hypertension -d outputs/faq
        """
    )
    parser.add_argument(
        "-i", "--topic",
        required=True,
        help="The name of the medical topic to generate FAQs for."
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
    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()


def app_cli() -> int:
    """CLI entry point."""
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file="medical_faq.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Topic: {args.topic}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Output File: {args.output if args.output else 'Default'}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate FAQ
    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalFAQGenerator(model_config)
        faq = generator.generate_text(topic=args.topic, structured=args.structured)

        if faq is None:
            logger.error("✗ Failed to generate FAQ.")
            sys.exit(1)

        # Display formatted result
        print_result(faq, title="Medical FAQ")

        # Save if output path is specified
        if args.output:
            generator.save(faq, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.topic.lower().replace(' ', '_')}_faq.json"
            generator.save(faq, default_path)

        logger.debug("✓ FAQ generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ FAQ generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(app_cli())
