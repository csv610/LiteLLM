"""
drug_drug_interaction.py - Drug-Drug Interaction Analysis

Analyze potential harmful interactions between two medicines and provide comprehensive
clinical recommendations using structured data models and the MedKit AI client
with schema-aware prompting.

This module helps healthcare providers identify dangerous drug combinations and
understand the mechanisms, clinical effects, and management strategies for interactions.

QUICK START:
    from drug_drug_interaction import DrugDrugInteraction, DrugDrugInteractionConfig

    # Configure the analysis
    config = DrugDrugInteractionConfig(medicine1="aspirin", medicine2="ibuprofen")

    # Create an analyzer and get the interaction
    interaction = DrugDrugInteraction(config).analyze()

    # Check severity
    if interaction.severity_level.value in ["SIGNIFICANT", "CONTRAINDICATED"]:
        print(f"⚠️ Serious interaction: {interaction.mechanism_of_interaction}")

    # Get management recommendations
    print(f"Recommendations: {interaction.management_recommendations}")

COMMON USES:
    1. Identify dangerous drug combinations before prescribing
    2. Counsel patients on medication compatibility
    3. Review patient medications for interactions
    4. Support polypharmacy management in elderly patients
    5. Generate clinical decision support recommendations
    6. Create interaction reports for healthcare providers

KEY CONCEPTS:
    - DrugInteractionSeverity: How serious the interaction is (NONE to CONTRAINDICATED)
    - ConfidenceLevel: Strength of evidence (HIGH, MODERATE, LOW)
    - DataSourceType: Where the interaction evidence comes from
    - DrugInteractionDetails: Complete information about the interaction

INTERACTION INFORMATION:
    - Mechanism of interaction: How drugs interact chemically/pharmacologically
    - Clinical effects: Observable symptoms and complications
    - Management recommendations: How to handle the interaction
    - Timing considerations: Spacing between doses
    - Monitoring requirements: What to watch for
"""

import logging
import sys
import json
import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.pydantic_prompt_generator import PromptStyle
from medkit.utils.logging_config import setup_logger

from drug_drug_interaction_models import (
    DrugInteractionSeverity,
    ConfidenceLevel,
    DataSourceType,
    DrugInteractionDetails,
    PatientFriendlySummary,
    DataAvailabilityInfo,
    DrugInteractionResult,
)

# Configure logging
logger = setup_logger(__name__)
logger.info("="*80)
logger.info("Drug-Drug Interaction Module Initialized")
logger.info("="*80)


