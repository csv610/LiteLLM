from ..base_recognizer import BaseRecognizer
from .genetic_variant_models import GeneticVariantIdentifierModel, ModelOutput
from .genetic_variant_prompts import PromptBuilder, GeneticVariantInput

class GeneticVariantIdentifier(BaseRecognizer):
    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(GeneticVariantInput(name)),
            response_format=GeneticVariantIdentifierModel if structured else None,
        )
        
        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)
