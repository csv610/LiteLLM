"""
medical_speciality.py - Medical Specialists Database and Lookup

This module provides data models and utilities for organizing and querying medical specialties,
including specialty categories, individual specialists, and their subspecialties.

QUICK START:
    from medical_speciality import MedicalSpecialityGenerator
    generator = MedicalSpecialityGenerator()
    db = generator.generate()
    
    # Query specialists by category
    cardiology_specialists = db.get_by_category("Cardiovascular")

    # Find specialists for a condition
    heart_specialists = db.search_by_condition("heart disease")

COMMON USES:
    1. Find appropriate specialists for patient referrals
    2. Understand medical specialty categories and organization
    3. Look up what conditions specialists treat
    4. Generate comprehensive medical specialty database using AI

GENERATE DATABASE:
    python medical_speciality.py -o output_path.json
"""

import json
import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import List, Optional

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
    """Configuration for the medical speciality generator."""
    default_output_filename: str = "medical_specialists.json"
    verbose: bool = False

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_speciality.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR SPECIALITY STRUCTURE
# ============================================================================ 

class SpecialtyCategory(BaseModel):
    """
    Medical specialty category for organizing related specialties.
    """
    name: str = Field(..., description="Name of the category (e.g., 'Cardiovascular', 'Neurological', 'Digestive')")
    description: str = Field(..., description="Brief description of what this category encompasses")


class Subspecialty(BaseModel):
    """
    Subspecialty within a medical specialty field.
    """
    name: str = Field(..., description="Name of the subspecialty")
    description: str = Field(..., description="Brief description of what the subspecialty focuses on")


class MedicalSpecialist(BaseModel):
    """
    Complete information about a medical specialist and their field.
    """
    specialty_name: str = Field(..., description="Official name of the medical specialty")
    category: SpecialtyCategory = Field(..., description="Category this specialty belongs to")
    description: str = Field(..., description="Detailed description of what this specialist does")
    treats: List[str] = Field(..., description="List of conditions, diseases, or body systems treated")
    common_referral_reasons: List[str] = Field(..., description="Common reasons patients see this specialist")
    subspecialties: Optional[List[Subspecialty]] = Field(default=None, description="Subspecialties within this field")
    is_surgical: bool = Field(default=False, description="Whether this is primarily a surgical specialty")
    patient_population: Optional[str] = Field(default=None, description="Specific patient population if applicable (e.g., 'children', 'elderly', 'women')")


class MedicalSpecialistDatabase(BaseModel):
    """
    Complete database of medical specialists with query methods.
    """
    specialists: List[MedicalSpecialist] = Field(
        ...,
        description="Comprehensive list of all medical specialists including primary care, surgical, diagnostic, and subspecialty fields"
    )

    def get_by_category(self, category_name: str) -> List[MedicalSpecialist]:
        """
        Get all specialists in a specific category.
        """
        return [s for s in self.specialists if s.category.name.lower() == category_name.lower()]

    def get_all_categories(self) -> List[SpecialtyCategory]:
        """
        Get all unique specialty categories in the database.
        """
        seen = {}
        for s in self.specialists:
            if s.category.name not in seen:
                seen[s.category.name] = s.category
        return list(seen.values())

    def get_surgical_specialists(self) -> List[MedicalSpecialist]:
        """
        Get all surgical specialists in the database.
        """
        return [s for s in self.specialists if s.is_surgical]

    def search_by_condition(self, condition: str) -> List[MedicalSpecialist]:
        """
        Search for specialists who treat a specific condition.
        """
        condition_lower = condition.lower()
        return [s for s in self.specialists
                if any(condition_lower in treat.lower() for treat in s.treats)]

# ============================================================================ 
# MEDICAL SPECIALITY GENERATOR CLASS
# ============================================================================ 

class MedicalSpecialityGenerator:
    """Generate a comprehensive database of medical specialities."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.output_path: Optional[Path] = None

    def generate(self, output_path: Optional[Path] = None) -> MedicalSpecialistDatabase:
        """
        Generate and save a comprehensive medical specialists database.

        Args:
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalSpecialistDatabase object.
        """
        if output_path is None:
            output_path = self.config.output_dir / self.config.default_output_filename
        
        self.output_path = output_path

        logger.info("Generating medical specialist database using MedKit client.")
        
        prompt = '''
Generate a comprehensive list of medical specialists covering all major fields of medicine.

First, identify logical categories to organize the specialists (such as by body system, type of care, patient population, etc.).

Then for each category, list all relevant medical specialists including:
- Primary care specialties
- Surgical specialties
- Medical (non-surgical) specialties
- Diagnostic specialties
- Subspecialties

For each specialist, provide:
1. The formal specialty name
2. The category it belongs to (with category name and description)
3. Clear description of their role
4. Comprehensive list of conditions/diseases they treat
5. Common reasons patients are referred to them
6. Any important subspecialties within that field
7. Whether it's primarily a surgical specialty
8. Any specific patient population focus (if applicable)

Be thorough and include both common specialties (like cardiology, dermatology) and less well-known ones (like physiatry, interventional radiology).
'''
        
        database = self.client.generate_text(
            prompt=prompt,
            schema=MedicalSpecialistDatabase
        )

        self.save(database, self.output_path)
        self.print_summary(database)
        
        return database

    def save(self, database: MedicalSpecialistDatabase, output_path: Path) -> Path:
        """
        Save the database to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(database.model_dump(), f, indent=2)
        
        logger.info(f"✓ Medical specialist database saved to {output_path}")
        return output_path

    def print_summary(self, database: MedicalSpecialistDatabase) -> None:
        """
        Print a summary of the generated database.
        """
        if not self.config.verbose:
            return
        print("\n" + "="*70)
        print("MEDICAL SPECIALIST DATABASE SUMMARY")
        print("="*70)
        print(f"  - Total Specialists: {len(database.specialists)}")
        print(f"  - Categories: {len(database.get_all_categories())}")
        print(f"  - Surgical Specialties: {len(database.get_surgical_specialists())}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def generate_specialist_database(output_path: Optional[Path] = None, verbose: bool = False) -> MedicalSpecialistDatabase:
    """
    High-level function to generate and optionally save the medical specialist database.
    """
    config = Config(verboset=verbose)
    generator = MedicalSpecialityGenerator(config=config)
    return generator.generate(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical specialist database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate database and save to outputs/medical_specialists.json
  python medical_speciality.py

  # Custom output path
  python medical_speciality.py -o custom_specialists.json
        """
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path to save JSON output."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose console output."
    )

    args = parser.parse_args()

    try:
        config = Config(verbose=args.verbose)
        generator = MedicalSpecialityGenerator(config=config)
        output_file_path = Path(args.output) if args.output else None
        generator.generate(output_path=output_file_path)
        if args.verbose:
            print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
   main()
