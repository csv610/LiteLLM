import json
import sys
import uuid
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

from synthetic_case_report_models import (
    PatientInformation,
    ClinicalFindings,
    Timeline,
    DiagnosticAssessment,
    TherapeuticInterventions,
    FollowUpAndOutcomes,
    Discussion,
    PatientPerspective,
    InformedConsent,
    CaseReportMetadata,
    SyntheticCaseReport,
)

# Configure logging
logger = setup_logger(__name__)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the synthetic case report generator."""
    specialty: str = "Medicine/Advanced Clinical Case"

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "synthetic_case_report.lmdb"
            )
        # Call parent validation
        super().__post_init__()

# ============================================================================ 
# SYNTHETIC CASE REPORT GENERATOR CLASS
# ============================================================================ 

class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-pro"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, disease_condition: str, output_path: Optional[Path] = None) -> SyntheticCaseReport:
        logger.info(f"Starting case report generation for: {disease_condition}")

        if not disease_condition or not disease_condition.strip():
            logger.error("Disease condition cannot be empty")
            raise ValueError("Disease condition cannot be empty")

        if output_path is None:
            condition_name = disease_condition.replace(" ", "_").lower()
            output_path = self.config.output_dir / f"{condition_name}_casereport.json"
            logger.debug(f"Generated output path: {output_path}")

        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory ensured: {self.config.output_dir}")

        generation_prompt = (
            f"Create a realistic synthetic medical case report for a patient with {disease_condition}. "
            f"CRITICAL INSTRUCTION: Do NOT explicitly mention the disease or condition name anywhere in the report. "
            f"DO NOT state the diagnosis. Present only the clinical findings, symptoms, test results, and observations. "
            f"The report should be detailed enough that a specialized physician can independently determine the diagnosis "
            f"based solely on the presented clinical data. Include realistic and medically accurate findings consistent with "
            f"this condition, but never explicitly name it in any field."
        )
        logger.debug("Generation prompt prepared")

        try:
            logger.info(f"Generating case report using MedKit client for specialty: {self.config.specialty}")
            result = self.client.generate_text(
                prompt=generation_prompt,
                schema=SyntheticCaseReport,
            )
            logger.info(f"Successfully generated case report for: {disease_condition}")

            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w") as f:
                    json.dump(result.model_dump(), f, indent=2)
                logger.info(f"Saved case report to: {output_path}")

            self.print_summary(result)
            return result
        except Exception as e:
            logger.error(f"Error generating case report for {disease_condition}: {e}")
            raise

    def generate_multiple(self, disease_condition: str, num_cases: int = 1, output_dir: Optional[Path] = None) -> List[SyntheticCaseReport]:
        logger.info(f"Starting generation of {num_cases} case reports for: {disease_condition}")

        if num_cases < 1:
            logger.error("Number of cases must be at least 1")
            raise ValueError("Number of cases must be at least 1")

        if output_dir is None:
            output_dir = self.config.output_dir
            logger.debug(f"Using default output directory: {output_dir}")

        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory ensured: {output_dir}")

        results = []
        for i in range(num_cases):
            condition_name = disease_condition.replace(" ", "_").lower()
            case_filename = f"{condition_name}_casereport.json"
            output_path = output_dir / case_filename
            logger.debug(f"Generating case {i+1}/{num_cases}: {output_path}")

            try:
                case_report = self.generate(disease_condition=disease_condition, output_path=output_path)
                results.append(case_report)
                logger.info(f"Successfully generated case {i+1}/{num_cases}")
                print(f"✓ Generated case {i+1}/{num_cases}")
            except Exception as e:
                logger.error(f"Error generating case {i+1}/{num_cases}: {e}")
                print(f"✗ Error generating case {i+1}: {e}")
                raise

        logger.info(f"Successfully generated all {num_cases} case reports for: {disease_condition}")
        return results

    def print_summary(self, case_report: SyntheticCaseReport):
        print("\n" + "="*70)
        print(f"SYNTHETIC CASE REPORT SUMMARY: {case_report.metadata.case_report_title}")
        print("="*70)
        print(f"  - Specialty: {case_report.metadata.medical_specialty}")
        print(f"  - Patient: {case_report.patient_information.age}-year-old {case_report.patient_information.gender}")
        print(f"  - Chief Complaint: {case_report.clinical_findings.chief_complaint}")
        print(f"\n✓ Generation complete.")

# ============================================================================
# CLI INTERFACE
# ============================================================================

def get_case_report(disease_condition: str, output_path: Optional[str] = None, verbose: bool = False) -> Optional[SyntheticCaseReport]:
    """
    High-level function to generate and optionally save a synthetic case report.
    """
    config = Config(verbose=verbose)
    generator = SyntheticCaseReportGenerator(config=config)
    return generator.generate(disease_condition, output_path=Path(output_path) if output_path else None)

def main():
    """
    CLI entry point for generating synthetic case reports.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic medical case reports.")
    parser.add_argument("-i", "--condition", nargs="?", help="Name of the disease or medical condition")
    parser.add_argument("-n", "--num-cases", type=int, default=1, help="Number of case reports to generate.")
    parser.add_argument("-o", "--output", type=Path, help="Output directory for case reports.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging output.")

    args = parser.parse_args()

    if not args.condition:
        parser.print_help()
        logger.error("Disease condition is required")
        sys.exit(1)

    try:
        config = Config(verbose=args.verbose)
        generator = SyntheticCaseReportGenerator(config=config)
        logger.info(f"CLI invoked with condition: {args.condition}, num_cases: {args.num_cases}")

        output_dir = args.output if args.output else None
        generator.generate_multiple(disease_condition=args.condition, num_cases=args.num_cases, output_dir=output_dir)
        logger.info(f"Successfully generated {args.num_cases} case reports for: {args.condition}")
        print(f"✓ Successfully generated {args.num_cases} case reports!")

    except Exception as e:
        logger.critical(f"Fatal error in CLI: {e}")
        print(f"✗ Failed to generate case reports: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
