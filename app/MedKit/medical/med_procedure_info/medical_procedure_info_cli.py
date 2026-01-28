"""medical_procedure_info - Generate comprehensive medical procedure documentation."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from medical_procedure_info_models import MedicalProcedureInfoModel, ModelOutput

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return "You are an expert medical documentation specialist. Generate comprehensive, evidence-based procedure information."

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"Generate complete, evidence-based information for the medical procedure: {procedure}"


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug(f"Initialized MedicalProcedureInfoGenerator")

    def generate_text(self, procedure: str, structured: bool = False) -> ModelOutput:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        # Store the procedure for later use in save
        self.procedure_name = procedure
        logger.debug(f"Starting medical procedure information generation for: {procedure}")

        response_format = None
        if structured:
            response_format = MedicalProcedureInfoModel

        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(procedure),
            response_format=response_format,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self._ask_llm(model_input)
            logger.debug("✓ Successfully generated procedure information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating procedure information: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the procedure information to a file."""
        if self.procedure_name is None:
            raise ValueError("No procedure information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.procedure_name.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive information for a medical procedure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_procedure_info_cli.py -i "appendectomy"
  python medical_procedure_info_cli.py -i "cardiac catheterization" -d outputs/procedures
        """
    )
    parser.add_argument(
        "-i", "--procedure", 
        required=True, 
        help="Name of the medical procedure"
    )
    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )
    parser.add_argument(
        "-m", "--model", 
        default="ollama/gemma3", 
        help="Model to use (default: ollama/gemma3)"
    )
    parser.add_argument(
        "-s", "--structured", 
        action="store_true", 
        default=False, 
        help="Use structured output (Pydantic model) for the response."
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
        log_file=str(Path(__file__).parent / "logs" / "medical_procedure_info.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Procedure: {args.procedure}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalProcedureInfoGenerator(model_config=model_config)
        
        result = generator.generate_text(procedure=args.procedure, structured=args.structured)

        if result is None:
            logger.error("✗ Failed to generate procedure information.")
            return 1

        # Save result to output directory
        generator.save(result, output_dir)

        logger.debug("✓ Procedure information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Procedure information generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == '__main__':
    app_cli()
