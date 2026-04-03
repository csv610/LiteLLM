"""
liteagents.py - Unified for med_ethics
"""
from unittest.mock import patch
from lite.utils import save_model_response
from tqdm import tqdm
import logging
from lite.lite_client import LiteClient
import pytest
from pathlib import Path
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys
from app.MedKit.medical.med_ethics.shared.models import *

"""Medical Ethics Analysis Generator CLI."""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .med_ethics import MedEthicalQA
except (ImportError, ValueError):
    from medical.med_ethics.agentic.med_ethics import MedEthicalQA

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical ethics analysis."
    )
    parser.add_argument(
        "question",
        help="Medical ethics question, scenario, or file path containing them.",
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="med_ethics.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.question)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.question]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedEthicalQA(model_config)

        for item in tqdm(items, desc="Analyzing"):
            result = generator.generate_text(question=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

#!/usr/bin/env python3
"""
Medical Ethics module.

This module provides the core MedEthicsGenerator class for generating
comprehensive medical ethics analysis based on provided configuration.
"""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


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

        context = f"ANALYST REPORT:
{analyst_output.markdown or analyst_output.data}

COMPLIANCE REPORT:
{compliance_output.markdown or compliance_output.data}"
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

        context = f"FINAL SYNTHESIZED REPORT:
{synthesized_report.markdown or synthesized_report.data}"
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
        """Generate comprehensive medical ethics analysis using a 3-tier system."""
        if not question or not str(question).strip():
            raise ValueError("Medical ethics question or scenario cannot be empty")

        self.question = question
        logger.info(f"Starting 3-tier ethical analysis for: {question}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("Tier 1: Specialists analyzing ethical scenario...")
            analyst_res = self.analyst.analyze(question, structured=structured)
            compliance_res = self.compliance.check_compliance(question, structured=structured)
            
            if structured:
                spec_data = EthicalAnalysisModel(
                    case_title=question[:50],
                    summary="Synthesized findings",
                    principles=analyst_res.data.principles if hasattr(analyst_res.data, 'principles') else [],
                    stakeholders=analyst_res.data.stakeholders if hasattr(analyst_res.data, 'stakeholders') else [],
                    legal_frameworks=compliance_res.data.legal_frameworks if hasattr(compliance_res.data, 'legal_frameworks') else [],
                    recommendations=[],
                    conclusion="Pending synthesis"
                )
                spec_json = spec_data.model_dump_json(indent=2)
            else:
                spec_json = f"ANALYST:
{analyst_res.markdown}

COMPLIANCE:
{compliance_res.markdown}"

            # 2. Auditor Stage (JSON Audit)
            logger.debug("Tier 2: Safety Critic auditing analysis...")
            # For simplicity, passing everything to audit
            audit_res = self.safety_critic.audit(question, analyst_res, structured=structured)
            if structured:
                audit_json = audit_res.data.model_dump_json(indent=2)
            else:
                audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug("Tier 3: Output Synthesis (Final Closer)...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                question, spec_json, audit_json
            )
            
            final_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.client.generate_text(model_input=final_input)

            logger.info("✓ Successfully generated 3-tier medical ethics analysis")
            return ModelOutput(
                data=spec_data if structured else None,
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Ethics generation failed: {e}")
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

        first_line = md_content.split("
")[0].strip("*# ")
        sanitized_title = (
            re.sub(r"[^\w\s-]", "", first_line).strip().lower().replace(" ", "_")
        )

        filename = f"{sanitized_title}.md"
        file_path = output_dir / filename

        with open(file_path, "w") as f:
            f.write(md_content)

        logger.info(f"✓ Saved markdown analysis to {file_path}")
        return file_path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))



    EthicalAnalysisModel,
    EthicalPrincipleModel,
    LegalFrameworkModel,
    ModelOutput,
    StakeholderModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_ethics.agentic.med_ethics.LiteClient") as mock:
        yield mock


def test_med_ethical_qa_init():
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    assert generator.model_config == config
    assert generator.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)
    mock_output_analyst = ModelOutput(
        markdown="Analyst report", data_available=True
    )
    mock_output_compliance = ModelOutput(
        markdown="Compliance report", data_available=True
    )
    mock_output_synthesis = ModelOutput(
        markdown="Final synthesized report", data_available=True
    )
    mock_output_safety = ModelOutput(
        markdown="Safety audit passed", data_available=True
    )
    
    mock_lite_client.return_value.generate_text.side_effect = [
        mock_output_analyst,
        mock_output_compliance,
        mock_output_synthesis,
        mock_output_safety
    ]

    result = generator.generate_text("Organ transplantation ethics")
    assert result.markdown == "Final synthesized report"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedEthicalQA(config)

        AnalystOutput,
        ComplianceOutput,
        SafetyCheckModel,
    )

    mock_analyst_data = AnalystOutput(
        principles=[
            EthicalPrincipleModel(
                principle="Autonomy",
                application="Self-determination",
                implications=["Choice"],
            )
        ],
        stakeholders=[
            StakeholderModel(name="Patient", interests=["Health"], rights=["Care"])
        ],
        ethical_issues=["Issue"],
    )
    
    mock_compliance_data = ComplianceOutput(
        legal_considerations=LegalFrameworkModel(
            regulations=["Law"], professional_guidelines=["Guide"], citations=[]
        )
    )

    mock_final_data = EthicalAnalysisModel(
        case_title="Organ Transplant",
        summary="Dilemma",
        facts=["Fact"],
        ethical_issues=["Issue"],
        principles=mock_analyst_data.principles,
        stakeholders=mock_analyst_data.stakeholders,
        legal_considerations=mock_compliance_data.legal_considerations,
        recommendations=["Action"],
        conclusion="Complex topic",
    )

    mock_safety_data = SafetyCheckModel(
        passed=True,
        critical_omissions=[],
        hallucination_warnings=[],
        recommendations_for_improvement=[]
    )
    
    mock_lite_client.return_value.generate_text.side_effect = [
        ModelOutput(data=mock_analyst_data),
        ModelOutput(data=mock_compliance_data),
        ModelOutput(data=mock_final_data),
        ModelOutput(data=mock_safety_data)
    ]

    result = generator.generate_text("Organ transplantation", structured=True)
    assert result.data.case_title == "Organ Transplant"
    assert mock_lite_client.return_value.generate_text.call_count == 4