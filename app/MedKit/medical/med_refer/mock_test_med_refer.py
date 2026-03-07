import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.med_refer.med_refer import MedReferral
from lite.config import ModelConfig

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_refer.med_refer.LiteClient') as mock:
        yield mock

def test_med_referral_init():
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)
    assert referral.config == config

def test_generate_text(mock_lite_client):
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)
    
    mock_lite_client.return_value.generate_text.return_value = "Cardiologist"
    
    result = referral.generate_text("I have heart pain")
    assert result == "Cardiologist"

def test_generate_text_error(mock_lite_client):
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)
    
    mock_lite_client.return_value.generate_text.side_effect = Exception("API Error")
    
    result = referral.generate_text("I have heart pain")
    assert "Error: API Error" in result
