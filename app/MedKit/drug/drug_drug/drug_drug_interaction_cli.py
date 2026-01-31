import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from drug_drug_interaction import DrugDrugInteractionGenerator
from drug_drug_interaction_prompts import DrugDrugInput, PromptStyle

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer - Check interactions between two medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python drug_drug_interaction_cli.py "Warfarin" "Aspirin"
  python drug_drug_interaction_cli.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"
  python drug_drug_interaction_cli.py "Simvastatin" "Clarithromycin" --style detailed -v 3
        """
    )
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine"
    )
    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine"
    )
    parser.add_argument(
        "--age", "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)"
    )
    parser.add_argument(
        "--dosage1", "-d1",
        type=str,
        default=None,
        help="Dosage information for first medicine"
    )
    parser.add_argument(
        "--dosage2", "-d2",
        type=str,
        default=None,
        help="Dosage information for second medicine"
    )
    parser.add_argument(
        "--conditions", "-c",
        type=str,
        default=None,
        help="Patient's medical conditions (comma-separated)"
    )
    parser.add_argument(
        "--style", "-s",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)"
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
        "-t", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()


def create_drug_drug_interaction_report(args) -> int:
    """Generate drug-drug interaction report."""
    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_drug_interaction.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Medicine 1: {args.medicine1}")
    logger.debug(f"  Medicine 2: {args.medicine2}")
    logger.debug(f"  Age: {args.age}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = DrugDrugInteractionGenerator(model_config)
        
        # Create input configuration
        input_config = DrugDrugInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.conditions,
            prompt_style=PromptStyle(args.style)
        )
        
        interaction_info = generator.generate_text(config=input_config, structured=args.structured)

        if interaction_info is None:
            logger.error("✗ Failed to generate drug-drug interaction information.")
            return 1

        # Save result to output directory
        generator.save(interaction_info, output_dir)

        logger.debug("✓ Drug-drug interaction generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Drug-drug interaction generation failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_drug_drug_interaction_report(args)
