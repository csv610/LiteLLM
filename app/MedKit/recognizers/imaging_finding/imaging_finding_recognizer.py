from ..base_recognizer import BaseRecognizer
from .imaging_finding_models import ImagingFindingIdentifierModel, ModelOutput
from .imaging_finding_prompts import PromptBuilder, ImagingFindingInput

class ImagingFindingIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(ImagingFindingInput(name)),
            response_format=ImagingFindingIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