@dataclass
class DrugDrugInteractionConfig(MedKitConfig):
    """
    Configuration for drug-drug interaction analysis.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to drug_drug_interaction.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    output_path: Optional[Path] = None
    verbosity: bool = False
    prompt_style: PromptStyle = PromptStyle.DETAILED
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "drug_drug_interaction.lmdb"
            )
        # Call parent validation
        super().__post_init__()


class DrugDrugInteraction:
    """Analyzes drug-drug interactions based on provided configuration."""

    def __init__(self, config: DrugDrugInteractionConfig):
        self.config = config

        # Load model name from ModuleConfig
        model_name = "ollama/gemma3:12b"  # Default model for this module

        self.client = MedKitClient(model_name=model_name)

    def analyze(
        self,
        medicine1: str,
        medicine2: str,
        age: Optional[int] = None,
        dosage1: Optional[str] = None,
        dosage2: Optional[str] = None,
        medical_conditions: Optional[str] = None,
    ) -> DrugInteractionResult:
        """
        Analyzes how two drugs interact.

        Args:
            medicine1: Name of the first medicine
            medicine2: Name of the second medicine
            age: Patient's age in years (optional, 0-150)
            dosage1: Dosage information for first medicine (optional)
            dosage2: Dosage information for second medicine (optional)
            medical_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            DrugInteractionResult: Comprehensive interaction analysis with management recommendations
        """
        # Validate inputs
        if not medicine1 or not medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not medicine2 or not medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if age is not None and (age < 0 or age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting drug-drug interaction analysis")
        logger.info(f"Drug 1: {medicine1}")
        logger.info(f"Drug 2: {medicine2}")
        logger.info(f"Prompt Style: {self.config.prompt_style.value if hasattr(self.config.prompt_style, 'value') else self.config.prompt_style}")

        output_path = self.config.output_path
        if output_path is None:
            medicine1_clean = medicine1.lower().replace(' ', '_')
            medicine2_clean = medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_{medicine2_clean}_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        context_parts = [f"Checking interaction between {medicine1} and {medicine2}"]
        if age is not None:
            context_parts.append(f"Patient age: {age} years")
            logger.info(f"Patient age: {age}")
        if dosage1:
            context_parts.append(f"{medicine1} dosage: {dosage1}")
            logger.info(f"{medicine1} dosage: {dosage1}")
        if dosage2:
            context_parts.append(f"{medicine2} dosage: {dosage2}")
            logger.info(f"{medicine2} dosage: {dosage2}")
        if medical_conditions:
            context_parts.append(f"Patient conditions: {medical_conditions}")
            logger.info(f"Medical conditions: {medical_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        logger.info("Calling MedKitClient.generate_text()...")
        try:
            result = self.client.generate_text(
                prompt=f"{medicine1} and {medicine2} interaction analysis. {context}",
                schema=DrugInteractionResult,
            )

            logger.info(f"✓ Successfully analyzed interaction")
            logger.info(f"Severity: {result.interaction_details.severity_level if result.interaction_details else 'N/A'}")
            logger.info(f"Data Available: {result.data_availability.data_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error analyzing drug interaction: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise


def get_drug_drug_interaction(
    medicine1: str,
    medicine2: str,
    config: DrugDrugInteractionConfig,
    age: Optional[int] = None,
    dosage1: Optional[str] = None,
    dosage2: Optional[str] = None,
    medical_conditions: Optional[str] = None,
) -> DrugInteractionResult:
    """
    Get drug-drug interaction analysis.

    This is a convenience function that instantiates and runs the
    DrugDrugInteraction analyzer.

    Args:
        medicine1: Name of the first medicine
        medicine2: Name of the second medicine
        config: Configuration object for the analysis
        age: Patient's age in years (optional)
        dosage1: Dosage information for first medicine (optional)
        dosage2: Dosage information for second medicine (optional)
        medical_conditions: Patient's medical conditions (optional)

    Returns:
        DrugInteractionResult: The result of the analysis
    """
    analyzer = DrugDrugInteraction(config)
    return analyzer.analyze(
        medicine1=medicine1,
        medicine2=medicine2,
        age=age,
        dosage1=dosage1,
        dosage2=dosage2,
        medical_conditions=medical_conditions,
    )


def create_cli_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer - Check interactions between two medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_drug_interaction.py "Warfarin" "Aspirin"

  # With patient details
  python drug_drug_interaction.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"

  # With medical conditions and custom output
  python drug_drug_interaction.py "Ibuprofen" "Aspirin" --conditions "hypertension, diabetes" --output interaction.json

  # With detailed prompt style
  python drug_drug_interaction.py "Simvastatin" "Clarithromycin" --prompt-style detailed --verbose
        """,
    )

    # Required arguments
    parser.add_argument(
        "medicine1",
        type=str,
        help="Name of the first medicine",
    )

    parser.add_argument(
        "medicine2",
        type=str,
        help="Name of the second medicine",
    )

    # Optional arguments
    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--dosage1",
        "-d1",
        type=str,
        default=None,
        help="Dosage information for first medicine",
    )

    parser.add_argument(
        "--dosage2",
        "-d2",
        type=str,
        default=None,
        help="Dosage information for second medicine",
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
        help="Output file path for results (default: outputs/{medicine1}_{medicine2}_interaction.json)",
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
        "--no-schema",
        action="store_true",
        default=False,
        help="Disable schema-based prompt generation",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Enable verbose logging output",
    )

    parser.add_argument(
        "--json-output",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
    )

    return parser


def parse_prompt_style(style_str: str) -> PromptStyle:
    """
    Parse prompt style string to PromptStyle enum.

    Args:
        style_str: String representation of prompt style

    Returns:
        PromptStyle: The corresponding enum value

    Raises:
        ValueError: If style string is not a valid prompt style
    """
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


