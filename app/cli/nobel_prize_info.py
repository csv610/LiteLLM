import argparse
import logging
import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# Add project root directory to path to import lite module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from logging_util import setup_logging

logger = setup_logging(str(Path(__file__).parent / "logs" / "nobel_prize_info.log"))

# ==============================================================================
# Pydantic Models
# ==============================================================================

class FAQItem(BaseModel):
    """Frequently asked question about the discovery."""
    question: str = Field(..., description="The frequently asked question")
    answer: str = Field(..., description="The answer to the question")


class GlossaryItem(BaseModel):
    """A glossary term with its definition."""
    term: str = Field(..., description="The technical term or concept")
    definition: str = Field(..., description="Clear, concise definition of the term")


class PersonalBackground(BaseModel):
    """Early life and educational background of the laureate."""
    birth_date: str = Field(..., description="Birth date (format: YYYY-MM-DD or approximate year if exact date unknown)")
    birth_place: str = Field(..., description="Place of birth (city, country)")
    nationality: str = Field(..., description="Primary nationality/nationalities")
    family_background: str = Field(..., description="Family background, parents' professions, and early influences. Include relevant family members who influenced their career.")
    education: list[str] = Field(..., description="Chronological list of educational institutions and degrees (e.g., 'B.Sc. Physics, University of X (1975)', 'Ph.D. Chemistry, University of Y (1980)')", min_length=1)
    early_influences: str = Field(..., description="Key people, mentors, or experiences that shaped their scientific interests and career direction during formative years")


class CareerPosition(BaseModel):
    """Represents a single career position or role."""
    title: str = Field(..., description="Job title or position (e.g., 'Professor of Physics', 'Research Scientist')")
    institution: str = Field(..., description="Institution or organization name")
    location: str = Field(..., description="City and country of the institution")
    start_year: int = Field(..., description="Start year of position", ge=1900, le=2025)
    end_year: Optional[int] = Field(None, description="End year of position (null if current)")
    description: str = Field(..., description="Brief description of role and responsibilities")


class BroaderRecognition(BaseModel):
    """Recognition, awards, and broader roles outside the Nobel Prize."""
    honors_and_awards: list[str] = Field(..., description="List of major awards and honors received (excluding Nobel Prize)", min_length=1)
    academy_memberships: list[str] = Field(..., description="Memberships in prestigious academies and societies (e.g., 'Fellow of the Royal Society', 'Member of National Academy of Sciences')", min_length=1)
    editorial_roles: list[str] = Field(..., description="Editorial positions in scientific journals and publications", min_length=0)
    mentorship_contributions: str = Field(..., description="Notable students, postdocs, and collaborators mentored; their achievements and contributions to science")
    leadership_roles: list[str] = Field(..., description="Leadership positions in scientific organizations, departments, or research initiatives", min_length=0)
    public_engagement: str = Field(..., description="Public communication, outreach efforts, scientific advocacy, or policy influence. Include speaking engagements, public lectures, and involvement in science communication.")


