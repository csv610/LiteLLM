"""medical_term_extractor - Extract and categorize medical concepts from text.

This module extracts and categorizes medical terms and concepts from unstructured clinical text
and medical documents. Identifies diseases, medicines, symptoms, treatments, procedures, anatomical
terms, side effects, and relationships between medical concepts. Uses the MedKit AI client with
structured Pydantic schemas for accurate, context-aware extraction with context preservation.

QUICK START:
    Extract medical terms from text:

    >>> from medical_term_extractor import MedicalTermExtractor
    >>> extractor = MedicalTermExtractor()
    >>> result = extractor.generate("Patient has diabetes and hypertension...")
    >>> print(f"Diseases: {len(result.diseases)}")
    Diseases: 2

    Extract from a file:

    >>> result = extractor.generate_from_file("medical_note.txt")

    Or use the CLI:

    $ python medical_term_extractor.py medical_text.txt
    $ python medical_term_extractor.py medical_text.txt -o output.json

COMMON USES:
    1. Medical record analysis - extracting structured data from clinical notes and unstructured text
    2. Text mining - identifying medical concepts for research, epidemiology, and classification
    3. NLP preprocessing - preparing text for downstream medical AI models and analysis pipelines
    4. Knowledge extraction - building databases of medical relationships and concept ontologies
    5. Clinical documentation review - ensuring comprehensive documentation and identifying missed concepts

KEY FEATURES AND COVERAGE AREAS:
    - Diseases and conditions - medical diagnoses, health conditions, and clinical presentations
    - Medicines and drugs - pharmaceutical names, trade names, and medication references
    - Symptoms and signs - patient-reported symptoms and clinical observations and findings
    - Treatments and therapies - therapeutic interventions, modalities, and clinical management
    - Procedures and tests - medical procedures, diagnostic tests, and clinical investigations
    - Medical specialties - healthcare disciplines, specialties, and clinical departments
    - Anatomical terms - body structures, anatomical references, and anatomical locations
    - Side effects and adverse reactions - medication side effects and adverse drug reactions
    - Causation relationships - connections between concepts (disease causes symptom, treatment leads to recovery)
    - Context preservation - sentence-level context and surrounding text for each extracted term
    - Relationship mapping - identifying clinical connections between extracted medical concepts
"""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List
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
    """Configuration for the medical term extractor."""

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_term_extractor.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR TERM EXTRACTION
# ============================================================================ 

class Disease(BaseModel):
    """Disease or medical condition."""
    name: str = Field(description="Name of the disease or condition")
    context: str = Field(description="Context where it was mentioned in the text")


class Medicine(BaseModel):
    """Medicine, drug, or pharmaceutical."""
    name: str = Field(description="Name of the medicine or drug")
    context: str = Field(description="Context where it was mentioned in the text")


class Symptom(BaseModel):
    """Symptom or clinical sign."""
    name: str = Field(description="Name of the symptom or sign")
    context: str = Field(description="Context where it was mentioned in the text")


class Treatment(BaseModel):
    """Treatment or therapeutic procedure."""
    name: str = Field(description="Name of the treatment or procedure")
    context: str = Field(description="Context where it was mentioned in the text")


class Procedure(BaseModel):
    """Medical procedure or test."""
    name: str = Field(description="Name of the procedure or test")
    context: str = Field(description="Context where it was mentioned in the text")


class Specialty(BaseModel):
    """Medical specialty or field."""
    name: str = Field(description="Name of the medical specialty")
    context: str = Field(description="Context where it was mentioned in the text")


class AnatomicalTerm(BaseModel):
    """Anatomical structure or body part."""
    name: str = Field(description="Name of the anatomical structure")
    context: str = Field(description="Context where it was mentioned in the text")


class SideEffect(BaseModel):
    """Side effect or adverse reaction."""
    name: str = Field(description="Name of the side effect")
    related_medicine: Optional[str] = Field(
        description="Medicine or treatment that may cause this side effect",
        default=None
    )
    context: str = Field(description="Context where it was mentioned in the text")


class CausationRelationship(BaseModel):
    """Causation relationship between medical concepts."""
    cause: str = Field(description="The cause (disease, condition, or factor)")
    effect: str = Field(description="The effect or consequence")
    relationship_type: str = Field(
        description="Type of relationship (causes, leads_to, triggers, results_in, etc.)"
    )
    context: str = Field(description="Context where this relationship was mentioned")


