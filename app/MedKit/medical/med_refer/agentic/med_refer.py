import logging

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

from .medrefer_prompts import PromptBuilder, SymptomAnalysis, SpecialistList, Recommendation

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

    def generate_text(self, question):
        """
        Orchestrates the multi-agent flow to determine medical referrals.
        """
        try:
            logger.info(f"Starting multi-agent analysis for: {question}")

            # Agent 1: Symptom Analysis
            sys_p, user_p = PromptBuilder.get_symptom_analysis_prompts(question)
            analysis: SymptomAnalysis = self.agent_generate_text(sys_p, user_p, SymptomAnalysis)
            logger.info(f"Symptom analysis completed: {analysis.severity}")

            # Agent 2: Specialist Matching
            sys_p, user_p = PromptBuilder.get_specialist_matching_prompts(analysis)
            referrals: SpecialistList = self.agent_generate_text(sys_p, user_p, SpecialistList)
            logger.info(f"Specialist matching completed: {', '.join(referrals.specialists)}")

            # Coordinator: Consolidate Final Recommendation
            final_recommendation = Recommendation(
                analysis=analysis,
                referrals=referrals
            )

            # Convert to markdown for CLI compatibility
            return self._format_recommendation(final_recommendation)

        except Exception as e:
            logger.error(f"Error in multi-agent orchestration: {e}")
            return f"Error: {str(e)}"

    def _format_recommendation(self, rec: Recommendation) -> str:
        """Formats the recommendation into a readable markdown string."""
        symptoms_str = ", ".join(rec.analysis.symptoms)
        body_parts_str = ", ".join(rec.analysis.affected_body_parts)
        specialists_str = ", ".join(rec.referrals.specialists)

        return f"""# Medical Referral Analysis

## Symptom Analysis
- **Symptoms:** {symptoms_str}
- **Severity:** {rec.analysis.severity}
- **Affected Body Parts:** {body_parts_str}

## Recommended Specialists
- **Specialists:** {specialists_str}
- **Reasoning:** {rec.referrals.reasoning}

## Medical Disclaimer
> {rec.disclaimer}
"""
