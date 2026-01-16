import sys
import argparse
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import hashlib

from medkit.utils.logging_config import setup_logger
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from disease_info_models import (
    RiskFactors,
    DiagnosticCriteria,
    DiseaseIdentity,
    DiseaseBackground,
    DiseaseEpidemiology,
    DiseaseClinicalPresentation,
    DiseaseDiagnosis,
    DiseaseManagement,
    DiseaseResearch,
    DiseaseSpecialPopulations,
    DiseaseLivingWith,
    DiseaseInfo,
)

# Configure logging
logger = setup_logger(__name__)

try:
    from medkit.core.medkit_client import MedKitClient, MedKitConfig
except ImportError as e:
    raise ImportError("MedKitClient not found. Install medkit-client package.") from e

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(MedKitConfig):
    """Configuration for the disease info generator."""
    speciality: str = "Internal Medicine"
    incremental_generate: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "disease_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================
# DISEASE INFO GENERATOR
# ============================================================================

class DiseaseInfoGenerator:
    """
    Generates comprehensive disease information using the MedKit AI client with LMDB caching.
    """
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "ollama/gemma3:12b"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize LMDB storage for caching
        if self.config.db_store:
            try:
                lmdb_config = LMDBConfig(
                    db_path=self.config.db_path,
                    capacity_mb=self.config.db_capacity_mb,
                    enable_logging=True,
                    compression_threshold=100
                )
                self.storage = LMDBStorage(config=lmdb_config)
                logger.info(f"LMDB storage initialized at: {self.config.db_path}")
            except Exception as e:
                logger.error(f"Failed to initialize LMDB storage: {e}. Caching disabled.")
                self.storage = None
                self.config.db_store = False
        else:
            self.storage = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def _generate_cache_key(self, disease: str, section_name: str) -> str:
        """
        Generates a unique cache key for a disease section query.

        Args:
            disease: The name of the disease.
            section_name: The name of the section being generated.

        Returns:
            A unique cache key combining disease and section name.
        """
        key_content = f"{disease}:{section_name}".lower().strip()
        return hashlib.sha256(key_content.encode()).hexdigest()

    def _generate_section(self, disease: str, model: BaseModel, section_name: str):
        """
        Generates a single section of the disease information.
        Checks cache first to avoid redundant LLM calls (unless replace_existing is True).
        """
        cache_key = self._generate_cache_key(disease, section_name)

        # Check if result is already in cache (unless replace_existing is True)
        if self.config.db_store and self.storage and not self.config.replace_existing:
            cached_value = self.storage.get(cache_key)
            if cached_value:
                logger.info(f"Retrieved {section_name} for {disease} from cache.")
                try:
                    # Deserialize the cached JSON back to the model
                    cached_data = json.loads(cached_value)
                    section = model(**cached_data)
                    return section
                except Exception as e:
                    logger.warning(f"Failed to deserialize cached {section_name}: {e}. Regenerating...")
                    # Fall through to regenerate if deserialization fails

        logger.info(f"Generating {section_name} for {disease}...")
        try:
            section = self.client.generate_text(
                prompt=f"Generate the {section_name} for the disease: {disease}. "
                f"Focus on providing comprehensive, evidence-based information. "
                f"The target audience is medical professionals in {self.config.speciality}.",
                schema=model
            )
            logger.info(f"Successfully generated {section_name} for {disease}.")

            # Cache the result
            if self.config.db_store and self.storage and section:
                try:
                    cached_json = json.dumps(section.model_dump())
                    if self.config.replace_existing:
                        logger.debug(f"Replacing existing {section_name} for {disease} in cache.")
                    self.storage.put(cache_key, cached_json)
                    logger.debug(f"Cached {section_name} for {disease}.")
                except Exception as e:
                    logger.warning(f"Failed to cache {section_name} for {disease}: {e}")

            return section
        except Exception as e:
            logger.error(f"Error generating {section_name} for {disease}: {e}")
            return None

    def generate(self, disease: str, output_path: Optional[str] = None) -> Optional[DiseaseInfo]:
        """
        Generates comprehensive disease information.

        Args:
            disease: The name of the disease.
            output_path: Optional path to save the generated JSON file.

        Returns:
            A DiseaseInfo object or None if generation fails.
        """
        logger.info(f"Starting disease information generation for: {disease}")

        if self.config.incremental_generate:
            sections = {
                "identity": self._generate_section(disease, DiseaseIdentity, "Identity"),
                "background": self._generate_section(disease, DiseaseBackground, "Background"),
                "epidemiology": self._generate_section(disease, DiseaseEpidemiology, "Epidemiology"),
                "clinical_presentation": self._generate_section(disease, DiseaseClinicalPresentation, "Clinical Presentation"),
                "diagnosis": self._generate_section(disease, DiseaseDiagnosis, "Diagnosis"),
                "management": self._generate_section(disease, DiseaseManagement, "Management"),
                "research": self._generate_section(disease, DiseaseResearch, "Research"),
                "special_populations": self._generate_section(disease, DiseaseSpecialPopulations, "Special Populations"),
                "living_with": self._generate_section(disease, DiseaseLivingWith, "Living With"),
            }

            if any(value is None for value in sections.values()):
                logger.error(f"Failed to generate one or more sections for {disease}.")
                return None

            disease_info = DiseaseInfo(**sections)
        else:
            logger.info("Generating all sections in a single request...")
            disease_info = self._generate_section(disease, DiseaseInfo, "Comprehensive Disease Information")

        if not disease_info:
            logger.error(f"Failed to generate disease information for {disease}.")
            return None

        if output_path:
            self.save(disease_info, output_path)

        logger.info(f"Successfully generated all disease information for: {disease}")
        return disease_info

    def save(self, disease_info: DiseaseInfo, output_path: str):
        """
        Saves the disease information to a JSON file.
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(disease_info.model_dump(), f, indent=2)
        logger.info(f"Saved disease information to: {output_file}")

    def close(self):
        """
        Closes the LMDB storage and releases resources.
        Should be called when done using the generator.
        """
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

# ============================================================================
# CLI INTERFACE
# ============================================================================

def get_disease_info(disease: str, output_path: Optional[str] = None) -> Optional[DiseaseInfo]:
    """
    High-level function to generate and optionally save disease information.
    Uses context manager for proper resource cleanup.
    """
    with DiseaseInfoGenerator() as generator:
        return generator.generate(disease, output_path)

def main():
    """
    CLI entry point for generating disease information.
    """
    parser = argparse.ArgumentParser(description="Generate comprehensive disease information.")
    parser.add_argument("-i", "--disease", help="The name of the disease to generate information for.")
    parser.add_argument("-o", "--output", help="Path to save the output JSON file.")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching of results.")
    args = parser.parse_args()

    # Create custom config with caching option
    config = Config(db_store=not args.no_cache)

    with DiseaseInfoGenerator(config=config) as generator:
        generator.generate(args.disease, args.output)

if __name__ == "__main__":
    main()
