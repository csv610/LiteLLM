from typing import Optional
from pydantic import BaseModel, Field

from medkit.utils.logging_config import setup_logger
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .prescription_extractor import PrescriptionExtractor, PrescriptionData

logger = setup_logger(__name__, enable_file_handler=False)

class PrescriptionAnalysis(BaseModel):
    """Structured analysis for a medical prescription."""
    extracted_data: PrescriptionData = Field(description="Extracted prescription data")
    drug_interactions: str = Field(description="Potential drug-drug interactions and warnings")
    allergy_warnings: str = Field(description="Allergy warnings based on patient history (if available)")
    dosage_compliance: str = Field(description="Compliance with standard dosage guidelines for the medication")
    overall_assessment: str = Field(description="Overall safety and validity assessment of the prescription")

def analyze_prescription(image_path: str, config: Optional[ModelConfig] = None) -> PrescriptionAnalysis:
    """
    Analyzes a prescription from an image, performing extraction and clinical assessment.
    
    Args:
        image_path: Path to the prescription image file.
        config: Optional ModelConfig for the LiteClient.
        
    Returns:
        PrescriptionAnalysis: Complete assessment of the prescription.
    """
    logger.info(f"Analyzing prescription from image: {image_path}")
    
    if config is None:
        config = ModelConfig(model="gemini-1.5-flash", temperature=0.2)
        
    client = LiteClient(config)
    
    # Step 1: Extract data
    extractor = PrescriptionExtractor(config=config)
    extracted_data = extractor.extract(image_path)
    
    # Step 2: Analyze the extracted data
    logger.debug("Generating clinical analysis for the prescription...")
    
    medications_info = "\n".join([
        f"- Medication: {m.name}, Dosage: {m.dosage}, Frequency: {m.frequency}, Route: {m.route}, Duration: {m.duration}"
        for m in extracted_data.medications
    ])
    
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
        user_prompt=analysis_prompt,
        response_format=PrescriptionAnalysis
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
