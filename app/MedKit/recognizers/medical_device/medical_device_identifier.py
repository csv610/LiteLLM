from ..base_recognizer import BaseRecognizer
from .medical_device_models import MedicalDeviceIdentifierModel, ModelOutput
from .medical_device_prompts import PromptBuilder, MedicalDeviceIdentifierInput

class MedicalDeviceIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalDeviceIdentifierInput(name)),
            response_format=MedicalDeviceIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
