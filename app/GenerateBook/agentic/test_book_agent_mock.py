import pytest
from unittest.mock import patch, MagicMock
import json

from app.GenerateBook.agentic.bookchapters_generator import BookChaptersGenerator
from app.GenerateBook.agentic.bookchapters_models import (
    BookInput, CurriculumPlanModel, BookChaptersModel, 
    ReviewedBookChaptersModel, ChapterSuggestion, EducationLevel, PlannedLevel
)
from lite.config import ModelConfig

@pytest.fixture
def mock_lite_client():
    with patch('app.GenerateBook.agentic.bookchapters_generator.LiteClient') as mock:
        yield mock

def test_generate_book_agentic(mock_lite_client):
    instance = mock_lite_client.return_value
    
    # 1. Planner
    planned_level = PlannedLevel(
        level="Intermediate",
        audience="Students",
        age_range="18-22",
        sequencing_rationale="Logical flow",
        chapter_outline=["Intro"]
    )
    plan = CurriculumPlanModel(
        subject="Quantum Physics",
        planning_notes="Start with basics",
        levels=[planned_level]
    )
    
    # 2. Generator
    chapter = ChapterSuggestion(
        chapter_number=1,
        title="Chapter 1",
        summary="Intro to Quantum",
        key_concepts=["Wave-particle duality"],
        learning_objectives=["Explain duality"],
        observations=["Double slit"],
        experiments=["Laser test"],
        projects=["Paper on Bohr"]
    )
    edu_level = EducationLevel(
        level="Intermediate",
        age_range="18-22",
        chapters=[chapter],
        rationale="Fits undergrads"
    )
    draft = BookChaptersModel(
        subject="Quantum Physics",
        description="A book on quantum",
        education_levels=[edu_level]
    )
    
    # 3. Reviewer
    reviewed = ReviewedBookChaptersModel(
        final_curriculum=draft,
        reviewer_summary="Good draft",
        revision_count=0,
        issues_found=[]
    )
    
    instance.generate_text.side_effect = [plan, draft, reviewed]
    
    generator = BookChaptersGenerator(ModelConfig(model="mock"))
    book_input = BookInput(subject="Quantum Physics", level="Intermediate", num_chapters=1)
    result = generator.generate_text(book_input)
    
    assert result.subject == "Quantum Physics"
    assert len(result.education_levels) == 1
    assert instance.generate_text.call_count == 3
