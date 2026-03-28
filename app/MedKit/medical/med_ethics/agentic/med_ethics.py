#!/usr/bin/env python3
"""
Medical Ethics module.

This module provides the core MedEthicsGenerator class for generating
comprehensive medical ethics analysis based on provided configuration.
"""

import logging
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .med_ethics_models import (
        AnalystOutput,
        ComplianceOutput,
        EthicalAnalysisModel,
        ModelOutput,
        SafetyCheckModel,
    )
    from .med_ethics_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.med_ethics.agentic.med_ethics_models import (
        AnalystOutput,
        ComplianceOutput,
        EthicalAnalysisModel,
        ModelOutput,
        SafetyCheckModel,
    )
    from medical.med_ethics.agentic.med_ethics_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for agents."""

    def __init__(self, client: LiteClient):
        self.client = client

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        response = self.client.generate_text(model_input=model_input)

        if isinstance(response, ModelOutput):
            return response
        elif isinstance(response, (EthicalAnalysisModel, AnalystOutput, ComplianceOutput)):
            return ModelOutput(data=response)
        elif isinstance(response, str):
            return ModelOutput(markdown=response)
        else:
            return ModelOutput(markdown=str(response))


class AnalystAgent(BaseAgent):
    """Ethical analysis specialist agent."""

    def analyze(self, question: str, structured: bool = False) -> ModelOutput:
        logger.debug(f"AnalystAgent: Analyzing scenario: {question[:50]}...")
        system_prompt = PromptBuilder.create_analyst_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(question)

        response_format = None
        if structured:
            response_format = AnalystOutput

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        return self.ask_llm(model_input)


class ComplianceAgent(BaseAgent):
    """Compliance and legal specialist agent."""

    def check_compliance(self, question: str, structured: bool = False) -> ModelOutput:
        logger.debug(f"ComplianceAgent: Checking compliance for: {question[:50]}...")
        system_prompt = PromptBuilder.create_compliance_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(question)

        response_format = None
        if structured:
            response_format = ComplianceOutput

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        return self.ask_llm(model_input)


class SynthesisAgent(BaseAgent):
    """Agent for synthesizing reports into a final document."""

    def synthesize(
        self,
        question: str,
        analyst_output: ModelOutput,
        compliance_output: ModelOutput,
        structured: bool = False,
    ) -> ModelOutput:
        logger.debug(f"SynthesisAgent: Synthesizing final report...")
        system_prompt = PromptBuilder.create_synthesis_system_prompt()

        context = f"ANALYST REPORT:\n{analyst_output.markdown or analyst_output.data}\n\nCOMPLIANCE REPORT:\n{compliance_output.markdown or compliance_output.data}"
        user_prompt = PromptBuilder.create_user_prompt(question, context=context)

        response_format = None
        if structured:
            response_format = EthicalAnalysisModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        return self.ask_llm(model_input)


class SafetyCriticAgent(BaseAgent):
    """Agent for reviewing reports for safety and accuracy."""

    def audit(
        self, question: str, synthesized_report: ModelOutput, structured: bool = False
    ) -> ModelOutput:
        logger.debug("SafetyCriticAgent: Auditing final report...")
        system_prompt = PromptBuilder.create_safety_critic_system_prompt()

        context = f"FINAL SYNTHESIZED REPORT:\n{synthesized_report.markdown or synthesized_report.data}"
        user_prompt = PromptBuilder.create_user_prompt(question, context=context)

        response_format = None
        if structured:
            response_format = SafetyCheckModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        return self.ask_llm(model_input)


class MedEthicalQA:
    """Orchestrates multiple agents to generate medical ethics analysis."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the agents."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.analyst = AnalystAgent(self.client)
        self.compliance = ComplianceAgent(self.client)
        self.synthesizer = SynthesisAgent(self.client)
        self.safety_critic = SafetyCriticAgent(self.client)
        self.question = None
        logger.debug("Initialized MedEthicalQA with multi-agent architecture")

    def generate_text(self, question: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive medical ethics analysis using multiple agents."""
        if not question or not str(question).strip():
            raise ValueError("Medical ethics question or scenario cannot be empty")

        self.question = question

        # 1. Get ethical analysis
        analyst_result = self.analyst.analyze(question, structured=structured)

        # 2. Get compliance check
        compliance_result = self.compliance.check_compliance(
            question, structured=structured
        )

        # 3. Synthesize the final report
        final_result = self.synthesizer.synthesize(
            question, analyst_result, compliance_result, structured=structured
        )

        # 4. Audit for safety
        try:
            safety_result = self.safety_critic.audit(
                question, final_result, structured=structured
            )
            logger.debug("✓ Successfully audited analysis for safety")

            if structured and safety_result.data and not safety_result.data.passed:
                logger.warning("! Safety audit flagged issues in the report")

            return final_result
        except Exception as e:
            logger.error(f"✗ Error during safety audit: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical ethics analysis to a file (JSON if structured, Markdown otherwise)."""
        if self.question is None:
            raise ValueError(
                "No medical ethics question available. Call generate_text first."
            )

        import re

        if result.data:
            # Structured output - Save as JSON using the title for filename
            title = getattr(result.data, "case_title", None) or self.question[:50]
            sanitized_title = (
                re.sub(r"[^\w\s-]", "", title).strip().lower().replace(" ", "_")
            )
            logger.info(
                f"✓ Saving structured analysis to {output_dir / sanitized_title}.json"
            )
            return save_model_response(result, output_dir / sanitized_title)

        # Markdown output
        md_content = result.markdown
        if not md_content:
            raise ValueError("No content to save.")

        first_line = md_content.split("\n")[0].strip("*# ")
        sanitized_title = (
            re.sub(r"[^\w\s-]", "", first_line).strip().lower().replace(" ", "_")
        )

        filename = f"{sanitized_title}.md"
        file_path = output_dir / filename

        with open(file_path, "w") as f:
            f.write(md_content)

        logger.info(f"✓ Saved markdown analysis to {file_path}")
        return file_path
