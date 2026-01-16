"""Medical Dictionary - AI-generated medical term definitions and explanations.

Generates comprehensive medical dictionary entries for any medical term including definitions,
detailed explanations, contraindications, and clinical categorization using structured LLM outputs.

QUICK START:
    from medical_dictionary import MedicalDictionaryGenerator
    dictionary = MedicalDictionaryGenerator()
    entry = dictionary.generate("Hypertension")
    print(entry.definition)

COMMON USES:
    - Generate medical definitions for healthcare professionals and patients
    - Create structured medical glossaries and reference materials
    - Support patient education with accurate medical terminology
    - Build knowledge bases with categorized medical terms
    - Provide contraindications and clinical context for conditions

KEY CONCEPTS:
    - MedicalTerm schema defines structured entry format (term, definition, explanation)
    - Categories: Disease, Anatomy, Procedure, Medication, Symptom, Sign, Treatment, Physiology, Clinical, Neurology
    - Uses MedKitClient for LLM-powered generation with medical expert prompting
    - Supports batch queries and interactive CLI mode for term lookups
"""

import argparse
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, Field

from medkit.core.medkit_client import MedKitClient, MedKitConfig

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# Configure logging
logger = setup_logger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical dictionary generator."""

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_dictionary.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODEL FOR DICTIONARY ENTRY
# ============================================================================ 

class MedicalTerm(BaseModel):
    """Schema for medical dictionary entries following standard medical dictionary format."""
    term: str = Field(..., description="Medical term name")
    alternative_name: Optional[str] = Field(None, description="Alternative name or common synonym in parentheses")
    definition: str = Field(..., description="Concise definition (1-2 sentences, max 30 words)")
    explanation: str = Field(..., description="Detailed explanation of how it works, when used, and key details (2-3 sentences)")
    contraindications: Optional[str] = Field(None, description="Important contraindications, precautions, or age restrictions if applicable")
    category: str = Field(..., description="Category: Disease, Anatomy, Procedure, Medication, Symptom, Sign, Treatment, Physiology, Clinical, Neurology")

# ============================================================================ 
# MEDICAL DICTIONARY GENERATOR CLASS
# ============================================================================ 

class MedicalDictionaryGenerator:
    """Medical dictionary using MedKitClient for generation."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize Medical Dictionary.

        Args:
            config: Optional Config dataclass. If not provided, creates default.
        """
        self.config = config or Config()
        self.medkit_client = MedKitClient()
        self.term_query: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate(self, term_query: str, output_path: Optional[Path] = None) -> MedicalTerm:
        """
        Generate a medical dictionary entry and save it to a file.

        Args:
            term_query: The medical term to define.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalTerm object.
        """
        if not term_query or not term_query.strip():
            raise ValueError("Term query cannot be empty")

        self.term_query = term_query
        
        if output_path is None:
            output_path = self.config.output_dir / f"{term_query.lower().replace(' ', '_')}_definition.json"
        
        self.output_path = output_path

        logger.info(f"Generating medical dictionary entry for: {term_query}")
        print(f"Generating entry for '{term_query}'...")

        sys_prompt = """You are an expert medical lexicographer. Provide accurate, evidence-based medical information aligned with current medical guidelines and best practices."""

        medical_term = self.medkit_client.generate_text(
            prompt=f"Generate a medical dictionary entry for: {term_query}",
            schema=MedicalTerm,
            sys_prompt=sys_prompt,
        )

        logger.info(f"✓ Medical dictionary entry generated for: {term_query}")
        
        self.save(medical_term, self.output_path)
        self.print_summary(medical_term)
        
        return medical_term

    def save(self, medical_term: MedicalTerm, output_path: Path) -> Path:
        """
        Save the generated medical term to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(medical_term.model_dump(), f, indent=2)
        
        logger.info(f"✓ Medical term saved to {output_path}")
        return output_path

    def print_summary(self, medical_term: MedicalTerm) -> None:
        """
        Print a summary of the generated medical term.
        """
        if self.config.verbosity < 3:
            return
        print("\n" + "="*70)
        print(f"MEDICAL DICTIONARY ENTRY SUMMARY: {medical_term.term}")
        print("="*70)
        print(f"  - Category: {medical_term.category}")
        print(f"  - Definition: {medical_term.definition}")
        if medical_term.alternative_name:
            print(f"  - Also Known As: {medical_term.alternative_name}")
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

class MedicalDictionary:
    """
    A wrapper for the MedicalDictionaryGenerator to provide a simple query interface.
    """
    def __init__(self, config: Optional[Config] = None):
        self.generator = MedicalDictionaryGenerator(config)

    def query(self, term: str, output_path: Optional[Path] = None) -> MedicalTerm:
        """
        Queries the dictionary for a medical term.

        Args:
            term: The medical term to look up.
            output_path: Optional path to save the generated JSON file.

        Returns:
            A MedicalTerm object.
        """
        return self.generator.generate(term, output_path)


def main():
    parser = argparse.ArgumentParser(description="Generate a medical dictionary entry.")
    parser.add_argument("-i", "--input", type=str, required=True, help="The medical term to define.")
    parser.add_argument("-o", "--output", ype=str, default=None, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--quiet", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    generator = MedicalDictionaryGenerator()
    generator.generate(term_query=args.input, output_path=output_file_path)

if __name__ == "__main__":
   main()
