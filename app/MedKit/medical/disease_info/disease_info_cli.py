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

from disease_info_models import (
    RiskFactors,
    DiagnosticCriteria,
    DiseaseIdentity,
    DiseaseBackground,
    DiseaseEpidemiology,
    DiseaseClinicalPresentation,
    DiseaseDiagnosis,
    DiseaseManagement,
    DiseaseResearch,
    DiseaseSpecialPopulations,
    DiseaseLivingWith,
    DiseaseInfoModel,
)

logger = logging.getLogger(__name__)


@final
class DiseaseInfoGenerator:
    """Generates comprehensive disease information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def generate_text(self, disease: str) -> DiseaseInfoModel:
        """Generates comprehensive disease information."""
        # Validate inputs
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        logger.info(f"Starting disease information generation for: {disease}")

        user_prompt = f"Generate comprehensive information for the disease: {disease}."
        logger.debug(f"Prompt: {user_prompt}")

        model_input = ModelInput(
            user_prompt=user_prompt,
            response_format=DiseaseInfoModel,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated disease information")
            logger.info(f"Disease: {result.identity.disease_name}")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating disease information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> DiseaseInfoModel:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, disease_info: DiseaseInfoModel, output_path: Path) -> Path:
        """Save the generated disease information to a JSON file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(disease_info.model_dump(), f, indent=2, default=str)
            logger.info(f"Saved disease information to: {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"Error saving disease information to {output_path}: {e}")
            raise

    @property
    def logger(self):
        return logger


def print_result(result: DiseaseInfoModel) -> None:
    """Print disease information in a formatted manner using rich."""
    console = Console()

    # Extract main fields from the result model
    result_dict = result.model_dump()

    # Create a formatted panel showing the result
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

    logger.info("="*80)
    logger.info("DISEASE INFO CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Disease: {args.disease}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create model configuration
    model_config = ModelConfig(model=args.model, temperature=0.7)

    # Generate disease information
    try:
        generator = DiseaseInfoGenerator(model_config)
        disease_info = generator.generate_text(disease=args.disease)

        if disease_info is None:
            logger.error("✗ Failed to generate disease information.")
            sys.exit(1)

        # Display formatted result
        print_result(disease_info)

        # Save if output path is specified
        if args.output:
            generator.save(disease_info, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.disease.lower().replace(' ', '_')}_info.json"
            generator.save(disease_info, default_path)

        logger.info("="*80)
        logger.info("✓ Disease information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Disease information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)



if __name__ == "__main__":
    sys.exit(app_cli())
