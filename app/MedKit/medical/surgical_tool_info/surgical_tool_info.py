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
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(tool),
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
