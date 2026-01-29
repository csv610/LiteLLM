"""Module docstring - Medical Decision Guide Generator.

Generate medical decision trees for symptom assessment using structured data models
and the LiteClient with schema-aware prompting for clinical decision support.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_decision_guide import MedicalDecisionGuideGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate medical decision trees for symptom assessment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_decision_guide_cli.py -i fever
  python medical_decision_guide_cli.py -i "sore throat" -o output.json -v 3
  python medical_decision_guide_cli.py -i cough -d outputs/guides
        """
    )
    parser.add_argument(
        "-i", "--symptom",
        required=True,
        help="The name of the symptom to generate a decision tree for."
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
    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()


def create_medical_decision_guide_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_decision_guide.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("MEDICAL DECISION GUIDE CLI - Starting")
    logger.info("="*80)

    logger.debug(f"CLI Arguments:")
    logger.debug(f"  Symptom: {args.symptom}")
    logger.debug(f"  Output Dir: {args.output_dir}")
    logger.debug(f"  Output File: {args.output if args.output else 'Default'}")
    logger.debug(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate decision guide
    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalDecisionGuideGenerator(model_config)
        guide = generator.generate_text(symptom=args.symptom, structured=args.structured)

        if guide is None:
            logger.error("✗ Failed to generate decision guide.")
            sys.exit(1)

        # Save if output path is specified
        if args.output:
            generator.save(guide, Path(args.output))
        else:
            # Save to default location
            default_path = output_dir / f"{args.symptom.lower().replace(' ', '_')}_decision_tree.json"
            generator.save(guide, default_path)

        logger.debug("✓ Decision guide generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"✗ Decision guide generation failed: {e}")
        logger.exception("Full exception details:")
        sys.exit(1)


if __name__ == "__main__":
    args = get_user_arguments()
    create_medical_decision_guide_report(args)
