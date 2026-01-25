import argparse
import json
import logging
import sys
from pathlib import Path
from typing import final, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from utils.output_formatter import print_result

from disease_info_models import DiseaseInfoModel

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for disease information."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for disease information generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a medical expert specializing in disease pathology, diagnosis, and management with comprehensive clinical knowledge.

Your responsibilities include:
- Providing accurate, evidence-based information about diseases and medical conditions
- Explaining etiology, pathophysiology, and clinical manifestations
- Describing diagnostic criteria, differential diagnoses, and testing approaches
- Outlining treatment options, prognosis, and preventive measures
- Discussing epidemiology, risk factors, and public health implications
- Addressing special populations and quality of life considerations

Guidelines:
- Base all information on current medical evidence and clinical guidelines
- Present information systematically covering all aspects of the disease
- Emphasize patient safety and evidence-based practice
- Include both acute management and long-term care considerations
- Highlight red flags and conditions requiring urgent intervention
- Provide balanced, comprehensive information suitable for healthcare professionals
- Reference established diagnostic criteria and treatment protocols"""

    @staticmethod
    def create_user_prompt(disease: str) -> str:
        """
        Create the user prompt for disease information.

        Args:
            disease: The name of the disease

        Returns:
            str: Formatted user prompt
        """
        return f"Generate comprehensive information for the disease: {disease}."


class DiseaseInfoGenerator:
    """Generates comprehensive disease information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def generate_text(self, disease: str, structured: bool = False) -> Union[DiseaseInfoModel, str]:
        """Generates comprehensive disease information."""
        # Validate inputs
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        logger.debug(f"Starting disease information generation for: {disease}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(disease)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = DiseaseInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            if isinstance(result, DiseaseInfoModel):
                logger.debug(f"Disease: {result.identity.disease_name}")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating disease information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[DiseaseInfoModel, str]:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, disease_info: Union[DiseaseInfoModel, str], output_path: Path) -> Path:
        """Save the generated disease information to a JSON or MD file."""
        if isinstance(disease_info, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(disease_info, output_path)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate comprehensive disease information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python disease_info_cli.py -i diabetes
  python disease_info_cli.py -i "heart disease" -o output.json -v 3
  python disease_info_cli.py -i pneumonia -d outputs/diseases
        """
    )
    parser.add_argument(
        "-i", "--disease",
        required=True,
        help="The name of the disease to generate information for."
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
        help="Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). Default: 2."
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

    # Apply logging configuration
    configure_logging(
        log_file="disease_info.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Disease: {args.disease}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Output File: {args.output if args.output else 'Default'}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create model configuration
    model_config = ModelConfig(model=args.model, temperature=0.7)

    # Generate disease information
    try:
        generator = DiseaseInfoGenerator(model_config)
        disease_info = generator.generate_text(disease=args.disease, structured=args.structured)

        if disease_info is None:
            logger.error("✗ Failed to generate disease information.")
            sys.exit(1)

        print_result(disease_info, title="Disease Information")

        # Save if output path is specified
        if args.output:
            generator.save(disease_info, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.disease.lower().replace(' ', '_')}_info.json"
            generator.save(disease_info, default_path)

        logger.debug("✓ Disease information generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Disease information generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)



if __name__ == "__main__":
    sys.exit(app_cli())
