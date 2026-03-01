from pydantic import BaseModel, Field


class ArticleEvaluation(BaseModel):
    """Evaluation of a single article's strengths and weaknesses."""

    strengths: list[str] = Field(description="List of key strengths of the article")
    weaknesses: list[str] = Field(
        description="List of key weaknesses or gaps in the article"
    )
    overall_quality: str = Field(
        description="Overall quality assessment of the article"
    )


class ComparisonResult(BaseModel):
    """Side-by-side comparison of two articles."""

    article1_evaluation: ArticleEvaluation = Field(
        description="Evaluation of the first article"
    )
    article2_evaluation: ArticleEvaluation = Field(
        description="Evaluation of the second article"
    )
    winner: str = Field(
        description="Which article is better and why, or how they complement each other"
    )
    comparison_summary: str = Field(
        description="A summary highlighting the key differences and similarities"
    )
