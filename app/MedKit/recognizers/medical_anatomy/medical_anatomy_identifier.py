from ..base_recognizer import BaseRecognizer
from .medical_anatomy_identifier_models import MedicalAnatomyIdentifierModel, ModelOutput
from .medical_anatomy_identifier_prompts import PromptBuilder, MedicalAnatomyIdentifierInput

class MedicalAnatomyIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalAnatomyIdentifierInput(name)),
            response_format=MedicalAnatomyIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
