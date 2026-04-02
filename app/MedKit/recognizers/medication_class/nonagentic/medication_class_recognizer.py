from ...base_recognizer import BaseRecognizer
from .medication_class_models import MedicationClassIdentifierModel, ModelOutput
from .medication_class_prompts import MedicationClassIdentifierInput, PromptBuilder


class MedicationClassIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                MedicationClassIdentifierInput(name)
            ),
            response_format=MedicationClassIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
