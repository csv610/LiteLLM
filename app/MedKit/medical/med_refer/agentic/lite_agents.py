"""
liteagents.py - Unified for med_refer
"""
from .medrefer_prompts import PromptBuilder, SymptomAnalysis, SpecialistList, Recommendation, ModelOutput
from unittest.mock import patch
from tqdm import tqdm
from lite.lite_client import LiteClient
import logging
import pytest
from app.MedKit.medical.med_refer.shared.models import *
from pathlib import Path
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys




logger = logging.getLogger(__name__)


class MedReferral:
    """
    A multi-agent medical referral system.
    """

    medical_specialists = frozenset(
        [
            "Allergist",
            "Anesthesiologist",
            "Cardiologist",
            "Cardiothoracic Surgeon",
            "Colorectal Surgeon",
            "Child and Adolescent Psychiatrist",
            "Dermatologist",
            "Endocrinologist",
            "Forensic Psychiatrist",
            "Gastroenterologist",
            "General Surgeon",
            "Geriatrician",
            "Geriatric Psychiatrist",
            "Gynecologist",
            "Hematologist",
            "Infectious Disease Specialist",
            "Internal Medicine Doctor (Internist)",
            "Immunologist",
            "Maternal-Fetal Medicine Specialist",
            "Nephrologist",
            "Neurologist",
            "Neurosurgeon",
            "Neonatologist",
            "Nuclear Medicine Specialist",
            "Obstetrician",
            "Occupational Medicine Specialist",
            "Oncologist",
            "Orthopedic Surgeon",
            "Ophthalmologist",
            "Otolaryngologist (ENT Specialist)",
            "Pediatrician",
            "Pathologist",
            "Pulmonologist",
            "Pediatric Surgeon",
            "Plastic Surgeon",
            "Physical Medicine & Rehabilitation (PM&R) Specialist",
            "Pain Management Specialist",
            "Psychiatrist",
            "Rheumatologist",
            "Radiologist",
            "Sports Medicine Doctor",
            "Sleep Medicine Specialist",
            "Trauma Surgeon",
            "Transplant Surgeon",
            "Urologist",
        ]
    )

    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = LiteClient(model_config=config)

    def agent_generate_text(self, system_prompt: str, user_prompt: str, response_format: type):
        """Helper to run a specialized agent with structured output."""
        try:
            model_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=response_format
            )
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"Agent error: {e}")
            raise

    def generate_text(self, question: str, structured: bool = False) -> ModelOutput:
        """
        Orchestrates the 3-tier multi-agent flow: Analysis -> Matching Audit -> Output.
        """
        try:
            logger.info(f"Starting 3-tier multi-agent analysis for: {question}")

            # 1. Run generation agent (Specialist - JSON)
            sys_p, user_p = PromptBuilder.get_symptom_analysis_prompts(question)
            analysis_res = self.agent_generate_text(sys_p, user_p, SymptomAnalysis if structured else None)
            
            if structured:
                analysis_data = analysis_res.data
                analysis_content = analysis_data.model_dump_json(indent=2)
            else:
                analysis_content = analysis_res.markdown
                analysis_data = None
            
            logger.info("Symptom analysis completed")

            # 2. Compliance Audit Stage (JSON/Audit)
            logger.debug("Running Specialist Matching audit...")
            sys_p, user_p = PromptBuilder.get_specialist_matching_prompts(analysis_data or SymptomAnalysis(symptoms=[question], severity="Low", affected_body_parts=[]))
            referrals_res = self.agent_generate_text(sys_p, user_p, SpecialistList if structured else None)
            
            if structured:
                referrals_data = referrals_res.data
                matching_content = referrals_data.model_dump_json(indent=2)
                
                final_recommendation = Recommendation(
                    analysis=analysis_data,
                    referrals=referrals_data
                )
            else:
                matching_content = referrals_res.markdown
                final_recommendation = None

            # 3. Final Synthesis (Output Stage - Markdown)
            logger.info("Running Output Synthesis (Final Closer)")
            sys_p, user_p = PromptBuilder.get_output_synthesis_prompts(question, analysis_content, matching_content)
            
            closer_input = ModelInput(
                system_prompt=sys_p,
                user_prompt=user_p,
                response_format=None # Always Markdown for synthesis
            )
            
            final_markdown = self.client.generate_text(model_input=closer_input)

            return ModelOutput(
                data=final_recommendation,
                markdown=final_markdown
            )

        except Exception as e:
            logger.error(f"Error in 3-tier multi-agent orchestration: {e}")
            raise

"""Medical Specialist Referral CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    from .med_refer import MedReferral
except (ImportError, ValueError):
    try:
        from medical.med_refer.agentic.med_refer import MedReferral
    except ImportError:
        from med_refer import MedReferral

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recommend medical specialists based on symptoms."
    )
    parser.add_argument("question", help="Symptoms or file path containing questions.")
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
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="med_refer.log", verbosity=args.verbosity, enable_console=True
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
        model_config = ModelConfig(model=args.model, temperature=0.0)
        med_referral = MedReferral(model_config)

        for item in tqdm(items, desc="Recommending"):
            result = med_referral.generate_text(item)
            if result and not result.startswith("Error"):
                fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                with open(output_dir / f"{fname}.md", "w") as f:
                    f.write(result)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))





@pytest.fixture
def mock_lite_client():
    with patch("medical.med_refer.agentic.med_refer.LiteClient") as mock:
        yield mock


def test_med_referral_init():
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)
    assert referral.config == config


def test_generate_text_agentic(mock_lite_client):
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)

    # Prepare mock return values for sequential calls
    analysis_mock = SymptomAnalysis(
        symptoms=["heart pain"],
        severity="Urgent",
        affected_body_parts=["Chest"]
    )
    specialists_mock = SpecialistList(
        specialists=["Cardiologist"],
        reasoning="Patient reports chest pain."
    )

    # Set up mock to return values in order
    mock_lite_client.return_value.generate_text.side_effect = [
        analysis_mock,
        specialists_mock
    ]

    result = referral.generate_text("I have heart pain")

    assert "# Medical Referral Analysis" in result
    assert "Cardiologist" in result
    assert "Urgent" in result
    assert "Chest" in result
    assert mock_lite_client.return_value.generate_text.call_count == 2


def test_generate_text_error(mock_lite_client):
    config = ModelConfig(model="test-model")
    referral = MedReferral(config)

    mock_lite_client.return_value.generate_text.side_effect = Exception("API Error")

    result = referral.generate_text("I have heart pain")
    assert "Error: API Error" in result