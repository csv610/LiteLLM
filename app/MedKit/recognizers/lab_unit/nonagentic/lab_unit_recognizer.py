from ...base_recognizer import BaseRecognizer
from .lab_unit_models import LabUnitIdentifierModel, ModelOutput
from .lab_unit_prompts import LabUnitInput, PromptBuilder


class LabUnitIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(LabUnitInput(name)),
            response_format=LabUnitIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
