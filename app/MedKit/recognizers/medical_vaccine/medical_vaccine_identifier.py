from ..base_recognizer import BaseRecognizer
from .medical_vaccine_models import ModelOutput, VaccineIdentifierModel
from .medical_vaccine_prompts import PromptBuilder


class MedicalVaccineIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(name),
            response_format=VaccineIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
