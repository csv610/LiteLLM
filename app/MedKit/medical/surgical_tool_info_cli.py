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
