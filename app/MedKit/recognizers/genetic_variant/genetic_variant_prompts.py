from dataclasses import dataclass

@dataclass
class GeneticVariantInput:
    variant_name: str
    def __post_init__(self):
        if not self.variant_name or not self.variant_name.strip():
            raise ValueError("Variant name cannot be empty")

class PromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return "You are a clinical geneticist focusing on gene variants, mutations, and their clinical impact."
    @staticmethod
    def create_user_prompt(config: GeneticVariantInput) -> str:
        return f"Identify and describe the genetic variant or gene '{config.variant_name}'."
