from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .medical_supplement_models import SupplementIdentifierModel, ModelOutput
from .medical_supplement_prompts import PromptBuilder, SupplementIdentifierInput

class MedicalSupplementIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(SupplementIdentifierInput(name)),
            response_format=SupplementIdentifierModel if structured else None,
        ))
