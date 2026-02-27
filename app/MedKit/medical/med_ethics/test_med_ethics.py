import pytest
from unittest.mock import MagicMock, patch
from med_ethics import MedEthicalQA
from lite.config import ModelConfig
from med_ethics_models import EthicalAnalysisModel, ModelOutput

@pytest.fixture
def mock_lite_client():
    # Make sure we're mocking the class correctly in its module
    with patch('med_ethics.LiteClient') as mock:
        yield mock

def test_med_ethical_qa_init():
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    assert generator.model_config == config
    assert generator.client is not None

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    
    mock_client_instance = mock_lite_client.return_value
    mock_output = ModelOutput(markdown="Ethics analysis in markdown")
    mock_client_instance.generate_text.return_value = mock_output
    
    output = generator.generate_text(question="Is it ethical to use AI in medicine?", structured=False)
    
    assert output.markdown == "Ethics analysis in markdown"
    assert output.data is None
    mock_client_instance.generate_text.assert_called_once()

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    
    # Minimal mock data for structured output
    mock_data = MagicMock(spec=EthicalAnalysisModel)
    mock_output = ModelOutput(data=mock_data)
    
    mock_client_instance = mock_lite_client.return_value
    mock_client_instance.generate_text.return_value = mock_output
    
    output = generator.generate_text(question="Is it ethical to use AI in medicine?", structured=True)
    
    assert output.data == mock_data
    assert output.markdown is None
    mock_client_instance.generate_text.assert_called_once()

def test_save_with_case_title(tmp_path):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    generator.question = "Should I let old person die to save a newly born child?"
    
    # Mock result with case_title using a real object or dict to satisfy Pydantic
    analysis_data = EthicalAnalysisModel(
        case_title="Intergenerational Resource Allocation",
        summary="A summary",
        facts=["Fact 1"],
        ethical_issues=["Issue 1"],
        stakeholders=[],
        principles=[],
        legal_considerations={"regulations": [], "professional_guidelines": []},
        recommendations=["Rec 1"],
        conclusion="Conclusion"
    )
    mock_output = ModelOutput(data=analysis_data)
    
    with patch('med_ethics.save_model_response') as mock_save:
        mock_save.return_value = tmp_path / "intergenerational_resource_allocation.md"
        generator.save(mock_output, tmp_path)
        
        # Check if the base_filename passed to save_model_response is correct
        args, _ = mock_save.call_args
        assert args[1].name == "intergenerational_resource_allocation"

def test_save_fallback_to_question(tmp_path):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    generator.question = "Short question?"
    
    # Mock result without data (unstructured)
    # The new save method uses the first line of markdown for filename
    mock_output = ModelOutput(markdown="# Short Title\nSome text")
    
    output_path = generator.save(mock_output, tmp_path)
    
    assert output_path.name == "short_title.md"
    assert output_path.exists()
    assert output_path.read_text() == "# Short Title\nSome text"
