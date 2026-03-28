"""Agents for generating surgical position information."""

import logging
from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

from .surgical_pose_info_models import (
    PoseBasicsModel,
    PoseIndicationsModel,
    PatientSetupModel,
    PostOperativeCareModel,
    SafetyConsiderationsModel,
    PhysiologicalEffectsModel,
    ContraindicationsAndModificationsModel
)
from .surgical_pose_info_prompts import PromptBuilder

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
