from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .models import MedicalCodingIdentifierModel, ModelOutput
from .prompts import PromptBuilder, MedicalCodingInput

class MedicalCodingIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalCodingInput(name)),
            response_format=MedicalCodingIdentifierModel if structured else None,
        ))
