"""
surgery_info - Generate comprehensive surgical procedure documentation.

This module generates detailed, evidence-based surgical procedure documentation using
structured Pydantic data models and the MedKit AI client with schema-aware prompting.
Content covers the complete surgical journey from indications through recovery and includes
clinical rationale, patient education, and evidence-based guidelines for each aspect.

QUICK START:
    Get comprehensive information about a surgical procedure:

    >>> from surgery_info import SurgeryInfoGenerator
    >>> generator = SurgeryInfoGenerator()
    >>> result = generator.generate("Knee Replacement")
    >>> print(f"Generated surgical information for {result.metadata.surgery_name}")

    With custom output path:

    >>> result = generator.generate("Coronary Artery Bypass", output_path="cardiac_surgery.json")

    Or use the CLI:

    $ python surgery_info.py "Knee Replacement"
    $ python surgery_info.py "Coronary Artery Bypass" -o cardiac_procedures/

COMMON USES:
    1. Patient education - providing comprehensive, understandable surgical information before procedures
    2. Clinical reference - quick access to surgical indications, contraindications, and techniques
    3. Surgical planning - detailed pre-operative assessment and risk stratification guidance
    4. Medical training - resident and student learning of surgical procedures and techniques
    5. Research compilation - gathering evidence-based surgical practice guidelines and outcomes data

KEY FEATURES AND COVERAGE AREAS:
    - Metadata and procedure identification with CPT/ICD codes and category classification
    - Indications including absolute, relative, and emergency indications with contraindications
    - Historical and anatomical background with epidemiology of the procedure
    - Pre-operative phase with patient evaluation, testing, risk assessment, and counseling
    - Operative phase with surgical approaches, anesthesia, steps, instruments, and duration
    - Operative risks covering intraoperative, early, and late postoperative complications
    - Postoperative management including pain control, monitoring, diet, and discharge criteria
    - Recovery timeline with rehabilitation, return to work, success rates, and long-term outcomes
    - Alternative treatments including medical management, minimally invasive, and conservative approaches
    - Technical details with surgeon qualifications, facility requirements, and technology used
    - Current research and innovations including robotic surgery, AI applications, and clinical trials
    - Special populations considerations for pediatric, geriatric, and pregnant patients
    - Patient education with plain language explanation, key takeaways, and misconception correction
    - Evidence summary with evidence levels and comparative effectiveness research
    - Cost and insurance information including procedures codes and financial assistance programs
"""

import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

from surgery_info_models import SurgeryInfo

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the surgery info generator."""
    specialty: str = "Surgery/Procedure"

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "surgery_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# SURGERY INFO GENERATOR CLASS
# ============================================================================ 

class SurgeryInfoGenerator:
    """Generate comprehensive information for surgical procedures."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.surgery_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, surgery_name: str, output_path: Optional[Path] = None) -> SurgeryInfo:
        if not surgery_name or not surgery_name.strip():
            raise ValueError("Surgery name cannot be empty")

        self.surgery_name = surgery_name

        if output_path is None:
            output_path = self.config.output_dir / f"{surgery_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting surgical information generation for: {surgery_name}")

        surgery_info = self._generate_info()

        self.save(surgery_info, self.output_path)
        self.print_summary(surgery_info)
        
        return surgery_info

    def _generate_info(self) -> SurgeryInfo:
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of surgical procedures and clinical practice in {self.config.specialty}.

Generate comprehensive, evidence-based procedure information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between common/expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates)

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the surgical procedure: {self.surgery_name}",
            schema=SurgeryInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, surgery_info: SurgeryInfo, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(surgery_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Surgical information saved to {output_path}")
        return output_path

    def print_summary(self, surgery_info: SurgeryInfo) -> None:
        if self.config.verbosity < 3:
            return
        print("\n" + "="*70)
        print(f"SURGERY INFORMATION SUMMARY: {surgery_info.metadata.surgery_name}")
        print("="*70)
        print(f"  - Category: {surgery_info.metadata.surgery_category}")
        print(f"  - Body Systems: {surgery_info.metadata.body_systems_involved}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

    def close(self):
        """Close LMDB storage and release resources."""
        if self.storage:
            try:
                self.storage.close()
                logger.info("LMDB storage closed successfully.")
            except Exception as e:
                logger.error(f"Error closing LMDB storage: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

def get_surgery_info(surgery_name: str, output_path: Optional[Path] = None, verbosity: int = 2) -> SurgeryInfo:
    """
    High-level function to generate and optionally save surgery information.
    """
    config = Config(verbosity=verbosity)
    generator = SurgeryInfoGenerator(config=config)
    return generator.generate(surgery_name, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate comprehensive surgical procedure information.")
    parser.add_argument("surgery", nargs='+', help="Name of the surgical procedure")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    try:
        surgery_name = " ".join(args.surgery)
        config = Config(quiet=not args.verbose)
        generator = SurgeryInfoGenerator(config=config)
        generator.generate(surgery_name=surgery_name, output_path=args.output)
        if args.verbose:
            print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
