from ..base_recognizer import BaseRecognizer
from .medical_condition_models import MedicalConditionIdentifierModel, ModelOutput
from .medical_condition_prompts import PromptBuilder, MedicalConditionIdentifierInput

class MedicalConditionIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(MedicalConditionIdentifierInput(name)),
            response_format=MedicalConditionIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
