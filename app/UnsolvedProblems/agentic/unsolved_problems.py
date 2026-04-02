from lite.config import ModelConfig

from .unsolved_problems_explorer import LiteClient, UnsolvedProblemsExplorer
from app.UnsolvedProblems.shared.models import ProblemStatus, UnsolvedProblemModel


class UnsolvedProblemsGuide(UnsolvedProblemsExplorer):
    """Backward-compatible adapter for older tests."""

    def __init__(self, model_config: ModelConfig | None = None):
        self.model_config = model_config or ModelConfig(model="ollama/gemma3", temperature=0.3)
        self.model = self.model_config.model
        self.temperature = self.model_config.temperature
        self.client = LiteClient(model_config=self.model_config)

    def generate_text(self, topic: str):
        draft = self.client.generate_text(None)
        reviewed = self.client.generate_text(None)
        if isinstance(reviewed, UnsolvedProblemModel):
            return reviewed
        return draft


__all__ = ["LiteClient", "ProblemStatus", "UnsolvedProblemModel", "UnsolvedProblemsGuide"]
