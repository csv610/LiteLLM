import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional, final, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from surgery_info_models import SurgeryInfoModel, ModelOutput
from surgery_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgeryInfoGenerator:
    """Generates comprehensive surgery information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.surgery = None  # Store the surgery being analyzed
        logger.debug(f"Initialized SurgeryInfoGenerator")

    def generate_text(self, surgery: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive surgery information."""
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        # Store the surgery for later use in save
        self.surgery = surgery
        logger.debug(f"Starting surgical procedure information generation for: {surgery}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(surgery)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = SurgeryInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated surgery information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgery information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the surgery information to a file."""
        if self.surgery is None:
            raise ValueError("No surgery information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.surgery.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical procedure information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python surgery_info_cli.py -i "appendectomy"
  python surgery_info_cli.py -i "coronary bypass" -v 3
  python surgery_info_cli.py -i "knee replacement" -d outputs/surgeries
        """
    )
    parser.add_argument(
        "-i", "--surgery",
        required=True,
        help="The name of the surgical procedure to generate information for."
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
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "surgery_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("SURGERY INFO CLI - Starting")
    logger.info("="*80)

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SurgeryInfoGenerator(model_config)
        surgery_info = generator.generate_text(surgery=args.surgery, structured=args.structured)

        if surgery_info is None:
            logger.error("✗ Failed to generate surgery information.")
            return 1

        # Save result to output directory
        generator.save(surgery_info, output_dir)

        logger.debug("✓ Surgery information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Surgery information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1

if __name__ == "__main__":
    app_cli()
