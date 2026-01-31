import argparse
import logging
from pathlib import Path
from typing import Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from synthetic_case_report_models import SyntheticCaseReportModel, ModelOutput
from synthetic_case_report_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.condition = None  # Store the condition being analyzed
        logger.debug(f"Initialized SyntheticCaseReportGenerator")

    def generate_text(self, condition: str, structured: bool = False) -> ModelOutput:
        """Generates a synthetic medical case report."""
        if not condition or not str(condition).strip():
            raise ValueError("Condition name cannot be empty")

        # Store the condition for later use in save
        self.condition = condition
        logger.debug(f"Starting synthetic case report generation for: {condition}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(condition)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = SyntheticCaseReportModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated synthetic case report")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating synthetic case report: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the case report to a file."""
        if self.condition is None:
            raise ValueError("No condition information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.condition.lower().replace(' ', '_')}_casereport"
        
        return save_model_response(result, output_dir / base_filename)



def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic medical case reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-i", "--condition",
        required=True,
        help="The name of the disease or medical condition for the case report."
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
        log_file=str(Path(__file__).parent / "logs" / "synthetic_case_report.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("SYNTHETIC CASE REPORT CLI - Starting")
    logger.info("="*80)

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SyntheticCaseReportGenerator(model_config)
        result = generator.generate_text(condition=args.condition, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate synthetic case report.")
            return 1

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Synthetic case report generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Synthetic case report generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    app_cli()
