from pydantic import BaseModel, Field
from typing import Optional, List

class StatementAnalysis(BaseModel):
    """Detailed analysis of a single statement."""
    statement: str = Field(description="The original statement being analyzed")
    classification: str = Field(description="Fact or Fiction")
    confidence_level: str = Field(description="Confidence level (high, medium, low)")
    confidence_percentage: int = Field(description="Confidence as percentage (0-100)")


class FactualSupport(BaseModel):
    """Support for factual statements."""
    supporting_sources: str = Field(description="Known sources that support this fact, comma-separated")
    evidence_type: str = Field(description="Type of evidence (scientific, historical, observational, etc)")
    verification_method: str = Field(description="How this fact can be verified")
    related_facts: str = Field(description="Related facts that corroborate this statement, comma-separated")


class FictionIndicators(BaseModel):
    """Indicators suggesting a statement is fiction."""
    red_flags: str = Field(description="Red flags or indicators of fiction, comma-separated")
    factual_errors: str = Field(description="Specific factual errors or contradictions found")
    lack_of_evidence: str = Field(description="Absence of supporting evidence or contradictions with known facts")
    fictional_elements: str = Field(description="Elements that appear to be fictional or speculative, comma-separated")


class ContextInformation(BaseModel):
    """Context and background information."""
    subject_area: str = Field(description="Subject area or domain of the statement (science, history, general knowledge, etc)")
    key_terms: str = Field(description="Key terms or concepts in the statement, comma-separated")
    assumptions: str = Field(description="Assumptions made in the statement, comma-separated")
    scope_clarity: str = Field(description="Whether the scope of the statement is clear (too vague, precise, etc)")


class DetailedAnalysis(BaseModel):
    """Comprehensive fact/fiction analysis of a statement."""
    statement_analysis: StatementAnalysis
    factual_support: Optional[FactualSupport] = Field(description="Support information if statement is a fact")
    fiction_indicators: Optional[FictionIndicators] = Field(description="Fiction indicators if statement is fiction")
    context: ContextInformation
    explanation: str = Field(description="Plain language explanation of why statement is fact or fiction")
    potential_confusion: str = Field(description="Common misconceptions or reasons why people might believe differently")


class AnalyzerMetadata(BaseModel):
    """Metadata about the analysis."""
    analysis_date: str = Field(description="Date of analysis")
    knowledge_cutoff: str = Field(description="Knowledge cutoff date of the analyzer")
    analysis_method: str = Field(description="Method used for analysis")
    limitations: str = Field(description="Limitations of this analysis")


class FactFictionAnalysis(BaseModel):
    """
    Comprehensive fact/fiction analysis for statements.
    """
    detailed_analysis: DetailedAnalysis
    metadata: AnalyzerMetadata
