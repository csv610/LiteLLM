from pydantic import BaseModel, Field

class KeywordList(BaseModel):
    """Structured keyword output from LLM."""

    keywords: list[str] = Field(description="List of medical keywords and important terms")


class KeywordResult(BaseModel):
    """Result for a single item extraction."""

    id: str = Field(description="Identifier for the item")
    keywords: list[str] = Field(description="Extracted keywords")
