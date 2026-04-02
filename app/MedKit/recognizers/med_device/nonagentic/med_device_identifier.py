from ...base_recognizer import BaseRecognizer, ModelOutput
from .med_device_models import MedicalDeviceIdentifierModel
from .med_device_prompts import MedicalDeviceIdentifierInput, PromptBuilder


class MedicalDeviceIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(
                MedicalDeviceIdentifierInput(name)
            ),
            response_format=MedicalDeviceIdentifierModel if structured else None,
        )

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
