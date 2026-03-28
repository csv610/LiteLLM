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
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        self.target = surgery
        logger.debug(f"Starting surgical tray information generation for: {surgery}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(surgery),
            response_format=SurgicalTrayModel if structured else None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated surgical tray information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical tray information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.target is None:
            raise ValueError("No information available. Call generate_text first.")
        base_filename = f"{self.target.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)
