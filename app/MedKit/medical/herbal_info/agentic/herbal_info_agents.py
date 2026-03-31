"""
Specialized agents for herbal information generation.
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Type, Dict, Any
from pydantic import BaseModel, Field

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

try:
    from .herbal_info_models import (
        HerbalMetadataModel,
        HerbalClassificationModel,
        HerbalBackgroundModel,
        HerbalMechanismModel,
        HerbalEvidenceModel,
        HerbalResearchModel,
        UsageAndAdministrationModel,
        EfficacyModel,
        AlternativesModel,
        SafetyInformationModel,
        SpecialInstructionsModel,
        SpecialPopulationsModel,
        HerbalEducationModel,
        CostAndAvailabilityModel,
        ModelOutput,
    )
except (ImportError, ValueError):
    try:
        from herbal_info_models import (
            HerbalMetadataModel,
            HerbalClassificationModel,
            HerbalBackgroundModel,
            HerbalMechanismModel,
            HerbalEvidenceModel,
            HerbalResearchModel,
            UsageAndAdministrationModel,
            EfficacyModel,
            AlternativesModel,
            SafetyInformationModel,
            SpecialInstructionsModel,
            SpecialPopulationsModel,
            HerbalEducationModel,
            CostAndAvailabilityModel,
            ModelOutput,
        )
    except ImportError:
        from medical.herbal_info.agentic.herbal_info_models import (
            HerbalMetadataModel,
            HerbalClassificationModel,
            HerbalBackgroundModel,
            HerbalMechanismModel,
            HerbalEvidenceModel,
            HerbalResearchModel,
            UsageAndAdministrationModel,
            EfficacyModel,
            AlternativesModel,
            SafetyInformationModel,
            SpecialInstructionsModel,
            SpecialPopulationsModel,
            HerbalEducationModel,
            CostAndAvailabilityModel,
            ModelOutput,
        )

logger = logging.getLogger(__name__)

# Define output models for each agent
class BotanicalOutput(BaseModel):
    metadata: HerbalMetadataModel
    classification: HerbalClassificationModel
    background: HerbalBackgroundModel

class PharmacologicalOutput(BaseModel):
    mechanism: HerbalMechanismModel
    evidence: HerbalEvidenceModel
    research: HerbalResearchModel

class ClinicalOutput(BaseModel):
    usage_and_administration: UsageAndAdministrationModel
    efficacy: EfficacyModel
    alternatives: AlternativesModel

class SafetyOutput(BaseModel):
    safety: SafetyInformationModel
    special_instructions: SpecialInstructionsModel
    special_populations: SpecialPopulationsModel

class EducatorOutput(BaseModel):
    education: HerbalEducationModel
    cost_and_availability: CostAndAvailabilityModel

class BaseAgent:
    """Base class for specialized herbal agents."""
    
    def __init__(self, model_config: ModelConfig, client: LiteClient):
        self.model_config = model_config
        self.client = client
        self.agent_name = self.__class__.__name__

    def get_system_prompt(self) -> str:
        raise NotImplementedError

    def get_user_prompt(self, herb: str) -> str:
        raise NotImplementedError

    def get_response_format(self, structured: bool = False) -> Optional[Type[BaseModel]]:
        if structured:
            return self._get_response_format()
        return None

    def _get_response_format(self) -> Type[BaseModel]:
        raise NotImplementedError

    def generate(self, herb: str, structured: bool = False) -> ModelOutput:
        """Generates agent-specific herbal information."""
        logger.debug(f"{self.agent_name} starting for: {herb}")
        
        model_input = ModelInput(
            system_prompt=self.get_system_prompt(),
            user_prompt=self.get_user_prompt(herb),
            response_format=self.get_response_format(structured),
        )
        
        return self.client.generate_text(model_input=model_input)

class BotanicalAgent(BaseAgent):
    """Specializes in botanical classification and history."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert Botanist and Ethnobotanist. 
Focus exclusively on botanical identification, classification, origin, and historical context of herbs.
Be precise with scientific names and plant families."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide botanical metadata, classification, and background for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return BotanicalOutput

class PharmacologicalAgent(BaseAgent):
    """Specializes in mechanisms and research."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert Pharmacognosist and Clinical Researcher. 
Focus on chemical mechanisms of action, active constituents, and modern clinical evidence."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide pharmacological mechanism, evidence-based data, and current research for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return PharmacologicalOutput

class SafetyAgent(BaseAgent):
    """Specializes in safety and toxicology."""
    
    def get_system_prompt(self) -> str:
        return """You are a specialized Herbal Safety and Toxicology Expert. 
Focus strictly on contraindications, drug interactions, and safety considerations for special populations."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide comprehensive safety information, special population guidance, and toxicology warnings for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return SafetyOutput

class ClinicalAgent(BaseAgent):
    """Specializes in usage and efficacy."""
    
    def get_system_prompt(self) -> str:
        return """You are an experienced Clinical Herbalist. 
Focus on practical administration, dosage, clinical efficacy, and herbal/non-herbal alternatives."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide clinical usage, administration guidance, efficacy outcomes, and alternatives for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return ClinicalOutput

class EducatorAgent(BaseAgent):
    """Specializes in patient communication."""
    
    def get_system_prompt(self) -> str:
        return """You are a Health Educator and Consumer Advocate. 
Focus on explaining concepts in plain language, key takeaways, sustainability, and market availability."""

    def get_user_prompt(self, herb: str) -> str:
        return f"Provide patient education content, cost, and availability information for: {herb}"

    def _get_response_format(self) -> Type[BaseModel]:
        return EducatorOutput
