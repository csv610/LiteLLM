from ..base_recognizer import BaseRecognizer
from .medical_supplement_models import ModelOutput, SupplementIdentifierModel
from .medical_supplement_prompts import PromptBuilder


class MedicalSupplementIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(name),
            response_format=SupplementIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
