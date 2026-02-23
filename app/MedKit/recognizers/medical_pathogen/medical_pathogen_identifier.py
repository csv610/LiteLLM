from ..base_recognizer import BaseRecognizer
from .medical_pathogen_models import PathogenIdentifierModel, ModelOutput
from .medical_pathogen_prompts import PromptBuilder, PathogenIdentifierInput

class MedicalPathogenIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(PathogenIdentifierInput(name)),
            response_format=PathogenIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
