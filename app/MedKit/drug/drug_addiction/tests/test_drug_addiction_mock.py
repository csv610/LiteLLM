import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from drug_addiction import DrugAddiction
from drug_addiction_prompts import DrugAddictionInput, PromptBuilder
from drug_addiction_models import DrugAddictionModel, ModelOutput, DrugAddictionDetailsModel, AddictionPotential, ConfidenceLevel, AddictionMechanismModel
from lite.config import ModelConfig, ModelInput

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def drug_addiction_analyzer(mock_model_config):
    with patch("drug_addiction.LiteClient"):
        return DrugAddiction(mock_model_config)

def test_drug_addiction_input_validation():
    # Valid input
    valid_input = DrugAddictionInput(medicine_name="Ketamine")
    valid_input.validate()  # Should not raise

    # Invalid input (empty)
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        DrugAddictionInput(medicine_name="").validate()
    
    # Invalid input (whitespace)
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        DrugAddictionInput(medicine_name="   ").validate()

def test_prompt_builder():
    config = DrugAddictionInput(medicine_name="Ketamine", usage_duration="2 weeks")
    
    system_prompt = PromptBuilder.create_system_prompt()
    assert "expert in addiction medicine" in system_prompt
    
    user_prompt = PromptBuilder.create_user_prompt(config)
    assert "Analyze the addiction potential and risks for Ketamine" in user_prompt
    assert "Reported usage duration: 2 weeks" in user_prompt

@patch("drug_addiction.LiteClient")
def test_generate_text_mock(mock_client_class, mock_model_config):
    # Setup mock client to return raw markdown string
    mock_client_instance = mock_client_class.return_value
    raw_markdown = "# Analysis for Ketamine"
    mock_client_instance.generate_text.return_value = raw_markdown
    
    analyzer = DrugAddiction(mock_model_config)
    config = DrugAddictionInput(medicine_name="Ketamine")
    
    result = analyzer.generate_text(config)
    
    assert isinstance(result, ModelOutput)
    assert result.markdown == raw_markdown
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput passed to client
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Ketamine" in model_input.user_prompt
    assert model_input.response_format is None

@patch("drug_addiction.LiteClient")
def test_generate_text_structured_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    
    # Create a dummy structured result (raw DrugAddictionModel)
    details = DrugAddictionDetailsModel(
        medicine_name="Ketamine",
        addiction_potential=AddictionPotential.MODERATE,
        mechanism=AddictionMechanismModel(
            neurotransmitter_impact="Glutamate",
            psychological_factors="Dissociation",
            physiological_dependence="Low"
        ),
        withdrawal_symptoms=[],
        long_term_effects=[],
        risk_factors=[],
        treatment_options=[],
        prevention_strategies=[],
        confidence_level=ConfidenceLevel.HIGH
    )
    structured_raw = DrugAddictionModel(
        addiction_details=details,
        technical_summary="Summary"
    )
    mock_client_instance.generate_text.return_value = structured_raw
    
    analyzer = DrugAddiction(mock_model_config)
    config = DrugAddictionInput(medicine_name="Ketamine")
    
    result = analyzer.generate_text(config, structured=True)
    
    assert isinstance(result, ModelOutput)
    assert result.data == structured_raw
    assert result.data.addiction_details.medicine_name == "Ketamine"
    
    # Verify response_format was set
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert model_input.response_format == DrugAddictionModel

@patch("drug_addiction.save_model_response")
def test_save_mock(mock_save_response, drug_addiction_analyzer):
    result = ModelOutput(markdown="# Analysis")
    output_dir = Path("test_outputs")
    
    # Must call generate_text first to set self.config
    config = DrugAddictionInput(medicine_name="Ketamine")
    drug_addiction_analyzer.config = config
    
    drug_addiction_analyzer.save(result, output_dir)
    
    mock_save_response.assert_called_once()
    args, _ = mock_save_response.call_args
    assert args[0] == result.markdown
    assert "ketamine" in str(args[1])

def test_save_before_generate_raises(drug_addiction_analyzer):
    result = ModelOutput(markdown="# Analysis")
    with pytest.raises(ValueError, match="No configuration available"):
        drug_addiction_analyzer.save(result, Path("outputs"))
