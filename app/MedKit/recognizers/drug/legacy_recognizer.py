from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .drug_recognizer_model import DrugIdentifierModel, ModelOutput
from .drug_recognizer_prompts import PromptBuilder, DrugIdentifierInput

class DrugIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify_drug(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(DrugIdentifierInput(name)),
            response_format=DrugIdentifierModel if structured else None,
        ))
