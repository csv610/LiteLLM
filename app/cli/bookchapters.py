import sys
import json
import argparse
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


# Module-level constants
EDUCATION_LEVELS = [
    'Middle School',
    'High School',
    'Undergraduate',
    'Post-Graduate',
    'Professional',
    'General Public'
]

LEVEL_CODES = {
    'Middle School': '0',
    'High School': '1',
    'Undergraduate': '2',
    'Post-Graduate': '3',
    'Professional': '4',
    'General Public': '5'
}

DEFAULT_MODEL = "ollama/gemma3"
DEFAULT_CHAPTERS = 12


class ChapterSuggestion(BaseModel):
    chapter_number: int = Field(..., description="The sequential number of the chapter within the education level.")
    title: str = Field(..., description="The title of the chapter.")
    summary: str = Field(..., description="A brief summary of what the chapter covers.")
    key_concepts: list[str] = Field(..., description="List of key concepts and topics covered in the chapter.")
    prerequisites: list[str] = Field(default=[], description="What students should know before reading this chapter.")
    learning_objectives: list[str] = Field(..., description="Clear, measurable learning objectives stating exactly what students will be able to understand or do after reading this chapter. Use action verbs like 'identify', 'explain', 'analyze', 'apply', 'evaluate'.")
    page_estimate: int = Field(default=0, description="Estimated number of pages for this chapter.")
    observations: list[str] = Field(..., description="Hands-on observations and phenomena students should notice or look for related to the chapter content. Provide at least 5 detailed observations.")
    experiments: list[str] = Field(..., description="Practical experiments or demonstrations students can conduct to verify or explore concepts covered in this chapter. Provide at least 5 detailed experiments.")
    projects: list[str] = Field(..., description="Real-world projects or creative assignments that allow students to apply the chapter's concepts and learning objectives. Provide at least 5 detailed projects.")


class EducationLevel(BaseModel):
    level: str = Field(..., description="The education level (e.g., 'Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional', 'General Public').")
    age_range: str = Field(..., description="The typical age range or audience for this education level.")
    chapters: list[ChapterSuggestion] = Field(..., description="List of chapters appropriate for this education level.")
    rationale: str = Field(..., description="Explanation of why these chapters are appropriate for this level and how they engage the target audience.")


class BookChaptersResponse(BaseModel):
    subject: str = Field(..., description="The subject or topic being covered.")
    description: str = Field(..., description="A brief description of the overall learning progression across all levels.")
    education_levels: list[EducationLevel] = Field(..., description="List of education levels with their corresponding chapters.")


def build_prompt(subject, level, num_chapters):
    """Build the prompt for chapter generation."""
    if level is None:
        header = f"Create a comprehensive curriculum for teaching '{subject}' across all 6 education levels including General Public."
    else:
        header = f"Create a curriculum for teaching '{subject}' at the {level} level."

    return f"""{header}

Generate exactly {num_chapters} chapters.

For the education level(s):
1. Suggest appropriate chapters that engage and educate the target audience
2. Ensure concepts are age, experience, and audience-appropriate
3. Include prerequisites where applicable
4. For each chapter, provide CLEAR and MEASURABLE LEARNING OBJECTIVES using action verbs (identify, explain, analyze, apply, evaluate, synthesize, etc.)
5. Learning objectives should state exactly what the audience will be able to do or understand after completing the chapter

The curriculum should show logical progression:
- Middle School: introduces fundamental concepts with simple explanations
- High School: builds on fundamentals with more depth and real-world applications
- Undergraduate: covers theory, analysis, and practical applications
- Post-Graduate: includes advanced concepts, research, and specialized topics
- Professional: focuses on practical application, standards, and industry practices
- General Public: fascinating topics for general audience with no specialized background, emphasizing curiosity, wonder, and real-world relevance without technical jargon

For each chapter include:
- Chapter number (sequential within the level)
- Title
- Summary of content
- Key concepts
- Prerequisites (what audience needs to know first)
- Learning objectives (3-5 clear, measurable, action-oriented statements using verbs like: identify, explain, describe, analyze, apply, evaluate, compare, synthesize, appreciate, discover)
- Estimated page count
- Observations (AT LEAST 5 hands-on observations or phenomena students should notice or look for)
- Experiments (AT LEAST 5 practical experiments or demonstrations students can conduct)
- Projects (AT LEAST 5 real-world projects or creative assignments to apply concepts)

Make sure the learning is truly incremental and builds naturally. For General Public, emphasize engaging storytelling, real-world examples, and the "wow factor" of the subject. Adapt the observations, experiments, and projects to be age-appropriate and feasible for the education level."""


def generate_filename(subject, level):
    """Generate output filename based on subject and level."""
    subject_normalized = subject.replace(' ', '_').lower()
    level_code = LEVEL_CODES.get(level, '0') if level else 'all'
    return f"{subject_normalized}_{level_code}.json"


def save_response(data, filename):
    """Save response data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def cli(subject, level=None, num_chapters=DEFAULT_CHAPTERS, model_name=DEFAULT_MODEL):
    """Generate chapter suggestions for a subject at a specific education level using LiteClient.

    Args:
        subject (str): The subject or topic to create curriculum for
        level (str): The education level. If None, generates for all levels.
        num_chapters (int): Number of chapters to generate
        model_name (str): The model to use for generation
    """
    model_config = ModelConfig(model=model_name, temperature=0.2)
    client = LiteClient(model_config=model_config)

    prompt = build_prompt(subject, level, num_chapters)
    model_input = ModelInput(user_prompt=prompt, response_format=BookChaptersResponse)

    response = client.generate_text(model_input=model_input)

    # Handle both Pydantic model and string responses
    if isinstance(response, BookChaptersResponse):
        data = response.model_dump()
    elif isinstance(response, str):
        data = json.loads(response)
    else:
        raise ValueError(f"Unexpected response type: {type(response).__name__}")

    output_file = generate_filename(subject, level)
    save_response(data, output_file)

    level_display = level if level else 'All Levels'
    print(f"Chapter suggestions for '{subject}' ({level_display}) saved to {output_file}")


if __name__ == "__main__":
    levels_help = '\n'.join(f"  {code}: {level}" for level, code in LEVEL_CODES.items())

    parser = argparse.ArgumentParser(
        description="Generate educational curriculum chapters for any subject across education levels.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Education Levels:
{levels_help}

Examples:
  # Generate for all 6 levels (default)
  python bookchapters.py 'Quantum Physics'

  # Generate for specific level
  python bookchapters.py 'Climate Change' -l 'High School'
  python bookchapters.py 'Machine Learning' -l Undergraduate -n 5

  # Use custom model
  python bookchapters.py 'AI' -l 'Post-Graduate' -m 'openai/gpt-4'
  python bookchapters.py 'Black Holes' -l 'General Public' -n 8 -m 'anthropic/claude-3-5-sonnet'
        """
    )

    parser.add_argument(
        "subject",
        help="Subject or topic to create curriculum for"
    )
    parser.add_argument(
        "-l", "--level",
        default=None,
        help="Education level (0-5). Omit to generate for all 6 levels"
    )
    parser.add_argument(
        "-n", "--chapters",
        type=int,
        default=DEFAULT_CHAPTERS,
        help=f"Number of chapters per level (default: {DEFAULT_CHAPTERS})"
    )
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"LLM model to use (default: {DEFAULT_MODEL})"
    )

    args = parser.parse_args()
    cli(args.subject, args.level, args.chapters, args.model)
