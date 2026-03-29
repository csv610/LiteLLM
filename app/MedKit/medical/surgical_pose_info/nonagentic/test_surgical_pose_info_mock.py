import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.surgical_pose_info.surgical_pose_info import SurgicalPoseInfoGenerator
from medical.surgical_pose_info.surgical_pose_info_models import (
    ContraindicationsAndModificationsModel,
    ModelOutput,
    PatientSetupModel,
    PhysiologicalEffectsModel,
    PoseBasicsModel,
    PoseIndicationsModel,
    PostOperativeCareModel,
    SafetyConsiderationsModel,
    SurgicalPoseInfoModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.surgical_pose_info.surgical_pose_info.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)
    mock_output = ModelOutput(markdown="Supine info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Supine")
    assert result.markdown == "Supine info"
    assert generator.pose == "Supine"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)
    with pytest.raises(ValueError, match="Position name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)

    # Minimal mock data for structured output
    mock_data = SurgicalPoseInfoModel(
        pose_basics=PoseBasicsModel(
            position_name="Supine",
            alternative_names="Dorsal Decubitus",
            category="Dorsal",
            common_uses="Abdominal surgery",
        ),
        indications=PoseIndicationsModel(
            primary_procedures="Laparotomy",
            anatomical_access="Abdomen",
            specialty_usage="General Surgery",
        ),
        patient_setup=PatientSetupModel(
            equipment_needed="Arm boards",
            step_by_step_placement="1. Lay flat",
            head_and_neck="Neutral",
            upper_extremities="Abducted",
            lower_extremities="Straight",
            padding_requirements="Heels",
        ),
        safety_considerations=SafetyConsiderationsModel(
            pressure_points="Sacrum",
            nerve_risks="Brachial plexus",
            prevention_strategies="Padding",
            check_points="Eyes",
        ),
        physiological_effects=PhysiologicalEffectsModel(
            respiratory_effects="Reduced FRC",
            cardiovascular_effects="Minimal",
            other_physiological_changes="None",
        ),
        contraindications_and_modifications=ContraindicationsAndModificationsModel(
            absolute_contraindications="None",
            relative_contraindications="Respiratory distress",
            modifications_for_obesity="Wider table",
            modifications_for_pediatrics="Smaller pads",
            modifications_for_elderly="Skin protection",
        ),
        post_operative_care=PostOperativeCareModel(
            repositioning_care="Slow movement", monitoring_requirements="Vitals"
        ),
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Supine", structured=True)
    assert result.data.pose_basics.position_name == "Supine"


@patch("medical.surgical_pose_info.surgical_pose_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Supine")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("supine")
