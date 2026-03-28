import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .surgical_tool_info_models import ModelOutput, SurgicalToolInfoModel
    from .surgical_tool_info_prompts import PromptBuilder
except (ImportError, ValueError):
    from surgical_tool_info_models import ModelOutput, SurgicalToolInfoModel
    from surgical_tool_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgicalToolInfoGenerator:
    """Generates comprehensive surgical tool information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.tool = None
        logger.debug("Initialized SurgicalToolInfoGenerator")

    def generate_text(self, tool: str, structured: bool = False) -> ModelOutput:
        if not tool or not str(tool).strip():
            raise ValueError("Tool name cannot be empty")

        self.tool = tool
        logger.debug(f"Starting surgical tool information generation for: {tool}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_technical_expert_system_prompt(),  # Fallback to technical expert if not multi-agent
            user_prompt=PromptBuilder.create_technical_expert_user_prompt(tool),
            response_format=SurgicalToolInfoModel if structured else None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated surgical tool information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical tool information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.tool is None:
            raise ValueError("No tool information available. Call generate_text first.")
        base_filename = f"{self.tool.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)


class MultiAgentSurgicalToolInfoGenerator:
    """Generates comprehensive surgical tool information using multiple specialized agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.tool = None
        logger.debug("Initialized MultiAgentSurgicalToolInfoGenerator")

    def generate_text(self, tool: str, structured: bool = False) -> ModelOutput:
        if not tool or not str(tool).strip():
            raise ValueError("Tool name cannot be empty")

        self.tool = tool
        logger.info(f"Starting multi-agent surgical tool information generation for: {tool}")

        # 1. Technical Expert Agent
        logger.info("  - Invoking Technical Expert Agent...")
        tech_input = ModelInput(
            system_prompt=PromptBuilder.create_technical_expert_system_prompt(),
            user_prompt=PromptBuilder.create_technical_expert_user_prompt(tool),
        )
        tech_report = self.client.generate_text(model_input=tech_input).markdown

        # 2. Clinical Specialist Agent
        logger.info("  - Invoking Clinical Specialist Agent...")
        clinical_input = ModelInput(
            system_prompt=PromptBuilder.create_clinical_specialist_system_prompt(),
            user_prompt=PromptBuilder.create_clinical_specialist_user_prompt(tool),
        )
        clinical_report = self.client.generate_text(model_input=clinical_input).markdown

        # 3. Safety & Maintenance Specialist Agent
        logger.info("  - Invoking Safety & Maintenance Specialist Agent...")
        safety_input = ModelInput(
            system_prompt=PromptBuilder.create_safety_maintenance_specialist_system_prompt(),
            user_prompt=PromptBuilder.create_safety_maintenance_user_prompt(tool),
        )
        safety_report = self.client.generate_text(model_input=safety_input).markdown

        # 4. Medical Historian & Educator Agent
        logger.info("  - Invoking Medical Historian & Educator Agent...")
        history_input = ModelInput(
            system_prompt=PromptBuilder.create_medical_historian_educator_system_prompt(),
            user_prompt=PromptBuilder.create_medical_historian_educator_user_prompt(tool),
        )
        history_report = self.client.generate_text(model_input=history_input).markdown

        # 5. Orchestrator Agent (Synthesis)
        logger.info("  - Invoking Orchestrator Agent for synthesis...")
        combined_reports = f"""
TECHNICAL EXPERT REPORT:
{tech_report}

CLINICAL SPECIALIST REPORT:
{clinical_report}

SAFETY & MAINTENANCE SPECIALIST REPORT:
{safety_report}

MEDICAL HISTORIAN & EDUCATOR REPORT:
{history_report}
"""
        orchestrator_input = ModelInput(
            system_prompt=PromptBuilder.create_orchestrator_system_prompt(),
            user_prompt=PromptBuilder.create_orchestrator_user_prompt(tool, combined_reports),
            response_format=SurgicalToolInfoModel if structured else None,
        )

        try:
            result = self.client.generate_text(model_input=orchestrator_input)
            logger.info(f"✓ Successfully generated multi-agent surgical tool information for {tool}")
            return result
        except Exception as e:
            logger.error(f"✗ Error during multi-agent synthesis: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.tool is None:
            raise ValueError("No tool information available. Call generate_text first.")
        base_filename = f"{self.tool.lower().replace(' ', '_')}_multi_agent"
        return save_model_response(result, output_dir / base_filename)
