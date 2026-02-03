from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .medical_test_models import MedicalTestIdentifierModel, ModelOutput
from .medical_test_prompts import PromptBuilder, MedicalTestIdentifierInput

class MedicalTestIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalTestIdentifierInput(name)),
            response_format=MedicalTestIdentifierModel if structured else None,
        ))
