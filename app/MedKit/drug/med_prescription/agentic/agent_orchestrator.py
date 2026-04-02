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
