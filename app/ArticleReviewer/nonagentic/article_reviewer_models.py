"""
article_reviewer_models.py - Pydantic models for article review data structures

Defines comprehensive data models for article review system with detailed feedback
on deletions, modifications, and insertions.
"""

from pydantic import BaseModel, Field
from typing import List


class DeleteModel(BaseModel):
    """Model for content that should be removed from the article"""
    line_number: int = Field(..., description="The line number where the content to be deleted is located")
    content: str = Field(..., description="The specific phrase or sentence that should be deleted")
    reason: str = Field(..., description="Clear explanation of why this content should be removed")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', or 'critical'")


class ModifyModel(BaseModel):
    """Model for content that should be modified or improved"""
    line_number: int = Field(..., description="The line number of the content to be modified")
    original_content: str = Field(..., description="The original phrase or sentence")
    suggested_modification: str = Field(..., description="The improved version of the content")
    reason: str = Field(..., description="Explanation of why this modification improves the article")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', or 'critical'")


class InsertModel(BaseModel):
    """Model for content that should be added to the article"""
    line_number: int = Field(..., description="The line number after which content should be inserted")
    suggested_content: str = Field(..., description="The content that should be added")
    reason: str = Field(..., description="Explanation of why this content is necessary for completeness or accuracy")
    section: str = Field(..., description="The article section where this should be added (e.g., 'Introduction', 'Conclusion', 'Examples')")
    severity: str = Field(..., description="Severity level: 'low', 'medium', 'high', or 'critical'")


class ArticleReviewModel(BaseModel):
    """Complete article review response"""
    score: int = Field(..., description="Overall quality score from 0-100")
    total_issues: int = Field(..., description="Total number of issues found (deletions + modifications + insertions)")
    summary: str = Field(..., description="Brief overall assessment of the article quality")
    deletions: List[DeleteModel] = Field(default=[], description="List of content to remove")
    modifications: List[ModifyModel] = Field(default=[], description="List of content to modify")
    insertions: List[InsertModel] = Field(default=[], description="List of content to insert")
    proofreading_rules_applied: List[str] = Field(default=[], description="List of proofreading rule categories that were applied during the review")
