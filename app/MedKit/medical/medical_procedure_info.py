"""medical_procedure_info - Generate comprehensive medical procedure documentation.

This module generates detailed, evidence-based information about medical procedures
(surgical and non-surgical). It provides complete procedure documentation including
indications, preparation, step-by-step process, recovery, outcomes, and financial
considerations using the MedKit AI client with structured Pydantic schemas.

QUICK START:
    Generate procedure information:

    >>> from medical_procedure_info import MedicalProcedureInfoGenerator
    >>> generator = MedicalProcedureInfoGenerator()
    >>> result = generator.generate("Knee Replacement")
    >>> print(result.metadata.procedure_name)
    Knee Replacement

    Or use the CLI:

    $ python medical_procedure_info.py -i "Knee Replacement"
    $ python medical_procedure_info.py -i "Colonoscopy" -o custom_output.json

COMMON USES:
    1. Patient education - helping patients understand what to expect
    2. Informed consent - providing comprehensive pre-procedure information
    3. Clinical reference - detailed procedure guidelines for healthcare teams
    4. Surgical planning - procedure details, techniques, and facility requirements
    5. Insurance and billing - cost information, billing codes, coverage details

KEY FEATURES AND COVERAGE AREAS:
    - Procedure identification: official names, alternatives, specialties
    - Purpose and indications: clinical reasons for procedure, what it treats
    - Contraindications: medical conditions that prevent procedure
    - Pre-operative phase: fasting, medication adjustments, pre-tests
    - Operative phase: step-by-step process, anesthesia type, duration
    - Discomfort and risks: expected sensations, side effects, complications
    - Recovery: immediate aftermath, timeline, activity restrictions
    - Outcomes and effectiveness: success rates, expected benefits, longevity
    - Follow-up care: appointments, monitoring, physical therapy, medications
    - Cost and insurance: pricing, coverage, financial assistance programs
    - Alternatives: other procedures, non-surgical options, comparative advantages
    - Technical details: surgical techniques, equipment, surgeon qualifications
    - Limitations: patient populations unsuitable, age and anatomical limitations
    - Patient education: plain language explanations, misconceptions, key takeaways
"""

import json
import sys
import argparse
import logging
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field
from typing import Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig

from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# Configure logging
logger = setup_logger(__name__)

# Suppress logger output by default (can be overridden via set_verbose)
logger.setLevel(logging.WARNING)

