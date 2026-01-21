import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from medical_topic_models import MedicalTopic

logger = logging.getLogger(__name__)


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
        logger.info(f"Initialized MedicalTopicGenerator")

    def generate_text(self, topic: str) -> MedicalTopic:
        """Generates comprehensive medical topic information."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        logger.info(f"Starting medical topic information generation for: {topic}")

        system_prompt = create_system_prompt()
        user_prompt = create_user_prompt(topic)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=MedicalTopic,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated medical topic information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical topic information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> MedicalTopic:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, topic_info: MedicalTopic, output_path: Path) -> Path:
        """Saves the medical topic information to a JSON file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving medical topic information to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(topic_info.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved medical topic information to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving medical topic information to {output_path}: {e}")
            raise


def print_result(result: MedicalTopic) -> None:
    """Print result in a formatted manner using rich."""
    console = Console()

    result_dict = result.model_dump()

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

    return parser.parse_args()


def app_cli() -> int:
    """CLI entry point."""
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file="medical_topic.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL TOPIC CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Topic: {args.topic}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalTopicGenerator(model_config)
        topic_info = generator.generate_text(topic=args.topic)

        if topic_info is None:
            logger.error("✗ Failed to generate medical topic information.")
            sys.exit(1)

        # Display formatted result
        print_result(topic_info)

        if args.output:
            generator.save(topic_info, Path(args.output))
        else:
            default_path = output_dir / f"{args.topic.lower().replace(' ', '_')}_topic.json"
            generator.save(topic_info, default_path)

        logger.info("="*80)
        logger.info("✓ Medical topic information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Medical topic information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(app_cli())
