from ..base_recognizer import BaseRecognizer
from .medical_test_models import MedicalTestIdentifierModel, ModelOutput
from .medical_test_prompts import PromptBuilder


class MedicalTestIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(name),
            response_format=MedicalTestIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
