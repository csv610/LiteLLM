"""
millennium_prize_agents.py - Two-agent workflow for Millennium Prize Problems

Defines the lightweight agents used by the CLI:
- ProblemSelectionAgent prepares the selected problem and prompt payload.
- ExplanationGenerationAgent calls the model and returns generated text.
"""

from typing import Any, Dict, List, Optional

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from MillenniumPrize.agentic.millennium_prize_models import MillenniumProblem
from MillenniumPrize.agentic.millennium_prize_prompts import PromptBuilder


class ProblemSelectionAgent:
    """Selects a problem and prepares explanation inputs."""

    def __init__(self, problems_data: List[Dict[str, Any]]):
        self._problems = [MillenniumProblem(**problem) for problem in problems_data]

    def get_all_problems(self) -> List[MillenniumProblem]:
        """Return all problems."""
        return self._problems

    def prepare_problem_payload(self, problem_number: int) -> Dict[str, Any]:
        """Validate a selection and prepare the prompt payload for the next agent."""
        if problem_number < 1 or problem_number > len(self._problems):
            raise ValueError(f"Problem number must be between 1 and {len(self._problems)}")

        problem = self._problems[problem_number - 1]
        prompt = PromptBuilder.create_explanation_prompt(problem)

        return {
            "problem_number": problem_number,
            "problem": problem,
            "prompt": prompt,
        }


class ExplanationGenerationAgent:
    """Generates the optional explanation for a selected problem."""

    def __init__(self, model_name: Optional[str]):
        self.model_name = model_name

    def generate_explanation(self, prompt: str) -> str:
        """Generate a natural-language explanation for a prepared prompt."""
        if self.model_name is None:
            return ""

        model_config = ModelConfig(model=self.model_name, temperature=0.3)
        client = LiteClient(model_config=model_config)
        model_input = ModelInput(user_prompt=prompt)
        response_content = client.generate_text(model_input=model_input)

        if isinstance(response_content, str):
            return response_content

        return str(response_content)


class TwoAgentWorkflow:
    """Coordinates the selection and explanation agents for single-problem output."""

    def __init__(self, problems_data: List[Dict[str, Any]], model_name: Optional[str]):
        self._selection_agent = ProblemSelectionAgent(problems_data)
        self._explanation_agent = ExplanationGenerationAgent(model_name)
        self._model_name = model_name

    def get_all_problems(self) -> List[MillenniumProblem]:
        """Return all problems."""
        return self._selection_agent.get_all_problems()

    def process_problem(self, problem_number: int, skip_explanation: bool = False) -> Dict[str, Any]:
        """Run the two-agent workflow for a single problem."""
        selection_payload = self._selection_agent.prepare_problem_payload(problem_number)
        explanation = ""
        explanation_status = "skipped"

        if not skip_explanation and self._model_name is not None:
            try:
                explanation = self._explanation_agent.generate_explanation(
                    selection_payload["prompt"]
                )
                explanation_status = "completed"
            except Exception:
                explanation_status = "failed"

        result = {
            "problem_number": problem_number,
            "problem": selection_payload["problem"],
            "explanation": explanation,
            "agents": {
                "selection_agent": {
                    "status": "completed",
                    "selected_problem_number": selection_payload["problem_number"],
                },
                "explanation_agent": {
                    "status": explanation_status,
                    "model": self._model_name if explanation_status != "skipped" else None,
                },
            },
        }

        return result
