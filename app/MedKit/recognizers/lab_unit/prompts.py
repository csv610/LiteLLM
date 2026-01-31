from dataclasses import dataclass

@dataclass
class LabUnitInput:
    unit_name: str
    def __post_init__(self):
        if not self.unit_name or not self.unit_name.strip():
            raise ValueError("Unit name cannot be empty")

class PromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return "You are a laboratory director focusing on medical measurement units and reference intervals."
    @staticmethod
    def create_user_prompt(config: LabUnitInput) -> str:
        return f"Identify and describe the medical lab unit '{config.unit_name}'."
