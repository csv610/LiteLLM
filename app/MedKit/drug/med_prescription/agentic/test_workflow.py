import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to sys.path
current_dir = Path(__file__).resolve().parent
app_root = current_dir.parent.parent.parent.parent
sys.path.append(str(app_root))

from agent_orchestrator import PrescriptionAgentApp
from prescription_extractor import PrescriptionData, Medication
from prescription_analyzer import PrescriptionAnalysis

def test_full_agent_workflow():
    print("🧪 Testing 2-Agent Workflow (Mocked)...")
    
    # Mock data for Agent 1 (Extraction)
    mock_medication = Medication(
        name="Amoxicillin",
        dosage="500mg",
        frequency="TID",
        route="Oral",
        duration="7 days"
    )
    mock_extracted_data = PrescriptionData(
        medications=[mock_medication],
        prescriber="Dr. Smith",
        patient_name="John Doe",
        date_prescribed="2024-01-01"
    )
    
    # Mock data for Agent 2 (Analysis)
    mock_analysis = PrescriptionAnalysis(
        extracted_data=mock_extracted_data,
        drug_interactions="None identified.",
        allergy_warnings="No allergies reported.",
        dosage_compliance="Standard dosage for infection.",
        overall_assessment="Safe to proceed."
    )
    
    # Initialize the app
    app = PrescriptionAgentApp()
    
    # We will mock the extraction and analysis steps
    with patch.object(app.extractor, 'extract', return_value=mock_extracted_data) as mock_extract:
        with patch('agent_orchestrator.analyze_prescription', return_value=mock_analysis) as mock_analyze:
            
            print("🚀 Running app.run('mock_image.jpg')...")
            result = app.run("mock_image.jpg")
            
            # Assertions
            assert result is not None, "Workflow should return a result"
            assert result.extracted_data.patient_name == "John Doe", "Patient name should match"
            assert "Safe to proceed." in result.overall_assessment, "Assessment should be present"
            
            # Verify mocks were called
            mock_extract.assert_called_once_with("mock_image.jpg")
            mock_analyze.assert_called_once()
            
            print("\n✅ Test Passed: 2-Agent Orchestration works as expected!")

if __name__ == "__main__":
    try:
        test_full_agent_workflow()
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        sys.exit(1)
