import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.surgical_pose_info.agentic.surgical_pose_info import SurgicalPoseInfoGenerator
from medical.surgical_pose_info.agentic.surgical_pose_info_agents import (
    BasicsIndicationsAgent,
    ContraindicationsAgent,
    SafetyPhysiologyAgent,
    SetupCareAgent,
)
from medical.surgical_pose_info.agentic.surgical_pose_info_models import (
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
    with patch("medical.surgical_pose_info.agentic.surgical_pose_info_agents.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)

    def mock_generate_text(model_input):
        if model_input.response_format == BasicsIndicationsAgent.BasicsAndIndications:
            return ModelOutput(data=BasicsIndicationsAgent.BasicsAndIndications(
                pose_basics=PoseBasicsModel(position_name="Supine", alternative_names="", category="", common_uses=""),
                indications=PoseIndicationsModel(primary_procedures="", anatomical_access="", specialty_usage="")
            ))
        if model_input.response_format == SetupCareAgent.SetupAndCare:
            return ModelOutput(data=SetupCareAgent.SetupAndCare(
                patient_setup=PatientSetupModel(equipment_needed="", step_by_step_placement="", head_and_neck="", upper_extremities="", lower_extremities="", padding_requirements=""),
                post_operative_care=PostOperativeCareModel(repositioning_care="", monitoring_requirements="")
            ))
        if model_input.response_format == SafetyPhysiologyAgent.SafetyAndPhysiology:
            return ModelOutput(data=SafetyPhysiologyAgent.SafetyAndPhysiology(
                safety_considerations=SafetyConsiderationsModel(pressure_points="", nerve_risks="", prevention_strategies="", check_points=""),
                physiological_effects=PhysiologicalEffectsModel(respiratory_effects="", cardiovascular_effects="", other_physiological_changes="")
            ))
        if model_input.response_format == ContraindicationsAgent.Contraindications:
            return ModelOutput(data=ContraindicationsAgent.Contraindications(
                contraindications_and_modifications=ContraindicationsAndModificationsModel(absolute_contraindications="", relative_contraindications="", modifications_for_obesity="", modifications_for_pediatrics="", modifications_for_elderly="")
            ))
        return ModelOutput(markdown="Supine info")

    mock_lite_client.return_value.generate_text.side_effect = mock_generate_text

    result = generator.generate_text("Supine")
    assert "Surgical Position: Supine" in result.markdown
    assert generator.pose == "Supine"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)
    with pytest.raises(ValueError, match="Position name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)

    # Mock data for each agent
    basics_data = BasicsIndicationsAgent.BasicsAndIndications(
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
    )

    setup_data = SetupCareAgent.SetupAndCare(
        patient_setup=PatientSetupModel(
            equipment_needed="Arm boards",
            step_by_step_placement="1. Lay flat",
            head_and_neck="Neutral",
            upper_extremities="Abducted",
            lower_extremities="Straight",
            padding_requirements="Heels",
        ),
        post_operative_care=PostOperativeCareModel(
            repositioning_care="Slow movement", monitoring_requirements="Vitals"
        ),
    )

    safety_data = SafetyPhysiologyAgent.SafetyAndPhysiology(
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
    )

    contra_data = ContraindicationsAgent.Contraindications(
        contraindications_and_modifications=ContraindicationsAndModificationsModel(
            absolute_contraindications="None",
            relative_contraindications="Respiratory distress",
            modifications_for_obesity="Wider table",
            modifications_for_pediatrics="Smaller pads",
            modifications_for_elderly="Skin protection",
        ),
    )

    # Map each agent to its expected response
    def mock_generate_text(model_input):
        if model_input.response_format == BasicsIndicationsAgent.BasicsAndIndications:
            return ModelOutput(data=basics_data)
        if model_input.response_format == SetupCareAgent.SetupAndCare:
            return ModelOutput(data=setup_data)
        if model_input.response_format == SafetyPhysiologyAgent.SafetyAndPhysiology:
            return ModelOutput(data=safety_data)
        if model_input.response_format == ContraindicationsAgent.Contraindications:
            return ModelOutput(data=contra_data)
        return ModelOutput(markdown="Some text")

    mock_lite_client.return_value.generate_text.side_effect = mock_generate_text

    result = generator.generate_text("Supine", structured=True)
    assert result.data.pose_basics.position_name == "Supine"
    assert result.markdown is not None


@patch("medical.surgical_pose_info.agentic.surgical_pose_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalPoseInfoGenerator(config)

    # Just mock enough for save to work
    mock_lite_client.return_value.generate_text.return_value = ModelOutput(
        data=BasicsIndicationsAgent.BasicsAndIndications(
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
        )
    )

    # Note: the multi-agent call will fail if we only mock one,
    # so we need the side_effect for any test that calls generate_text
    def mock_generate_text(model_input):
        if model_input.response_format == BasicsIndicationsAgent.BasicsAndIndications:
            return ModelOutput(data=BasicsIndicationsAgent.BasicsAndIndications(
                pose_basics=PoseBasicsModel(position_name="Supine", alternative_names="", category="", common_uses=""),
                indications=PoseIndicationsModel(primary_procedures="", anatomical_access="", specialty_usage="")
            ))
        if model_input.response_format == SetupCareAgent.SetupAndCare:
            return ModelOutput(data=SetupCareAgent.SetupAndCare(
                patient_setup=PatientSetupModel(equipment_needed="", step_by_step_placement="", head_and_neck="", upper_extremities="", lower_extremities="", padding_requirements=""),
                post_operative_care=PostOperativeCareModel(repositioning_care="", monitoring_requirements="")
            ))
        if model_input.response_format == SafetyPhysiologyAgent.SafetyAndPhysiology:
            return ModelOutput(data=SafetyPhysiologyAgent.SafetyAndPhysiology(
                safety_considerations=SafetyConsiderationsModel(pressure_points="", nerve_risks="", prevention_strategies="", check_points=""),
                physiological_effects=PhysiologicalEffectsModel(respiratory_effects="", cardiovascular_effects="", other_physiological_changes="")
            ))
        if model_input.response_format == ContraindicationsAgent.Contraindications:
            return ModelOutput(data=ContraindicationsAgent.Contraindications(
                contraindications_and_modifications=ContraindicationsAndModificationsModel(absolute_contraindications="", relative_contraindications="", modifications_for_obesity="", modifications_for_pediatrics="", modifications_for_elderly="")
            ))
        return ModelOutput(markdown="Info")

    mock_lite_client.return_value.generate_text.side_effect = mock_generate_text

    result = generator.generate_text("Supine")
    generator.save(result, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == result
    assert str(args[1]).endswith("supine")
