import argparse
import json
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from herbal_info_models import HerbalInfo

# Configure logging
logger = setup_logger(__name__)

# Logging will be configured based on verbosity level in __init__


try:
    from medkit.core.medkit_client import MedKitClient, MedKitConfig
except ImportError as e:
    raise ImportError("MedKitClient not found. Install medkit-client package.") from e

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the herbal info generator."""

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "herbal_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# HERBAL INFO GENERATOR CLASS
# ============================================================================ 

class HerbalInfoGenerator:
    """Generate comprehensive information for herbal remedies."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        level = verbosity_levels.get(self.config.verbosity, "WARNING")
        logger.setLevel(level)
        logging.getLogger().setLevel(level)
        logging.getLogger("medkit").setLevel(level)
        logging.getLogger("medkit.core.gemini_client").setLevel(level)

        # Load model name from ModuleConfig


        model_name = "gemini-1.5-flash"  # Default model for this module


        


        self.client = MedKitClient(model_name=model_name)
        self.herb_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, herb_name: str, output_path: Optional[Path] = None) -> HerbalInfo:
        """
        Generate and save comprehensive herbal information.

        Args:
            herb_name: Name of the herb.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated HerbalInfo object.
        
        Raises:
            ValueError: If herb_name is empty.
        """
        if not herb_name or not herb_name.strip():
            raise ValueError("Herb name cannot be empty")

        self.herb_name = herb_name

        if output_path is None:
            output_path = self.config.output_dir / f"{herb_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting herbal information generation for: {herb_name}")

        herbal_info = self._generate_info()

        self.save(herbal_info, self.output_path)
        self.print_summary(herbal_info)
        
        return herbal_info

    def _generate_info(self) -> HerbalInfo:
        """Generates the herbal information."""
        prompt = f"""Generate comprehensive herbal information for: {self.herb_name}

Include detailed information about:
1. Herb name (common and botanical names)
2. Plant family and active constituents
3. Traditional uses and classification
4. Mechanism of action and energetics
5. Forms and preparation methods
6. Dosage and usage guidelines
7. Safety, side effects, and contraindications
8. Interactions with medicines and foods
9. Special populations and precautions
10. Research evidence and efficacy
11. Cost and availability information

Provide accurate, evidence-based herbal remedy information."""

        result = self.client.generate_text(
            prompt,
            schema=HerbalInfo
        )
        return result

    def save(self, herbal_info: HerbalInfo, output_path: Path) -> Path:
        """
        Save the generated herbal information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(herbal_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Herbal information saved to {output_path}")
        return output_path

    def print_summary(self, herbal_info: HerbalInfo) -> None:
        """
        Print a summary of the generated herbal information.
        """
        if not self.config.verbose:
            return

        print("\n" + "="*70)
        print(f"HERBAL INFORMATION SUMMARY: {herbal_info.metadata.common_name}")
        print("="*70)
        print(f"  - Botanical Name: {herbal_info.metadata.botanical_name}")
        print(f"  - Plant Family: {herbal_info.metadata.plant_family}")
        print(f"  - Primary Uses: {herbal_info.classification.primary_uses}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_herbal_info(herb_name: str, output_path: Optional[Path] = None, verbose: bool = False) -> HerbalInfo:
    """
    High-level function to generate and optionally save herbal information.

    Args:
        herb_name: Name of the herb to generate information for.
        output_path: Optional path to save the output JSON file.
        verbose: If True, show console output and logging.
    """
    config = Config(verbose=verbose)
    generator = HerbalInfoGenerator(config)
    return generator.generate(herb_name, output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive information for an herbal remedy.")
    parser.add_argument("-i", "--herbal", type=str, required=True, help="The name of the herb to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output and logging.")

    args = parser.parse_args()

    print(f"Herbal:{args.herbal}")
    get_herbal_info(args.herbal, args.output, verbose=args.verbose)
    print(f"Successful: output stored in output/{args.output}")
   
if __name__ == "__main__":
   main()
