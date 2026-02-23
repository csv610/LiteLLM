import logging
from pathlib import Path
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from .surgery_info_models import SurgeryInfoModel, ModelOutput
from .surgery_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)

class SurgeryInfoGenerator:
    """Generates comprehensive surgery information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.surgery = None
        logger.debug(f"Initialized SurgeryInfoGenerator")

    def generate_text(self, surgery: str, structured: bool = False) -> ModelOutput:
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        self.surgery = surgery
        logger.debug(f"Starting surgical procedure information generation for: {surgery}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(surgery),
            response_format=SurgeryInfoModel if structured else None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated surgery information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgery information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.surgery is None:
            raise ValueError("No surgery information available. Call generate_text first.")
        base_filename = f"{self.surgery.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)
