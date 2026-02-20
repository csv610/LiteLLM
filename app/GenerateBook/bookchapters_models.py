"""bookchapters_models.py - Pydantic models for book chapters generation

Contains data models for educational curriculum generation including
chapters, education levels, and book structure.
"""

from pydantic import BaseModel, Field
from typing import Optional


class BookInput(BaseModel):
    """Input parameters for book chapters generation."""
    subject: str = Field(..., description="The subject or topic to create curriculum for")
    level: Optional[str] = Field(default=None, description="The education level")
    num_chapters: int = Field(default=12, description="Number of chapters to generate")


class ChapterSuggestion(BaseModel):
    """Represents a suggested chapter within an educational curriculum."""
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
    """Represents an education level with its corresponding chapters."""
    level: str = Field(..., description="The education level (e.g., 'Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional', 'General Public').")
    age_range: str = Field(..., description="The typical age range or audience for this education level.")
    chapters: list[ChapterSuggestion] = Field(..., description="List of chapters appropriate for this education level.")
    rationale: str = Field(..., description="Explanation of why these chapters are appropriate for this level and how they engage the target audience.")


class BookChaptersModel(BaseModel):
    """Complete response containing curriculum for all education levels."""
    subject: str = Field(..., description="The subject or topic being covered.")
    description: str = Field(..., description="A brief description of the overall learning progression across all levels.")
    education_levels: list[EducationLevel] = Field(..., description="List of education levels with their corresponding chapters.")