class PrizeWinner(BaseModel):
    """Represents a Nobel Prize winner and their contribution."""

    name: str = Field(..., description="Full name of the prize winner(s)")
    year: int = Field(..., description="Year the prize was awarded", ge=1901, le=2025)
    category: str = Field(..., description="Nobel Prize category (Physics, Chemistry, Medicine, etc.)")
    contribution: str = Field(
        ...,
        description="Objective, concise description of the scientific work that won the prize. Focus on what was discovered/invented, not superlatives."
    )

    # Biographical Information
    personal_background: PersonalBackground = Field(..., description="Early life, education, and family background of the laureate")
    career_timeline: list[CareerPosition] = Field(..., description="Chronological list of major career positions and institutional affiliations", min_length=1)
    broader_recognition: BroaderRecognition = Field(..., description="Honors, recognition, and broader roles in the scientific community outside the Nobel Prize")

    # Historical context - objective facts
    history: str = Field(
        ...,
        description="Chronological history of the discovery with specific dates, names, and events. Include key experimental methods and findings. Avoid subjective language. Focus on facts and progression of research.",
        min_length=50
    )

    # Scientific impact - measurable effects
    impact: str = Field(
        ...,
        description="Measurable scientific impact: how the discovery changed our understanding of natural phenomena. Include specific examples of what became possible because of this work. Avoid phrases like 'profound,' 'revolutionary,' or 'transformed.' Use objective language.",
        min_length=50
    )

    # Cross-disciplinary influence
    foundation: str = Field(
        ...,
        description="Specific ways this discovery influenced or enabled research in other scientific fields. Give concrete examples of which fields were affected and how. Avoid vague statements.",
        min_length=50
    )

    # Practical applications - real world use cases
    applications: list[str] = Field(
        ...,
        description="List of specific, verified real-world applications and implementations. Only include applications that are actually used today or in development. Be concrete, not speculative.",
        min_length=1
    )

    # Current relevance - factual assessment
    relevancy: str = Field(
        ...,
        description="How the idea is still valid and relevant today. Explain current research directions, active fields using this work, ongoing investigations, and practical uses in modern science and industry. Include specific examples of how the discovery continues to influence contemporary work. Avoid subjective claims about importance.",
        min_length=50
    )

    # Subsequent research - building on the work
    advancements: list[str] = Field(
        ...,
        description="List of specific advancements, new discoveries, and technologies developed based on this work. Include years where known. Focus on factual extensions of the original discovery.",
        min_length=1
    )

    # Methodological improvements
    refinements: list[str] = Field(
        ...,
        description="List of major improvements to the experimental methods, theoretical models, or practical techniques developed after the original work. Be specific about what was improved and how.",
        min_length=1
    )

    # Open questions and limitations
    gaps: list[str] = Field(
        ...,
        description="List of known limitations, open questions, unsolved problems, or areas not yet understood. Be specific about what remains unknown or incompletely explained.",
        min_length=1
    )

    # Important keywords
    keywords: list[str] = Field(
        ...,
        description="List of important keywords and technical terms related to the discovery. Include core concepts, methods, substances, phenomena, and fields that are central to understanding this work.",
        min_length=1
    )

    # Learning objectives
    learning_objectives: list[str] = Field(
        ...,
        description="List of learning objectives: what a student can learn from this discovery. Include conceptual understanding, methodological approaches, problem-solving techniques, and insights into the scientific process.",
        min_length=1
    )

    # Frequently asked questions about the discovery
    faq: list[FAQItem] = Field(
        ...,
        description="List of frequently asked questions about the discovery. Include common misconceptions, practical questions, and educational queries.",
        min_length=1
    )

    # Glossary of terms
    glossary: list[GlossaryItem] = Field(
        ...,
        description="List of key terms and concepts related to the discovery with clear, concise definitions. Include specialized vocabulary, technical terminology, and important concepts needed to understand the work.",
        min_length=1
    )


class PrizeResponse(BaseModel):
    """Response containing a list of Nobel Prize winners."""
    winners: list[PrizeWinner]


# ==============================================================================
# Core Functions
# ==============================================================================

