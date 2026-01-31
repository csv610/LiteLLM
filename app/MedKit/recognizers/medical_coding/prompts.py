from dataclasses import dataclass

@dataclass
class MedicalCodingInput:
    system_name: str
    def __post_init__(self):
        if not self.system_name or not self.system_name.strip():
            raise ValueError("System name cannot be empty")

class PromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return "You are a medical billing and documentation specialist focusing on healthcare coding systems."
    @staticmethod
    def create_user_prompt(config: MedicalCodingInput) -> str:
        return f"Identify and describe the medical coding system '{config.system_name}'."
