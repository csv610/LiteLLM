import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from unittest.mock import patch
from medical.med_faqs.medical_faq import MedicalFAQGenerator
from lite.config import ModelConfig
from medical.med_faqs.medical_faq_models import (
    MedicalFAQModel, ModelOutput, FAQItemModel, 
    MisconceptionItemModel, WhenToSeekCareModel, 
    SeeAlsoTopicsModel, PatientFAQModel, ProviderFAQModel
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_faqs.medical_faq.LiteClient') as mock:
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
        topic="Diabetes",
        patient_faqs=PatientFAQModel(items=[FAQItemModel(question="What is it?", answer="A condition", medical_context="General", key_points=["Chronic"])]),
        provider_faqs=ProviderFAQModel(items=[FAQItemModel(question="Management?", answer="Insulin", medical_context="Clinical", key_points=["Medication"])]),
        misconceptions=[MisconceptionItemModel(misconception="Only old people get it", reality="Anyone can")],
        when_to_seek_care=WhenToSeekCareModel(urgent_signs=["Very high sugar"], emergency_signs=["Coma"]),
        see_also=SeeAlsoTopicsModel(topics=["Insulin"], resources=["WHO"]),
        summary="Diabetes FAQ"
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("What is diabetes?", structured=True)
    assert result.data.topic == "Diabetes"
