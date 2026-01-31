from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .models import VaccineIdentifierModel, ModelOutput
from .prompts import PromptBuilder, VaccineIdentifierInput

class MedicalVaccineIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify_vaccine(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(VaccineIdentifierInput(name)),
            response_format=VaccineIdentifierModel if structured else None,
        ))
