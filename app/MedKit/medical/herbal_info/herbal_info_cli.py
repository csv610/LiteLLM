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

from herbal_info_models import HerbalInfoModel, ModelOutput

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for herbal information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for herbal information generation."""
        return """You are an expert herbalist and natural medicine specialist with extensive knowledge of medicinal plants.
Your role is to provide comprehensive, accurate, and evidence-based information about herbs and their uses.
Focus on safety, traditional uses, active compounds, and modern research where available."""

    @staticmethod
    def create_user_prompt(herb: str) -> str:
        """Create the user prompt for herbal information generation.

        Args:
            herb: The name of the herb to generate information for.
        """
        return f"Generate comprehensive information for the herb: {herb}."


class HerbalInfoGenerator:
    """Generates comprehensive herbal remedy information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.herb = None  # Store the herb being analyzed
        logger.debug(f"Initialized HerbalInfoGenerator")

    def generate_text(self, herb: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive herbal information."""
        # Validate inputs
        if not herb or not str(herb).strip():
            raise ValueError("Herb name cannot be empty")

        # Store the herb for later use in save
        self.herb = herb
        logger.debug(f"Starting herbal information generation for: {herb}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(herb)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = HerbalInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating herbal information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the herbal information to a file."""
        if self.herb is None:
            raise ValueError("No herb information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.herb.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)

def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive herbal information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python herbal_info_cli.py -i ginger
  python herbal_info_cli.py -i "echinacea" -o output.json -v 3
  python herbal_info_cli.py -i turmeric -d outputs/herbs
        """
    )
    parser.add_argument(
        "-i", "--herb",
        required=True,
        help="The name of the herb to generate information for."
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


def app_cli():
    """CLI entry point."""
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "herbal_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Herb: {args.herb}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate herbal information
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = HerbalInfoGenerator(model_config)
        herbal_info = generator.generate_text(herb=args.herb, structured=args.structured)

        if herbal_info is None:
            logger.error("✗ Failed to generate herbal information.")
            return 1

        # Save result to output directory
        generator.save(herbal_info, output_dir)

        logger.debug("✓ Herbal information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Herbal information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    app_cli()
