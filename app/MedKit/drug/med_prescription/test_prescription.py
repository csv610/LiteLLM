import sys
from pathlib import Path

# Add the project root to sys.path for proper imports
# Current file is in /Users/csv610/Projects/LiteLLM/app/MedKit/drug/med_prescription
# We want to add /Users/csv610/Projects/LiteLLM/app to the path
current_dir = Path(__file__).resolve().parent
app_dir = current_dir.parent.parent.parent # drug -> MedKit -> app
sys.path.append(str(app_dir))

print(f"Added to sys.path: {app_dir}")

try:
    # Try importing medkit (since it's macOS, MedKit should match medkit)
    import MedKit
    print("✓ Successfully imported MedKit")
    
    from MedKit.drug.med_prescription.prescription_extractor import PrescriptionExtractor, PrescriptionData
    from MedKit.drug.med_prescription.prescription_analyzer import analyze_prescription
    from lite.config import ModelConfig
    
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
