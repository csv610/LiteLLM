import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .surgery_info_models import (
    ClinicalBackgroundOutput,
    MedicalPolicyEducationOutput,
    ModelOutput,
    MultiAgentOutput,
    PerioperativeCareOutput,
    SurgicalTechnicalOutput,
    SurgeryInfoModel,
)
from .surgery_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgeryInfoGenerator:
    """Generates comprehensive surgery information using a parallelized multi-agent approach."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.surgery = None
        logger.debug("Initialized Parallel Multi-Agent SurgeryInfoGenerator")

    def _run_agent(
        self, system_prompt: str, user_prompt: str, response_format: Optional[type] = None
    ) -> ModelOutput:
        """Helper to run a single agent's task."""
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Agent failed: {e}")
            return None

    def generate_multi_agent(self, surgery: str) -> ModelOutput:
        """Generates surgical information using multiple focused agents in parallel."""
        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        self.surgery = surgery
        logger.info(f"🚀 Starting parallel multi-agent generation for: {surgery}")

        user_prompt = PromptBuilder.create_user_prompt(surgery)

        # Define agent tasks for parallel execution
        agent_tasks = {
            "clinical": (
                PromptBuilder.create_clinical_background_system_prompt(),
                user_prompt,
                ClinicalBackgroundOutput,
            ),
            "perioperative": (
                PromptBuilder.create_perioperative_care_system_prompt(),
                user_prompt,
                PerioperativeCareOutput,
            ),
            "technical": (
                PromptBuilder.create_surgical_technical_system_prompt(),
                user_prompt,
                SurgicalTechnicalOutput,
            ),
            "policy": (
                PromptBuilder.create_medical_policy_education_system_prompt(),
                user_prompt,
                MedicalPolicyEducationOutput,
            ),
        }

        # Run worker agents in parallel
        agent_results = {}
        with ThreadPoolExecutor(max_workers=len(agent_tasks)) as executor:
            future_to_agent = {
                executor.submit(self._run_agent, *task): name
                for name, task in agent_tasks.items()
            }
            for future in future_to_agent:
                agent_name = future_to_agent[future]
                agent_results[agent_name] = future.result()

        clinical_data = agent_results.get("clinical").data if agent_results.get("clinical") else None
        perioperative_data = agent_results.get("perioperative").data if agent_results.get("perioperative") else None
        technical_data = agent_results.get("technical").data if agent_results.get("technical") else None
        policy_data = agent_results.get("policy").data if agent_results.get("policy") else None

        multi_agent_data = MultiAgentOutput(
            clinical_background=clinical_data,
            perioperative_care=perioperative_data,
            surgical_technical=technical_data,
            medical_policy_education=policy_data,
        )

        # Combine into a single SurgeryInfoModel
        combined_data = None
        if clinical_data and perioperative_data and technical_data and policy_data:
            combined_data = SurgeryInfoModel(
                metadata=clinical_data.metadata,
                background=clinical_data.background,
                indications=clinical_data.indications,
                alternatives=clinical_data.alternatives,
                preoperative=perioperative_data.preoperative,
                postoperative=perioperative_data.postoperative,
                recovery_outcomes=perioperative_data.recovery_outcomes,
                follow_up=perioperative_data.follow_up,
                operative=technical_data.operative,
                operative_risks=technical_data.operative_risks,
                technical=technical_data.technical,
                special_populations=policy_data.special_populations,
                research=policy_data.research,
                evidence=policy_data.evidence,
                education=policy_data.education,
                cost_and_insurance=policy_data.cost_and_insurance,
            )

        # Step 5: Synthesizer Agent - Create a cohesive Markdown report
        markdown_report = None
        if combined_data:
            logger.info("  - Running Synthesizer Agent...")
            # Prepare data summary for the synthesizer
            data_summary = combined_data.model_dump_json(indent=2)
            synth_user_prompt = PromptBuilder.create_synthesizer_user_prompt(
                surgery, data_summary
            )
            synth_result = self._run_agent(
                PromptBuilder.create_synthesizer_system_prompt(),
                synth_user_prompt,
                None,  # Markdown output
            )
            if synth_result:
                markdown_report = synth_result.markdown

        logger.info("✓ Successfully completed multi-agent generation")
        return ModelOutput(
            data=combined_data,
            multi_agent_data=multi_agent_data,
            markdown=markdown_report,
        )

    def generate_text(self, surgery: str, structured: bool = False) -> ModelOutput:
        """Generates surgery information. Defaults to multi-agent if structured."""
        if structured:
            return self.generate_multi_agent(surgery)

        if not surgery or not str(surgery).strip():
            raise ValueError("Surgery name cannot be empty")

        self.surgery = surgery
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_clinical_background_system_prompt(),  # Use first agent's prompt for general text
            user_prompt=PromptBuilder.create_user_prompt(surgery),
            response_format=None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            return result
        except Exception as e:
            logger.error(f"Error generating surgery information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.surgery is None:
            raise ValueError(
                "No surgery information available. Call generate_text first."
            )
        base_filename = f"{self.surgery.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)
