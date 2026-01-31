from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .models import SupplementIdentifierModel, ModelOutput
from .prompts import PromptBuilder, SupplementIdentifierInput

class MedicalSupplementIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify_supplement(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(SupplementIdentifierInput(name)),
            response_format=SupplementIdentifierModel if structured else None,
        ))
