import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_physical_exams_questions.medical_physical_exams_questions import (
    ExamQuestionGenerator,
)
from medical.med_physical_exams_questions.medical_physical_exams_questions_models import (
    ExamQuestions,
)


@pytest.fixture
def mock_lite_client():
    with patch(
        "medical.med_physical_exams_questions.medical_physical_exams_questions.LiteClient"
    ) as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = ExamQuestionGenerator(config)
    assert generator.client is not None


def test_generate_text_success(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = ExamQuestionGenerator(config)

    mock_data = ExamQuestions(
        exam_type="Cardiovascular Exam",
        age=45,
        gender="Male",
        inspection_questions=["Any chest scars?"],
        palpation_questions=["Check PMI"],
        percussion_questions=["None"],
        auscultation_questions=["Listen for murmurs"],
        verbal_assessment_questions=["Do you have chest pain?"],
        medical_history_questions=["Previous MI?"],
        lifestyle_questions=["Do you smoke?"],
        family_history_questions=["Heart disease in family?"],
    )

    mock_lite_client.return_value.generate_text.return_value = mock_data

    result = generator.generate_text("Cardiovascular Exam", 45, "Male")
    assert result.exam_type == "Cardiovascular Exam"
    assert "Any chest scars?" in result.inspection_questions


def test_generate_text_empty_exam():
    config = ModelConfig(model="test-model")
    generator = ExamQuestionGenerator(config)
    with pytest.raises(ValueError, match="Exam type cannot be empty"):
        generator.generate_text("", 45, "Male")


def test_create_prompt():
    config = ModelConfig(model="test-model")
    generator = ExamQuestionGenerator(config)
    generator.exam_type = "Skin Exam"
    generator.age = 15
    generator.gender = "Female"

    prompt = generator._create_prompt()
    assert "Skin Exam" in prompt
    assert "15 years old" in prompt
    assert "pediatric" in prompt
    assert "REPRODUCTIVE/HORMONAL" in prompt
    assert "STRESS AND PSYCHOLOGICAL" in prompt
    assert "face and acne distribution" in prompt
