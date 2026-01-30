import logging
import re
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from med_speciality_roles_prompts import PromptBuilder

logger = logging.getLogger(__name__)

class MedSpecialityRoles:
    """
    A class for determining the roles and responsibilities of a medical specialist.
    """
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.client = LiteClient(model_config=config)
    
    def generate_text(self, speciality):
        """
        Generates a description of roles and responsibilities for a given medical speciality.
        """
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(speciality)

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
