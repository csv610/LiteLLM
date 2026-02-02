import argparse
import json
import logging
from pathlib import Path

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from surgical_tray_info_models import SurgicalTrayModel, ModelOutput
from surgical_tray_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgicalTrayGenerator:
    """Generates comprehensive surgical tray information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.target = None  # Store the surgery being analyzed
        logger.debug(f"Initialized SurgicalInfoGenerator")

    def generate_text(self, surgery: str, structured: bool = False) -> ModelOutput:
        """Generates surgical tray information."""
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        # Store the surgery for later use in save
        self.target = surgery
        logger.debug(f"Starting surgical tray information generation for: {surgery}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(surgery)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = SurgicalTrayModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.info("Calling LiteClient.generate_text() for tray...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated surgical tray information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical tray information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the information to a file."""
        if self.target is None:
            raise ValueError("No information available. Call generate_tray first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.target.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical tray information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-i", "--surgery",
        required=True,
        help="The name of the surgery to generate a tray for."
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
        log_file=str(Path(__file__).parent / "logs" / "surgical_tray_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Surgery: {args.surgery}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SurgicalTrayGenerator(model_config)
        
        info = generator.generate_text(surgery=args.surgery, structured=args.structured)

        if info is None:
            logger.error("✗ Failed to generate tray information.")
            return 1

        # Save result to output directory
        generator.save(info, output_dir)

        logger.debug("✓ Tray information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Tray information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    app_cli()
