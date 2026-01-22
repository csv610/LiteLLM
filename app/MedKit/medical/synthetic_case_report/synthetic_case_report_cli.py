import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional, final

from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from synthetic_case_report_models import SyntheticCaseReport

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for synthetic case report generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for synthetic case report generation."""
        return """You are an expert medical case report writer with extensive clinical experience across multiple specialties.
Generate realistic, comprehensive, and clinically accurate synthetic medical case reports. Focus on presenting coherent patient narratives,
relevant clinical findings, diagnostic processes, treatment approaches, and outcomes. Ensure all information is medically sound and follows
standard case report structure."""

    @staticmethod
    def create_user_prompt(condition: str) -> str:
        """Create the user prompt for synthetic case report generation.

        Args:
            condition: The name of the disease or medical condition for the case report.

        Returns:
            A comprehensive prompt asking for a detailed synthetic case report.
        """
        return f"""Generate a comprehensive synthetic medical case report for: {condition}.

Include the following components:
- Patient demographics and presenting complaint
- Medical history and relevant background
- Physical examination findings
- Diagnostic investigations and results
- Differential diagnosis considerations
- Treatment plan and interventions
- Clinical course and outcomes
- Discussion and learning points"""


@final
class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        logger.info(f"Initialized SyntheticCaseReportGenerator")

    def generate_text(self, condition: str) -> SyntheticCaseReport:
        """Generates a synthetic medical case report."""
        if not condition or not str(condition).strip():
            raise ValueError("Condition name cannot be empty")

        logger.info(f"Starting synthetic case report generation for: {condition}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(condition)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=SyntheticCaseReport,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.info("✓ Successfully generated synthetic case report")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating synthetic case report: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> SyntheticCaseReport:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, case_report: SyntheticCaseReport, output_path: Path) -> Path:
        """Saves the case report to a JSON file."""
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Saving case report to: {output_path}")
            with open(output_path, "w") as f:
                json.dump(case_report.model_dump(), f, indent=2, default=str)
            logger.info(f"✓ Successfully saved case report to {output_path}")
            return output_path
        except (OSError, IOError) as e:
            logger.error(f"✗ Error saving case report to {output_path}: {e}")
            raise

    @property
    def logger(self):
        return logger


def print_result(result: SyntheticCaseReport) -> None:
    """Print result in a formatted manner using rich."""
    console = Console()

    result_dict = result.model_dump()

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
        description="Generate synthetic medical case reports.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python synthetic_case_report_cli.py -i "myocardial infarction"
  python synthetic_case_report_cli.py -i "pneumonia" -o output.json -v 3
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
        log_file="synthetic_case_report.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    logger.info("="*80)
    logger.info("SYNTHETIC CASE REPORT CLI - Starting")
    logger.info("="*80)

    logger.info(f"CLI Arguments:")
    logger.info(f"  Condition: {args.condition}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbosity: {args.verbosity}")

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = SyntheticCaseReportGenerator(model_config)
        case_report = generator.generate_text(condition=args.condition)

        # Display formatted result
        print_result(case_report)

        if args.output:
            generator.save(case_report, Path(args.output))
        else:
            default_path = output_dir / f"{args.condition.lower().replace(' ', '_')}_casereport.json"
            generator.save(case_report, default_path)

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


if __name__ == "__main__":
    sys.exit(app_cli())
