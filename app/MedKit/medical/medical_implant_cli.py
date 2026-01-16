"""medical_implant - Generate comprehensive medical implant documentation.

This module generates detailed, evidence-based information about medical implants
(orthopedic, cardiovascular, neurological, etc.). It provides complete implant
documentation including indications, materials, installation procedures, outcomes,
complications, and maintenance using the MedKit AI client with structured Pydantic schemas.

QUICK START:
    Generate implant information:

    >>> from medical_implant import MedicalImplantInfoGenerator
    >>> generator = MedicalImplantInfoGenerator()
    >>> result = generator.generate("Hip Replacement")
    >>> print(result.metadata.implant_name)
    Hip Replacement

    Or use the CLI:

    $ python medical_implant.py -i "Hip Replacement"
    $ python medical_implant.py -i "Pacemaker" -o custom_output.json

COMMON USES:
    1. Patient education - helping patients understand implant details
    2. Informed consent - providing comprehensive pre-implant information
    3. Clinical reference - detailed implant guidelines for healthcare teams
    4. Surgical planning - implant specifications, installation techniques, compatibility
    5. Insurance and billing - cost information, billing codes, coverage details
    6. Follow-up care - long-term monitoring and management requirements

KEY FEATURES AND COVERAGE AREAS:
    - Implant identification: official names, types, manufacturers, models
    - Purpose and indications: clinical reasons for implant, what it treats
    - Implant materials: composition, biocompatibility, allergic considerations
    - Installation procedure: surgical approach, duration, anesthesia type
    - Recovery and healing: timeline, restrictions, pain management
    - Functionality: how the implant works, expected performance, adjustments
    - Complications and risks: infection, rejection, displacement, failure rates
    - Lifespan and longevity: expected durability, revision rates, replacement timeline
    - Imaging and testing: MRI/CT compatibility, monitoring requirements, diagnostic tools
    - Activity restrictions: permanent limitations, sports, lifting, activities
    - Maintenance and care: cleaning, inspections, replacements, upgrades
    - Cost and insurance: pricing, coverage, financial assistance programs
    - Alternatives: other implants, non-implant options, comparative advantages
    - Patient education: plain language explanations, daily living with implant, misconceptions
"""

import json
import sys
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.logging_config import setup_logger

from medical_implant_models import ImplantInfo

# Configure logging
logger = setup_logger(__name__)

# Suppress logger output by default (can be overridden via set_verbose)
logger.setLevel(logging.WARNING)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical implant info generator."""
    specialty: str = "Surgery/Implantology"

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_implant.lmdb"
            )
        # Call parent validation
        super().__post_init__()

# ============================================================================
# MEDICAL IMPLANT INFO GENERATOR CLASS
# ============================================================================

class MedicalImplantInfoGenerator:
    """Generate comprehensive information for medical implants."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.implant_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, implant_name: str, output_path: Optional[Path] = None) -> ImplantInfo:
        """
        Generate and save comprehensive medical implant information.

        Args:
            implant_name: Name of the medical implant.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated ImplantInfo object.

        Raises:
            ValueError: If implant_name is empty.
        """
        if not implant_name or not implant_name.strip():
            raise ValueError("Implant name cannot be empty")

        self.implant_name = implant_name

        if output_path is None:
            output_path = self.config.output_dir / f"{implant_name.lower().replace(' ', '_')}_info.json"

        self.output_path = output_path

        logger.info(f"Starting medical implant information generation for: {implant_name}")

        implant_info = self._generate_info()

        self.save(implant_info, self.output_path)
        self.print_summary(implant_info)

        return implant_info

    def _generate_info(self) -> ImplantInfo:
        """Generates the implant information."""
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of medical implants in {self.config.specialty}.

Generate comprehensive, evidence-based implant information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates, longevity data)
- Addresses both the technical and patient-facing aspects of the implant

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the medical implant: {self.implant_name}",
            schema=ImplantInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, implant_info: ImplantInfo, output_path: Path) -> Path:
        """
        Save the generated implant information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(implant_info.model_dump(), f, indent=2)

        logger.info(f"✓ Implant information saved to {output_path}")
        return output_path

    def print_summary(self, implant_info: ImplantInfo) -> None:
        """
        Print a summary of the generated implant information.
        """
        if not self.config.verbose:
            return
        print("\n" + "="*70)
        print(f"IMPLANT INFORMATION SUMMARY: {implant_info.metadata.implant_name}")
        print("="*70)
        print(f"  - Type: {implant_info.metadata.implant_type}")
        print(f"  - Specialty: {implant_info.metadata.medical_specialty}")
        print(f"  - Purpose: {implant_info.purpose.primary_purpose}")
        print(f"  - Expected Lifespan: {implant_info.functionality.lifespan}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_implant_info(implant_name: str, output_path: Optional[Path] = None, verbose: bool = True) -> ImplantInfo:
    """
    High-level function to generate and optionally save implant information.
    """
    config = Config(verbose=verbose)
    generator = MedicalImplantInfoGenerator(config=config)
    return generator.generate(implant_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical implant.")
    parser.add_argument("-i", "--implant", type=str, required=True, help="The name of the medical implant to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output.")

    args = parser.parse_args()
    get_implant_info(args.implant, args.output, args.verbose)
