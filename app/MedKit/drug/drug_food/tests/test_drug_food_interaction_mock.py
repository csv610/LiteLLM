from unittest.mock import MagicMock, patch

import pytest
from drug_food_interaction import DrugFoodInteraction
from drug_food_interaction_models import (
    DataAvailabilityInfoModel,
    DrugFoodInteractionModel,
    ModelOutput,
)
from drug_food_interaction_prompts import DrugFoodInput
from lite.config import ModelConfig, ModelInput


@pytest.fixture
def model_config():
    return ModelConfig(model="mock-model", temperature=0.2)

@pytest.fixture
def analyzer(model_config):
    return DrugFoodInteraction(model_config)

@pytest.fixture
def drug_food_input():
    return DrugFoodInput(
        medicine_name="Warfarin",
        diet_type="Vegan",
        medical_conditions="Atrial Fibrillation",
        age=65,
        specific_food=None,
        prompt_style="detailed",
    )

@patch("drug_food_interaction.LiteClient")
def test_generate_text_unstructured(mock_lite_client_class, analyzer, drug_food_input):
    # Setup mock
    mock_client = MagicMock()
    mock_lite_client_class.return_value = mock_client
    analyzer.client = mock_client
    
    # LiteClient.generate_text returns a string when unstructured
    mock_response = "Interaction details for Warfarin..."
    mock_client.generate_text.return_value = mock_response
    
    # Execute
    result = analyzer.generate_text(drug_food_input, structured=False)
    
    # Assert
    assert isinstance(result, ModelOutput)
    assert result.markdown == "Interaction details for Warfarin..."
    mock_client.generate_text.assert_called_once()
    
    # Verify model_input passed
    args, kwargs = mock_client.generate_text.call_args
    model_input = kwargs['model_input']
    assert isinstance(model_input, ModelInput)
    assert model_input.response_format is None

@patch("drug_food_interaction.LiteClient")
def test_generate_text_structured(mock_lite_client_class, analyzer, drug_food_input):
    # Setup mock
    mock_client = MagicMock()
    mock_lite_client_class.return_value = mock_client
    analyzer.client = mock_client
    
    # LiteClient.generate_text returns the model when structured
    mock_data = DrugFoodInteractionModel(
        technical_summary="Technical summary for Warfarin",
        data_availability=DataAvailabilityInfoModel(data_available=True)
    )
    mock_client.generate_text.return_value = mock_data
    
    # Execute
    result = analyzer.generate_text(drug_food_input, structured=True)
    
    # Assert
    assert isinstance(result, ModelOutput)
    assert result.data.technical_summary == "Technical summary for Warfarin"
    mock_client.generate_text.assert_called_once()
    
    # Verify model_input passed with response_format
    args, kwargs = mock_client.generate_text.call_args
    model_input = kwargs['model_input']
    assert model_input.response_format == DrugFoodInteractionModel

@patch("drug_food_interaction.save_model_response")
def test_save(mock_save_model_response, analyzer, drug_food_input, tmp_path):
    # Setup
    analyzer.user_input = drug_food_input
    mock_response = ModelOutput(markdown="Some result")
    mock_save_model_response.return_value = tmp_path / "warfarin_food_interaction.md"
    
    # Execute
    output_path = analyzer.save(mock_response, tmp_path)
    
    # Assert
    assert output_path == tmp_path / "warfarin_food_interaction.md"
    mock_save_model_response.assert_called_once_with(
        mock_response, tmp_path / "warfarin_food_interaction"
    )

def test_generate_text_error(analyzer, drug_food_input):
    # Setup mock to raise exception
    analyzer.client.generate_text = MagicMock(side_effect=Exception("LLM Error"))
    
    # Execute and Assert
    with pytest.raises(Exception, match="LLM Error"):
        analyzer.generate_text(drug_food_input)
