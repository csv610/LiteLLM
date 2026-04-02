from ...base_recognizer import BaseRecognizer, ModelOutput
from .med_procedure_models import MedicalProcedureIdentifierModel
from .med_procedure_prompts import MedicalProcedureIdentifierInput, PromptBuilder


class MedicalProcedureIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                MedicalProcedureIdentifierInput(name)
            ),
            response_format=MedicalProcedureIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
