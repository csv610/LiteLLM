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
from typing import Optional, final, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

#from utils.output_formatter import print_result

from medical_anatomy_models import MedicalAnatomyModel, ModelOutput
from medical_anatomy_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalAnatomyGenerator:
    """Generates comprehensive anatomical information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.body_part = None  # Store the body part being analyzed
        logger.debug(f"Initialized MedicalAnatomyGenerator")

    def generate_text(self, body_part: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive anatomical information."""
        if not body_part or not str(body_part).strip():
            raise ValueError("Body part name cannot be empty")

        # Store the body part for later use in save
        self.body_part = body_part
        logger.debug(f"Starting anatomical information generation for: {body_part}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(body_part)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalAnatomyModel

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
            logger.error(f"✗ Error generating anatomical information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the anatomical information to a file."""
        if self.body_part is None:
            raise ValueError("No body part information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.body_part.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)

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
        "-i", "--body_part",
        required=True,
        help="The name of the anatomical part  to generate information for."
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
        log_file=str(Path(__file__).parent / "logs" / "medical_anatomy.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate anatomical information
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalAnatomyGenerator(model_config)
        result = generator.generate_text(body_part=args.body_part, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate anatomical information.")
            sys.exit(1)

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Anatomical information generation completed successfully")
        return 
    except Exception as e:
        logger.error(f"✗ Anatomical information generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


if __name__ == "__main__":
    app_cli()
