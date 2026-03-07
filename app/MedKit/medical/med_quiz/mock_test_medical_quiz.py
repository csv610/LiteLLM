import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.med_quiz.medical_quiz import MedicalQuizGenerator
from lite.config import ModelConfig
from medical.med_quiz.medical_quiz_models import (
    MedicalQuizModel, ModelOutput, QuizQuestionModel
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_quiz.medical_quiz.LiteClient') as mock:
        yield mock

def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    assert generator.model_config == config

def test_sanitize_topic():
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    assert generator._sanitize_topic("Diabetes Mellitus") == "Diabetes_Mellitus"
    assert generator._sanitize_topic("Test/Topic?") == "TestTopic"

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    mock_output = ModelOutput(markdown="Quiz content", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Diabetes", "Easy", 1)
    assert result.markdown == "Quiz content"
    assert generator.topic == "Diabetes"

def test_generate_text_invalid_inputs():
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    with pytest.raises(ValueError, match="Topic cannot be empty"):
        generator.generate_text("", "Easy", 1)
    with pytest.raises(ValueError, match="Number of questions must be >= 1"):
        generator.generate_text("Diabetes", "Easy", 0)
    with pytest.raises(ValueError, match="Number of options must be >= 2"):
        generator.generate_text("Diabetes", "Easy", 1, 1)

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    
    mock_data = MedicalQuizModel(
        topic="Diabetes",
        difficulty="Easy",
        questions=[
            QuizQuestionModel(
                id=1,
                question="What is the main symptom of diabetes?",
                options={"A": "Polyuria", "B": "Headache", "C": "Cough", "D": "Rash"},
                answer="A",
                explanation="Polyuria is excessive urination."
            )
        ]
    )
    
    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Diabetes", "Easy", 1, structured=True)
    assert result.data.topic == "Diabetes"

@patch('medical.med_quiz.medical_quiz.save_model_response')
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    mock_output = ModelOutput(markdown="Quiz content")
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    generator.generate_text("Diabetes", "Easy", 1)
    generator.save(mock_output, Path("/tmp"))
    
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("diabetes_quiz")
