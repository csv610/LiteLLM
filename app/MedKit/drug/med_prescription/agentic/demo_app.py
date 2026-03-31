import sys
from pathlib import Path
import logging

# Set up paths
current_dir = Path(__file__).resolve().parent
app_root = current_dir.parent.parent.parent.parent
sys.path.append(str(app_root))

from .agent_orchestrator import PrescriptionAgentApp
from unittest.mock import MagicMock
from lite.config import ModelInput

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
