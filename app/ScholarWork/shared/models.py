from typing import Any

"""
scholar_work_models.py - Pydantic models for scholar major works

Defines data models for generating and storing narrative-driven explanations
of major scientific work done by a given scientist.
"""

from lite import ModelOutput


class ResearchBrief(BaseModel):
    """A detailed research brief about a scholar's major works and contributions."""

    scholar_name: str = Field(..., description="The name of the scholar")
    major_contributions: List[str] = Field(
        ...,
        description="A comprehensive list of the specific major works or breakthroughs",
    )
    historical_context: str = Field(
        ...,
        description="The scientific and social landscape during the time of discovery",
    )
    scientific_core: str = Field(
        ...,
        description="The fundamental scientific principles and logic behind the major discoveries",
    )
    revolutionary_impact: str = Field(
        ..., description="How these works changed existing paradigms or understanding"
    )
    modern_legacy: List[str] = Field(
        ...,
        description="3-5 concrete ways this work influences science or society today",
    )
    key_anecdotes: List[str] = Field(
        ...,
        description="Potential human-interest stories or anecdotes related to the discoveries",
    )

    @model_validator(mode="before")
    @classmethod
    def _coerce_legacy_fields(cls, data):
        if (
            isinstance(data, dict)
            and "major_contributions" not in data
            and data.get("major_contribution")
        ):
            data = dict(data)
            data["major_contributions"] = [data["major_contribution"]]
        return data

    @property
    def major_contribution(self) -> str:
        return self.major_contributions[0] if self.major_contributions else ""


class SynthesizedReport(BaseModel):
    """A synthesized technical report of a scholar's major work."""

    scholar_name: str = Field(..., description="The name of the scholar")
    contributions: List[str] = Field(
        ..., description="A list of detailed technical descriptions of major works"
    )


class ScholarMajorWork(BaseModel):
    """A comprehensive list and explanation of major works by a scholar"""

    scholar_name: str = Field(..., description="Name of the scholar being described")
    title: str = Field(..., description="A clear title for the report")
    subtitle: str = Field(..., description="A descriptive subtitle or summary line")

    # The complete list of works and contributions
    contribution_list: str = Field(
        ...,
        description="A comprehensive, structured list of major works and contributions with detailed explanations for each.",
    )

    # Supporting materials
    key_terms: str = Field(
        ...,
        description="Brief explanations of technical terms or concepts used in the report",
    )
    impact_summary: str = Field(
        ...,
        description="A summary of the long-term impact of these works on science or society",
    )
    discussion_questions: List[str] = Field(
        ...,
        description="Thought-provoking questions for readers to reflect on (3-5 questions)",
    )

    @model_validator(mode="before")
    @classmethod
    def _coerce_legacy_fields(cls, data):
        if isinstance(data, dict):
            data = dict(data)
            if "contribution_list" not in data and data.get("story"):
                data["contribution_list"] = data["story"]
        return data

    @property
    def story(self) -> str:
        return self.contribution_list

    @property
    def major_contribution(self) -> str:
        if not self.contribution_list:
            return self.title
        first_line = self.contribution_list.splitlines()[0].strip()
        return first_line or self.title
