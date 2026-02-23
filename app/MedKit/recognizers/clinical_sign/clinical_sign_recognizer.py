from ..base_recognizer import BaseRecognizer
from .clinical_sign_models import ClinicalSignIdentifierModel, ModelOutput
from .clinical_sign_prompts import PromptBuilder, ClinicalSignInput

class ClinicalSignIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(ClinicalSignInput(name)),
            response_format=ClinicalSignIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
