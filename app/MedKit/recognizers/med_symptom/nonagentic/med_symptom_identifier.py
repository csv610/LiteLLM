from ...base_recognizer import BaseRecognizer, ModelOutput
from .med_symptom_models import MedicalSymptomIdentifierModel
from .med_symptom_prompts import MedicalSymptomIdentifierInput, PromptBuilder


class MedicalSymptomIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                MedicalSymptomIdentifierInput(name)
            ),
            response_format=MedicalSymptomIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
