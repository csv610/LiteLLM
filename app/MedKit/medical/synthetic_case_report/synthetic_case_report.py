import logging
from pathlib import Path
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from .synthetic_case_report_models import SyntheticCaseReportModel, ModelOutput
from .synthetic_case_report_prompts import PromptBuilder

logger = logging.getLogger(__name__)

class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.condition = None
        logger.debug(f"Initialized SyntheticCaseReportGenerator")

    def generate_text(self, condition: str, structured: bool = False) -> ModelOutput:
        if not condition or not str(condition).strip():
            raise ValueError("Condition name cannot be empty")

        self.condition = condition
        logger.debug(f"Starting synthetic case report generation for: {condition}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(condition),
            response_format=SyntheticCaseReportModel if structured else None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated synthetic case report")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating synthetic case report: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.condition is None:
            raise ValueError("No condition information available. Call generate_text first.")
        base_filename = f"{self.condition.lower().replace(' ', '_')}_casereport"
        return save_model_response(result, output_dir / base_filename)
