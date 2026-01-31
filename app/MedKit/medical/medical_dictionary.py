"""Medical Dictionary Generator Module.

This module provides functionality for generating and managing medical
dictionary entries using the MedKit framework. It includes configuration
classes, data models, and generator classes for creating comprehensive
medical definitions.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


from pydantic import BaseModel, Field

from lite.utils import save_model_response
from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.logging_config import setup_logger


# Configure logging
logger = setup_logger(__name__)

# Configuration Classes

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


# Data Models

class MedicalTerm(BaseModel):
    """Schema for medical dictionary entries.

    Follows standard medical dictionary format with comprehensive fields
    for terms, definitions, explanations, and clinical information.
    """

    term: str = Field(..., description="Medical term name")
    alternative_name: Optional[str] = Field(
        None, description="Alternative name or common synonym"
    )
    definition: str = Field(
        ..., description="Concise definition (1-2 sentences, max 30 words)"
    )
    explanation: str = Field(
        ...,
        description="Detailed explanation of how it works, when used, and "
        "key details (2-3 sentences)",
    )
    contraindications: Optional[str] = Field(
        None,
        description="Important contraindications, precautions, or "
        "age restrictions if applicable",
    )
    category: str = Field(
        ...,
        description="Category: Disease, Anatomy, Procedure, Medication, "
        "Symptom, Sign, Treatment, Physiology, Clinical, Neurology",
    )


# Generator Classes

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

    def generate(
        self, term_query: str, output_path: Optional[Path] = None
    ) -> MedicalTerm:
        """Generate a medical dictionary entry and save it to a file.

        Args:
            term_query: The medical term to define.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalTerm object.

        Raises:
            ValueError: If term_query is empty or contains only whitespace.
        """
        if not term_query or not term_query.strip():
            raise ValueError("Term query cannot be empty")

        self.term_query = term_query

        if output_path is None:
            safe_name = term_query.lower().replace(" ", "_")
            output_path = (
                self.config.output_dir / f"{safe_name}_definition.json"
            )

        self.output_path = output_path

        logger.info(f"Generating medical dictionary entry for: {term_query}")
        print(f"Generating entry for '{term_query}'...")

        sys_prompt = (
            "You are an expert medical lexicographer. Provide accurate, "
            "evidence-based medical information aligned with current "
            "medical guidelines and best practices."
        )

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
        """Save the generated medical term to a JSON file.

        Args:
            medical_term: MedicalTerm object to save.
            output_path: Path where the JSON file should be saved.

        Returns:
            Path to the saved file.
        """
        return save_model_response(medical_term, output_path)

    def print_summary(self, medical_term: MedicalTerm) -> None:
        """Print a summary of the generated medical term.

        Args:
            medical_term: MedicalTerm object to summarize.
        """
        if self.config.verbosity < 3:
            return
        print("\n" + "=" * 70)
        print(f"MEDICAL DICTIONARY ENTRY SUMMARY: {medical_term.term}")
        print("=" * 70)
        print(f"  - Category: {medical_term.category}")
        print(f"  - Definition: {medical_term.definition}")
        if medical_term.alternative_name:
            print(f"  - Also Known As: {medical_term.alternative_name}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")



class MedicalDictionary:
    """Wrapper for MedicalDictionaryGenerator.

    Provides a simple query interface for accessing medical dictionary
    functionality.
    """

    def __init__(self, config: Optional[Config] = None):
        """Initialize the MedicalDictionary wrapper.

        Args:
            config: Optional Config object for customization.
        """
        self.generator = MedicalDictionaryGenerator(config)

    def query(
        self, term: str, output_path: Optional[Path] = None
    ) -> MedicalTerm:
        """Query the dictionary for a medical term.

        Args:
            term: The medical term to look up.
            output_path: Optional path to save the generated JSON file.

        Returns:
            A MedicalTerm object containing the definition and details.
        """
        return self.generator.generate(term, output_path)


def main() -> int:
    """Main entry point for medical dictionary generation.

    Returns:
        int: Exit code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Generate a medical dictionary entry."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The medical term to define.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Optional path to save the output JSON file.",
    )
    parser.add_argument(
        "-v",
        "--quiet",
        action="store_true",
        help="Verbosity level (default: 2=WARNING)",
    )

    args = parser.parse_args()

    generator = MedicalDictionaryGenerator()
    output_path = Path(args.output) if args.output else None
    generator.generate(term_query=args.input, output_path=output_path)
    return 0


if __name__ == "__main__":
    main()
