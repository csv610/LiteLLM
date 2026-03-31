import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_speciality_roles.agentic.med_speciality_roles import MedSpecialityRoles


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_speciality_roles.agentic.med_speciality_roles.LiteClient") as mock:
        yield mock


def test_med_speciality_roles_init():
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)
    assert roles.config == config


def test_generate_text(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_lite_client.return_value.generate_text.return_value = (
        "Cardiologist treats heart"
    )

    result = roles.generate_text("Cardiologist")
    assert result == "Cardiologist treats heart"


def test_generate_text_error(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_lite_client.return_value.generate_text.side_effect = Exception("API Error")

    result = roles.generate_text("Cardiologist")
    assert "Error: API Error" in result
