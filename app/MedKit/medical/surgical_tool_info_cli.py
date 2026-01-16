"""
surgical_tool_info - Generate comprehensive surgical instrument documentation.

This module generates detailed, evidence-based surgical tool and instrument documentation using
structured Pydantic data models and the MedKit AI client. Coverage includes physical specifications,
operational characteristics, safety features, maintenance requirements, and clinical applications
with emphasis on user value and practical operational guidance.

QUICK START:
    Get comprehensive information about a surgical instrument:

    >>> from surgical_tool_info import SurgicalToolInfoGenerator
    >>> generator = SurgicalToolInfoGenerator()
    >>> result = generator.generate("Surgical Scalpel")
    >>> print(f"Generated tool information for {result.tool_basics.tool_name}")

    With custom output path:

    >>> result = generator.generate("Surgical Forceps", output_path="instruments/forceps.json")

    Or use the CLI:

    $ python surgical_tool_info.py "Surgical Scalpel"
    $ python surgical_tool_info.py "Hemostatic Clamp" -o surgical_instruments/

COMMON USES:
    1. Surgeon training - comprehensive learning resources for safe and effective tool use
    2. Instrument procurement - specifications and comparisons for OR equipment purchasing decisions
    3. Operating room management - maintenance schedules, sterilization protocols, and inventory tracking
    4. Surgical safety - identifying risks, complications, and best practices for tool usage
    5. Equipment evaluation - comparing alternatives and understanding advantages/disadvantages

KEY FEATURES AND COVERAGE AREAS:
    - Tool basics with official names, categories, surgical specialties, and instrument families
    - Purpose and applications including surgical use, anatomical targets, tissue types, and advantages
    - Physical specifications including dimensions, weight, material composition, finish, and design
    - Operational characteristics with cutting/grasping force, actuation, precision level, and range
    - Safety features including locks, guards, quick-release mechanisms, and damage prevention
    - Pre-operative preparation with inspection, cleaning, sterilization, and quality assurance
    - Intraoperative use with positioning, handling technique, hand position, and coordination with other tools
    - Complications and risks including surgeon fatigue, common errors, tissue damage, and infections
    - Maintenance and care with post-operative cleaning, lubrication, inspection, and lifespan
    - Sterilization and disinfection with approved methods, incompatible procedures, and validation standards
    - Alternatives and comparisons with similar tools, advantages, disadvantages, and cost analysis
    - Historical context with invention history, evolution, clinical evidence, and current role in surgery
    - Specialty-specific considerations for general surgery, orthopedics, cardiac, neuro, and vascular
    - Training and certification requirements with proficiency indicators and mentoring best practices
    - Regulatory and standards compliance including FDA classification, ISO standards, and quality certifications
    - Cost and procurement information including single-use/reusable costs, vendors, and inventory recommendations
"""
import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.logging_config import setup_logger

from surgical_tool_info_models import SurgicalToolInfo

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the surgical tool info generator."""
    specialty: str = "Surgery/Surgical Instruments"

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "surgical_tool_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# SURGICAL TOOL INFO GENERATOR CLASS
# ============================================================================

class SurgicalToolInfoGenerator:
    """Generate comprehensive information for surgical tools."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.tool_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, tool_name: str, output_path: Optional[Path] = None) -> SurgicalToolInfo:
        if not tool_name or not tool_name.strip():
            raise ValueError("Tool name cannot be empty")

        self.tool_name = tool_name

        if output_path is None:
            output_path = self.config.output_dir / f"{tool_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting surgical tool information generation for: {tool_name}")

        tool_info = self._generate_info()

        self.save(tool_info, self.output_path)
        self.print_summary(tool_info)
        
        return tool_info

    def _generate_info(self) -> SurgicalToolInfo:
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of surgical procedures and clinical practice in {self.config.specialty}.

Generate comprehensive, evidence-based procedure information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between common/expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates)

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the surgical tool: {self.tool_name}",
            schema=SurgicalToolInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, tool_info: SurgicalToolInfo, output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(tool_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Surgical tool information saved to {output_path}")
        return output_path

    def print_summary(self, tool_info: SurgicalToolInfo) -> None:
        if self.config.verbosity < 3:
            return

        print("\n" + "="*70)
        print(f"SURGICAL TOOL INFORMATION SUMMARY: {tool_info.tool_basics.tool_name}")
        print("="*70)
        print(f"  - Category: {tool_info.tool_basics.tool_category}")
        print(f"  - Specialties: {tool_info.tool_basics.surgical_specialties}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_surgical_tool_info(tool_name: str, output_path: Optional[Path] = None, verbosity: int = 2) -> SurgicalToolInfo:
    """
    High-level function to generate and optionally save surgical tool information.

    Args:
        tool_name: Name of the surgical tool to generate information for.
        output_path: Optional path to save the output JSON file.
        quiet: If True, suppress console output (only save to file and logs).
    """
    config = Config(verbosity=verbosity)
    generator = SurgicalToolInfoGenerator(config=config)
    return generator.generate(tool_name, output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive surgical tool information.")
    parser.add_argument("-i", "--tool", nargs='+', help="Name of the surgical tool")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    try:
        tool_name = " ".join(args.tool)
        config = Config(quiet=not args.verbose)
        generator = SurgicalToolInfoGenerator(config=config)
        generator.generate(tool_name=tool_name, output_path=args.output)
        if args.verbose:
            print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
   main()
