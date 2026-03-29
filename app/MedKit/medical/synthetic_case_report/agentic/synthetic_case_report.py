import logging
import json
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .synthetic_case_report_models import (
    DiagnosticTherapeuticOutput,
    ModelOutput,
    PatientPresentationOutput,
    ReviewSynthesisOutput,
    SyntheticCaseReportModel,
)
from .synthetic_case_report_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SyntheticCaseReportGenerator:
    """Generates synthetic medical case reports based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.condition = None
        logger.debug("Initialized SyntheticCaseReportGenerator")

    def generate_text(self, condition: str, structured: bool = False) -> ModelOutput:
        if not condition or not str(condition).strip():
            raise ValueError("Condition name cannot be empty")

        self.condition = condition
        logger.debug(f"Starting synthetic case report generation for: {condition}")

        if not structured:
            return self._generate_single_agent(condition)

        return self._generate_multi_agent(condition)

    def _generate_single_agent(self, condition: str) -> ModelOutput:
        """Original single-agent generation for unstructured output."""
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(condition),
            response_format=None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated synthetic case report (single agent)")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating synthetic case report: {e}")
            raise

    def _generate_multi_agent(self, condition: str) -> ModelOutput:
        """Multi-agent sequential generation for structured output."""
        logger.info(f"🚀 Starting multi-agent generation for: {condition}")

        # Step 1: Patient & Presentation Agent
        logger.debug("Step 1: Patient & Presentation Agent")
        step1_input = ModelInput(
            system_prompt=PromptBuilder.create_patient_presentation_agent_prompt(),
            user_prompt=PromptBuilder.create_patient_presentation_user_prompt(condition),
            response_format=PatientPresentationOutput,
        )
        step1_result = self.client.generate_text(model_input=step1_input)
        step1_data: PatientPresentationOutput = step1_result.data

        # Step 2: Diagnostic & Therapeutic Agent
        logger.debug("Step 2: Diagnostic & Therapeutic Agent")
        step2_input = ModelInput(
            system_prompt=PromptBuilder.create_diagnostic_therapeutic_agent_prompt(),
            user_prompt=PromptBuilder.create_diagnostic_therapeutic_user_prompt(
                condition, json.dumps(step1_data.model_dump(), indent=2)
            ),
            response_format=DiagnosticTherapeuticOutput,
        )
        step2_result = self.client.generate_text(model_input=step2_input)
        step2_data: DiagnosticTherapeuticOutput = step2_result.data

        # Step 3: Review & Synthesis Agent
        logger.debug("Step 3: Review & Synthesis Agent")
        full_context = {
            "presentation": step1_data.model_dump(),
            "diagnostic_therapeutic": step2_data.model_dump(),
        }
        step3_input = ModelInput(
            system_prompt=PromptBuilder.create_review_synthesis_agent_prompt(),
            user_prompt=PromptBuilder.create_review_synthesis_user_prompt(
                condition, json.dumps(full_context, indent=2)
            ),
            response_format=ReviewSynthesisOutput,
        )
        step3_result = self.client.generate_text(model_input=step3_input)
        step3_data: ReviewSynthesisOutput = step3_result.data

        # Assemble Final Model
        logger.debug("Step 4: Assembling final model")
        final_report = SyntheticCaseReportModel(
            metadata=step3_data.metadata,
            patient_information=step1_data.patient_information,
            clinical_findings=step1_data.clinical_findings,
            timeline=step1_data.timeline,
            diagnostic_assessment=step2_data.diagnostic_assessment,
            therapeutic_interventions=step2_data.therapeutic_interventions,
            follow_up_and_outcomes=step2_data.follow_up_and_outcomes,
            discussion=step3_data.discussion,
            patient_perspective=step3_data.patient_perspective,
            informed_consent=step3_data.informed_consent,
        )

        logger.info("✓ Successfully generated multi-agent synthetic case report")
        return ModelOutput(data=final_report, markdown=None)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.condition is None:
            raise ValueError(
                "No condition information available. Call generate_text first."
            )
        base_filename = f"{self.condition.lower().replace(' ', '_')}_casereport"
        return save_model_response(result, output_dir / base_filename)
