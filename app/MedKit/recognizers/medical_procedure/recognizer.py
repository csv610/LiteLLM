from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .models import MedicalProcedureIdentifierModel, ModelOutput
from .prompts import PromptBuilder, MedicalProcedureIdentifierInput

class MedicalProcedureIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify_procedure(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalProcedureIdentifierInput(name)),
            response_format=MedicalProcedureIdentifierModel if structured else None,
        ))
