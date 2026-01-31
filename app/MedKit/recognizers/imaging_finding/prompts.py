from dataclasses import dataclass

@dataclass
class ImagingFindingInput:
    finding_name: str
    def __post_init__(self):
        if not self.finding_name or not self.finding_name.strip():
            raise ValueError("Finding name cannot be empty")

class PromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return "You are a senior radiologist focusing on descriptive imaging findings and radiology reports."
    @staticmethod
    def create_user_prompt(config: ImagingFindingInput) -> str:
        return f"Identify and describe the medical imaging finding '{config.finding_name}'."
