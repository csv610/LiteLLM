from ...base_recognizer import BaseRecognizer, ModelOutput
from .med_supplement_models import SupplementIdentifierModel
from .med_supplement_prompts import PromptBuilder, SupplementIdentifierInput


class MedicalSupplementIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                SupplementIdentifierInput(name)
            ),
            response_format=SupplementIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
