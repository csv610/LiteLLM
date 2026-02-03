from dataclasses import dataclass

@dataclass
class ClinicalSignInput:
    sign_name: str
    def __post_init__(self):
        if not self.sign_name or not self.sign_name.strip():
            raise ValueError("Sign name cannot be empty")

class PromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return "You are an expert clinical diagnostician focusing on physical examination findings and clinical signs."
    @staticmethod
    def create_user_prompt(config: ClinicalSignInput) -> str:
        return f"Identify and describe the clinical sign '{config.sign_name}'."
