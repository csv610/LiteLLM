import sys
import json
import argparse
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


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


def cli(subject, level=None, num_chapters=None, model_name=None):
    """Generate chapter suggestions for a subject at a specific education level using LiteClient.

    Args:
        subject (str): The subject or topic to create curriculum for
        level (str): The education level (e.g., 'High School', 'Undergraduate', 'General Public')
                    If None, defaults to all 6 levels: ['Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional', 'General Public']
        num_chapters (int): Number of chapters to generate for the level
                           If None, defaults to 12 chapters
        model_name (str): The model to use for generation
                         Default: 'gemini/gemini-2.5-flash'
    """
    if model_name is None:
        model_name = "gemini/gemini-2.5-flash"

    model_config = ModelConfig(model=model_name, temperature=0.2)
    client = LiteClient(model_config=model_config)

    # Set defaults if not provided
    if level is None:
        levels = ['Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional', 'General Public']
        prompt_header = f"Create a comprehensive curriculum for teaching '{subject}' across all 6 education levels including General Public."
        generate_all_levels = True
    else:
        levels = [level]
        prompt_header = f"Create a curriculum for teaching '{subject}' at the {level} level."
        generate_all_levels = False

    chapters_instruction = ""
    if num_chapters:
        chapters_instruction = f"Generate exactly {num_chapters} chapters."
    else:
        chapters_instruction = "Generate exactly 12 chapters."
        num_chapters = 12

    prompt = f"""{prompt_header}

{chapters_instruction}

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

    model_input = ModelInput(user_prompt=prompt, response_format=BookChaptersResponse)

    response_content = client.generate_text(model_input=model_input)

    # Parse and save the formatted JSON output
    if isinstance(response_content, str):
        data = json.loads(response_content)
        # Generate automatic filename with numeric level codes
        subject_normalized = subject.replace(' ', '_').lower()

        # Map education levels to numeric codes
        level_codes = {
            'Middle School': '0',
            'High School': '1',
            'Undergraduate': '2',
            'Post-Graduate': '3',
            'Professional': '4',
            'General Public': '5'
        }

        if level:
            level_code = level_codes.get(level, '0')
            output_file = f"{subject_normalized}_{level_code}.json"
        else:
            output_file = f"{subject_normalized}_all.json"

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Chapter suggestions for '{subject}' ({level if level else 'All Levels'}) saved to {output_file}")
    else:
        print("Error: Expected string response from model")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate chapter suggestions for a subject at a specific education level using LiteClient.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bookchapters.py 'Quantum Physics'
  python bookchapters.py 'Climate Change' -l 'High School'
  python bookchapters.py 'Machine Learning' --level Undergraduate -n 5
  python bookchapters.py 'AI' -l 'Post-Graduate' -n 6 -m 'gpt-4'
  python bookchapters.py 'Black Holes' -l 'General Public' -n 8
        """
    )

    parser.add_argument(
        "subject",
        help="The subject or topic to create curriculum for"
    )
    parser.add_argument(
        "-l", "--level",
        default=None,
        help="Single education level to focus on. Available levels: 'Middle School' (0), 'High School' (1), 'Undergraduate' (2), 'Post-Graduate' (3), 'Professional' (4), 'General Public' (5). Default: Generate curriculum for all 6 levels"
    )
    parser.add_argument(
        "-n", "--chapters",
        type=int,
        default=None,
        help="Number of chapters to generate (default: 12)"
    )
    parser.add_argument(
        "-m", "--model",
        default=None,
        help="Model to use for generation (default: 'gemini/gemini-2.5-flash')"
    )

    args = parser.parse_args()
    cli(args.subject, args.level, args.chapters, args.model)
