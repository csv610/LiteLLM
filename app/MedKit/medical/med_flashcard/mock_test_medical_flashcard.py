import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.med_flashcard.medical_flashcard import MedicalLabelExtractor, MedicalTermExplainer
from lite.config import ModelConfig
from medical.med_flashcard.medical_flashcard_models import (
    MedicalLabelInfoModel, ModelOutput
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_flashcard.medical_flashcard.LiteClient') as mock:
        yield mock

def test_medical_label_extractor_init():
    config = ModelConfig(model="test-model")
    extractor = MedicalLabelExtractor(config)
    assert extractor.client is not None

def test_extract_terms(mock_lite_client):
    config = ModelConfig(model="test-model")
    extractor = MedicalLabelExtractor(config)
    
    mock_response = MagicMock()
    mock_response.markdown = """Term1, Term2
Term3"""
    mock_lite_client.return_value.generate_text.return_value = mock_response
    
    terms = extractor.extract_terms("dummy_image.png")
    assert terms == ["Term1", "Term2", "Term3"]

def test_medical_term_explainer_init():
    config = ModelConfig(model="test-model")
    explainer = MedicalTermExplainer(config)
    assert explainer.client is not None

def test_explain_label_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    explainer = MedicalTermExplainer(config)
    mock_output = ModelOutput(markdown="Explanation of term", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = explainer.explain_label("Diabetes")
    assert result.markdown == "Explanation of term"

def test_explain_label_empty():
    config = ModelConfig(model="test-model")
    explainer = MedicalTermExplainer(config)
    with pytest.raises(ValueError, match="Term name cannot be empty"):
        explainer.explain_label("")

def test_explain_label_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    explainer = MedicalTermExplainer(config)
    
    mock_data = MedicalLabelInfoModel(
        term="Diabetes",
        explanation="A condition where sugar levels are high."
    )
    
    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = explainer.explain_label("Diabetes", structured=True)
    assert result.data.term == "Diabetes"

@patch('medical.med_flashcard.medical_flashcard.save_model_response')
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    explainer = MedicalTermExplainer(config)
    mock_output = ModelOutput(markdown="Explanation")
    
    explainer.save(mock_output, Path("/tmp"), "Diabetes")
    
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("diabetes")
