"""
article_reviewer_prompts.py - Prompt builder for article reviewer

Provides comprehensive prompt building functionality for article review system
with detailed instructions and proofreading rules.
"""

import json
from typing import Dict


class PromptBuilder:
    """Builder for creating comprehensive article review prompts"""
    
    # Comprehensive proofreading rules
    PROOFREADING_RULES = {
        "Grammar & Syntax": {
            "subject_verb_agreement": "Verify subject and verb agreement in all sentences",
            "tense_consistency": "Maintain consistent verb tense throughout the article",
            "pronoun_reference": "Ensure pronouns clearly refer to their antecedents",
            "article_usage": "Correct usage of articles (a, an, the)",
            "preposition_usage": "Verify proper preposition usage"
        },
        "Style & Clarity": {
            "active_voice": "Prefer active voice over passive voice where appropriate",
            "sentence_clarity": "Ensure sentences are clear and concise",
            "redundancy": "Eliminate redundant words and phrases",
            "jargon": "Explain technical terms or avoid unnecessary jargon",
            "word_choice": "Verify precise and appropriate word choices",
            "sentence_length": "Maintain appropriate sentence length to avoid confusion"
        },
        "Formatting & Punctuation": {
            "punctuation": "Correct punctuation usage (commas, periods, semicolons, etc.)",
            "capitalization": "Verify correct capitalization of proper nouns and sentence starts",
            "quotation_marks": "Ensure proper quotation mark usage and consistency",
            "apostrophe_usage": "Correct apostrophe usage in contractions and possessives",
            "numbering": "Consistent formatting of numbers (spelled out vs. digits)",
            "hyphenation": "Correct hyphenation of compound words"
        },
        "Content & Structure": {
            "fact_accuracy": "Verify factual accuracy of claims and statements",
            "sources": "Include proper citations and sources where needed",
            "completeness": "Ensure article covers all necessary aspects of the topic",
            "logical_flow": "Verify logical progression and coherence of ideas",
            "relevance": "Ensure all content is relevant to the article's purpose",
            "introduction": "Article has clear introduction with thesis or purpose statement",
            "conclusion": "Article has meaningful conclusion summarizing key points"
        },
        "Consistency": {
            "terminology": "Use consistent terminology throughout the article",
            "formatting_style": "Maintain consistent formatting style across all sections",
            "tone": "Maintain consistent tone appropriate for the audience",
            "section_structure": "Maintain consistent structure across similar sections"
        }
    }

    @classmethod
    def create_review_prompt(cls, article_text: str) -> str:
        """Create a comprehensive article review prompt
        
        Args:
            article_text: The full text of the article to review
            
        Returns:
            str: Complete prompt for article review
        """
        return f"""You are an expert article reviewer and proofreader. Review the following article comprehensively.

ARTICLE TO REVIEW:
<article>
{article_text}
</article>

PROOFREADING RULES TO APPLY:
{json.dumps(cls.PROOFREADING_RULES, indent=2)}

INSTRUCTIONS:
1. Review the article against all proofreading rule categories above
2. Identify specific issues and categorize them as deletions, modifications, or insertions
3. For each issue, provide:
   - The exact line number
   - The complete, full text (for deletions and modifications)
   - Clear, specific, and actionable reason
   - Severity level (low, medium, high, critical)
4. ALL suggestions must be COMPLETE and UNAMBIGUOUS:
   - Never provide partial or fragmented text
   - Include full sentences or phrases, not excerpts
   - Make suggestions ready to implement without additional interpretation
   - Be specific about what to do, not vague

DELETION SUGGESTIONS:
- Remove redundant phrases, unnecessary words, or irrelevant content
- Flag repeated information
- Remove unsupported claims or outdated references
- REQUIREMENT: Provide the COMPLETE phrase or sentence to be deleted
NOTE: Do NOT include empty lines or whitespace issues as deletions - these are cosmetic and not substantive.

MODIFICATION SUGGESTIONS:
- Improve clarity and readability
- Fix grammar, punctuation, and style issues
- Enhance word choice for precision
- Convert passive to active voice where appropriate
- Break up overly long sentences
- REQUIREMENT: Provide the COMPLETE original text and COMPLETE suggested replacement (full sentences or phrases, not fragments)

INSERTION SUGGESTIONS:
- Add missing context or explanations
- Include citations where needed
- Add examples for clarity
- Include introduction/conclusion if missing
- Add transitions between ideas
- REQUIREMENT: Provide COMPLETE, ready-to-use content for insertion (full sentences or paragraphs)

SCORING GUIDELINES:
- 90-100: Excellent - minimal issues, professional quality
- 80-89: Good - well-written with minor improvements
- 70-79: Fair - several issues that should be addressed
- 60-69: Poor - significant issues requiring revision
- Below 60: Very Poor - substantial revision needed

Provide a fair assessment based on the total number and severity of issues found. Focus on substantive content issues, not cosmetic formatting."""

    @classmethod
    def get_proofreading_rules(cls) -> Dict[str, Dict[str, str]]:
        """Get the complete proofreading rules dictionary
        
        Returns:
            Dict: Complete proofreading rules organized by category
        """
        return cls.PROOFREADING_RULES.copy()

    @classmethod
    def get_rules_by_category(cls, category: str) -> Dict[str, str]:
        """Get proofreading rules for a specific category
        
        Args:
            category: The category name (e.g., "Grammar & Syntax")
            
        Returns:
            Dict: Rules for the specified category
        """
        return cls.PROOFREADING_RULES.get(category, {})

    @classmethod
    def get_all_categories(cls) -> list[str]:
        """Get all proofreading rule categories
        
        Returns:
            list: List of all category names
        """
        return list(cls.PROOFREADING_RULES.keys())
