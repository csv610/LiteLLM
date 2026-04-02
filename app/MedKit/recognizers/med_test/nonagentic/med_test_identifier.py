from ...base_recognizer import BaseRecognizer, ModelOutput
from .med_test_models import MedicalTestIdentifierModel
from .med_test_prompts import MedicalTestIdentifierInput, PromptBuilder


class MedicalTestIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                MedicalTestIdentifierInput(name)
            ),
            response_format=MedicalTestIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
