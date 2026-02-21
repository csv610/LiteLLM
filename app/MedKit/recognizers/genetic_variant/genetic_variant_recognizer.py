from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .genetic_variant_models import GeneticVariantIdentifierModel, ModelOutput
from .genetic_variant_prompts import PromptBuilder, GeneticVariantInput

class GeneticVariantIdentifier:
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def identify(self, name: str, structured: bool = True) -> ModelOutput:
        return self.client.generate_text(model_input=ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(GeneticVariantInput(name)),
            response_format=GeneticVariantIdentifierModel if structured else None,
        ))
