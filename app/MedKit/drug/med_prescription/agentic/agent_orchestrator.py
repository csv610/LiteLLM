import logging
import sys
from pathlib import Path
from typing import Optional

# Add project root to sys.path
current_dir = Path(__file__).resolve().parent
app_root = current_dir.parent.parent.parent.parent
sys.path.append(str(app_root))

from lite.config import ModelConfig
from .prescription_extractor import PrescriptionExtractor
from .prescription_analyzer import analyze_prescription, PrescriptionAnalysis

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
        
        logger.info(f"Initialized 2-Agent App with: {model}")

    def run(self, image_path: str) -> Optional[PrescriptionAnalysis]:
        """Executes the 2-agent sequential workflow."""
        print(f"\n🚀 Starting Prescription Analysis Workflow\n")
        
        try:
            # AGENT 1: Vision Extraction
            print(f"[AGENT 1] Reading image and extracting data...")
            extracted_data = self.extractor.extract(image_path)
            
            print("✓ Extraction complete. Found:")
            print(f"  - Patient: {extracted_data.patient_name}")
            print(f"  - Medications: {len(extracted_data.medications)} items identified.")

            # AGENT 2: Clinical Reasoning
            print(f"\n[AGENT 2] Performing clinical safety analysis...")
            analysis = analyze_prescription(extracted_data, config=self.config)
            
            # Print Final Report
            self._print_report(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            return None

    def _print_report(self, analysis: PrescriptionAnalysis):
        """Helper to format and print the final safety report."""
        print("\n" + "="*50)
        print("CLINICAL SAFETY REPORT")
        print("="*50)
        print(f"Patient: {analysis.extracted_data.patient_name}")
        print("-" * 50)
        print(f"1. Drug-Drug Interactions:\n   {analysis.drug_interactions}")
        print("-" * 50)
        print(f"2. Dosage Compliance:\n   {analysis.dosage_compliance}")
        print("-" * 50)
        print(f"3. Overall Assessment:\n   {analysis.overall_assessment}")
        print("="*50 + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run the 2-agent Prescription Analysis app.")
    parser.add_argument("image", help="Path to the prescription image.")
    args = parser.parse_args()
    
    app = PrescriptionAgentApp()
    app.run(args.image)
