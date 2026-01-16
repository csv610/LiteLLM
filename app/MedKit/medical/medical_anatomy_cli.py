import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

from medical_anatomy_models import MedicalAnatomy

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical anatomy generator."""

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_anatomy.lmdb"
            )
        # Call parent validation
        super().__post_init__()

# ============================================================================
# MEDICAL ANATOMY GENERATOR CLASS
# ============================================================================

class MedicalAnatomyGenerator:
    """Generate comprehensive information for anatomical structures."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.structure_name: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, structure_name: str, output_path: Optional[Path] = None) -> MedicalAnatomy:
        """
        Generate and save comprehensive anatomical information.

        Args:
            structure_name: Name of the anatomical structure.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalAnatomy object.
        
        Raises:
            ValueError: If structure_name is empty.
        """
        if not structure_name or not structure_name.strip():
            raise ValueError("Structure name cannot be empty")

        self.structure_name = structure_name

        if output_path is None:
            output_path = self.config.output_dir / f"{structure_name.lower().replace(' ', '_')}_anatomy.json"
        
        self.output_path = output_path

        logger.info(f"Starting anatomical information generation for: {structure_name}")

        anatomy_info = self._generate_info()

        self.save(anatomy_info, self.output_path)
        self.print_summary(anatomy_info)
        
        return anatomy_info

    def _generate_info(self) -> MedicalAnatomy:
        """Generates the anatomical information."""
        prompt = f"""Generate comprehensive anatomical information for: {self.structure_name}

Include:
1. Anatomical overview and classification
2. Location and anatomical position
3. Gross morphology and structure
4. Microscopic/histological structure
5. Functions and roles
6. Vascular supply and innervation
7. Anatomical variations and anomalies
8. Developmental anatomy
9. Clinical significance and pathologies
10. Imaging characteristics
11. Surface anatomy and surgical approaches
12. Cross-references to related structures (see_also) - include adjacent structures, functionally related structures, structures with shared innervation, and structures in same system

For see_also cross-references, identify:
- Related anatomical structures that help readers understand anatomical relationships
- Types of connections (adjacent, continuous, functionally related, innervated by, supplied by, part of same system, etc.)
- Brief explanation of anatomical relationships

Provide accurate, detailed anatomical information based on standard anatomical references."""

        result = self.client.generate_text(
            prompt,
            schema=MedicalAnatomy
        )
        return result

    def save(self, anatomy_info: MedicalAnatomy, output_path: Path) -> Path:
        """
        Save the generated anatomical information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(anatomy_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Anatomical information saved to {output_path}")
        return output_path

    def print_summary(self, anatomy_info: MedicalAnatomy) -> None:
        """
        Print a summary of the generated anatomical information.
        """
        if self.config.verbosity < 3:
            return
        print("\n" + "="*70)
        print(f"ANATOMY INFORMATION SUMMARY: {anatomy_info.overview.structure_name}")
        print("="*70)
        print(f"  - Body System: {anatomy_info.overview.body_system}")
        print(f"  - Location: {anatomy_info.anatomical_position.anatomical_location}")
        print(f"  - Classification: {anatomy_info.overview.anatomical_classification}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_anatomy_info(structure_name: str, output_path: Optional[Path] = None, verbosity: int = 2) -> MedicalAnatomy:
    """
    High-level function to generate and optionally save anatomy information.
    """
    config = Config(verbosity=verbosity)
    generator = MedicalAnatomyGenerator(config=config)
    return generator.generate(structure_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for an anatomical structure.")
    parser.add_argument("-i", "--anatomy", type=str, required=True, help="The name of the anatomical structure to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG")

    args = parser.parse_args()

    get_anatomy_info(args.anatomy, args.output, args.verbosity)


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
