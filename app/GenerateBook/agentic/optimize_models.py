"""
optimize_models.py - Script to optimize Pydantic models for GenerateBook using DSPydantic with Ollama.
"""

import dspy
from bookchapters_models import BookInput
from bookchapters_generator import BookChaptersGenerator

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
from dspy.teleprompt import BootstrapFewShot

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


from typing import Any

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
