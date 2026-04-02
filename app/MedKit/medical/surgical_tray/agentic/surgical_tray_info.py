import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .surgical_tray_info_models import ModelOutput, SurgicalTrayModel
    from .surgical_tray_info_prompts import PromptBuilder
except (ImportError, ValueError):
    from surgical_tray_info_models import ModelOutput, SurgicalTrayModel
    from surgical_tray_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgicalTrayGenerator:
    """Generates comprehensive surgical tray information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.target = None
        logger.debug("Initialized SurgicalTrayGenerator")

    def generate_text(self, surgery: str, structured: bool = False) -> ModelOutput:
        """Generates surgical tray information using a 3-tier agent system."""
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        self.target = surgery
        logger.info(f"Starting 3-tier surgical tray generation for: {surgery}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("[Specialist] Generating tray list...")
            spec_input = ModelInput(
                system_prompt=PromptBuilder.create_system_prompt(),
                user_prompt=PromptBuilder.create_user_prompt(surgery),
                response_format=SurgicalTrayModel if structured else None,
            )
            spec_res = self.client.generate_text(model_input=spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("[Auditor] Auditing tray accuracy...")
            audit_sys, audit_usr = PromptBuilder.create_tray_auditor_prompts(surgery, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.client.generate_text(model_input=audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("[Output] Synthesizing final tray report...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(surgery, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.client.generate_text(model_input=out_input)

            logger.info("✓ Successfully generated 3-tier surgical tray information")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Surgical Tray generation failed: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.target is None:
            raise ValueError("No information available. Call generate_text first.")
        base_filename = f"{self.target.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)
