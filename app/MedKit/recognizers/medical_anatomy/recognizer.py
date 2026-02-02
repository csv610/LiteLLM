import sys
from pathlib import Path


from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from .models import MedicalAnatomyIdentifierModel, ModelOutput
from .prompts import PromptBuilder, MedicalAnatomyIdentifierInput

class MedicalAnatomyIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify_anatomy(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalAnatomyIdentifierInput(name)),
            response_format=MedicalAnatomyIdentifierModel if structured else None,
        ))
