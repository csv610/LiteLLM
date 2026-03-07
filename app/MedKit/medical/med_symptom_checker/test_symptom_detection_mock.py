import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest

from medical.med_symptom_checker.symptom_detection_qa import (
    EmergencyException,
    MedicalConsultation,
)


def test_detect_red_flags():
    consultation = MedicalConsultation()

    is_emergency, flags = consultation.detect_red_flags(
        "I have severe chest pain and chest pressure"
    )
    assert is_emergency is True
    assert "chest pain" in flags
    assert "chest pressure" in flags

    is_emergency, flags = consultation.detect_red_flags("I have a mild cough")
    assert is_emergency is False
    assert len(flags) == 0


def test_parse_json_from_response():
    consultation = MedicalConsultation()

    # Standard JSON
    res = consultation._parse_json_from_response('{"key": "value"}')
    assert res == {"key": "value"}

    # Markdown JSON
    res = consultation._parse_json_from_response("""Some text ```json
{"key": "value"}
``` other text""")
    assert res == {"key": "value"}

    # Loose JSON
    res = consultation._parse_json_from_response('Here is the data: {"key": "value"}')
    assert res == {"key": "value"}


def test_emergency_exception():
    with pytest.raises(EmergencyException) as excinfo:
        raise EmergencyException(["Chest pain"], "John Doe")
    assert "Chest pain" in str(excinfo.value)
    assert excinfo.value.patient_name == "John Doe"


@patch("medical.med_symptom_checker.symptom_detection_qa.LiteClient")
def test_consultation_init(mock_client):
    consultation = MedicalConsultation(model="test-model")
    assert consultation.config.model == "test-model"
    assert consultation.client is not None