class MedicalTerms(BaseModel):
    """
    Comprehensive extraction of medical terms from text.
    """
    diseases: List[Disease] = Field(default_factory=list, description="Diseases and conditions found")
    medicines: List[Medicine] = Field(default_factory=list, description="Medicines and drugs found")
    symptoms: List[Symptom] = Field(default_factory=list, description="Symptoms and signs found")
    treatments: List[Treatment] = Field(default_factory=list, description="Treatments found")
    procedures: List[Procedure] = Field(default_factory=list, description="Procedures and tests found")
    specialties: List[Specialty] = Field(default_factory=list, description="Medical specialties found")
    anatomical_terms: List[AnatomicalTerm] = Field(default_factory=list, description="Anatomical structures found")
    side_effects: List[SideEffect] = Field(default_factory=list, description="Side effects and adverse reactions found")
    causation_relationships: List[CausationRelationship] = Field(
        default_factory=list,
        description="Causation relationships between medical concepts"
    )

# ============================================================================ 
# MEDICAL TERM EXTRACTOR CLASS
# ============================================================================ 

class MedicalTermExtractor:
    """Extracts and categorizes medical terms from text."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the extractor."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)

    def generate(self, text: str, output_path: Optional[Path] = None) -> MedicalTerms:
        """
        Extract medical terms from text.

        Args:
            text: The input text to extract medical terms from.
            output_path: Optional path to save the JSON output.

        Returns:
            The extracted medical terms.
        
        Raises:
            ValueError: If text is empty.
        """
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        logger.info("Starting medical term extraction")

        if output_path is None:
            output_path = self.config.output_dir / "extracted_medical_terms.json"

        extraction_prompt = f"""You are a medical term extraction expert. Extract all medical terms from the following text and structure them according to the provided schema.

Text to extract from:
{text}

For each category:
- Extract only relevant terms that appear in the text
- Include the context (the sentence or phrase where it appears)
- For side_effects, include the related_medicine if mentioned
- For causation_relationships, identify connections between medical concepts (e.g., "disease X causes symptom Y")

Be thorough and accurate. Extract ALL medical terms found in the text."""

        sys_prompt = """You are an expert medical documentation specialist. Your task is to extract medical terms accurately based on the provided text."""

        try:
            result = self.client.generate_text(
                prompt=extraction_prompt,
                schema=MedicalTerms,
                sys_prompt=sys_prompt,
            )
            self.save(result, output_path)
            self.print_summary(result)
            return result

        except Exception as e:
            logger.error(f"Error during medical term extraction: {str(e)}")
            raise

    def generate_from_file(self, file_path: Path, output_path: Optional[Path] = None) -> MedicalTerms:
        """
        Extract medical terms from a file.

        Args:
            file_path: Path to the input text file.
            output_path: Optional path to save JSON output.

        Returns:
            The extracted medical terms.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        if output_path is None:
            output_path = self.config.output_dir / f"{file_path.stem}_medical_terms.json"

        return self.generate(text, output_path=output_path)

    def save(self, terms: MedicalTerms, output_path: Path) -> Path:
        """
        Save the extracted terms to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(terms.model_dump(), f, indent=2)
        
        logger.info(f"✓ Medical terms extracted and saved to {output_path}")
        return output_path

    def print_summary(self, terms: MedicalTerms) -> None:
        """
        Print a summary of the extracted terms.
        """
        if self.config.verbosity < 3:
            return
        print("\n" + "="*70)
        print("MEDICAL TERM EXTRACTION SUMMARY")
        print("="*70)
        print(f"  - Diseases: {len(terms.diseases)}")
        print(f"  - Medicines: {len(terms.medicines)}")
        print(f"  - Symptoms: {len(terms.symptoms)}")
        print(f"  - Treatments: {len(terms.treatments)}")
        print(f"  - Procedures: {len(terms.procedures)}")
        print(f"  - Anatomical Terms: {len(terms.anatomical_terms)}")
        print(f"  - Side Effects: {len(terms.side_effects)}")
        print(f"  - Causation Relationships: {len(terms.causation_relationships)}")
        print("\n✓ Extraction complete.")

def extract_medical_terms(text: str, output_path: Optional[Path] = None, verbosity: int = 2) -> MedicalTerms:
    """
    High-level function to extract and optionally save medical terms from text.
    """
    config = Config(verbosity=verbosity)
    extractor = MedicalTermExtractor(config=config)
    return extractor.generate(text, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract medical terms from text or a file.")
    parser.add_argument("input", type=str, help="The input text file path or a string of text.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level (default: 2=WARNING)")

    args = parser.parse_args()

    config = Config(quiet=not args.verbose)
    extractor = MedicalTermExtractor(config=config)

    input_path = Path(args.input)
    output_file_path = Path(args.output) if args.output else None

    if input_path.is_file():
        extractor.generate_from_file(file_path=input_path, output_path=output_file_path)
    else:
        extractor.generate(text=args.input, output_path=output_file_path)

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
