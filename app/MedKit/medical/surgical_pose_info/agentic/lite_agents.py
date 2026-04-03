"""
liteagents.py - Unified for surgical_pose_info
"""
from app.MedKit.medical.surgical_pose_info.shared.models import *
from typing import Type
from unittest.mock import patch
from lite.utils import save_model_response
from tqdm import tqdm
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import logging
from lite.lite_client import LiteClient
import pytest
from pathlib import Path
from abc import ABC, abstractmethod
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys

"""Agents for generating surgical position information."""




    PoseBasicsModel,
    PoseIndicationsModel,
    PatientSetupModel,
    PostOperativeCareModel,
    SafetyConsiderationsModel,
    PhysiologicalEffectsModel,
    ContraindicationsAndModificationsModel
)

logger = logging.getLogger(__name__)


class SurgicalPoseAgent(ABC):
    """Base class for surgical position information agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)

    @abstractmethod
    def run(self, position: str) -> BaseModel:
        """Run the agent's task."""
        pass


class BasicsIndicationsAgent(SurgicalPoseAgent):
    """Agent for generating basics and indications for a surgical position."""

    class BasicsAndIndications(BaseModel):
        pose_basics: PoseBasicsModel
        indications: PoseIndicationsModel

    def run(self, position: str) -> BasicsAndIndications:
        logger.info(f"BasicsIndicationsAgent generating info for: {position}")
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_basics_agent_prompt(position),
            response_format=self.BasicsAndIndications,
        )
        return self.client.generate_text(model_input=model_input).data


class SetupCareAgent(SurgicalPoseAgent):
    """Agent for generating setup and care for a surgical position."""

    class SetupAndCare(BaseModel):
        patient_setup: PatientSetupModel
        post_operative_care: PostOperativeCareModel

    def run(self, position: str) -> SetupAndCare:
        logger.info(f"SetupCareAgent generating info for: {position}")
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_setup_agent_prompt(position),
            response_format=self.SetupAndCare,
        )
        return self.client.generate_text(model_input=model_input).data


class SafetyPhysiologyAgent(SurgicalPoseAgent):
    """Agent for generating safety and physiological effects for a surgical position."""

    class SafetyAndPhysiology(BaseModel):
        safety_considerations: SafetyConsiderationsModel
        physiological_effects: PhysiologicalEffectsModel

    def run(self, position: str) -> SafetyAndPhysiology:
        logger.info(f"SafetyPhysiologyAgent generating info for: {position}")
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_safety_physiology_agent_prompt(position),
            response_format=self.SafetyAndPhysiology,
        )
        return self.client.generate_text(model_input=model_input).data


class ContraindicationsAgent(SurgicalPoseAgent):
    """Agent for generating contraindications and modifications for a surgical position."""

    class Contraindications(BaseModel):
        contraindications_and_modifications: ContraindicationsAndModificationsModel

    def run(self, position: str) -> Contraindications:
        logger.info(f"ContraindicationsAgent generating info for: {position}")
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_contraindications_agent_prompt(position),
            response_format=self.Contraindications,
        )
        return self.client.generate_text(model_input=model_input).data

"""Surgical Position Information Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .surgical_pose_info import COMMON_SURGICAL_POSITIONS, SurgicalPoseInfoGenerator
except (ImportError, ValueError):
    from medical.surgical_pose_info.agentic.surgical_pose_info import (
        COMMON_SURGICAL_POSITIONS,
        SurgicalPoseInfoGenerator,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical position information."
    )
    parser.add_argument(
        "pose", nargs="?", help="Position name or file path containing names."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", help="List common surgical positions."
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()

    if args.list:
        print("Common Surgical Positions:")
        for pos in COMMON_SURGICAL_POSITIONS:
            print("- {}".format(pos))
        return 0

    if not args.pose:
        print("Error: 'pose' argument is required unless --list is used.")
        return 1

    configure_logging(
        log_file="surgical_pose_info.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.pose)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.pose]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = SurgicalPoseInfoGenerator(model_config)

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(pose=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    BasicsIndicationsAgent,
    ContraindicationsAgent,
    SafetyPhysiologyAgent,
    SetupCareAgent,
)
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

"""Surgical Position Information Generator.

