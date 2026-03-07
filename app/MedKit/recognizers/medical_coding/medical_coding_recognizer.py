from ..base_recognizer import BaseRecognizer
from .medical_coding_models import MedicalCodingIdentifierModel, ModelOutput
from .medical_coding_prompts import MedicalCodingInput, PromptBuilder


class MedicalCodingIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalCodingInput(name)),
            response_format=MedicalCodingIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
