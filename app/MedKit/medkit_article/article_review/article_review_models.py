from pydantic import BaseModel, Field


class ArticleReview(BaseModel):
    """Comprehensive evaluation of a single medical article."""

    title: str = Field(description="Title of the article")
    summary: str = Field(
        description="A concise summary of the article's main findings and methodology"
    )
    strengths: list[str] = Field(description="List of key strengths of the article")
    weaknesses: list[str] = Field(
        description="List of key weaknesses, limitations, or gaps in the article"
    )
    clinical_implications: str = Field(
        description="Key clinical implications or practical takeaways for healthcare providers"
    )
    overall_quality: str = Field(
        description="Overall quality assessment of the article (e.g., High, Moderate, Low with justification)"
    )
