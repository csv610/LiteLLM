"""
medical_test_info.py - Medical Test Information Generator

Generate comprehensive, evidence-based medical test documentation using structured
data models and the MedKit AI client with schema-aware prompting.

This module creates detailed information about medical tests and diagnostics for
clinicians and patient education.

For usage guide, see medical_test_info_guide.md
"""

import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

from medkit.utils.logging_config import setup_logger
from medkit.core.medkit_client import MedKitClient, MedKitConfig

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

from medical_test_info_models import MedicalTestInfo

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical test info generator."""
    enable_cache: bool = True
    verbosity: int = 2  # 0=CRITICAL, 1=ERROR, 2=WARNING (default), 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_test_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()

# ============================================================================
# MEDICAL TEST INFO GENERATOR CLASS
# ============================================================================ 

class MedicalTestInfoGenerator:
    """Generate comprehensive information for medical tests."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.test_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {
            0: "CRITICAL",
            1: "ERROR",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG"
        }
        log_level = verbosity_levels.get(self.config.verbosity, "WARNING")
        logger.setLevel(log_level)

    def build_user_prompt(self, test_name: str) -> str:
        """
        Build a comprehensive prompt for generating medical test information.

        Args:
            test_name: The name of the medical test.

        Returns:
            A formatted prompt string for the AI model.
        """
        prompt = f"""Generate comprehensive medical test information for: {test_name}

Include detailed information about:
1. Test name and alternative names
2. Purpose and clinical use
3. Test indications and when it is ordered
4. Sample requirements and collection procedures
5. Test methodology and technology
6. Normal reference ranges and result interpretation
7. Preparatory requirements and restrictions
8. Risks, benefits, and limitations
9. Cost and availability information
10. Results interpretation and follow-up actions

Provide accurate, evidence-based medical test information."""
        return prompt

    def generate_test_info(self, test_name: str) -> MedicalTestInfo:
        """
        Generate the core medical test information.

        Args:
            test_name: The name of the medical test.

        Returns:
            A MedicalTestInfo object with the generated data.
        """
        logger.info(f"Generating medical test information for: {test_name}")
        try:
            prompt = self.build_user_prompt(test_name)
            result = self.client.generate_text(prompt, schema=MedicalTestInfo)
            logger.info(f"Successfully generated medical test information for: {test_name}")
            return result
        except Exception as e:
            logger.error(f"Error generating medical test information for {test_name}: {e}")
            raise

    def generate(self, test_name: str, output_path: Optional[Path] = None) -> MedicalTestInfo:
        """
        Generate and save comprehensive medical test information.

        Args:
            test_name: Name of the medical test.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated MedicalTestInfo object.

        Raises:
            ValueError: If test_name is empty.
        """
        if not test_name or not test_name.strip():
            logger.error("Test name cannot be empty")
            raise ValueError("Test name cannot be empty")

        self.test_name = test_name

        if output_path is None:
            output_path = self.config.output_dir / f"{test_name.lower().replace(' ', '_')}_info.json"

        self.output_path = output_path

        logger.info(f"Starting medical test information generation for: {test_name}")

        try:
            test_info = self.generate_test_info(test_name)
            self.save(test_info, self.output_path)
            logger.info(f"Successfully generated all test information for: {test_name}")
            self.print_summary(test_info)
            return test_info
        except Exception as e:
            logger.error(f"Failed to generate test information for {test_name}: {e}")
            raise

    def save(self, test_info: MedicalTestInfo, output_path: Path) -> Path:
        """
        Save the generated test information to a JSON file.

        Args:
            test_info: The MedicalTestInfo object to save.
            output_path: The path to save the file to.

        Returns:
            The path to the saved file.
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(test_info.model_dump(), f, indent=2)
            logger.info(f"Saved test information to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error saving test information to {output_path}: {e}")
            raise

    def print_summary(self, test_info: MedicalTestInfo) -> None:
        """
        Print a summary of the generated test information.

        Args:
            test_info: The MedicalTestInfo object.
        """
        print("\n" + "="*70)
        print(f"MEDICAL TEST INFORMATION SUMMARY: {test_info.test_name}")
        print("="*70)
        print(f"  - Category: {test_info.test_category}")
        print(f"  - Specialty: {test_info.medical_specialty}")
        print(f"  - Purpose: {test_info.test_purpose.primary_purpose}")
        print(f"  - Sample Type: {test_info.specimen_information.sample_type}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_medical_test_info(test_name: str, output_path: Optional[Path] = None) -> MedicalTestInfo:
    """
    High-level function to generate and optionally save test information.
    """
    generator = MedicalTestInfoGenerator()
    return generator.generate(test_name, output_path)


def argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        A configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Generate comprehensive information for a medical test."
    )
    parser.add_argument(
        "-i",
        "--test",
        type=str,
        required=True,
        help="The name of the medical test to generate information for."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Optional: The path to save the output JSON file."
    )
    return parser


def cli():
    parser = argument_parser()
    args = parser.parse_args()

    generator = MedicalTestInfoGenerator()
    output_file_path = Path(args.output) if args.output else None

    generator.generate(test_name=args.test, output_path=output_file_path)

if __name__ == "__main__":
   cli()
