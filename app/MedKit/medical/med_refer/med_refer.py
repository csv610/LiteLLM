import logging
import re
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from medrefer_prompts import PromptBuilder

logger = logging.getLogger(__name__)

class MedReferral:
    """
    A class for determining the appropriate medical specialists based on a given question using OpenAI GPT model.
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
    
    def generate_text(self, question):
        """
        Determines the appropriate medical specialists for a given question.
        """
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(question)

        try:
            logger.debug(f"Sending request to model: {self.config.model}")
            
            model_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )
            
            response = self.client.generate_text(model_input=model_input)

            return response

        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return f"Error: {str(e)}"
