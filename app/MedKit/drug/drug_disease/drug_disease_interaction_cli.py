"""Drug-Disease Interaction Analysis module."""

import argparse
import logging
from pathlib import Path
from typing import Optional, Union

from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from drug_disease_interaction import DrugDiseaseInteraction, DrugDiseaseInput, PromptStyle
from drug_disease_interaction_prompts import PromptBuilder

logger = logging.getLogger(__name__)


def parse_prompt_style(style_str: str) -> PromptStyle:
    """Parse prompt style string to PromptStyle enum."""
    style_mapping = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "balanced": PromptStyle.BALANCED,
    }

    if style_str.lower() not in style_mapping:
        raise ValueError(
            f"Invalid prompt style: {style_str}. "
            f"Choose from: {', '.join(style_mapping.keys())}"
        )
    return style_mapping[style_str.lower()]


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Drug-Disease Interaction Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    parser.add_argument(
        "condition_name",
        type=str,
        help="Name of the medical condition",
    )

    parser.add_argument(
        "--severity",
        "-S",
        type=str,
        choices=["mild", "moderate", "severe"],
        default=None,
        help="Severity of the condition (mild, moderate, severe)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--medications",
        "-M",
        type=str,
        default=None,
        help="Other medications the patient is taking (comma-separated)",
    )

    parser.add_argument(
        "--style",
        "-s",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--output-dir",
        "-od",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )

    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    parser.add_argument(
        "--structured",
        "-t",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response"
    )

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        default="ollama/gemma3",
        help="LLM model to use for analysis (default: ollama/gemma3)",
    )

    return parser.parse_args()


def create_drug_disease_interaction_report(args) -> int:

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_disease_interaction.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("DRUG-DISEASE INTERACTION CLI - Starting")
    logger.info("="*80)

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        config = DrugDiseaseInput(
            medicine_name=args.medicine_name,
            condition_name=args.condition_name,
            condition_severity=args.severity,
            age=args.age,
            other_medications=args.medications,
            prompt_style=parse_prompt_style(args.style),
        )

        logger.info("Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = DrugDiseaseInteraction(model_config)
        result = analyzer.generate_text(config, structured=args.structured)
        
        if result is None:
            logger.error("✗ Failed to analyze drug-disease interaction.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drug-disease interaction analysis completed successfully")
        return 0

    except ValueError as e:
        logger.error(f"✗ Invalid input: {e}")
        return 1
    except Exception as e:
        logger.error(f"✗ Drug-disease interaction analysis failed: {e}")
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    args = get_user_arguments()
    create_drug_disease_interaction_report(args)