def print_results(result: DrugInteractionResult, verbose: bool = False) -> None:
    """
    Print interaction analysis results in a formatted manner using rich.

    Args:
        result: The analysis result to print
        verbose: Whether to print detailed information
    """
    console = Console()

    # Print data availability
    if not result.data_availability.data_available:
        console.print(
            Panel(
                f"⚠️  [yellow]{result.data_availability.reason}[/yellow]",
                title="Data Availability",
                border_style="yellow",
            )
        )
        return

    # Print interaction details
    if result.interaction_details:
        details = result.interaction_details

        # Determine severity color
        severity_color = {
            "NONE": "green",
            "MINOR": "blue",
            "SIGNIFICANT": "yellow",
            "CONTRAINDICATED": "red",
        }.get(details.severity_level.value, "white")

        # Create details panel
        details_text = (
            f"[bold]Drug 1:[/bold] {details.drug1_name}\n"
            f"[bold]Drug 2:[/bold] {details.drug2_name}\n"
            f"[bold]Severity:[/bold] [{severity_color}]{details.severity_level.value}[/{severity_color}]\n"
            f"[bold]Confidence:[/bold] {details.confidence_level.value}\n"
            f"[bold]Data Source:[/bold] {details.data_source_type.value}"
        )

        console.print(
            Panel(
                details_text,
                title="Drug Interaction Details",
                border_style="cyan",
            )
        )

        # Mechanism of interaction
        console.print(
            Panel(
                details.mechanism_of_interaction,
                title="Mechanism of Interaction",
                border_style="blue",
            )
        )

        # Clinical effects
        effects = [effect.strip() for effect in details.clinical_effects.split(",")]
        console.print("[bold cyan]Clinical Effects:[/bold cyan]")
        for effect in effects:
            console.print(f"  • {effect}")
        console.print()

        # Management recommendations
        recommendations = [
            rec.strip() for rec in details.management_recommendations.split(",")
        ]
        console.print("[bold cyan]Management Recommendations:[/bold cyan]")
        for rec in recommendations:
            console.print(f"  • {rec}")
        console.print()

        # Alternative medicines
        alternatives = [
            alt.strip() for alt in details.alternative_medicines.split(",")
        ]
        console.print("[bold cyan]Alternative Medicines:[/bold cyan]")
        for alt in alternatives:
            console.print(f"  • {alt}")
        console.print()

    # Print patient-friendly summary
    if result.patient_friendly_summary:
        summary = result.patient_friendly_summary

        # Simple explanation
        console.print(
            Panel(
                summary.simple_explanation,
                title="Simple Explanation",
                border_style="green",
            )
        )

        # What patient should do
        console.print(
            Panel(
                summary.what_patient_should_do,
                title="What You Should Do",
                border_style="green",
            )
        )

        # Warning signs
        warning_signs = [sign.strip() for sign in summary.warning_signs.split(",")]
        console.print("[bold yellow]Warning Signs:[/bold yellow]")
        for sign in warning_signs:
            console.print(f"  • {sign}")
        console.print()

        # When to seek help
        console.print(
            Panel(
                summary.when_to_seek_help,
                title="When to Seek Help",
                border_style="red",
            )
        )

    # Print technical summary
    console.print(
        Panel(
            result.technical_summary,
            title="Technical Summary",
            border_style="magenta",
        )
    )


def main() -> int:
    """
    Main entry point for the drug-drug interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    # Configure logging verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    try:
        # Parse prompt style
        prompt_style = parse_prompt_style(args.prompt_style)

        # Create configuration
        config = DrugDrugInteractionConfig(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.conditions,
            output_path=args.output,
            use_schema_prompt=not args.no_schema,
            prompt_style=prompt_style,
        )

        logger.info(f"Configuration created successfully")

        # Run analysis
        analyzer = DrugDrugInteraction(config)
        result = analyzer.analyze()

        # Print results
        print_results(result, verbose=args.verbose)

        # Save results to file
        if args.output:
            output_path = args.output
        else:
            medicine1_clean = args.medicine1.lower().replace(' ', '_')
            medicine2_clean = args.medicine2.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine1_clean}_{medicine2_clean}_interaction.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write(result.model_dump_json(indent=2))

        logger.info(f"✓ Results saved to {output_path}")
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
        logger.exception("Full exception details:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
