from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .medical_pathogen_models import PathogenIdentifierModel, ModelOutput
from .medical_pathogen_prompts import PromptBuilder, PathogenIdentifierInput

class MedicalPathogenIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(PathogenIdentifierInput(name)),
            response_format=PathogenIdentifierModel if structured else None,
        ))
