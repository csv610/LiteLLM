"""Module docstring - Medicines Comparison Tool.

Compare medicines side-by-side across clinical, regulatory, and practical metrics to help
healthcare professionals and patients make informed treatment decisions.
"""

import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from utils.output_formatter import print_result

from drugs_comparison_models import MedicinesComparisonResult

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for medicines comparison analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for medicines comparison analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in comparative medication analysis. Your role is to provide comprehensive, objective comparisons between medications to help healthcare professionals and patients make informed treatment decisions.

When comparing medications, you must:

1. Compare efficacy and effectiveness based on clinical evidence
2. Analyze safety profiles, side effects, and contraindications
3. Evaluate cost, availability, and insurance coverage considerations
4. Compare mechanisms of action and pharmacokinetics
5. Assess suitability for different patient populations (age, conditions, etc.)
6. Identify key differences in dosing, administration, and monitoring requirements
7. Consider drug interactions and precautions for each medication
8. Provide evidence-based recommendations considering patient-specific factors
9. Base analysis on established medical literature, clinical trials, and regulatory guidance

Always maintain objectivity and present balanced information to support informed decision-making."""

    @staticmethod
    def create_user_prompt(medicine1: str, medicine2: str, context: str) -> str:
        """
        Create the user prompt for medicines comparison analysis.

        Args:
            medicine1: The name of the first medicine
            medicine2: The name of the second medicine
            context: Additional context for the comparison

        Returns:
            str: Formatted user prompt
        """
        return f"Detailed side-by-side comparison between {medicine1} and {medicine2}. {context}"


@dataclass
class DrugsComparisonInput:
    """Configuration and input for medicines comparison."""
    medicine1: str
    medicine2: str
    use_case: Optional[str] = None
    patient_age: Optional[int] = None
    patient_conditions: Optional[str] = None
    prompt_style: str = "detailed"


class DrugsComparison:
    """Compares two medicines based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugsComparisonInput, structured: bool = False) -> Union[MedicinesComparisonResult, str]:
        """Compares two medicines across clinical, regulatory, and practical metrics."""
        self._validate_input(config)

        logger.debug(f"Starting medicines comparison analysis")
        logger.debug(f"Medicine 1: {config.medicine1}")
        logger.debug(f"Medicine 2: {config.medicine2}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        user_prompt = PromptBuilder.create_user_prompt(config.medicine1, config.medicine2, context)
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=MedicinesComparisonResult if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.debug(f"✓ Successfully compared medicines")
        return result

    def _validate_input(self, config: DrugsComparisonInput) -> None:
        """Validate input parameters."""
        if not config.medicine1 or not config.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not config.medicine2 or not config.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if config.patient_age is not None and (config.patient_age < 0 or config.patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugsComparisonInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Comparing {config.medicine1} and {config.medicine2}"]
        if config.use_case:
            context_parts.append(f"Use case: {config.use_case}")
            logger.debug(f"Use case: {config.use_case}")
        if config.patient_age is not None:
            context_parts.append(f"Patient age: {config.patient_age} years")
            logger.debug(f"Patient age: {config.patient_age}")
        if config.patient_conditions:
            context_parts.append(f"Patient conditions: {config.patient_conditions}")
            logger.debug(f"Patient conditions: {config.patient_conditions}")
        return ". ".join(context_parts) + "."


    def _ask_llm(self, model_input: ModelInput) -> Union[MedicinesComparisonResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during medicines comparison: {e}")
            logger.exception("Full exception details:")
            raise


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Medicines Comparison Tool - Compare two medicines side-by-side",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic comparison
  python drugs_comparison.py "Aspirin" "Ibuprofen"

  # With use case
  python drugs_comparison.py "Lisinopril" "Losartan" --use-case "hypertension management"

  # With patient details
  python drugs_comparison.py "Metformin" "Glipizide" --age 68 --conditions "type-2 diabetes, kidney disease"

  # With custom model and JSON output
  python drugs_comparison.py "Atorvastatin" "Simvastatin" --model "ollama/llama3" --json-output
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine to compare",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine to compare",
    )

    # Optional arguments
    parser.add_argument(
        "--use-case",
        "-u",
        type=str,
        default=None,
        help="Use case or indication for the comparison (e.g., 'pain relief', 'hypertension')",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--conditions",
        "-c",
        type=str,
        default=None,
        help="Patient's medical conditions (comma-separated)",
    )

    parser.add_argument(
        "--prompt-style",
        "-p",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
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
        "--model",
        "-m",
        type=str,
        default="ollama/gemma2",
        help="Model ID to use for the comparison (e.g., 'ollama/llama3', 'openai/gpt-4o')",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout",
    )

    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser.parse_args()

def main() -> int:
    """
    Main entry point for the drugs comparison CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    args = get_user_arguments()

    # Apply verbosity level using centralized logging configuration
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drugs_comparison.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        # Create configuration
        config = DrugsComparisonInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            use_case=args.use_case,
            patient_age=args.age,
            patient_conditions=args.conditions,
            prompt_style=args.prompt_style,
        )

        # Removed redundant log: logger.info(f"Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugsComparison(model_config)
        result = analyzer.generate_text(config, structured=args.structured)

        # Print results
        print_result(result, title="Medicines Comparison Result")

        # Output JSON to stdout if requested
        if args.json_output:
            if isinstance(result, str):
                print(f"\n{result}")
            else:
                print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1



if __name__ == "__main__":
    sys.exit(main())
