import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_faqs.nonagentic.medical_faq import MedicalFAQGenerator
from medical.med_faqs.nonagentic.medical_faq_models import (
    FAQItemModel,
    MedicalFAQModel,
    MisconceptionItemModel,
    ModelOutput,
    PatientFAQModel,
    SeeAlsoTopicsModel,
    WhenToSeekCareModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_faqs.nonagentic.medical_faq.LiteClient") as mock:
        yield mock


def test_medical_faq_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    mock_output = ModelOutput(markdown="FAQ answer", data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("What is diabetes?")
    assert result.markdown == "FAQ answer"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalFAQGenerator(config)
    mock_data = MedicalFAQModel(
        topic_name="Diabetes",
        metadata={"version": "1.0"},
        patient_faq=PatientFAQModel(
            topic_name="Diabetes",
            introduction="Intro",
            faqs=[FAQItemModel(question="What is it?", answer="A condition")],
            when_to_seek_care=[
                WhenToSeekCareModel(
                    symptom_or_condition="Fever",
                    urgency_level="Urgent",
                    action_needed="See doctor",
                )
            ],
            misconceptions=[
                MisconceptionItemModel(
                    misconception="Myth", clarification="Truth", explanation="Reason"
                )
            ],
            see_also=[
                SeeAlsoTopicsModel(
                    name="Insulin", category="test", description="Desc", relevance="Rel"
                )
            ],
        ),
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("What is diabetes?", structured=True)
    assert result.data.topic_name == "Diabetes"
