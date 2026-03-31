"""Three-agent curriculum generator: planner, generator, reviewer."""

import json
from pathlib import Path

# Add parent directories to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from .bookchapters_models import (
    AgentTrace,
    BookChaptersModel,
    BookInput,
    CurriculumPlanModel,
    ReviewedBookChaptersModel,
)
from .bookchapters_prompts import PromptBuilder


class BookChaptersGenerator:
    """Generator class for the three-agent curriculum workflow."""
    
    def __init__(self, model_config: ModelConfig):
        """
        Initialize the generator with model configuration.
        
        Args:
            model_config: ModelConfig with model settings
        """
        self.model_config = model_config
        self.model = model_config.model or "ollama/gemma3"
        self.client = LiteClient(model_config=model_config)

    def _run_planner_agent(self, book_input: BookInput) -> CurriculumPlanModel:
        """Run the planner agent and return a typed curriculum plan."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_planner_prompt(
                book_input.subject,
                book_input.level,
                book_input.num_chapters,
            ),
            response_format=CurriculumPlanModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, CurriculumPlanModel):
            return response
        raise ValueError(f"Expected CurriculumPlanModel, got {type(response).__name__}")

    def _run_generator_agent(
        self,
        book_input: BookInput,
        plan: CurriculumPlanModel,
    ) -> BookChaptersModel:
        """Run the generator agent using the planner output."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_generator_prompt(
                book_input.subject,
                book_input.num_chapters,
                json.dumps(plan.model_dump(), indent=2),
            ),
            response_format=BookChaptersModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, BookChaptersModel):
            return response
        raise ValueError(f"Expected BookChaptersModel, got {type(response).__name__}")

    def _run_reviewer_agent(
        self,
        book_input: BookInput,
        plan: CurriculumPlanModel,
        draft: BookChaptersModel,
    ) -> ReviewedBookChaptersModel:
        """Run the reviewer agent and return the corrected curriculum."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_reviewer_prompt(
                book_input.subject,
                json.dumps(plan.model_dump(), indent=2),
                json.dumps(draft.model_dump(), indent=2),
            ),
            response_format=ReviewedBookChaptersModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, ReviewedBookChaptersModel):
            return response
        raise ValueError(f"Expected ReviewedBookChaptersModel, got {type(response).__name__}")

    def generate_text(self, book_input: BookInput) -> BookChaptersModel:
        """Generate curriculum through planner, generator, and reviewer agents."""
        plan = self._run_planner_agent(book_input)
        draft = self._run_generator_agent(book_input, plan)
        reviewed = self._run_reviewer_agent(book_input, plan, draft)

        final_curriculum = reviewed.final_curriculum.model_copy(deep=True)
        final_curriculum.agent_trace = AgentTrace(
            planner_notes=plan.planning_notes,
            reviewer_summary=reviewed.reviewer_summary,
            revision_count=reviewed.revision_count,
        )
        return final_curriculum
    
    def save_to_file(self, response: BookChaptersModel, book_input: BookInput) -> str:
        """
        Save the generated curriculum to a JSON file.
        
        Args:
            response: BookChaptersResponse with generated curriculum
            book_input: BookInput containing subject and level for filename
            
        Returns:
            Path to the saved file
        """
        level_code = PromptBuilder.get_level_code(book_input.level)
        subject_normalized = book_input.subject.replace(' ', '_').lower()
        filename = f"{subject_normalized}_{level_code}.json"
        
        try:
            data = response.model_dump()
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            
            return filename
            
        except Exception:
            raise
    
    def generate_and_save(self, book_input: BookInput) -> str:
        """
        Generate chapters and save to file in one operation.
        
        Args:
            book_input: BookInput containing subject, level, and num_chapters
            
        Returns:
            Path to the saved file
        """
        response = self.generate_text(book_input)
        return self.save_to_file(response, book_input)
