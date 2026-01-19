"""Module docstring - Medicine Information Generator.

Generate comprehensive, evidence-based pharmaceutical documentation using structured
data models and the LiteClient with schema-aware prompting for patient education and
clinical reference purposes.
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
from rich.table import Table

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from medicine_info_models import (
    MedicineGeneralInformation,
    TherapeuticClassification,
    MedicineBackground,
    Dosage,
    AdministrationGuidance,
    UsageAndAdministration,
    DrugInteractions,
    SafetyInformation,
    SpecialInstructions,
    SpecialPopulations,
    Efficacy,
    Alternatives,
    MedicineEducation,
    CostAndAvailability,
    MedicineEvidence,
    MedicineResearch,
    MedicineInfoResult,
)

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
class MedicineInfoConfig:
    """Configuration for generating medicine information."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False
    enable_cache: bool = True


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class MedicineInfoGenerator:
    """Generates comprehensive medicine information based on provided configuration."""

    def __init__(self, config: MedicineInfoConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        # Apply verbosity to logger
        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized MedicineInfoGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        medicine: str,
        patient_age: Optional[int] = None,
        medical_conditions: Optional[str] = None,
    ) -> MedicineInfoResult:
        """
        Generates comprehensive medicine information.

        Args:
            medicine: Name of the medicine
            patient_age: Patient's age in years (optional)
            medical_conditions: Patient's medical conditions (optional, comma-separated)

        Returns:
            MedicineInfoResult: Validated medicine information object
        """
        # Validate inputs
        if not medicine or not str(medicine).strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        logger.info("-" * 80)
        logger.info(f"Starting medicine information generation")
        logger.info(f"Medicine Name: {medicine}")

        # Determine output path
        output_path = self.config.output_path
        if output_path is None:
            output_path = self.config.output_dir / f"{medicine.lower().replace(' ', '_')}_info.json"
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path}")

        # Build context
        context_parts = [f"Generating information for {medicine}"]
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
            logger.info(f"Patient age provided: {patient_age}")
        if medical_conditions:
            context_parts.append(f"Patient conditions: {medical_conditions}")
            logger.info(f"Patient conditions provided: {medical_conditions}")

        context = ". ".join(context_parts) + "."
        logger.debug(f"Context: {context}")

        # Generate medicine information
        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate comprehensive information for the medicine: {medicine}. {context}"
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=MedicineInfoResult,
                )
            )

            logger.info(f"✓ Successfully generated medicine information")
            logger.info(f"Generic name: {result.general_information.generic_name}")
            logger.info(f"Brand names: {result.general_information.brand_names}")
            logger.info(f"Available forms: {result.general_information.forms_available}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medicine information: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, medicine_info: MedicineInfoResult, output_path: str):
        """
        Saves the medicine information to a JSON file.

        Args:
            medicine_info: The MedicineInfoResult object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving medicine information to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(medicine_info.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved medicine information")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving medicine information: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def get_medicine_info(
    medicine: str,
    config: MedicineInfoConfig,
    patient_age: Optional[int] = None,
    medical_conditions: Optional[str] = None,
) -> Optional[MedicineInfoResult]:
    """
    Get comprehensive medicine information.

    This is a convenience function that instantiates and runs the
    MedicineInfoGenerator.

    Args:
        medicine: Name of the medicine
        config: Configuration object for the generation
        patient_age: Patient's age in years (optional)
        medical_conditions: Patient's medical conditions (optional)

    Returns:
        MedicineInfoResult: The result of the generation, or None if it fails
    """
    try:
        generator = MedicineInfoGenerator(config)
        return generator.generate(
            medicine=medicine,
            patient_age=patient_age,
            medical_conditions=medical_conditions,
        )
    except Exception as e:
        logger.error(f"Failed to generate medicine information: {e}")
        return None


# ==============================================================================
# DISPLAY/OUTPUT FUNCTIONS
# ==============================================================================

def print_result(medicine_info: MedicineInfoResult) -> None:
    """
    Print medicine information in a formatted manner using rich.

    Args:
        medicine_info: The MedicineInfoResult object to display
    """
    console = Console()

    # General Information
    gen_info = medicine_info.general_information
    general_text = (
        f"[bold]Generic Name:[/bold] {gen_info.generic_name}\n"
        f"[bold]Brand Names:[/bold] {gen_info.brand_names}\n"
        f"[bold]Strength:[/bold] {gen_info.strength}\n"
        f"[bold]Forms Available:[/bold] {gen_info.forms_available}\n"
        f"[bold]Manufacturer:[/bold] {gen_info.manufacturer}"
    )
    console.print(
        Panel(
            general_text,
            title="General Information",
            border_style="cyan",
        )
    )

    # Classification
    classification = medicine_info.classification
    class_text = (
        f"[bold]Therapeutic Class:[/bold] {classification.therapeutic_class}\n"
        f"[bold]Pharmacological Class:[/bold] {classification.pharmacological_class}\n"
        f"[bold]Chemical Type:[/bold] {classification.chemical_type}"
    )
    console.print(
        Panel(
            class_text,
            title="Classification",
            border_style="blue",
        )
    )

    # Usage and Administration
    usage = medicine_info.usage_and_administration
    console.print(
        Panel(
            usage.indications,
            title="Indications (Uses)",
            border_style="green",
        )
    )

    console.print(
        Panel(
            usage.dosage_and_administration,
            title="Dosage and Administration",
            border_style="green",
        )
    )

    # Adverse Effects
    console.print(
        Panel(
            medicine_info.adverse_effects.common_side_effects,
            title="Common Side Effects",
            border_style="yellow",
        )
    )

    if medicine_info.adverse_effects.serious_adverse_effects:
        console.print(
            Panel(
                medicine_info.adverse_effects.serious_adverse_effects,
                title="Serious Adverse Effects",
                border_style="red",
            )
        )

    # Safety Information
    safety = medicine_info.safety_information
    safety_text = (
        f"[bold]Contraindications:[/bold]\n{safety.contraindications}\n\n"
        f"[bold]Warnings:[/bold]\n{safety.warnings}\n\n"
        f"[bold]Precautions:[/bold]\n{safety.precautions}"
    )
    console.print(
        Panel(
            safety_text,
            title="Safety Information",
            border_style="red",
        )
    )

    # Special Populations
    special_pops = medicine_info.special_populations
    special_text = (
        f"[bold]Pregnancy:[/bold] {special_pops.pregnancy_category}\n{special_pops.pregnancy_information}\n\n"
        f"[bold]Lactation:[/bold]\n{special_pops.lactation_information}\n\n"
        f"[bold]Pediatric Use:[/bold]\n{special_pops.pediatric_use}\n\n"
        f"[bold]Geriatric Use:[/bold]\n{special_pops.geriatric_use}"
    )
    console.print(
        Panel(
            special_text,
            title="Special Populations",
            border_style="magenta",
        )
    )

    # Cost and Availability
    cost = medicine_info.cost_and_availability
    cost_text = (
        f"[bold]Availability Status:[/bold] {cost.availability_status}\n"
        f"[bold]Typical Cost Range:[/bold] {cost.typical_cost_range}\n"
        f"[bold]Insurance Coverage:[/bold] {cost.insurance_coverage}"
    )
    console.print(
        Panel(
            cost_text,
            title="Cost and Availability",
            border_style="blue",
        )
    )


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating medicine information.
    """
    logger.info("="*80)
    logger.info("MEDICINE INFO CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate comprehensive medicine information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medicine_info.py -m aspirin
  python medicine_info.py -m "ibuprofen" -o output.json -v
  python medicine_info.py -m "metformin" -a 65 --conditions "diabetes, hypertension"
        """
    )
    parser.add_argument(
        "-m", "--medicine",
        required=True,
        help="The name of the medicine to generate information for."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save the output JSON file."
    )
    parser.add_argument(
        "-a", "--age",
        type=int,
        help="Patient age for context-specific information."
    )
    parser.add_argument(
        "-c", "--conditions",
        help="Comma-separated list of patient medical conditions."
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

    # Create configuration
    config = MedicineInfoConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Medicine: {args.medicine}")
    logger.info(f"  Age: {args.age if args.age else 'Not specified'}")
    logger.info(f"  Conditions: {args.conditions if args.conditions else 'None'}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Generate medicine information
    try:
        generator = MedicineInfoGenerator(config)
        medicine_info = generator.generate(
            medicine=args.medicine,
            patient_age=args.age,
            medical_conditions=args.conditions,
        )

        if medicine_info is None:
            logger.error("✗ Failed to generate medicine information.")
            sys.exit(1)

        # Display results
        print_result(medicine_info)

        # Save if output path is specified
        if args.output:
            generator.save(medicine_info, args.output)
        else:
            # Save to default location
            default_path = config.output_dir / f"{args.medicine.lower().replace(' ', '_')}_info.json"
            generator.save(medicine_info, str(default_path))

        logger.info("="*80)
        logger.info("✓ Medicine information generation completed successfully")
        logger.info("="*80)
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Medicine information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
