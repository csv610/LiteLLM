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
    Analyzes structured prescription data for clinical assessment.

    Args:
        extracted_data: Structured prescription data from the extraction agent.
        config: Optional ModelConfig for the LiteClient.

    Returns:
        PrescriptionAnalysis: Complete assessment of the prescription.
    """
    logger.info("Starting clinical analysis of prescription data...")

    if config is None:
        config = ModelConfig(model="gemini-1.5-flash", temperature=0.2)

    client = LiteClient(config)

    # Agent 2: Analyze the extracted data
    logger.debug("Generating clinical analysis for the prescription...")

    medications_info = "\n".join(
        [
            f"- Medication: {m.name}, Dosage: {m.dosage}, Frequency: {m.frequency}, Route: {m.route}, Duration: {m.duration}"
            for m in extracted_data.medications
        ]
    )

    analysis_prompt = (
        f"Analyze the following prescription data for clinical safety and validity:\n\n"
        f"Patient: {extracted_data.patient_name}\n"
        f"Prescriber: {extracted_data.prescriber}\n"
        f"Date: {extracted_data.date_prescribed}\n"
        f"Medications:\n{medications_info}\n\n"
        "Provide a detailed assessment including potential drug-drug interactions, "
        "dosage compliance for each medication, and an overall safety assessment."
    )

    model_input = ModelInput(
        user_prompt=analysis_prompt, response_format=PrescriptionAnalysis
    )

    try:
        result = client.generate_text(model_input=model_input)

        if result and result.data:
            # Override the extracted_data with our actual extracted_data for consistency
            analysis = result.data
            analysis.extracted_data = extracted_data
            logger.info("✓ Prescription analysis completed successfully")
            return analysis

        raise ValueError("Failed to generate structured prescription analysis.")

    except Exception as e:
        logger.error(f"✗ Error during prescription analysis: {e}")
        raise
