import argparse
import json
import logging
import sys
from pathlib import Path
from typing import final

from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from herbal_info_models import HerbalInfo

logger = logging.getLogger(__name__)


def build_system_prompt() -> str:
    """Build the system prompt for herbal information generation."""
    return """You are an expert herbalist and natural medicine specialist with extensive knowledge of medicinal plants.
Your role is to provide comprehensive, accurate, and evidence-based information about herbs and their uses.
Focus on safety, traditional uses, active compounds, and modern research where available."""


def build_user_prompt(herb: str) -> str:
    """Build the user prompt for herbal information generation.

    Args:
        herb: The name of the herb to generate information for.
    """
    return f"Generate comprehensive information for the herb: {herb}."


@final
class HerbalInfoGenerator:
    """Generates comprehensive herbal remedy information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.info(f"Initialized HerbalInfoGenerator")

    def generate_text(self, herb: str) -> HerbalInfo:
        """Generates comprehensive herbal information."""
        # Validate inputs
        if not herb or not str(herb).strip():
            raise ValueError("Herb name cannot be empty")

        logger.info(f"Starting herbal information generation for: {herb}")

        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(herb)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=HerbalInfo,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated herbal information")
            if hasattr(result, 'metadata') and hasattr(result.metadata, 'common_name'):
                logger.info(f"Herb: {result.metadata.common_name}")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating herbal information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> HerbalInfo:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, herbal_info: HerbalInfo, output_path: Path) -> Path:
        """
        Saves the herbal information to a JSON file.

        Args:
            herbal_info: The HerbalInfo object to save
            output_path: Path where the JSON file should be saved
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving herbal information to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(herbal_info.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved herbal information to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving herbal information to {output_path}: {e}")
            raise

def print_result(result: HerbalInfo) -> None:
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
        log_file="herbal_info.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("HERBAL INFO CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Herb: {args.herb}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate herbal information
    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = HerbalInfoGenerator(model_config)
        herbal_info = generator.generate_text(herb=args.herb)

        if herbal_info is None:
            logger.error("✗ Failed to generate herbal information.")
            sys.exit(1)

        # Display formatted result
        print_result(herbal_info)

        # Save if output path is specified
        if args.output:
            generator.save(herbal_info, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.herb.lower().replace(' ', '_')}_info.json"
            generator.save(herbal_info, default_path)

        logger.info("="*80)
        logger.info("✓ Herbal information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Herbal information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)



if __name__ == "__main__":
    sys.exit(app_cli())
