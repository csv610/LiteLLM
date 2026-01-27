import argparse
import logging
import sys
from pathlib import Path
from typing import Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from medical_topic_models import MedicalTopicModel, ModelOutput

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for medical topic information."""

    @staticmethod
    def create_system_prompt() -> str:
        """Creates the system prompt for medical topic generation."""
        return """You are a medical information expert specializing in providing comprehensive, accurate, and well-structured information about medical topics.

Your task is to generate detailed medical topic information including:
- Clear definitions and descriptions
- Key concepts and terminology
- Clinical significance and applications
- Related conditions or concepts
- Current understanding and research perspectives

Provide information that is:
- Medically accurate and evidence-based
- Well-organized and easy to understand
- Comprehensive yet concise
- Appropriate for healthcare professionals and students"""

    @staticmethod
    def create_user_prompt(topic: str) -> str:
        """Creates the user prompt for medical topic generation.

        Args:
            topic: The name of the medical topic to generate information for

        Returns:
            A formatted user prompt string
        """
        return f"Generate comprehensive information for the medical topic: {topic}."


class MedicalTopicGenerator:
    """Generates comprehensive medical topic information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.debug(f"Initialized MedicalTopicGenerator")

    def generate_text(self, topic: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive medical topic information."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        logger.debug(f"Starting medical topic information generation for: {topic}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(topic)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalTopicModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical topic information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical topic information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_path: Path) -> Path:
        """Saves the medical topic information to a JSON or MD file."""
        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(result, output_path)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical topic information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_topic_cli.py -i inflammation
  python medical_topic_cli.py -i "immune response" -o output.json -v 3
  python medical_topic_cli.py -i metabolism -d outputs/topics
        """
    )
    parser.add_argument(
        "-i", "--topic",
        required=True,
        help="The name of the medical topic to generate information for."
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
        log_file=str(Path(__file__).parent / "logs" / "medical_topic.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL TOPIC CLI - Starting")
    logger.info("="*80)

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Topic: {args.topic}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Output File: {args.output if args.output else 'Default'}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalTopicGenerator(model_config)
        topic_info = generator.generate_text(topic=args.topic, structured=args.structured)

        if topic_info is None:
            logger.error("✗ Failed to generate medical topic information.")
            sys.exit(1)

        if args.output:
            generator.save(topic_info, Path(args.output))
        else:
            default_path = output_dir / f"{args.topic.lower().replace(' ', '_')}_topic.json"
            generator.save(topic_info, default_path)

        logger.debug("✓ Medical topic information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Medical topic information generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(app_cli())
