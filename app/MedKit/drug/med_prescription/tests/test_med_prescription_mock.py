import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from prescription_extractor import PrescriptionExtractor, PrescriptionData, Medication
from prescription_analyzer import analyze_prescription, PrescriptionAnalysis
from lite.config import ModelConfig, ModelInput

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.2)

@patch("prescription_extractor.LiteClient")
def test_prescription_extractor_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    
    # Mock result from LiteClient
    mock_med = Medication(
        name="Amoxicillin",
        dosage="500mg",
        frequency="TID",
        route="Oral",
        duration="7 days"
    )
    mock_data = PrescriptionData(
        medications=[mock_med],
        prescriber="Dr. Smith",
        patient_name="John Doe",
        date_prescribed="2023-10-27"
    )
    
    # LiteClient.generate_text returns a result object that has a .data attribute
    mock_result = MagicMock()
    mock_result.data = mock_data
    mock_client_instance.generate_text.return_value = mock_result
    
    extractor = PrescriptionExtractor(config=mock_model_config)
    image_path = "dummy_path.png"
    
    result = extractor.extract(image_path)
    
    assert result.patient_name == "John Doe"
    assert result.medications[0].name == "Amoxicillin"
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert model_input.image_path == image_path
    assert model_input.response_format == PrescriptionData

@patch("prescription_analyzer.LiteClient")
@patch("prescription_analyzer.PrescriptionExtractor")
def test_analyze_prescription_mock(mock_extractor_class, mock_client_class, mock_model_config):
    # Mock extractor
    mock_extractor_instance = mock_extractor_class.return_value
    mock_med = Medication(
        name="Amoxicillin",
        dosage="500mg",
        frequency="TID",
        route="Oral",
        duration="7 days"
    )
    mock_data = PrescriptionData(
        medications=[mock_med],
        prescriber="Dr. Smith",
        patient_name="John Doe",
        date_prescribed="2023-10-27"
    )
    mock_extractor_instance.extract.return_value = mock_data
    
    # Mock LiteClient for analysis
    mock_client_instance = mock_client_class.return_value
    mock_analysis = PrescriptionAnalysis(
        extracted_data=mock_data,
        drug_interactions="None",
        allergy_warnings="None",
        dosage_compliance="High",
        overall_assessment="Safe"
    )
    mock_result = MagicMock()
    mock_result.data = mock_analysis
    mock_client_instance.generate_text.return_value = mock_result
    
    image_path = "dummy_path.png"
    result = analyze_prescription(image_path, config=mock_model_config)
    
    assert result.overall_assessment == "Safe"
    assert result.extracted_data.patient_name == "John Doe"
    mock_extractor_instance.extract.assert_called_once_with(image_path)
    mock_client_instance.generate_text.assert_called_once()
