"""Three-agent curriculum generator: planner, generator, reviewer with 3-tier artifact output."""

import json
import logging
from pathlib import Path
from typing import Callable, Optional

# Add parent directories to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from app.GenerateBook.shared.models import (
    AgentTrace,
    BookChaptersModel,
    BookInput,
    CurriculumPlanModel,
    ReviewedBookChaptersModel,
    ModelOutput
)
from app.GenerateBook.shared.prompts import PromptBuilder

logger = logging.getLogger(__name__)


class BookChaptersGenerator:
    """Generator class for the 3rd-tier curriculum workflow."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the generator with model configuration."""
        self.model_config = model_config
        self.model = model_config.model or "ollama/gemma3"
        self.client = LiteClient(model_config=model_config)

    def _run_planner_agent(self, book_input: BookInput) -> CurriculumPlanModel:
        """Run the planner agent (Tier 1 Specialist)."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_planner_prompt(
                book_input.subject,
                book_input.level,
                book_input.num_chapters,
            ),
            response_format=CurriculumPlanModel,
        )
        response = self.client.generate_text(model_input=model_input)
        return response.data

    def _run_generator_agent(
        self,
        book_input: BookInput,
        plan: CurriculumPlanModel,
    ) -> BookChaptersModel:
        """Run the generator agent (Tier 1 Specialist)."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_generator_prompt(
                book_input.subject,
                book_input.num_chapters,
                json.dumps(plan.model_dump(), indent=2),
            ),
            response_format=BookChaptersModel,
        )
        response = self.client.generate_text(model_input=model_input)
        return response.data

    def _run_reviewer_agent(
        self,
        book_input: BookInput,
        plan: CurriculumPlanModel,
        draft: BookChaptersModel,
    ) -> ReviewedBookChaptersModel:
        """Run the reviewer agent (Tier 2 Auditor)."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_reviewer_prompt(
                book_input.subject,
                json.dumps(plan.model_dump(), indent=2),
                json.dumps(draft.model_dump(), indent=2),
            ),
            response_format=ReviewedBookChaptersModel,
        )
        response = self.client.generate_text(model_input=model_input)
        return response.data

    def generate_text(self, book_input: BookInput) -> ModelOutput:
        """Generate curriculum through 3-tier multi-agent pipeline."""
        logger.info(f"Starting 3rd-tier book generation for: {book_input.subject}")
        
        # Tier 1 & 2
        plan = self._run_planner_agent(book_input)
        draft = self._run_generator_agent(book_input, plan)
        reviewed = self._run_reviewer_agent(book_input, plan, draft)

        final_curriculum = reviewed.final_curriculum.model_copy(deep=True)
        
        # Tier 3: Output Synthesis (Markdown Closer)
        logger.debug("Synthesizing final Markdown book report...")
        synth_prompt = (
            f"Synthesize a beautiful Markdown book curriculum for: '{book_input.subject}'.\n\n"
            f"PLANNING NOTES: {plan.planning_notes}\n\n"
            f"REVIEWER SUMMARY: {reviewed.reviewer_summary}\n\n"
            f"CHAPTERS:\n"
            + "\n".join([f"### {c.title}\n{c.description}" for c in final_curriculum.chapters])
        )
        
        final_markdown_res = self.client.generate_text(ModelInput(
            system_prompt="You are a Lead Educational Editor. Synthesize a structured curriculum into a professional and engaging Markdown book report.",
            user_prompt=synth_prompt,
            response_format=None
        ))
        final_markdown = final_markdown_res.markdown

        return ModelOutput(
            data=final_curriculum,
            markdown=final_markdown,
            metadata={
                "planner_notes": plan.planning_notes,
                "reviewer_summary": reviewed.reviewer_summary,
                "revision_count": reviewed.revision_count
            }
        )
    
    def save_to_file(self, output: ModelOutput, book_input: BookInput) -> str:
        """Save the artifact to Markdown and JSON."""
        level_code = PromptBuilder.get_level_code(book_input.level)
        subject_normalized = book_input.subject.replace(' ', '_').lower()
        base_name = f"{subject_normalized}_{level_code}"
        
        md_path = f"{base_name}.md"
        json_path = f"{base_name}.json"
        
        if output.markdown:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(output.markdown)
        
        if output.data:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output.data.model_dump(), f, indent=4)
            
        return md_path
    
    def generate_and_save(self, book_input: BookInput) -> str:
        """Generate and save in one operation."""
        output = self.generate_text(book_input)
        return self.save_to_file(output, book_input)