This module contains the core logic for generating comprehensive surgical position information
using a multi-agentic architecture.
"""



    BasicsIndicationsAgent,
    SetupCareAgent,
    SafetyPhysiologyAgent,
    ContraindicationsAgent
)

logger = logging.getLogger(__name__)

COMMON_SURGICAL_POSITIONS = [
    "Supine (Dorsal Decubitus)",
    "Dorsal Recumbent",
    "Hips-Flexed Supine",
    "Recumbent",
    "Head-Elevated Supine",
    "Sniffing Position",
    "Trendelenburg Position",
    "Reverse Trendelenburg",
    "Lateral (Right/Left)",
    "Lateral Kidney Position",
    "Lithotomy Position",
    "Prone Position",
    "Jackknife Position",
    "Knee-Chest Position",
    "Sims' Position (Left Lateral)",
    "Fowler's Position",
    "High Fowler's",
    "Semi-Fowler's",
    "Orthopneic Position",
    "Knee-Chest",
    "Lloyd-Davies Position",
    "Kraske Position",
    "Modified Lithotomy",
    "Legs-Elevated Supine",
    "Beach Chair Position",
    "Sitting Position",
    "Lateral Decubitus",
    "Oblique Position",
    "Reverse Trendelenburg with Head Up",
    "Rotational Bed Position",
    "Frog-Leg Position",
    "Cradle Position",
    "Swaddled Supine",
    "Recovery Position",
    "Shock Position",
    "Neutral Spine Immobilization Position",
]


class SurgicalPoseInfoGenerator:
    """Generates comprehensive surgical position information using a multi-agentic approach."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.basics_agent = BasicsIndicationsAgent(model_config)
        self.setup_agent = SetupCareAgent(model_config)
        self.safety_agent = SafetyPhysiologyAgent(model_config)
        self.contra_agent = ContraindicationsAgent(model_config)
        self.pose = None
        logger.debug("Initialized SurgicalPoseInfoGenerator (Multi-Agentic)")

    def generate_text(self, pose: str, structured: bool = False) -> ModelOutput:
        """Generates surgical position information using a 3-tier agent system."""
        if not pose or not str(pose).strip():
            raise ValueError("Position name cannot be empty")

        self.pose = pose
        logger.info(f"Starting 3-tier generation for: {pose}")

        try:
            # 1. Specialist Stage (JSON - Run in parallel)
            logger.debug("Tier 1: Specialists generating raw positioning data...")
            with ThreadPoolExecutor(max_workers=4) as executor:
                future_basics = executor.submit(self.basics_agent.run, pose)
                future_setup = executor.submit(self.setup_agent.run, pose)
                future_safety = executor.submit(self.safety_agent.run, pose)
                future_contra = executor.submit(self.contra_agent.run, pose)

                basics_res = future_basics.result()
                setup_res = future_setup.result()
                safety_res = future_safety.result()
                contra_res = future_contra.result()

            spec_data = SurgicalPoseInfoModel(
                pose_basics=basics_res.pose_basics,
                indications=basics_res.indications,
                patient_setup=setup_res.patient_setup,
                post_operative_care=setup_res.post_operative_care,
                safety_considerations=safety_res.safety_considerations,
                physiological_effects=safety_res.physiological_effects,
                contraindications_and_modifications=contra_res.contraindications_and_modifications
            )
            spec_json = spec_data.model_dump_json(indent=2)

            # 2. Auditor Stage (JSON Audit)
            logger.debug("Tier 2: Auditor performing safety check...")
            audit_sys, audit_usr = self.basics_agent.prompts.create_compliance_auditor_prompts(pose, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.basics_agent.client.generate_text(model_input=audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("Tier 3: Output Agent synthesizing final surgical report...")
            out_sys, out_usr = self.basics_agent.prompts.create_output_synthesis_prompts(pose, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.basics_agent.client.generate_text(model_input=out_input)

            logger.info("✓ Successfully generated 3-tier surgical position information")
            return ModelOutput(
                data=spec_data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Surgical generation failed: {e}")
            raise

    def _to_markdown(self, data: SurgicalPoseInfoModel) -> str:
        """Converts structured data to a markdown report."""
        report = [
            f"# Surgical Position: {data.pose_basics.position_name}",
            f"
## Basics",
            f"- **Alternative Names**: {data.pose_basics.alternative_names}",
            f"- **Category**: {data.pose_basics.category}",
            f"- **Common Uses**: {data.pose_basics.common_uses}",
            f"
## Indications",
            f"- **Primary Procedures**: {data.indications.primary_procedures}",
            f"- **Anatomical Access**: {data.indications.anatomical_access}",
            f"- **Specialty Usage**: {data.indications.specialty_usage}",
            f"
## Patient Setup",
            f"- **Equipment Needed**: {data.patient_setup.equipment_needed}",
            f"- **Placement**: {data.patient_setup.step_by_step_placement}",
            f"- **Head & Neck**: {data.patient_setup.head_and_neck}",
            f"- **Upper Extremities**: {data.patient_setup.upper_extremities}",
            f"- **Lower Extremities**: {data.patient_setup.lower_extremities}",
            f"- **Padding**: {data.patient_setup.padding_requirements}",
            f"
## Safety & Physiology",
            f"- **Pressure Points**: {data.safety_considerations.pressure_points}",
            f"- **Nerve Risks**: {data.safety_considerations.nerve_risks}",
            f"- **Prevention**: {data.safety_considerations.prevention_strategies}",
            f"- **Safety Checks**: {data.safety_considerations.check_points}",
            f"- **Respiratory Effects**: {data.physiological_effects.respiratory_effects}",
            f"- **Cardiovascular Effects**: {data.physiological_effects.cardiovascular_effects}",
            f"
## Contraindications & Modifications",
            f"- **Absolute**: {data.contraindications_and_modifications.absolute_contraindications}",
            f"- **Relative**: {data.contraindications_and_modifications.relative_contraindications}",
            f"- **Obesity**: {data.contraindications_and_modifications.modifications_for_obesity}",
            f"- **Pediatrics**: {data.contraindications_and_modifications.modifications_for_pediatrics}",
            f"- **Elderly**: {data.contraindications_and_modifications.modifications_for_elderly}",
            f"
## Post-Operative Care",
            f"- **Repositioning Care**: {data.post_operative_care.repositioning_care}",
            f"- **Monitoring**: {data.post_operative_care.monitoring_requirements}",
        ]
        return "
".join(report)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the surgical position information to a file."""
        if self.pose is None:
            raise ValueError(
                "No position information available. Call generate_text first."
            )

        base_filename = f"{self.pose.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)