import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from lite.config import ModelConfig

from medical.med_speciality_roles.agentic.med_speciality_roles import MedSpecialityRoles
from medical.med_speciality_roles.agentic.med_speciality_roles_models import (
    ModelOutput,
    SpecialityRoleInfo,
    ComplianceReviewModel,
    MedicalSpecialityRolesModel
)


@pytest.fixture
def mock_lite_client():
    # Mock the LiteClient in the agents module
    with patch("medical.med_speciality_roles.agentic.med_speciality_roles_agents.LiteClient") as mock:
        yield mock


def test_med_speciality_roles_init():
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)
    assert roles.config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_instance = mock_lite_client.return_value
    mock_instance.generate_text.side_effect = [
        ModelOutput(markdown="Specialist info"),
        ModelOutput(markdown="Compliance: All clear."),
        ModelOutput(markdown="Final Markdown Report"),
    ]

    result = roles.generate_text("Cardiologist", structured=False)
    assert result.markdown == "Final Markdown Report"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_instance = mock_lite_client.return_value

    # 1. SpecialityAgent
    spec_info = SpecialityRoleInfo(
        speciality_name="Cardiologist",
        primary_focus="Heart",
        key_responsibilities=["Treat heart"],
        common_procedures=["EKG"]
    )
    # 2. ComplianceAgent
    compliance_info = ComplianceReviewModel(
        is_compliant=True,
        issues_found=[],
        required_disclaimers=["Disclaimer"],
        suggested_edits=None
    )
    # 3. OutputAgent (Always returns markdown)
    output_res = ModelOutput(markdown="# Final Report\n\nSome content.")

    mock_instance.generate_text.side_effect = [
        ModelOutput(data=spec_info),
        ModelOutput(data=compliance_info),
        output_res,
    ]

    result = roles.generate_text("Cardiologist", structured=True)
    assert result.data.speciality_name == "Cardiologist"
    assert result.data.roles_info.primary_focus == "Heart"
    assert result.data.compliance_review.is_compliant is True
    assert result.markdown == "# Final Report\n\nSome content."


def test_generate_text_error(mock_lite_client):
    config = ModelConfig(model="test-model")
    roles = MedSpecialityRoles(config)

    mock_lite_client.return_value.generate_text.side_effect = Exception("API Error")

    with pytest.raises(Exception) as excinfo:
        roles.generate_text("Cardiologist")
    assert "API Error" in str(excinfo.value)
