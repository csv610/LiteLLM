class PromptBuilder:
    """Class to manage and build LLM prompts for medical article review."""

    @staticmethod
    def get_review_prompt(article_text: str) -> str:
        """
        Build a prompt for evaluating a single medical article.

        Args:
            article_text: Text of the article to be reviewed.

        Returns:
            The formatted prompt string.
        """
        return f"""Conduct a thorough review of the following medical article. 
Identify its key findings, evaluate its methodology, and discuss its clinical relevance.

Article:
{article_text}

---

Provide a comprehensive review, including:
1.  Title and summary.
2.  Key strengths (e.g., sample size, study design).
3.  Weaknesses or limitations (e.g., bias, narrow scope).
4.  Clinical implications for healthcare practitioners.
5.  An overall quality assessment."""
