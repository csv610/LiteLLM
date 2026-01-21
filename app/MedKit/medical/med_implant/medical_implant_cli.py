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

from medical_implant_models import ImplantInfo

logger = logging.getLogger(__name__)

@final
class MedicalImplantGenerator:
    """Generates comprehensive medical implant information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.info(f"Initialized MedicalImplantGenerator")

    def generate_text(self, implant: str) -> ImplantInfo:
        """Generates comprehensive medical implant information."""
        if not implant or not str(implant).strip():
            raise ValueError("Implant name cannot be empty")

        logger.info(f"Starting medical implant information generation for: {implant}")

        user_prompt = f"Generate comprehensive information for the medical implant: {implant}."
        logger.debug(f"Prompt: {user_prompt}")

        model_input = ModelInput(
            user_prompt=user_prompt,
            response_format=ImplantInfo,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated implant information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating implant information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ImplantInfo:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, implant_info: ImplantInfo, output_path: Path) -> Path:
        """Saves the implant information to a JSON file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving implant information to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(implant_info.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved implant information to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving implant information to {output_path}: {e}")
            raise

def print_result(result: ImplantInfo) -> None:
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
        description="Generate comprehensive medical implant information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_implant_cli.py -i "cardiac pacemaker"
  python medical_implant_cli.py -i "hip prosthesis" -o output.json -v 3
  python medical_implant_cli.py -i "cochlear implant" -d outputs/implants
        """
    )
    parser.add_argument(
        "-i", "--implant",
        required=True,
        help="The name of the medical implant to generate information for."
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
        log_file="medical_implant.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL IMPLANT CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Implant: {args.implant}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalImplantGenerator(model_config)
        implant_info = generator.generate_text(implant=args.implant)

        if implant_info is None:
            logger.error("✗ Failed to generate implant information.")
            sys.exit(1)

        # Display formatted result
        print_result(implant_info)

        if args.output:
            generator.save(implant_info, Path(args.output))
        else:
            default_path = output_dir / f"{args.implant.lower().replace(' ', '_')}_info.json"
            generator.save(implant_info, default_path)

        logger.info("="*80)
        logger.info("✓ Implant information generation completed successfully")
        logger.info("="*80)
        return 
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Implant information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    app_cli()
