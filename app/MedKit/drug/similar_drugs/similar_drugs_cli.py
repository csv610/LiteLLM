"""Module docstring - Similar Medicines Finder and Comparator.

Find alternative medicines with similar active ingredients, therapeutic classes, and
mechanisms of action. Provides detailed comparisons to help identify suitable substitutes.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import logging
import sys
from pathlib import Path
from typing import Optional, Union
from utils.output_formatter import print_result


# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from similar_drugs_models import SimilarMedicinesResult

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logger = logging.getLogger(__name__)


# ==============================================================================
# CONSTANTS
# ==============================================================================
console = Console()


# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class SimilarDrugsConfig:
    """Configuration for finding similar drugs."""
    output_path: Optional[Path] = None
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG
    enable_cache: bool = True

# ==============================================================================
# MAIN CLASS
# ==============================================================================

class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: SimilarDrugsConfig, model_config: ModelConfig):
        self.config = config
        self.client = LiteClient(model_config)

        # Apply verbosity level using centralized logging configuration
        configure_logging(
            log_file=str(Path(__file__).parent / "logs" / "similar_drugs.log"),
            verbosity=self.config.verbosity,
            enable_console=True
        )

    def find(
        self,
        medicine_name: str,
        include_generics: bool = True,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
        structured: bool = False,
    ) -> Union[SimilarMedicinesResult, str]:
        """
        Finds top 10-15 medicines similar to a given medicine.

        Args:
            medicine_name: Name of the medicine to find alternatives for
            include_generics: Whether to include generic formulations (default: True)
            patient_age: Patient's age in years (optional, 0-150)
            patient_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            SimilarMedicinesResult: Top 10-15 similar medicines with detailed information
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        context_parts = [f"Finding top 10-15 medicines similar to {medicine_name}"]
        if include_generics:
            context_parts.append("Include generic formulations")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "."

        response_format = None
        if structured:
            response_format = SimilarMedicinesResult

        result = self.client.generate_text(
            model_input=ModelInput(
                user_prompt=f"Find the top 10-15 most similar medicines to {medicine_name} - prioritize same active ingredients, then therapeutic class, then similar mechanism. {context}",
                response_format=response_format,
            )
        )

        return result


def get_similar_medicines(
    medicine_name: str,
    config: SimilarDrugsConfig,
    model_config: ModelConfig,
    include_generics: bool = True,
    patient_age: Optional[int] = None,
    patient_conditions: Optional[str] = None,
    structured: bool = False,
) -> Union[SimilarMedicinesResult, str]:
    """
    Get similar medicines.

    This is a convenience function that instantiates and runs the
    SimilarDrugs finder.

    Args:
        medicine_name: Name of the medicine to find alternatives for
        config: Configuration object for the analysis
        model_config: ModelConfig object containing model settings
        include_generics: Whether to include generic formulations (default: True)
        patient_age: Patient's age in years (optional)
        patient_conditions: Patient's medical conditions (optional)

    Returns:
        SimilarMedicinesResult: The result of the analysis
    """
    finder = SimilarDrugs(config, model_config)
    return finder.find(
        medicine_name=medicine_name,
        include_generics=include_generics,
        patient_age=patient_age,
        patient_conditions=patient_conditions,
        structured=structured,
    )


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Similar Drugs Finder - Find alternative medicines and similar drug options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python similar_drugs.py "Ibuprofen"

  # Include generics
  python similar_drugs.py "Aspirin" --include-generics

  # With patient details
  python similar_drugs.py "Metformin" --age 65 --conditions "kidney disease, hypertension"

  # With custom output
  python similar_drugs.py "Simvastatin" --output alternatives.json --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to find similar alternatives for",
    )

    # Optional arguments
    parser.add_argument(
        "--include-generics",
        action="store_true",
        default=True,
        help="Include generic formulations (default: True)",
    )

    parser.add_argument(
        "--no-generics",
        dest="include_generics",
        action="store_false",
        help="Exclude generic formulations",
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
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output file path for results (default: outputs/{medicine}_similar_medicines.json)",
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
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
    )

    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )

    return parser




# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    Main entry point for the similar drugs CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    try:
        # Create configuration
        config = SimilarDrugsConfig(
            output_path=args.output if hasattr(args, 'output') else None,
            verbosity=args.verbosity,
        )

        logger.debug(f"Configuration created successfully")

        # Run analysis
        model_config = ModelConfig(model="ollama/gemma2", temperature=0.7)
        analyzer = SimilarDrugs(config, model_config)
        result = analyzer.find(
            medicine_name=args.medicine_name,
            include_generics=args.include_generics if hasattr(args, 'include_generics') else True,
            patient_age=args.age if hasattr(args, 'age') else None,
            patient_conditions=args.conditions if hasattr(args, 'conditions') else None,
            structured=args.structured,
        )

        # Print results
        print_result(result, title="Similar Medicines Analysis")

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine_clean = args.medicine_name.lower().replace(' ', '_')
            suffix = ".json"
            if isinstance(result, str):
                suffix = ".md"
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines{suffix}"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")

        with open(output_path, "w") as f:
            if isinstance(result, str):
                f.write(result)
            else:
                f.write(result.model_dump_json(indent=2))

        logger.debug(f"✓ Results saved to {output_path}")
        print(f"\n✓ Results saved to: {output_path}")

        # Output JSON to stdout if requested
        if args.json_output:
            print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}", file=sys.stderr)
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        logger.error(f"Unexpected error: {e}")
        return 1


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
