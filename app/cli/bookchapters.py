import sys
import json
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


class EducationLevel(BaseModel):
    level: str = Field(..., description="The education level (e.g., 'Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional').")
    age_range: str = Field(..., description="The typical age range for this education level.")
    chapters: list[ChapterSuggestion] = Field(..., description="List of chapters appropriate for this education level.")
    rationale: str = Field(..., description="Explanation of why these chapters are appropriate for this level and how they build on previous levels.")


class BookChaptersResponse(BaseModel):
    subject: str = Field(..., description="The subject or topic being covered.")
    description: str = Field(..., description="A brief description of the overall learning progression across all levels.")
    education_levels: list[EducationLevel] = Field(..., description="List of education levels with their corresponding chapters.")


def cli(subject, level=None, num_chapters=None, model_name=None):
    """Generate chapter suggestions for a subject at a specific education level using LiteClient.

    Args:
        subject (str): The subject or topic to create curriculum for
        level (str): The education level (e.g., 'High School', 'Undergraduate')
                    If None, defaults to all 5 levels: ['Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional']
        num_chapters (int): Number of chapters to generate for the level
                           If None, defaults to an appropriate number based on the level
        model_name (str): The model to use for generation
                         Default: 'gemini/gemini-2.5-flash'
    """
    if model_name is None:
        model_name = "gemini/gemini-2.5-flash"

    model_config = ModelConfig(model=model_name, temperature=0.2)
    client = LiteClient(model_config=model_config)

    # Set defaults if not provided
    if level is None:
        levels = ['Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional']
        prompt_header = f"Create a comprehensive curriculum for teaching '{subject}' across all 5 education levels."
        generate_all_levels = True
    else:
        levels = [level]
        prompt_header = f"Create a curriculum for teaching '{subject}' at the {level} level."
        generate_all_levels = False

    chapters_instruction = ""
    if num_chapters:
        chapters_instruction = f"Generate exactly {num_chapters} chapters."
    else:
        chapters_instruction = "Generate an appropriate number of chapters (typically 4-7 chapters for single level, with more for higher levels)."

    prompt = f"""{prompt_header}

{chapters_instruction}

For the education level(s):
1. Suggest appropriate chapters that build incrementally on each other
2. Ensure concepts are age and experience-appropriate
3. Include prerequisites where applicable
4. For each chapter, provide CLEAR and MEASURABLE LEARNING OBJECTIVES using action verbs (identify, explain, analyze, apply, evaluate, synthesize, etc.)
5. Learning objectives should state exactly what students will be able to do or understand after completing the chapter

The curriculum should show logical progression:
- Middle School: introduces fundamental concepts with simple explanations
- High School: builds on fundamentals with more depth and real-world applications
- Undergraduate: covers theory, analysis, and practical applications
- Post-Graduate: includes advanced concepts, research, and specialized topics
- Professional: focuses on practical application, standards, and industry practices

For each chapter include:
- Chapter number (sequential within the level)
- Title
- Summary of content
- Key concepts
- Prerequisites (what students need to know first)
- Learning objectives (3-5 clear, measurable, action-oriented statements using verbs like: identify, explain, describe, analyze, apply, evaluate, compare, synthesize)
- Estimated page count

Make sure the learning is truly incremental and builds naturally."""

    model_input = ModelInput(user_prompt=prompt, response_format=BookChaptersResponse)

    response_content = client.generate_text(model_input=model_input)

    # Parse and save the formatted JSON output
    if isinstance(response_content, str):
        data = json.loads(response_content)
        if level:
            output_file = f"{subject.replace(' ', '_').lower()}_{level.replace(' ', '_').lower()}_chapters.json"
        else:
            output_file = f"{subject.replace(' ', '_').lower()}_chapters.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Chapter suggestions for '{subject}' ({level if level else 'All Levels'}) saved to {output_file}")
    else:
        print("Error: Expected string response from model")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bookchapters.py <subject> [OPTIONS]")
        print()
        print("Arguments:")
        print("  subject                    Required. The subject or topic to create curriculum for")
        print()
        print("Options:")
        print("  -l, --level LEVEL          Single education level to focus on")
        print("                            Available levels: 'Middle School', 'High School', 'Undergraduate',")
        print("                            'Post-Graduate', 'Professional'")
        print("                            Default: Generate curriculum for all 5 levels")
        print("  -n, --chapters N           Number of chapters to generate")
        print("                            Default: Auto-determined based on appropriateness")
        print("  -m, --model MODEL          Model to use for generation")
        print("                            Default: 'gemini/gemini-2.5-flash'")
        print()
        print("Examples:")
        print("  python bookchapters.py 'Quantum Physics'")
        print("  python bookchapters.py 'Climate Change' -l 'High School'")
        print("  python bookchapters.py 'Machine Learning' --level Undergraduate -n 5")
        print("  python bookchapters.py 'AI' -l 'Post-Graduate' -n 6 -m 'gpt-4'")
        sys.exit(1)

    subject = sys.argv[1]
    level = None
    num_chapters = None
    model_name = None

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if (sys.argv[i] == '-l' or sys.argv[i] == '--level') and i + 1 < len(sys.argv):
            level = sys.argv[i + 1]
            i += 2
        elif (sys.argv[i] == '-n' or sys.argv[i] == '--chapters') and i + 1 < len(sys.argv):
            try:
                num_chapters = int(sys.argv[i + 1])
            except ValueError:
                print(f"Error: chapters must be an integer, got '{sys.argv[i + 1]}'")
                sys.exit(1)
            i += 2
        elif (sys.argv[i] == '-m' or sys.argv[i] == '--model') and i + 1 < len(sys.argv):
            model_name = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            sys.exit(1)

    cli(subject, level, num_chapters, model_name)
