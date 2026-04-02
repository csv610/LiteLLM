"""
scholar_work_models.py - Pydantic models for scholar major works

Defines data models for generating and storing a complete list of major scientific
work and contributions done by a given scientist.
"""

from pydantic import BaseModel, Field, model_validator
from typing import List


class ScholarMajorWork(BaseModel):
    """A collection of major work and contributions by a scholar"""
    scholar_name: str = Field(..., description="Name of the scholar being described")
    title: str = Field(..., description="An engaging title for the collection of work")
    subtitle: str = Field(..., description="A compelling subtitle or subheading")

    # The major works and contributions
    major_contributions: List[str] = Field(..., description="A complete and detailed list of major work and contributions, each as a substantial paragraph")

    # Supporting materials
    key_terms: str = Field(..., description="Brief explanations of technical terms or concepts related to the contributions")
    impact_summary: str = Field(..., description="A summary of the long-term impact of these contributions on science or society")
    discussion_questions: List[str] = Field(..., description="Thought-provoking questions for readers to reflect on (3-5 questions)")

    @model_validator(mode="before")
    @classmethod
    def _coerce_legacy_fields(cls, data):
        if isinstance(data, dict):
            data = dict(data)
            if "major_contributions" not in data and data.get("major_contribution"):
                data["major_contributions"] = [data.get("story") or data["major_contribution"]]
        return data

    @property
    def story(self) -> str:
        return "\n\n".join(self.major_contributions)

    @property
    def major_contribution(self) -> str:
        return self.major_contributions[0] if self.major_contributions else ""


from typing import Any

class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
