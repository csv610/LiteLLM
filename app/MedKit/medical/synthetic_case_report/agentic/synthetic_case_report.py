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
        """Multi-agent sequential generation: Specialist (JSON) -> Compliance (JSON) -> Output (Markdown)."""
        logger.info(f"🚀 Starting 3-tier multi-agent generation for: {condition}")

        # Step 1: Patient & Presentation Agent (Specialist - JSON)
        logger.debug("Step 1: Patient & Presentation Agent")
        step1_input = ModelInput(
            system_prompt=PromptBuilder.create_patient_presentation_agent_prompt(),
            user_prompt=PromptBuilder.create_patient_presentation_user_prompt(condition),
            response_format=PatientPresentationOutput,
        )
        step1_result = self.client.generate_text(model_input=step1_input)
        step1_data: PatientPresentationOutput = step1_result.data

        # Step 2: Diagnostic & Therapeutic Agent (Specialist - JSON)
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

        # Step 3: Review & Compliance Agent (Auditor - JSON)
        logger.debug("Step 3: Review & Compliance Agent")
        full_context = {
            "presentation": step1_data.model_dump(),
            "diagnostic_therapeutic": step2_data.model_dump(),
        }
        specialist_json = json.dumps(full_context, indent=2)
        
        step3_input = ModelInput(
            system_prompt=PromptBuilder.create_review_synthesis_agent_prompt(),
            user_prompt=PromptBuilder.create_review_synthesis_user_prompt(
                condition, specialist_json
            ),
            response_format=ReviewSynthesisOutput,
        )
        step3_result = self.client.generate_text(model_input=step3_input)
        step3_data: ReviewSynthesisOutput = step3_result.data
        compliance_json = json.dumps(step3_data.model_dump(), indent=2)

        # Step 4: Output Synthesis Agent (Closer - Markdown)
        logger.debug("Step 4: Output Synthesis Agent")
        output_sys, output_user = PromptBuilder.create_output_synthesis_prompts(
            condition, specialist_json, compliance_json
        )
        
        output_input = ModelInput(
            system_prompt=output_sys,
            user_prompt=output_user,
            response_format=None,
        )
        
        final_markdown = self.client.generate_text(model_input=output_input)

        # Assemble Final Model (Optional - for backward compatibility if needed)
        # Note: step3_data now contains audit findings rather than synthesis, 
        # so final_report assembly might need adjustment if still used.
        final_report = None 

        logger.info("✓ Successfully generated 3-tier multi-agent synthetic case report")
        return ModelOutput(data=final_report, markdown=final_markdown)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.condition is None:
            raise ValueError(
                "No condition information available. Call generate_text first."
            )
        base_filename = f"{self.condition.lower().replace(' ', '_')}_casereport"
        return save_model_response(result, output_dir / base_filename)
