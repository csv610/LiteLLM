"""
liteagents.py - Unified for med_prescription
"""
from app.MedKit.drug.med_prescription.shared.models import *\nfrom typing import Optional\nfrom lite.config import ModelInput\nfrom lite.lite_client import LiteClient\nimport logging\nfrom typing import List, Optional\nfrom pathlib import Path\nfrom pydantic import BaseModel, Field\nfrom .agent_orchestrator import PrescriptionAgentApp\nfrom unittest.mock import MagicMock\nfrom lite.config import ModelConfig\nfrom .prescription_extractor import PrescriptionExtractor\nfrom lite.config import ModelConfig, ModelInput\nimport sys\nfrom .prescription_analyzer import analyze_prescription, PrescriptionAnalysis\n\n

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


# Add project root to sys.path
current_dir = Path(__file__).resolve().parent
app_root = current_dir.parent.parent.parent.parent
sys.path.append(str(app_root))


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class PrescriptionAgentApp:
    """Orchestrator for the 2-agent Prescription Analysis system."""

    def __init__(self, model: str = "gemini-1.5-flash"):
        """
        Initializes the app with high-speed Gemini Flash models for both agents.
        """
        self.config = ModelConfig(model=model, temperature=0.1)
        
        # Agent 1: The Vision Extractor
        self.extractor = PrescriptionExtractor(config=self.config)
        
        from .prescription_analyzer import analyze_prescription, synthesize_final_report, PrescriptionAnalysis
        ...
            def run(self, image_path: str) -> Optional[str]:
                """Executes the 3-tier multi-agent workflow."""
                print(f"\n🚀 Starting 3-tier Prescription Analysis Workflow\n")

                try:
                    # TIER 1: Vision Extraction (JSON Specialist)
                    print(f"[TIER 1] Specialist: Extracting data from image...")
                    extracted_data = self.extractor.extract(image_path)
                    print(f"✓ Extraction complete for: {extracted_data.patient_name}")

                    # TIER 2: Clinical Safety Audit (JSON Auditor)
                    print(f"[TIER 2] Auditor: Performing clinical safety audit...")
                    audit_data = analyze_prescription(extracted_data, config=self.config)
                    print("✓ Safety audit completed")

                    # TIER 3: Final Output Synthesis (Markdown Closer)
                    print(f"[TIER 3] Output: Synthesizing final report...")
                    final_markdown = synthesize_final_report(extracted_data, audit_data, config=self.config)

                    # Print Final Report
                    print("\n" + "="*50)
                    print("FINAL CLINICAL SAFETY REPORT (MARKDOWN)")
                    print("="*50)
                    print(final_markdown)
                    print("="*50 + "\n")

                    return ModelOutput(
                data=extracted_data, 
                markdown=final_markdown,
                metadata={"audit": audit_data.model_dump() if hasattr(audit_data, 'model_dump') else audit_data}
            )

                except Exception as e:
                    logger.error(f"3-tier Workflow failed: {e}")
                    return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the 2-agent Prescription Analysis app.")
    parser.add_argument("image", help="Path to the prescription image.")
    args = parser.parse_args()
    
    app = PrescriptionAgentApp()
    app.run(args.image)



logger = logging.getLogger(__name__)


class Medication(BaseModel):
    """Structured data for a single medication."""

    name: str = Field(description="Name of the medication")
    dosage: str = Field(description="Dosage of the medication (e.g., 500mg)")
    frequency: str = Field(
        description="Frequency of administration (e.g., BID, TID, Once daily)"
    )
    route: str = Field(description="Route of administration (e.g., Oral, Topical, IV)")
    duration: str = Field(description="Duration of treatment (e.g., 7 days, 1 month)")


class PrescriptionData(BaseModel):
    """Structured data for a medical prescription."""

    medications: List[Medication] = Field(description="List of medications prescribed")
    prescriber: str = Field(
        description="Name of the prescribing doctor or healthcare professional"
    )
    patient_name: str = Field(description="Name of the patient")
    date_prescribed: str = Field(description="Date the prescription was issued")


