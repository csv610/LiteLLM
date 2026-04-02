"""
liteagents.py - Unified LiteClient-based agents for GenerateBook.
"""

from app.GenerateBook.shared.models import (
from app.GenerateBook.shared.models import *
from app.GenerateBook.shared.prompts import PromptBuilder
from app.GenerateBook.shared.utils import *
from bookchapters_generator import BookChaptersGenerator
from bookchapters_models import BookInput
from dspy.teleprompt import BootstrapFewShot
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pathlib import Path
from typing import Any
from typing import Callable, Optional
import dspy
import json
import logging
import sys

"""Three-agent curriculum generator: planner, generator, reviewer with 3-tier artifact output."""

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

    AgentTrace,
    BookChaptersModel,
    BookInput,
    CurriculumPlanModel,
    ReviewedBookChaptersModel,
    ModelOutput
)

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

"""
optimize_models.py - Script to optimize Pydantic models for GenerateBook using DSPydantic with Ollama.
"""

# Configure DSPy to use Ollama
ollama_lm = dspy.Ollama(
    model="llama3",  # Change to your preferred Ollama model
    max_tokens=2000,
    temperature=0.2,  # Lower temperature for more consistent educational content
)
dspy.settings.configure(lm=ollama_lm)

def book_input_metric(example, pred, trace=None):
    """
    Validation metric for BookInput model.
    Checks that the generated content is appropriate for educational curriculum.
    """
    # Check required fields exist
    if not isinstance(pred.subject, str) or not pred.subject.strip():
        return False

    # Level can be None (for all levels) or a string
    if pred.level is not None and not isinstance(pred.level, str):
        return False

    # Check num_chapters is a positive integer
    if not isinstance(pred.num_chapters, int) or pred.num_chapters < 1:
        return False

    # For the actual generated content (chapters), we'd need to evaluate the generator output
    # Since BookInput is primarily an input model, we'll focus on validating that it makes sense
    # as input to the generator

    return True

# Example training data - REPLACE WITH YOUR HIGH-QUALITY EXAMPLES
trainset = [
    dspy.Example(
        subject="Renewable Energy Systems", level="Undergraduate", num_chapters=12
    ).with_inputs("subject", "level", "num_chapters"),
    dspy.Example(
        subject="Introduction to Python Programming",
        level="High School",
        num_chapters=8,
    ).with_inputs("subject", "level", "num_chapters"),
    dspy.Example(
        subject="Climate Change Science",
        level=None,  # All levels
        num_chapters=10,
    ).with_inputs("subject", "level", "num_chapters"),
    # Add more examples as needed
]

# Since BookChaptersGenerator is more complex, we'll show how to optimize its generation
# For now, we'll demonstrate the concept with validating BookInput and then show how
# we might approach optimizing the generator output

def generated_chapters_metric(example, pred, trace=None):
    """
    Validation metric for generated chapter content.
    This would evaluate the actual chapter suggestions produced by the generator.
    """
    if not isinstance(pred, str) or not pred.strip():
        return False

    # Basic quality checks for educational content
    if len(pred.strip()) < 50:  # Too short to be meaningful
        return False

    # Check for educational content elements
    educational_indicators = [
        "chapter",
        "learning",
        "objective",
        "concept",
        "theory",
        "practice",
        "example",
        "exercise",
        "summary",
        "conclusion",
        "introduction",
        "overview",
        "fundamental",
        "principle",
        "method",
        "technique",
    ]

    pred_lower = pred.lower()
    matches = sum(1 for indicator in educational_indicators if indicator in pred_lower)

    # Require several educational indicators in reasonable length content
    if len(pred) > 200 and matches < 5:
        return False

    # Should have some structure (numbers, bullet points, etc.)
    structure_indicators = ["1.", "2.", "3.", "•", "-", "Chapter", "Section"]
    structure_count = sum(1 for indicator in structure_indicators if indicator in pred)

    if structure_count < 3:
        return False

    return True

# Example training data for the generator output (what we want it to produce)
chapter_trainset = [
    dspy.Example(
        subject_input="Renewable Energy Systems",
        level_input="Undergraduate",
        num_chapters_input=12,
        generated_chapters="""Chapter 1: Introduction to Renewable Energy
Chapter 2: Solar Energy Fundamentals
Chapter 3: Wind Power Technology
Chapter 4: Hydroelectric and Ocean Energy
Chapter 5: Geothermal Energy Systems
Chapter 6: Bioenergy and Biomass Conversion
Chapter 7: Energy Storage Technologies
Chapter 8: Grid Integration and Smart Grids
Chapter 9: Energy Economics and Policy
Chapter 10: Environmental Impact Assessment
Chapter 11: Emerging Technologies and Future Trends
Chapter 12: Capstone Project: Designing a Renewable Energy System""",
    ).with_inputs("subject_input", "level_input", "num_chapters_input"),
    dspy.Example(
        subject_input="Web Development with JavaScript",
        level_input="High School",
        num_chapters_input=8,
        generated_chapters="""Chapter 1: Introduction to Web Development
Chapter 2: HTML5 Fundamentals
Chapter 3: CSS3 Styling and Layout
Chapter 4: JavaScript Basics and Syntax
Chapter 5: DOM Manipulation and Events
Chapter 6: Responsive Design and Frameworks
Chapter 7: Working with APIs and AJAX
Chapter 8: Final Project: Building Interactive Web Applications""",
    ).with_inputs("subject_input", "level_input", "num_chapters_input"),
    # Add more examples as needed
]

# Optimize using BootstrapFewShot for BookInput validation

print("Optimizing BookInput validation with Ollama...")
book_input_optimizer = BootstrapFewShot(
    metric=book_input_metric, max_bootstrapped_demos=3, max_labeled_demos=5
)

optimized_book_input_validator = book_input_optimizer.compile(
    BookInput, trainset=trainset
)

print("BookInput validation optimization complete!")

# Test the optimized validator
test_input = BookInput(
    subject="Machine Learning Basics", level="Undergraduate", num_chapters=10
)
print(f"\n=== BookInput Validation Test ===")
print(f"Subject: {test_input.subject}")
print(f"Level: {test_input.level}")
print(f"Num Chapters: {test_input.num_chapters}")
# Note: Since BookInput is primarily a data container, the "optimization" here is about
# validating that inputs make sense - the real value comes in using good examples
# to guide the generator to produce better output

print("\nOptimization scripts created for BookInput validation.")
print("For optimizing actual chapter generation, you would:")
print("1. Collect examples of good chapter suggestions from the generator")
print("2. Train on those examples using the generated_chapters_metric")
print("3. Use the optimized generator to produce better educational content")

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)

