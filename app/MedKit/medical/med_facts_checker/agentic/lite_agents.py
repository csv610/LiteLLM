"""
liteagents.py - Unified for med_facts_checker
"""
from unittest.mock import patch
from lite.utils import save_model_response
from typing import Optional
from tqdm import tqdm
from lite.lite_client import LiteClient
import logging
import pytest
import sys
from pathlib import Path
import argparse
from lite.config import ModelConfig, ModelInput
from app.MedKit.medical.med_facts_checker.shared.models import *
from lite.logging_config import configure_logging
from concurrent.futures import ThreadPoolExecutor

#!/usr/bin/env python3
"""
Medical Facts Checker Analysis module.

This module provides the core MedicalFactsChecker class for analyzing
medical statements for factual accuracy.
"""



try:
    from .medical_facts_checker_models import MedicalFactFictionAnalysisModel, ModelOutput
    from .medical_facts_checker_prompts import PromptBuilder
except ImportError:
    from medical_facts_checker_models import MedicalFactFictionAnalysisModel, ModelOutput
    from medical_facts_checker_prompts import PromptBuilder

logger = logging.getLogger(__name__)



class MedicalFactsChecker:
    """Analyzes medical statements for factual accuracy."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the facts checker."""
        self.client = LiteClient(model_config=model_config)
        self.statement: Optional[str] = None
        self.output_path: Optional[Path] = None
        logger.debug("Initialized MedicalFactsChecker")

    def generate_text(self, statement: str, structured: bool = False) -> ModelOutput:
        """Analyze a statement using a 3-tier agent system."""
        if not statement or not statement.strip():
            raise ValueError("Statement cannot be empty")

        self.statement = statement
        logger.info(f"Starting 3-tier analysis for: {statement}")

        try:
            # --- Tier 1: Specialist Stage (Parallel & Sequential JSON) ---
            with ThreadPoolExecutor(max_workers=2) as executor:
                # Parallel specialists
                f_res = executor.submit(self._ask_llm, ModelInput(
                    system_prompt=PromptBuilder.create_researcher_prompt(),
                    user_prompt=PromptBuilder.create_user_prompt(statement)
                ))
                f_skp = executor.submit(self._ask_llm, ModelInput(
                    system_prompt=PromptBuilder.create_skeptic_prompt(),
                    user_prompt=PromptBuilder.create_user_prompt(statement)
                ))
                res_md = f_res.result().markdown
                skp_md = f_skp.result().markdown

            # Lead Specialist Synthesis
            synth_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_synthesizer_prompt(res_md, skp_md),
                user_prompt=PromptBuilder.create_user_prompt(statement)
            ))
            spec_json = synth_res.markdown

            # --- Tier 2: Compliance Auditor Stage (JSON Audit) ---
            audit_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_compliance_officer_prompt(spec_json),
                user_prompt=PromptBuilder.create_user_prompt(statement),
                response_format=MedicalFactFictionAnalysisModel if structured else None
            ))
            
            if structured:
                audit_json = audit_res.data.model_dump_json(indent=2)
            else:
                audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                statement, spec_json, audit_json
            )
            final_res = self._ask_llm(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            logger.info("✓ Successfully generated 3-tier medical facts analysis")
            return ModelOutput(data=audit_res.data if structured else None, markdown=final_res.markdown)

        except Exception as e:
            logger.error(f"✗ 3-tier Facts generation failed: {e}")
            raise

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical facts analysis to a file."""
        if self.statement is None:
            raise ValueError(
                "No statement information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.statement.lower().replace(' ', '_')}_facts_analysis"

        return save_model_response(result, output_dir / base_filename)


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    AnalyzerMetadata,
    ContextInformation,
    DetailedAnalysis,
    FictionIndicators,
    MedicalFactFictionAnalysisModel,
    ModelOutput,
    StatementAnalysis,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_facts_checker.agentic.medical_facts_checker.LiteClient") as mock:
        yield mock


def test_medical_facts_checker_init():
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    assert checker.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    
    # Mock four responses: Researcher, Skeptic, Synthesizer, Compliance
    mock_responses = [
        ModelOutput(markdown="R", data=None),
        ModelOutput(markdown="S", data=None),
        ModelOutput(markdown="Synthesized Report", data=None),
        ModelOutput(markdown="Final Approved Report", data=None)
    ]
    mock_lite_client.return_value.generate_text.side_effect = mock_responses

    result = checker.generate_text("Water is wet")
    assert result.markdown == "Final Approved Report"
    assert result.researcher_report == "R"
    assert result.skeptic_report == "S"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_generate_text_empty_statement():
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    with pytest.raises(ValueError, match="Statement cannot be empty"):
        checker.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)

    mock_data = MedicalFactFictionAnalysisModel(
        detailed_analysis=DetailedAnalysis(
            statement_analysis=StatementAnalysis(
                statement="Vitamin C cures cancer",
                classification="Fiction",
                confidence_level="High",
                confidence_percentage=99,
            ),
            factual_support=None,
            fiction_indicators=FictionIndicators(
                red_flags="No clinical evidence",
                factual_errors="Vitamin C is an antioxidant, not a cure",
                lack_of_evidence="Large trials failed",
                fictional_elements="Alternative medicine myth",
            ),
            context=ContextInformation(
                subject_area="Oncology",
                key_terms="Vitamin C, Cancer",
                assumptions="High dose is effective",
                scope_clarity="Clear",
            ),
            explanation="No evidence supports this.",
            potential_confusion="Early lab studies were misinterpreted.",
        ),
        metadata=AnalyzerMetadata(
            analysis_date="2024-05-20",
            knowledge_cutoff="2023-12",
            analysis_method="Evidence review",
            limitations="Based on current clinical data",
        ),
    )

    # Mock four responses: Researcher, Skeptic, Synthesizer, Compliance (with data)
    mock_responses = [
        ModelOutput(markdown="R", data=None),
        ModelOutput(markdown="S", data=None),
        ModelOutput(markdown="Synthesized Report", data=None),
        ModelOutput(data=mock_data, markdown=None)
    ]
    mock_lite_client.return_value.generate_text.side_effect = mock_responses

    result = checker.generate_text("Vitamin C cures cancer", structured=True)
    assert result.data.detailed_analysis.statement_analysis.classification == "Fiction"
    assert result.researcher_report == "R"
    assert result.skeptic_report == "S"
    assert mock_lite_client.return_value.generate_text.call_count == 4


def test_save_error():
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    with pytest.raises(ValueError, match="No statement information available"):
        checker.save(ModelOutput(), Path("/tmp"))


@patch("medical.med_facts_checker.agentic.medical_facts_checker.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    checker = MedicalFactsChecker(config)
    
    mock_responses = [
        ModelOutput(markdown="R"),
        ModelOutput(markdown="S"),
        ModelOutput(markdown="Synth"),
        ModelOutput(markdown="Final")
    ]
    mock_lite_client.return_value.generate_text.side_effect = mock_responses

    checker.generate_text("Water is wet")
    mock_output = mock_responses[-1]
    checker.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("water_is_wet_facts_analysis")

"""Medical Facts Checker CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from medical_facts_checker import MedicalFactsChecker
except ImportError:
    from medical.med_facts_checker.agentic.medical_facts_checker import MedicalFactsChecker

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze statements and determine if they are fact or fiction."
    )
    parser.add_argument(
        "statement", help="Statement or file path containing statements."
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
        log_file="medical_facts_checker.log",
        verbosity=args.verbosity,
        enable_console=True,
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.statement)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.statement]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalFactsChecker(model_config)

        for item in tqdm(items, desc="Checking"):
            result = checker.generate_text(statement=item, structured=args.structured)
            if result:
                fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                save_model_response(result, output_dir / f"{fname}.json")

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())