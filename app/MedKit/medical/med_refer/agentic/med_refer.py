import logging

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient

from .medrefer_prompts import PromptBuilder, SymptomAnalysis, SpecialistList, Recommendation, ModelOutput

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
