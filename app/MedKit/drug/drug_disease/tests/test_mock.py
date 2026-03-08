import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from drug_disease_interaction import DrugDiseaseInteraction
from drug_disease_interaction_prompts import DrugDiseaseInput, PromptStyle
from drug_disease_interaction_models import ModelOutput, DrugDiseaseInteractionModel
from drug_disease_interaction_cli import create_drug_disease_interaction_report
from lite.config import ModelConfig

# --- Core Class Mock Tests ---

@pytest.fixture
def mock_lite_client():
    with patch("drug_disease_interaction.LiteClient") as mock:
        yield mock

@pytest.fixture
def analyzer(mock_lite_client):
    config = ModelConfig(model="test-model")
    return DrugDiseaseInteraction(config)

def test_generate_text_unstructured(analyzer, mock_lite_client):
    # Mock return value
    mock_response = ModelOutput(markdown="Test analysis result")
    analyzer.client.generate_text.return_value = mock_response

    input_config = DrugDiseaseInput(medicine_name="Aspirin", condition_name="Peptic Ulcer")
    result = analyzer.generate_text(input_config, structured=False)

    assert result.markdown == "Test analysis result"
    analyzer.client.generate_text.assert_called_once()
    
    # Check if the correct system prompt and user prompt were passed
    model_input = analyzer.client.generate_text.call_args.kwargs["model_input"]
    assert "clinical pharmacology expert" in model_input.system_prompt
    assert "Aspirin" in model_input.user_prompt
    assert "Peptic Ulcer" in model_input.user_prompt
    assert model_input.response_format is None

def test_generate_text_structured(analyzer, mock_lite_client):
    # Mock return value
    mock_data = MagicMock(spec=DrugDiseaseInteractionModel)
    mock_response = ModelOutput(data=mock_data)
    analyzer.client.generate_text.return_value = mock_response

    input_config = DrugDiseaseInput(medicine_name="Aspirin", condition_name="Peptic Ulcer")
    result = analyzer.generate_text(input_config, structured=True)

    assert result.data == mock_data
    analyzer.client.generate_text.assert_called_once()
    
    # Check if structured output format was requested
    model_input = analyzer.client.generate_text.call_args.kwargs["model_input"]
    assert model_input.response_format is DrugDiseaseInteractionModel

def test_save_method(analyzer):
    # Mock save_model_response
    with patch("drug_disease_interaction.save_model_response") as mock_save:
        mock_save.return_value = Path("outputs/aspirin_peptic_ulcer_interaction.md")
        
        input_config = DrugDiseaseInput(medicine_name="Aspirin", condition_name="Peptic Ulcer")
        # Need to call generate_text first to set analyzer.config
        analyzer.config = input_config
        
        result = ModelOutput(markdown="Test")
        output_dir = Path("outputs")
        
        save_path = analyzer.save(result, output_dir)
        
        assert save_path == Path("outputs/aspirin_peptic_ulcer_interaction.md")
        mock_save.assert_called_once()

def test_save_without_config(analyzer):
    result = ModelOutput(markdown="Test")
    with pytest.raises(ValueError, match="No configuration information available"):
        analyzer.save(result, Path("outputs"))

def test_ask_llm_error_handling(analyzer, mock_lite_client):
    analyzer.client.generate_text.side_effect = Exception("API error")
    
    from lite.config import ModelInput
    model_input = ModelInput(system_prompt="sys", user_prompt="user")
    
    with pytest.raises(Exception, match="API error"):
        analyzer._ask_llm(model_input)

# --- CLI Mock Tests ---

def test_parse_prompt_style():
    from drug_disease_interaction_cli import parse_prompt_style
    assert parse_prompt_style("detailed") == PromptStyle.DETAILED
    assert parse_prompt_style("concise") == PromptStyle.CONCISE
    assert parse_prompt_style("balanced") == PromptStyle.BALANCED
    
    with pytest.raises(ValueError, match="Invalid prompt style"):
        parse_prompt_style("unknown")

