import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.med_speciality.medical_speciality import MedicalSpecialityGenerator
from medical.med_speciality.medical_speciality_models import (
    MedicalSpecialist,
    MedicalSpecialistDatabase,
    SpecialtyCategory,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_speciality.medical_speciality.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)
    mock_lite_client.return_value.generate_text.return_value = "Specialists list"

    result = generator.generate_text()
    assert result == "Specialists list"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)

    cat = SpecialtyCategory(name="Cardiovascular", description="Heart and vessels")
    mock_data = MedicalSpecialistDatabase(
        specialists=[
            MedicalSpecialist(
                specialty_name="Cardiologist",
                category=cat,
                description="Heart doctor",
                treats=["Heart failure", "Arrhythmia"],
                common_referral_reasons=["Chest pain"],
                is_surgical=False,
            ),
            MedicalSpecialist(
                specialty_name="Cardiac Surgeon",
                category=cat,
                description="Heart surgeon",
                treats=["Valve disease"],
                common_referral_reasons=["Surgery needed"],
                is_surgical=True,
            ),
        ]
    )

    mock_lite_client.return_value.generate_text.return_value = mock_data

    result = generator.generate_text(structured=True)
    assert len(result.specialists) == 2
    assert len(result.get_surgical_specialists()) == 1
    assert result.get_by_category("Cardiovascular")[0].specialty_name == "Cardiologist"


@patch("medical.med_speciality.medical_speciality.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalSpecialityGenerator(config)
    mock_lite_client.return_value.generate_text.return_value = "Specialists"

    result = generator.generate_text()
    generator.save(result, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == "Specialists"
    assert str(args[1]).endswith("medical_specialities_database")
