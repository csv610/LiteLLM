from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .disease_identifier_models import DiseaseIdentifierModel, ModelOutput
from .disease_identifier_prompts import PromptBuilder, DiseaseIdentifierInput

class DiseaseIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(DiseaseIdentifierInput(name)),
            response_format=DiseaseIdentifierModel if structured else None,
        ))
