"""
nobel_prize_models.py - Pydantic models for Nobel Prize information

Contains data models for Nobel Prize winners, their biographical information,
career details, and related educational content.
"""

from pydantic import BaseModel, Field


class FAQItem(BaseModel):
    """Frequently asked question about a discovery."""
    question: str = Field(..., description="The frequently asked question")
    answer: str = Field(..., description="The answer to the question")


class GlossaryItem(BaseModel):
    """A glossary term with its definition."""
    term: str = Field(..., description="The technical term or concept")
    definition: str = Field(..., description="Clear, concise definition of term")


class PersonalBackground(BaseModel):
    """Early life and educational background of laureate."""
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
    end_year: int | None = Field(None, description="End year of position (null if current)")
    description: str = Field(..., description="Brief description of role and responsibilities")


class BroaderRecognition(BaseModel):
    """Recognition, awards, and broader roles outside of Nobel Prize."""
    honors_and_awards: list[str] = Field(..., description="List of major awards and honors received (excluding Nobel Prize)", min_length=1)
    academy_memberships: list[str] = Field(..., description="Memberships in prestigious academies and societies (e.g., 'Fellow of Royal Society', 'Member of National Academy of Sciences')", min_length=1)
    editorial_roles: list[str] = Field(..., description="Editorial positions in scientific journals and publications", min_length=0)
    mentorship_contributions: str = Field(..., description="Notable students, postdocs, and collaborators mentored; their achievements and contributions to science")
    leadership_roles: list[str] = Field(..., description="Leadership positions in scientific organizations, departments, or research initiatives", min_length=0)
    public_engagement: str = Field(..., description="Public communication, outreach efforts, scientific advocacy, or policy influence. Include speaking engagements, public lectures, and involvement in science communication.")


class PrizeWinner(BaseModel):
    """Represents a Nobel Prize winner and their contribution."""

    name: str = Field(..., description="Full name of the prize winner(s)")
    year: int = Field(..., description="Year of prize was awarded", ge=1901, le=2025)
    category: str = Field(..., description="Nobel Prize category (Physics, Chemistry, Medicine, etc.)")
    contribution: str = Field(
        ...,
        description="Objective, concise description of the scientific work that won the prize. Focus on what was discovered/invented, not superlatives."
    )

    # Biographical Information
    personal_background: PersonalBackground = Field(..., description="Early life, education, and family background of the laureate")
    career_timeline: list[CareerPosition] = Field(..., description="Chronological list of major career positions and institutional affiliations", min_length=1)
    broader_recognition: BroaderRecognition = Field(..., description="Honors, recognition, and broader roles in the scientific community outside of the Nobel Prize")

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
        description="List of major improvements to experimental methods, theoretical models, or practical techniques developed after the original work. Be specific about what was improved and how.",
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