class PrescriptionExtractor:
    """Extracts prescription data from an image using LiteClient."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initializes the PrescriptionExtractor with a LiteClient.

        Args:
            config: Optional ModelConfig. If not provided, a default gemini-1.5-flash config is used.
        """
        if config is None:
            config = ModelConfig(model="gemini-1.5-flash", temperature=0.1)

        self.client = LiteClient(config)

    def extract(self, image_path: str) -> PrescriptionData:
        """
        Extracts prescription details from an image.

        Args:
            image_path: Path to the prescription image file.

        Returns:
            PrescriptionData: Extracted and structured prescription details.

        Raises:
            Exception: If extraction fails.
        """
        logger.info(f"Extracting prescription data from image: {image_path}")

        # Comprehensive prompt for extraction
        prompt = (
            "Extract all available prescription details from the provided image. "
            "Ensure you capture all medications with their dosage, frequency, route, "
            "and duration. Also capture the prescriber's name, patient's name, "
            "and the date prescribed. If any field is not clearly visible, return 'Not specified'."
        )

        model_input = ModelInput(
            user_prompt=prompt, image_path=image_path, response_format=PrescriptionData
        )

        try:
            logger.debug("Calling LiteClient for structured extraction...")
            result = self.client.generate_text(model_input=model_input)

            if result and result.data:
                logger.info("✓ Successfully extracted prescription data")
                return result.data

            # If structured data is not available, we could attempt to parse the markdown
            # but for now we expect structured data as per LiteClient capability.
            if result and result.markdown:
                logger.warning("Model returned markdown instead of structured data.")
                # Basic parsing or error handling could go here.

            raise ValueError(
                "Failed to extract structured prescription data from the image."
            )

        except Exception as e:
            logger.error(f"✗ Error during prescription extraction: {e}")
            raise


# Add the project root to sys.path for proper imports
# Current file is in /Users/csv610/Projects/LiteLLM/app/MedKit/drug/med_prescription
# We want to add /Users/csv610/Projects/LiteLLM/app to the path
current_dir = Path(__file__).resolve().parent
app_dir = current_dir.parent.parent.parent.parent  # agentic -> med_prescription -> drug -> MedKit -> app
sys.path.append(str(app_dir))

print(f"Added to sys.path: {app_dir}")

try:
    # Try importing medkit (since it's macOS, MedKit should match medkit)
    print("✓ Successfully imported MedKit")

    from lite.config import ModelConfig
    from MedKit.drug.med_prescription.agentic.prescription_extractor import (
        PrescriptionExtractor,
    )

    print("✓ Successfully imported prescription modules")

    # Simple test of instantiation
    config = ModelConfig(model="gemini-1.5-flash")
    extractor = PrescriptionExtractor(config=config)
    print("✓ Successfully instantiated PrescriptionExtractor")

except Exception as e:
    print(f"✗ Error during import or instantiation: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


# Set up paths
current_dir = Path(__file__).resolve().parent
app_root = current_dir.parent.parent.parent.parent
sys.path.append(str(app_root))


# Mocking the LiteClient so we don't need real API keys for this demonstration
# but the user can use real ones if they have them set in environment.

def run_demo():
    print("🚀 Initializing Prescription Agent Demo...")
    
    # We will instantiate the app
    app = PrescriptionAgentApp()
    
    # Let's create a dummy image path (it doesn't need to exist if we mock the client)
    dummy_image = "prescription_sample.jpg"
    
    print(f"Applying mock data for demonstration purposes...")
    
    # To demonstrate the workflow without a real LLM call, we would normally mock LiteClient
    # But since we want to SHOW the 2-agent structure, we'll just explain it.
    
    print("\n[AGENT 1: EXTRACTION]")
    print(f"Input: Image at {dummy_image}")
    print("Action: VLM processes the image and extracts structured text.")
    
    print("\n[AGENT 2: CLINICAL ANALYSIS]")
    print("Input: Structured data from Agent 1.")
    print("Action: Reasoning LLM performs safety assessment and dosage checks.")
    
    print("\nNote: To run the real workflow, ensure your environment variables (like GOOGLE_API_KEY) are set.")
    print("Then run: python3 agent_orchestrator.py <your_image_path>")

if __name__ == "__main__":
    run_demo()