def create_prompt(category: str, year: str) -> str:
    """
    Create the prompt for fetching Nobel Prize information.

    Args:
        category: Nobel Prize category
        year: Year of the prize

    Returns:
        Formatted prompt string for the LLM
    """
    return f"""Provide detailed, objective information about Nobel Prize winners in {category} for {year}.

IMPORTANT: Focus on factual, educational content. Avoid subjective language and superlatives.

For each winner, provide:

BIOGRAPHICAL INFORMATION:
1. Personal Background:
   - Birth date and place
   - Nationality
   - Family background and parents' professions
   - Educational timeline with institutions, degrees, and years
   - Early influences and mentors who shaped their scientific direction

2. Career Timeline:
   - Chronological list of major positions (title, institution, location, start/end years)
   - Key roles including postdoctoral positions, faculty appointments, research leadership
   - Institutional affiliations and their significance

3. Broader Recognition:
   - Major awards and honors (excluding Nobel Prize)
   - Academy and society memberships
   - Editorial roles in scientific journals
   - Notable students, postdocs, and collaborators mentored
   - Leadership positions in scientific organizations
   - Public engagement, outreach, and scientific advocacy efforts

SCIENTIFIC WORK:
4. Contribution: What they discovered or invented (facts only)
5. History: Chronological facts with dates, names, methods used
6. Impact: Measurable changes in scientific understanding - what became possible?
7. Foundation: Specific cross-disciplinary influence with concrete examples
8. Applications: Real-world uses, not speculative
9. Relevancy: How the idea is still valid and relevant today - explain current research, active fields using this work, and practical uses in modern science/industry
10. Advancements: Specific improvements and extensions with dates
11. Refinements: Methodological and theoretical improvements
12. Gaps: Unknown questions, limitations, and unsolved problems

EDUCATIONAL CONTENT:
13. Keywords: Important keywords and technical terms related to the discovery (core concepts, methods, substances, phenomena, and fields)
14. Learning Objectives: What a student can learn from this discovery (conceptual understanding, methodological approaches, problem-solving techniques, insights into the scientific process)
15. FAQ: Frequently asked questions with answers (include common misconceptions, practical questions, and educational queries)
16. Glossary: Dictionary of key terms and concepts with clear, concise definitions (specialized vocabulary, technical terminology, important concepts needed to understand the work)

Use objective language. Avoid words like "revolutionary," "profound," "amazing," "transformed."
Instead, describe what specifically changed and how we know it changed."""


def _handle_api_error(error: Exception) -> None:
    """
    Handle and translate API errors to meaningful exceptions.

    Args:
        error: Exception raised during API call

    Raises:
        RuntimeError: With appropriate error message
    """
    error_str = str(error).lower()

    if "401" in str(error) or "authentication" in error_str:
        logger.error("Authentication failed: Check your API credentials")
        raise RuntimeError("API authentication failed. Check LITELLM_API_KEY or model-specific credentials.")
    elif "429" in str(error):
        logger.error("Rate limit exceeded")
        raise RuntimeError("API rate limit exceeded. Please try again later.")
    elif "404" in str(error):
        logger.error("Model not found")
        raise RuntimeError("Model not found or not available.")
    else:
        logger.error(f"Unexpected error: {error}")
        raise RuntimeError(f"Failed to fetch Nobel Prize information: {error}")


def fetch_nobel_winners(
    category: str,
    year: str,
    model: Optional[str] = None
) -> list[PrizeWinner]:
    """
    Fetch Nobel Prize winners for a specific field and year.

    Args:
        category: Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)
        year: Year of the prize
        model: LLM model to use (defaults to environment variable or gemini/gemini-2.5-flash)

    Returns:
        List of PrizeWinner instances

    Raises:
        ValueError: If API response is invalid or model response doesn't match schema
        RuntimeError: If API call fails or required credentials are missing
    """
    if model is None:
        model = os.getenv("NOBEL_PRIZE_MODEL", "gemini/gemini-2.5-flash")

    if not re.match(r'^[a-zA-Z0-9\-\./_]+$', model):
        raise ValueError(f"Invalid model name: {model}. Only alphanumeric characters, hyphens, slashes, dots, and underscores are allowed.")

    logger.info(f"Fetching Nobel Prize information for {category} in {year} using model: {model}")

    try:
        # Create ModelConfig and LiteClient
        model_config = ModelConfig(model=model, temperature=0.2)
        client = LiteClient(model_config=model_config)

        # Create ModelInput with prompt and response format
        model_input = ModelInput(
            user_prompt=create_prompt(category, year),
            response_format=PrizeResponse
        )

        # Generate text using LiteClient
        response_content = client.generate_text(model_input=model_input)

        # Parse the response
        if isinstance(response_content, str):
            prize_response = PrizeResponse.model_validate_json(response_content)
        else:
            raise ValueError("Expected string response from model")

        if not prize_response.winners or len(prize_response.winners) == 0:
            raise ValueError("No winners returned in response")

        logger.info(f"Successfully fetched {len(prize_response.winners)} winner(s)")
        return prize_response.winners

    except Exception as e:
        _handle_api_error(e)


