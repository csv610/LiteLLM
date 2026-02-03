from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .medical_procedure_models import ProcedureIdentifierModel, ModelOutput
from .medical_procedure_prompts import PromptBuilder, ProcedureIdentifierInput

class MedicalProcedureIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalProcedureIdentifierInput(name)),
            response_format=MedicalProcedureIdentifierModel if structured else None,
        ))
