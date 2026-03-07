from ..base_recognizer import BaseRecognizer
from .disease_identifier_models import DiseaseIdentifierModel, ModelOutput
from .disease_identifier_prompts import DiseaseIdentifierInput, PromptBuilder


class DiseaseIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(DiseaseIdentifierInput(name)),
            response_format=DiseaseIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