# ==============================================================================
# Validation Functions
# ==============================================================================

def validate_year(year_str: str) -> int:
    """
    Validate and convert year string to integer.

    Args:
        year_str: Year as string

    Returns:
        Year as integer

    Raises:
        argparse.ArgumentTypeError: If year is invalid
    """
    try:
        year_int = int(year_str)
        current_year = datetime.now().year
        if year_int < 1901:
            raise argparse.ArgumentTypeError(
                f"Nobel Prizes began in 1901, got {year_int}"
            )
        if year_int > current_year:
            raise argparse.ArgumentTypeError(
                f"Year cannot be in the future (current year: {current_year})"
            )
        return year_int
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Year must be a valid number, got '{year_str}'"
        )


def validate_category(category_str: str) -> str:
    """
    Validate and normalize Nobel Prize category.

    Args:
        category_str: Category name (case-insensitive)

    Returns:
        Normalized category name

    Raises:
        argparse.ArgumentTypeError: If category is invalid
    """
    valid_fields = ["Physics", "Chemistry", "Medicine", "Literature", "Peace", "Economics"]
    valid_fields_lower = [f.lower() for f in valid_fields]

    if category_str.lower() not in valid_fields_lower:
        raise argparse.ArgumentTypeError(
            f"'{category_str}' is not a valid Nobel Prize category. "
            f"Valid categories are: {', '.join(valid_fields)}"
        )

    # Return normalized (proper case) field
    return valid_fields[valid_fields_lower.index(category_str.lower())]


# ==============================================================================
# CLI Functions
# ==============================================================================

def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Fetch detailed information about Nobel Prize winners",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nobel_prize_info.py -c Physics -y 2023
  python nobel_prize_info.py --category Chemistry --year 2022
  python nobel_prize_info.py -c Medicine -y 2021 -m claude-3-opus
  NOBEL_PRIZE_MODEL=gpt-4 python nobel_prize_info.py -c Literature -y 2020
        """
    )

    parser.add_argument(
        "-c", "--category",
        required=True,
        type=validate_category,
        help="Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)"
    )

    parser.add_argument(
        "-y", "--year",
        required=True,
        type=validate_year,
        help="Year of the Nobel Prize (1901 onwards)"
    )

    parser.add_argument(
        "-m", "--model",
        default=None,
        help="LLM model to use (default: $NOBEL_PRIZE_MODEL or gemini/gemini-2.5-flash)"
    )

    return parser



def main() -> int:
    """
    Main entry point for the Nobel Prize information CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = arguments_parser()
    args = parser.parse_args()

    try:
        logger.info(f"Fetching Nobel Prize information for {args.category} in {args.year}...")

        winners = fetch_nobel_winners(args.category, str(args.year), model=args.model)

        if not winners:
            logger.error("No winners returned from API")
            print("Error: No winners found for the specified category and year.")
            return 1

        # Save to JSON file with format: {category}_{year}.json
        output_filename = os.path.basename(f"{args.category.lower()}_{args.year}.json")

        data_to_save = {
            "category": args.category,
            "year": args.year,
            "winners_count": len(winners),
            "winners": [winner.model_dump() for winner in winners]
        }

        with open(output_filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)

        os.chmod(output_filename, 0o600)

        logger.info(f"Successfully saved {len(winners)} winner(s) to {output_filename}")
        print(f"Results saved to {output_filename}")
        print(f"Winners retrieved: {len(winners)}")
        for i, winner in enumerate(winners, 1):
            print(f"  {i}. {winner.name} ({winner.year})")

        return 0

    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return 1
    except IOError as e:
        logger.error(f"File I/O error: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