def test_get_user_arguments():
    import sys
    from drug_disease_interaction_cli import get_user_arguments
    test_args = [
        "drug_disease_interaction_cli.py",
        "Aspirin",
        "Peptic Ulcer",
        "--severity", "moderate",
        "--age", "45",
        "--medications", "Metformin",
        "--style", "concise",
        "--structured"
    ]
    
    with patch.object(sys, 'argv', test_args):
        args = get_user_arguments()
        assert args.medicine_name == "Aspirin"
        assert args.condition_name == "Peptic Ulcer"
        assert args.severity == "moderate"
        assert args.age == 45
        assert args.medications == "Metformin"
        assert args.style == "concise"
        assert args.structured is True

def test_cli_execution_mocked():
    """Test the CLI main logic with a mocked analyzer."""
    args = MagicMock()
    args.medicine_name = "Aspirin"
    args.condition_name = "Peptic Ulcer"
    args.severity = "moderate"
    args.age = 45
    args.medications = "Metformin"
    args.style = "concise"
    args.structured = True
    args.output_dir = "outputs"
    args.verbosity = 2
    args.model = "test-model"

    with patch("drug_disease_interaction_cli.DrugDiseaseInteraction") as MockAnalyzer:
        mock_analyzer_instance = MockAnalyzer.return_value
        mock_result = MagicMock(spec=ModelOutput)
        mock_analyzer_instance.generate_text.return_value = mock_result
        
        exit_code = create_drug_disease_interaction_report(args)
        
        assert exit_code == 0
        MockAnalyzer.assert_called_once()
        mock_analyzer_instance.generate_text.assert_called_once()
        mock_analyzer_instance.save.assert_called_once_with(mock_result, Path("outputs"))

# --- Models Mock Tests ---

def test_drug_disease_input_validation():
    # Valid input
    config = DrugDiseaseInput(medicine_name="Aspirin", condition_name="Peptic Ulcer")
    assert config.medicine_name == "Aspirin"
    assert config.condition_name == "Peptic Ulcer"
    assert config.prompt_style == PromptStyle.DETAILED

def test_drug_disease_input_empty_medicine():
    with pytest.raises(ValueError, match="Medicine name cannot be empty"):
        DrugDiseaseInput(medicine_name="", condition_name="Peptic Ulcer")

def test_drug_disease_input_empty_condition():
    with pytest.raises(ValueError, match="Condition name cannot be empty"):
        DrugDiseaseInput(medicine_name="Aspirin", condition_name="")

def test_drug_disease_input_multiple_medicines():
    with pytest.raises(ValueError, match="Only one medicine can be analyzed"):
        DrugDiseaseInput(medicine_name="Aspirin, Ibuprofen", condition_name="Peptic Ulcer")

def test_drug_disease_input_multiple_conditions():
    with pytest.raises(ValueError, match="Only one condition can be analyzed"):
        DrugDiseaseInput(medicine_name="Aspirin", condition_name="Peptic Ulcer and GERD")

def test_drug_disease_input_invalid_age():
    with pytest.raises(ValueError, match="Age must be between 0 and 150 years"):
        DrugDiseaseInput(medicine_name="Aspirin", condition_name="Peptic Ulcer", age=160)

def test_prompt_builder_system_prompt():
    from drug_disease_interaction_prompts import PromptBuilder
    system_prompt = PromptBuilder.create_system_prompt()
    assert "clinical pharmacology expert" in system_prompt
    assert "drug-disease interactions" in system_prompt

def test_prompt_builder_user_prompt():
    from drug_disease_interaction_prompts import PromptBuilder, DrugDiseaseInput, PromptStyle
    config = DrugDiseaseInput(
        medicine_name="Warfarin",
        condition_name="Liver Cirrhosis",
        condition_severity="severe",
        age=65,
        other_medications="Metformin, Lisinopril",
        prompt_style=PromptStyle.BALANCED
    )
    user_prompt = PromptBuilder.create_user_prompt(config)
    assert "Warfarin" in user_prompt
    assert "Liver Cirrhosis" in user_prompt
    assert "severe" in user_prompt
    assert "65 years" in user_prompt
    assert "Metformin, Lisinopril" in user_prompt
    assert "balanced analysis" in user_prompt
