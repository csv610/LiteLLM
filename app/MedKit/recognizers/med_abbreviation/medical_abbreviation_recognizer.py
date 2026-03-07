from ..base_recognizer import BaseRecognizer
from .medical_abbreviation_models import AbbreviationIdentifierModel, ModelOutput
from .medical_abbreviation_prompts import AbbreviationIdentifierInput, PromptBuilder


class MedicalAbbreviationIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                AbbreviationIdentifierInput(name)
            ),
            response_format=AbbreviationIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
