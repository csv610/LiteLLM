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
        """Generates surgical tool information using a 3-tier multi-agent system."""
        if not tool or not str(tool).strip():
            raise ValueError("Tool name cannot be empty")

        self.tool = tool
        logger.info(f"Starting 3-tier multi-agent generation for: {tool}")

        try:
            # --- Tier 1: Specialist Stages (JSON) ---
            logger.info("Tier 1: Specialists generating specialized tool data...")
            # 1.1 Technical Expert
            tech_input = ModelInput(
                system_prompt=PromptBuilder.create_technical_expert_system_prompt(),
                user_prompt=PromptBuilder.create_technical_expert_user_prompt(tool),
            )
            tech_report = self.client.generate_text(model_input=tech_input).markdown

            # 1.2 Clinical Specialist
            clinical_input = ModelInput(
                system_prompt=PromptBuilder.create_clinical_specialist_system_prompt(),
                user_prompt=PromptBuilder.create_clinical_specialist_user_prompt(tool),
            )
            clinical_report = self.client.generate_text(model_input=clinical_input).markdown

            # 1.3 Safety & Maintenance
            safety_input = ModelInput(
                system_prompt=PromptBuilder.create_safety_maintenance_specialist_system_prompt(),
                user_prompt=PromptBuilder.create_safety_maintenance_user_prompt(tool),
            )
            safety_report = self.client.generate_text(model_input=safety_input).markdown

            # 1.4 Medical Historian
            history_input = ModelInput(
                system_prompt=PromptBuilder.create_medical_historian_educator_system_prompt(),
                user_prompt=PromptBuilder.create_medical_historian_educator_user_prompt(tool),
            )
            history_report = self.client.generate_text(model_input=history_input).markdown

            specialist_data = f"""
TECHNICAL REPORT:
{tech_report}

CLINICAL REPORT:
{clinical_report}

SAFETY REPORT:
{safety_report}

HISTORY REPORT:
{history_report}
"""

            # --- Tier 2: Compliance Auditor Stage (JSON Audit) ---
            logger.info("Tier 2: Auditor performing quality check...")
            orchestrator_input = ModelInput(
                system_prompt=PromptBuilder.create_orchestrator_system_prompt(),
                user_prompt=PromptBuilder.create_orchestrator_user_prompt(tool, specialist_data),
                response_format=SurgicalToolInfoModel if structured else None,
            )
            audit_res = self.client.generate_text(model_input=orchestrator_input)
            
            if structured:
                audit_json = audit_res.data.model_dump_json(indent=2)
            else:
                audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.info("Tier 3: Output Agent synthesizing final report...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                tool, specialist_data, audit_json
            )
            final_res = self.client.generate_text(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            logger.info(f"✓ Successfully generated 3-tier surgical tool report for {tool}")
            return ModelOutput(data=audit_res.data if structured else None, markdown=final_res.markdown)

        except Exception as e:
            logger.error(f"✗ 3-tier Surgical Tool generation failed: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.tool is None:
            raise ValueError("No tool information available. Call generate_text first.")
        base_filename = f"{self.tool.lower().replace(' ', '_')}_multi_agent"
        return save_model_response(result, output_dir / base_filename)
