import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from unittest.mock import MagicMock, patch
from medical.med_ethics.med_ethics import MedEthicalQA
from lite.config import ModelConfig
from medical.med_ethics.med_ethics_models import (
    EthicalAnalysisModel, ModelOutput, EthicalPrincipleModel,
    StakeholderModel, LegalFrameworkModel
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_ethics.med_ethics.LiteClient') as mock:
        yield mock

def test_med_ethical_qa_init():
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    assert generator.model_config == config
    assert generator.client is not None

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    mock_output = ModelOutput(markdown="Ethics analysis in markdown", data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Organ transplantation ethics")
    assert result.markdown == "Ethics analysis in markdown"

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    
    mock_data = EthicalAnalysisModel(
        topic="Organ transplantation",
        ethical_principles=[EthicalPrincipleModel(principle="Autonomy", principle_name="Autonomy", description="Self-determination", ethical_implications="Patient choice")],
        stakeholders=[StakeholderModel(name="Patient", stakeholder_name="Patient", interests=["Health"], interest_description="Access to care")],
        legal_frameworks=[LegalFrameworkModel(jurisdiction="Global", laws=["N/A"], framework_name="WHO", legal_framework_description="Global standards")],
        pros=["Saves lives"],
        cons=["Scarcity"],
        conclusion="Complex topic",
        summary="Ethics of organ transplantation"
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text("Organ transplantation", structured=True)
    assert result.data.topic == "Organ transplantation"