# ============================================================================ 
# CONFIGURATION
# ============================================================================ 

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical procedure info generator."""
    specialty: str = "Surgery/Procedure"

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_procedure_info.lmdb"
            )
        # Call parent validation
        super().__post_init__()
# ============================================================================ 
# PYDANTIC MODELS FOR PROCEDURE INFORMATION STRUCTURE
# ============================================================================ 

class ProcedurePurpose(BaseModel):
    primary_purpose: str = Field(description="Main reason this procedure is performed.")
    therapeutic_uses: str = Field(description="Specific conditions or diseases this procedure treats, comma-separated.")
    diagnostic_uses: str = Field(description="Diagnostic purposes of this procedure, comma-separated.")
    preventive_uses: str = Field(description="Preventive health applications of this procedure.")

class ProcedureIndications(BaseModel):
    when_recommended: str = Field(description="Clinical situations when this procedure is typically recommended, comma-separated.")
    symptoms_requiring_procedure: str = Field(description="Symptoms that lead doctors to recommend this procedure, comma-separated.")
    conditions_treated: str = Field(description="Medical conditions this procedure addresses, comma-separated.")
    contraindications: str = Field(description="Conditions that make this procedure unsafe or inappropriate, comma-separated.")

class PreparationRequirements(BaseModel):
    fasting_required: str = Field(description="Whether fasting is needed and for how long.")
    medication_adjustments: str = Field(description="Medications to stop or adjust before procedure, comma-separated.")
    dietary_restrictions: str = Field(description="Foods or drinks to avoid before procedure, comma-separated.")
    pre_procedure_tests: str = Field(description="Required tests or evaluations before procedure, comma-separated.")
    items_to_bring: str = Field(description="What to bring to the procedure appointment, comma-separated.")
    lifestyle_modifications: str = Field(description="Activities to avoid before procedure (smoking, alcohol, exercise), comma-separated.")

class ProcedureDetails(BaseModel):
    procedure_type: str = Field(description="Type of procedure (surgical, minimally invasive, endoscopic, etc).")
    anesthesia_type: str = Field(description="Type of anesthesia used (general, local, sedation, regional).")
    step_by_step_process: str = Field(description="Detailed steps of how the procedure is performed, numbered or comma-separated.")
    duration: str = Field(description="How long the procedure takes from start to finish.")
    location: str = Field(description="Where the procedure is typically performed (hospital, outpatient center, clinic).")
    equipment_used: str = Field(description="Medical equipment and instruments used, comma-separated.")
    hospital_stay: str = Field(description="Whether hospitalization is required and for how long.")

class DiscomfortAndRisks(BaseModel):
    discomfort_level: str = Field(description="Expected level of pain or discomfort during and after procedure.")
    common_sensations: str = Field(description="What patients typically feel during procedure, comma-separated.")
    common_side_effects: str = Field(description="Temporary side effects that are normal, comma-separated.")
    serious_risks: str = Field(description="Rare but serious complications to be aware of, comma-separated.")
    complication_rates: str = Field(description="Statistical rates of major complications.")
    mortality_risk: Optional[str] = Field(description="Risk of death from procedure if applicable.")

class RecoveryInformation(BaseModel):
    immediate_recovery: str = Field(description="What to expect immediately after procedure.")
    recovery_timeline: str = Field(description="Typical recovery milestones and duration.")
    pain_management: str = Field(description="How pain is managed during recovery, comma-separated.")
    activity_restrictions: str = Field(description="Physical limitations during recovery period, comma-separated.")
    return_to_work: str = Field(description="When patients can typically return to work.")
    return_to_normal_activities: str = Field(description="When patients can resume normal activities.")
    warning_signs: str = Field(description="Symptoms requiring immediate medical attention, comma-separated.")

class OutcomesAndEffectiveness(BaseModel):
    success_rate: str = Field(description="Percentage of successful outcomes.")
    expected_benefits: str = Field(description="What patients can expect to gain from procedure, comma-separated.")
    symptom_improvement: str = Field(description="How symptoms typically improve after procedure.")
    long_term_outcomes: str = Field(description="Long-term results and durability of procedure.")
    factors_affecting_outcomes: str = Field(description="Patient or clinical factors that influence success, comma-separated.")

class FollowUpCare(BaseModel):
    follow_up_schedule: str = Field(description="When and how often follow-up appointments are needed.")
    monitoring_required: str = Field(description="Tests or evaluations needed after procedure, comma-separated.")
    lifestyle_changes: str = Field(description="Permanent lifestyle modifications recommended, comma-separated.")
    medications_after: str = Field(description="Medications typically prescribed after procedure, comma-separated.")
    physical_therapy: str = Field(description="Whether physical therapy or rehabilitation is needed.")

class CostAndInsurance(BaseModel):
    typical_cost_range: str = Field(description="General cost range without insurance.")
    insurance_coverage: str = Field(description="How typically covered by insurance.")
    prior_authorization: str = Field(description="Whether insurance pre-approval is needed.")
    medicare_coverage: str = Field(description="Medicare coverage specifics.")
    medicaid_coverage: str = Field(description="Medicaid coverage information.")
    financial_assistance_programs: str = Field(description="Programs to help with costs, comma-separated.")
    cpt_codes: Optional[str] = Field(description="Current Procedural Terminology codes for billing.")

class Alternatives(BaseModel):
    alternative_procedures: str = Field(description="Other procedures that achieve similar goals, comma-separated.")
    non_surgical_alternatives: str = Field(description="Non-invasive treatment options, comma-separated.")
    advantages_over_alternatives: str = Field(description="Why this procedure may be preferred, comma-separated.")
    when_alternatives_preferred: str = Field(description="Clinical scenarios where other treatments are better, comma-separated.")

class TechnicalDetails(BaseModel):
    surgical_approach: str = Field(description="Surgical technique and approach used.")
    technology_used: str = Field(description="Advanced technology or robotics involved.")
    procedure_variations: str = Field(description="Different variations or modifications of the procedure, comma-separated.")
    surgeon_qualifications: str = Field(description="Required training and certifications for performing surgeon.")
    facility_requirements: str = Field(description="Hospital or facility requirements for performing procedure.")

class ProcedureLimitations(BaseModel):
    not_suitable_for: str = Field(description="Patient populations for whom procedure is not appropriate, comma-separated.")
    age_limitations: str = Field(description="Age-related considerations or restrictions.")
    medical_conditions_precluding: str = Field(description="Medical conditions that prevent procedure, comma-separated.")
    anatomical_limitations: str = Field(description="Anatomical factors that may limit procedure success, comma-separated.")

class ProcedureMetadata(BaseModel):
    """Basic information about the procedure."""
    procedure_name: str = Field(description="Official name of the procedure")
    alternative_names: str = Field(description="Other names for this procedure, comma-separated")
    procedure_category: str = Field(description="Category (surgical, minimally invasive, diagnostic, etc)")
    medical_specialty: str = Field(description="Primary medical specialties, comma-separated")


class ProcedureEducation(BaseModel):
    """Patient education and communication content."""
    plain_language_explanation: str = Field(description="Simple explanation for patients")
    key_takeaways: str = Field(description="3-5 most important points, comma-separated")
    common_misconceptions: str = Field(description="Common myths about this procedure, comma-separated")


class ProcedureEvidence(BaseModel):
    """Evidence-based information and clinical guidelines."""
    evidence_summary: str = Field(description="Summary of major guidelines and evidence quality")
    procedure_limitations: ProcedureLimitations


class ProcedureInfo(BaseModel):
    """
    Comprehensive medical procedure information.
    """
    # Core identification
    metadata: ProcedureMetadata

    # Clinical purpose and application
    purpose: ProcedurePurpose
    indications: ProcedureIndications

    # Pre-operative phase
    preparation: PreparationRequirements

    # Operative phase
    details: ProcedureDetails
    risks: DiscomfortAndRisks

    # Post-operative phase
    recovery: RecoveryInformation
    outcomes: OutcomesAndEffectiveness
    follow_up: FollowUpCare

    # Alternative treatment options
    alternatives: Alternatives

    # Advanced clinical information
    technical: TechnicalDetails
    evidence: ProcedureEvidence

    # Financial and insurance
    cost_and_insurance: CostAndInsurance

    # Patient communication
    education: ProcedureEducation

# ============================================================================ 
# MEDICAL PROCEDURE INFO GENERATOR CLASS
# ============================================================================ 

class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the generator with a configuration."""
        self.config = config or Config()
        # Load model name from ModuleConfig

        model_name = "gemini-1.5-flash"  # Default model for this module

        

        self.client = MedKitClient(model_name=model_name)
        self.procedure_name: Optional[str] = None
        self.output_path: Optional[Path] = None

        # Apply verbosity level to logger
        verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
        logger.setLevel(verbosity_levels.get(self.config.verbosity, "WARNING"))

    def generate(self, procedure_name: str, output_path: Optional[Path] = None) -> ProcedureInfo:
        """
        Generate and save comprehensive medical procedure information.

        Args:
            procedure_name: Name of the medical procedure.
            output_path: Optional path to save the JSON output.

        Returns:
            The generated ProcedureInfo object.
        
        Raises:
            ValueError: If procedure_name is empty.
        """
        if not procedure_name or not procedure_name.strip():
            raise ValueError("Procedure name cannot be empty")

        self.procedure_name = procedure_name

        if output_path is None:
            output_path = self.config.output_dir / f"{procedure_name.lower().replace(' ', '_')}_info.json"
        
        self.output_path = output_path

        logger.info(f"Starting medical procedure information generation for: {procedure_name}")

        procedure_info = self._generate_info()

        self.save(procedure_info, self.output_path)
        self.print_summary(procedure_info)
        
        return procedure_info

    def _generate_info(self) -> ProcedureInfo:
        """Generates the procedure information."""
        sys_prompt = f"""You are an expert medical documentation specialist with deep knowledge of surgical procedures and clinical practice in {self.config.specialty}.

Generate comprehensive, evidence-based procedure information ensuring all information is:
- Medically accurate and aligned with current guidelines
- Detailed enough for both patient education and clinical reference
- Supported by authoritative medical sources where applicable
- Clearly distinguished between common/expected outcomes and rare complications
- Includes statistical data when available (success rates, complication rates)

Return structured JSON matching the exact schema provided, with all required fields populated."""

        result = self.client.generate_text(
            prompt=f"Generate complete, evidence-based information for the medical procedure: {self.procedure_name}",
            schema=ProcedureInfo,
            sys_prompt=sys_prompt,
        )
        return result

    def save(self, procedure_info: ProcedureInfo, output_path: Path) -> Path:
        """
        Save the generated procedure information to a JSON file.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(procedure_info.model_dump(), f, indent=2)
        
        logger.info(f"✓ Procedure information saved to {output_path}")
        return output_path

    def print_summary(self, procedure_info: ProcedureInfo) -> None:
        """
        Print a summary of the generated procedure information.
        """
        if not self.config.verbose:
            return
        print("\n" + "="*70)
        print(f"PROCEDURE INFORMATION SUMMARY: {procedure_info.metadata.procedure_name}")
        print("="*70)
        print(f"  - Category: {procedure_info.metadata.procedure_category}")
        print(f"  - Specialty: {procedure_info.metadata.medical_specialty}")
        print(f"  - Purpose: {procedure_info.purpose.primary_purpose}")
        print(f"\n✓ Generation complete. Saved to {self.output_path}")

def get_procedure_info(procedure_name: str, output_path: Optional[Path] = None, verbose: bool = True) -> ProcedureInfo:
    """
    High-level function to generate and optionally save procedure information.
    """
    config = Config(verbose=verbose)
    generator = MedicalProcedureInfoGenerator(config=config)
    return generator.generate(procedure_name, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate comprehensive information for a medical procedure.")
    parser.add_argument("-i", "--procedure", type=str, required=True, help="The name of the medical procedure to generate information for.")
    parser.add_argument("-o", "--output", type=str, help="Optional: The path to save the output JSON file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show verbose console output.")

    args = parser.parse_args()
    get_procedure_info(args.procedure, args.output, args.verbose)


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
