"""Surgical Position Information Generator.

This module contains the core logic for generating comprehensive surgical position information
using a multi-agentic architecture.
"""

import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from .surgical_pose_info_models import ModelOutput, SurgicalPoseInfoModel
from .surgical_pose_info_agents import (
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
            f"\n## Basics",
            f"- **Alternative Names**: {data.pose_basics.alternative_names}",
            f"- **Category**: {data.pose_basics.category}",
            f"- **Common Uses**: {data.pose_basics.common_uses}",
            f"\n## Indications",
            f"- **Primary Procedures**: {data.indications.primary_procedures}",
            f"- **Anatomical Access**: {data.indications.anatomical_access}",
            f"- **Specialty Usage**: {data.indications.specialty_usage}",
            f"\n## Patient Setup",
            f"- **Equipment Needed**: {data.patient_setup.equipment_needed}",
            f"- **Placement**: {data.patient_setup.step_by_step_placement}",
            f"- **Head & Neck**: {data.patient_setup.head_and_neck}",
            f"- **Upper Extremities**: {data.patient_setup.upper_extremities}",
            f"- **Lower Extremities**: {data.patient_setup.lower_extremities}",
            f"- **Padding**: {data.patient_setup.padding_requirements}",
            f"\n## Safety & Physiology",
            f"- **Pressure Points**: {data.safety_considerations.pressure_points}",
            f"- **Nerve Risks**: {data.safety_considerations.nerve_risks}",
            f"- **Prevention**: {data.safety_considerations.prevention_strategies}",
            f"- **Safety Checks**: {data.safety_considerations.check_points}",
            f"- **Respiratory Effects**: {data.physiological_effects.respiratory_effects}",
            f"- **Cardiovascular Effects**: {data.physiological_effects.cardiovascular_effects}",
            f"\n## Contraindications & Modifications",
            f"- **Absolute**: {data.contraindications_and_modifications.absolute_contraindications}",
            f"- **Relative**: {data.contraindications_and_modifications.relative_contraindications}",
            f"- **Obesity**: {data.contraindications_and_modifications.modifications_for_obesity}",
            f"- **Pediatrics**: {data.contraindications_and_modifications.modifications_for_pediatrics}",
            f"- **Elderly**: {data.contraindications_and_modifications.modifications_for_elderly}",
            f"\n## Post-Operative Care",
            f"- **Repositioning Care**: {data.post_operative_care.repositioning_care}",
            f"- **Monitoring**: {data.post_operative_care.monitoring_requirements}",
        ]
        return "\n".join(report)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the surgical position information to a file."""
        if self.pose is None:
            raise ValueError(
                "No position information available. Call generate_text first."
            )

        base_filename = f"{self.pose.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)
