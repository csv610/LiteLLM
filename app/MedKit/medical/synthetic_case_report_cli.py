"""Module docstring - Synthetic Case Report Generator.

Generate synthetic medical case reports using structured data models and the
LiteClient with schema-aware prompting for clinical training and educational
purposes.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from rich.console import Console
from rich.panel import Panel

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from synthetic_case_report_models import SyntheticCaseReport

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTS
# ==============================================================================
console = Console()

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class SyntheticCaseReportConfig:
    """Configuration for generating synthetic case reports."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports based on provided configuration."""

    def __init__(self, config: SyntheticCaseReportConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized SyntheticCaseReportGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        condition: str,
        output_path: Optional[str] = None,
    ) -> SyntheticCaseReport:
        """
        Generates a synthetic medical case report.

        Args:
            condition: Name of the disease or medical condition
            output_path: Optional path to save the output JSON file

        Returns:
            SyntheticCaseReport: Validated case report object
        """
        if not condition or not str(condition).strip():
            raise ValueError("Condition name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting synthetic case report generation")
        logger.info(f"Condition Name: {condition}")

        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{condition.lower().replace(' ', '_')}_casereport.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate a comprehensive synthetic medical case report for: {condition}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=SyntheticCaseReport,
                )
            )

            logger.info(f"✓ Successfully generated synthetic case report")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating synthetic case report: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, case_report: SyntheticCaseReport, output_path: str):
        """
        Saves the case report to a JSON file.

        Args:
            case_report: The SyntheticCaseReport object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving case report to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(case_report.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved case report")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving case report: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: SyntheticCaseReport, verbose: bool = False) -> None:
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


def generate_case_report(
    condition: str,
    config: SyntheticCaseReportConfig,
    output_path: Optional[str] = None,
) -> Optional[SyntheticCaseReport]:
    """
    Generate a synthetic medical case report.

    This is a convenience function that instantiates and runs the
    SyntheticCaseReportGenerator.

    Args:
        condition: Name of the disease or medical condition
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        SyntheticCaseReport: The result of the generation, or None if it fails
    """
    try:
        generator = SyntheticCaseReportGenerator(config)
        return generator.generate(condition=condition, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate synthetic case report: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating synthetic case reports.
    """
    logger.info("="*80)
    logger.info("SYNTHETIC CASE REPORT CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate synthetic medical case reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python synthetic_case_report_cli.py -i "myocardial infarction"
  python synthetic_case_report_cli.py -i "pneumonia" -o output.json -v
  python synthetic_case_report_cli.py -i "diabetes" -d outputs/cases
        """
    )
    parser.add_argument(
        "-i", "--condition",
        required=True,
        help="The name of the disease or medical condition for the case report."
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
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose/debug logging output."
    )

    args = parser.parse_args()

    config = SyntheticCaseReportConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Condition: {args.condition}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    try:
        generator = SyntheticCaseReportGenerator(config)
        case_report = generator.generate(condition=args.condition, output_path=args.output)

        if case_report is None:
            logger.error("✗ Failed to generate synthetic case report.")
            sys.exit(1)

        # Display formatted result
        print_result(case_report, args.verbose)

        if args.output:
            generator.save(case_report, args.output)
        else:
            default_path = config.output_dir / f"{args.condition.lower().replace(' ', '_')}_casereport.json"
            generator.save(case_report, str(default_path))

        logger.info("="*80)
        logger.info("✓ Synthetic case report generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Synthetic case report generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
