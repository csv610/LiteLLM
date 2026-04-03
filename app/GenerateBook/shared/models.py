"""Pydantic models for the three-agent book chapters workflow."""

from lite import ModelOutput


class BookInput(BaseModel):
    """Input parameters for book chapters generation."""

    subject: str = Field(
        ..., description="The subject or topic to create curriculum for"
    )
    level: Optional[str] = Field(default=None, description="The education level")
    num_chapters: int = Field(default=12, description="Number of chapters to generate")


class PlannedLevel(BaseModel):
    """High-level curriculum plan for one audience segment."""

    level: str = Field(..., description="The education level or audience.")
    audience: str = Field(..., description="Short description of the target audience.")
    age_range: str = Field(..., description="Typical age range or learner profile.")
    sequencing_rationale: str = Field(
        ..., description="Why this order fits the audience."
    )
    chapter_outline: list[str] = Field(
        ..., description="Ordered chapter titles or themes."
    )


class CurriculumPlanModel(BaseModel):
    """Output from the planner agent."""

    subject: str = Field(..., description="The subject or topic being covered.")
    planning_notes: str = Field(..., description="How the curriculum should progress.")
    levels: list[PlannedLevel] = Field(
        ..., description="Planned structure for each requested level."
    )


class ChapterSuggestion(BaseModel):
    """Represents a suggested chapter within an educational curriculum."""

    chapter_number: int = Field(
        ...,
        description="The sequential number of the chapter within the education level.",
    )
    title: str = Field(..., description="The title of the chapter.")
    summary: str = Field(..., description="A brief summary of what the chapter covers.")
    key_concepts: list[str] = Field(
        ..., description="List of key concepts and topics covered in the chapter."
    )
    prerequisites: list[str] = Field(
        default=[], description="What students should know before reading this chapter."
    )
    learning_objectives: list[str] = Field(
        ...,
        description="Clear, measurable learning objectives stating exactly what students will be able to understand or do after reading this chapter. Use action verbs like 'identify', 'explain', 'analyze', 'apply', 'evaluate'.",
    )
    page_estimate: int = Field(
        default=0, description="Estimated number of pages for this chapter."
    )
    observations: list[str] = Field(
        ...,
        description="Hands-on observations and phenomena students should notice or look for related to the chapter content. Provide at least 5 detailed observations.",
    )
    experiments: list[str] = Field(
        ...,
        description="Practical experiments or demonstrations students can conduct to verify or explore concepts covered in this chapter. Provide at least 5 detailed experiments.",
    )
    projects: list[str] = Field(
        ...,
        description="Real-world projects or creative assignments that allow students to apply the chapter's concepts and learning objectives. Provide at least 5 detailed projects.",
    )


class EducationLevel(BaseModel):
    """Represents an education level with its corresponding chapters."""

    level: str = Field(
        ...,
        description="The education level (e.g., 'Middle School', 'High School', 'Undergraduate', 'Post-Graduate', 'Professional', 'General Public').",
    )
    age_range: str = Field(
        ..., description="The typical age range or audience for this education level."
    )
    chapters: list[ChapterSuggestion] = Field(
        ..., description="List of chapters appropriate for this education level."
    )
    rationale: str = Field(
        ...,
        description="Explanation of why these chapters are appropriate for this level and how they engage the target audience.",
    )


class AgentTrace(BaseModel):
    """Brief metadata showing the three-agent pipeline."""

    planner_notes: str = Field(
        ..., description="Planner summary used by the generator."
    )
    reviewer_summary: str = Field(
        ..., description="Reviewer summary of checks and fixes."
    )
    revision_count: int = Field(
        default=0, description="How many material corrections the reviewer made."
    )


class BookChaptersModel(BaseModel):
    """Complete response containing curriculum for all education levels."""

    subject: str = Field(..., description="The subject or topic being covered.")
    description: str = Field(
        ...,
        description="A brief description of the overall learning progression across all levels.",
    )
    education_levels: list[EducationLevel] = Field(
        ..., description="List of education levels with their corresponding chapters."
    )
    agent_trace: Optional[AgentTrace] = Field(
        default=None, description="Metadata from the three-agent workflow."
    )


class ReviewIssue(BaseModel):
    """One issue found by the reviewer."""

    level: str = Field(..., description="The affected education level.")
    chapter_number: Optional[int] = Field(
        default=None, description="Affected chapter if applicable."
    )
    severity: str = Field(
        ..., description="Issue severity, such as low, medium, or high."
    )
    issue: str = Field(..., description="Description of the issue found.")
    fix: str = Field(..., description="What was changed or should be changed.")


class ReviewedBookChaptersModel(BaseModel):
    """Reviewer output containing the corrected final curriculum."""

    reviewer_summary: str = Field(
        ..., description="Summary of checks and corrections performed."
    )
    revision_count: int = Field(
        ..., description="Count of meaningful fixes made by the reviewer."
    )
    issues_found: list[ReviewIssue] = Field(
        default_factory=list, description="Issues discovered during review."
    )
    final_curriculum: BookChaptersModel = Field(
        ..., description="The corrected final curriculum."
    )


BookChapters = BookChaptersModel


from typing import Any
