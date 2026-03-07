from ..base_recognizer import BaseRecognizer
from .medical_specialty_models import MedicalSpecialtyIdentifierModel, ModelOutput
from .medical_specialty_prompts import PromptBuilder


class MedicalSpecialtyIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(name),
            response_format=MedicalSpecialtyIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
