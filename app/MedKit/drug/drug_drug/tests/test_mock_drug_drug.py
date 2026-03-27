from unittest.mock import patch

import pytest
from drug_drug_interaction import DrugDrugInteractionGenerator
from drug_drug_interaction_models import (
    ConfidenceLevel,
    DataAvailabilityInfoModel,
    DataSourceType,
    DrugInteractionDetailsModel,
    DrugInteractionModel,
    DrugInteractionSeverity,
    ModelOutput,
    PatientFriendlySummaryModel,
)
from drug_drug_interaction_prompts import DrugDrugInput, PromptStyle
from lite.config import ModelConfig


@pytest.fixture
def model_config():
    return ModelConfig(model="test-model", temperature=0.2)

@pytest.fixture
def drug_drug_generator(model_config):
    return DrugDrugInteractionGenerator(model_config)

@pytest.fixture
def sample_input():
    return DrugDrugInput(
        medicine1="Aspirin",
        medicine2="Warfarin",
        age=65,
        dosage1="81mg",
        dosage2="5mg",
        medical_conditions="Atrial Fibrillation",
        prompt_style=PromptStyle.DETAILED
    )

@pytest.fixture
def mock_interaction_result():
    details = DrugInteractionDetailsModel(
        drug1_name="Aspirin",
        drug2_name="Warfarin",
        severity_level=DrugInteractionSeverity.SIGNIFICANT,
        mechanism_of_interaction="Both drugs inhibit hemostasis...",
        clinical_effects="Increased bleeding risk",
        management_recommendations="Monitor INR, avoid if possible",
        alternative_medicines="Clopidogrel",
        confidence_level=ConfidenceLevel.HIGH,
        data_source_type=DataSourceType.CLINICAL_STUDIES,
        references="Medscape, Drugs.com"
    )
    patient_summary = PatientFriendlySummaryModel(
        simple_explanation="Taking these together can make you bleed more easily.",
        what_patient_should_do="Tell your doctor you are taking both.",
        warning_signs="Easy bruising, nosebleeds",
        when_to_seek_help="If you have severe bleeding that won't stop"
    )
    data_availability = DataAvailabilityInfoModel(data_available=True)
    
    interaction_model = DrugInteractionModel(
        interaction_details=details,
        technical_summary="Aspirin and Warfarin have a significant interaction.",
        patient_friendly_summary=patient_summary,
        data_availability=data_availability
    )
    
    return ModelOutput(data=interaction_model, markdown="Markdown output")

def test_generate_text_unstructured(drug_drug_generator, sample_input):
    mock_raw_response = "Simple markdown response"
    
    with patch.object(drug_drug_generator.client, 'generate_text', return_value=mock_raw_response) as mock_ask:
        result = drug_drug_generator.generate_text(sample_input, structured=False)
        
        assert result.markdown == mock_raw_response
        assert drug_drug_generator.user_input == sample_input
        mock_ask.assert_called_once()
        
        # Verify the model input passed to client
        model_input = mock_ask.call_args[1]['model_input']
        assert "Aspirin" in model_input.user_prompt
        assert "Warfarin" in model_input.user_prompt
        assert model_input.response_format is None

def test_generate_text_structured(drug_drug_generator, sample_input, mock_interaction_result):
    # Mock return value is the internal data model, not ModelOutput
    mock_raw_data = mock_interaction_result.data
    with patch.object(drug_drug_generator.client, 'generate_text', return_value=mock_raw_data) as mock_ask:
        result = drug_drug_generator.generate_text(sample_input, structured=True)
        
        assert result.data == mock_raw_data
        assert result.data.interaction_details.drug1_name == "Aspirin"
        mock_ask.assert_called_once()
        
        # Verify response_format was set
        model_input = mock_ask.call_args[1]['model_input']
        assert model_input.response_format == DrugInteractionModel

def test_save(drug_drug_generator, sample_input, mock_interaction_result, tmp_path):
    drug_drug_generator.user_input = sample_input
    
    with patch('drug_drug_interaction.save_model_response') as mock_save:
        mock_save.return_value = tmp_path / "aspirin_warfarin_interaction.md"
        
        output_path = drug_drug_generator.save(mock_interaction_result, tmp_path)
        
        assert output_path == tmp_path / "aspirin_warfarin_interaction.md"
        mock_save.assert_called_once()
        # Check if base filename is correct
        args, kwargs = mock_save.call_args
        assert "aspirin_warfarin_interaction" in str(args[1])

def test_save_without_input_fails(drug_drug_generator, mock_interaction_result, tmp_path):
    with pytest.raises(ValueError, match="No configuration available"):
        drug_drug_generator.save(mock_interaction_result, tmp_path)
