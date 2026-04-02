import logging
from typing import Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pydantic import BaseModel, Field

try:
    from .prescription_extractor import PrescriptionData, PrescriptionExtractor
except ImportError:
    from prescription_extractor import PrescriptionData, PrescriptionExtractor

logger = logging.getLogger(__name__)


class PrescriptionAnalysis(BaseModel):
    """Structured analysis for a medical prescription."""

    extracted_data: PrescriptionData = Field(description="Extracted prescription data")
    drug_interactions: str = Field(
        description="Potential drug-drug interactions and warnings"
    )
    allergy_warnings: str = Field(
        description="Allergy warnings based on patient history (if available)"
    )
    dosage_compliance: str = Field(
        description="Compliance with standard dosage guidelines for the medication"
    )
    overall_assessment: str = Field(
        description="Overall safety and validity assessment of the prescription"
    )


def analyze_prescription(
    extracted_data: PrescriptionData, config: Optional[ModelConfig] = None
) -> PrescriptionAnalysis:
    """
    Acts as the Clinical Safety Auditor (JSON output).
    """
    logger.info("Starting clinical safety audit of prescription data...")

    if config is None:
        config = ModelConfig(model="gemini-1.5-flash", temperature=0.2)

    client = LiteClient(config)

    medications_info = "\n".join(
        [
            f"- Medication: {m.name}, Dosage: {m.dosage}, Frequency: {m.frequency}, Route: {m.route}, Duration: {m.duration}"
            for m in extracted_data.medications
        ]
    )

    analysis_prompt = (
        f"Audit the following prescription data for clinical safety and compliance:\n\n"
        f"Patient: {extracted_data.patient_name}\n"
        f"Medications:\n{medications_info}\n\n"
        "Output a structured JSON report identifying drug-drug interactions, "
        "dosage compliance, and any clinical red flags."
    )

    model_input = ModelInput(
        user_prompt=analysis_prompt, response_format=PrescriptionAnalysis
    )

    try:
        result = client.generate_text(model_input=model_input)
        analysis = result.data
        analysis.extracted_data = extracted_data
        logger.info("✓ Prescription safety audit completed")
        return analysis
    except Exception as e:
        logger.error(f"✗ Error during safety audit: {e}")
        raise

def synthesize_final_report(
    extracted_data: PrescriptionData, 
    audit_data: PrescriptionAnalysis,
    config: Optional[ModelConfig] = None
) -> str:
    """
    Acts as the Final Output synthesis agent (Markdown).
    """
    logger.info("Synthesizing final prescription safety report...")
    if config is None:
        config = ModelConfig(model="gemini-1.5-flash", temperature=0.3)
    
    client = LiteClient(config)
    
    system_prompt = (
        "You are the Lead Clinical Pharmacist. Your role is to take raw extracted "
        "prescription data and a clinical safety audit, then synthesize them into "
        "a FINAL, polished, and safe Markdown report for the patient. You MUST "
        "apply all fixes identified in the audit and ensure all safety warnings "
        "are prominent."
    )
    
    user_prompt = (
        f"Synthesize the final prescription safety report for: '{extracted_data.patient_name}'\n\n"
        f"EXTRACTED DATA:\n{extracted_data.model_dump_json(indent=2)}\n\n"
        f"SAFETY AUDIT:\n{audit_data.model_dump_json(indent=2)}\n\n"
        "Produce the final Markdown report. Ensure it is accurate, professional, "
        "and 100% compliant with safety standards."
    )
    
    model_input = ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=None
    )
    
    result = client.generate_text(model_input=model_input)
    return result.markdown
