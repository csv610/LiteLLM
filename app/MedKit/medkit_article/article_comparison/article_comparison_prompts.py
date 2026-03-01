class PromptBuilder:
    """Class to manage and build LLM prompts for medical article evaluation."""

    @staticmethod
    def get_comparison_prompt(article1_text: str, article2_text: str) -> str:
        """
        Build a prompt for comparing two medical articles.

        Args:
            article1_text: Text of the first article.
            article2_text: Text of the second article.

        Returns:
            The formatted prompt string.
        """
        return f"""Compare the following two medical articles side-by-side. 
Evaluate each article's strengths and weaknesses, identifying key medical findings, research methodologies, and clinical implications.

Article 1:
{article1_text}

---

Article 2:
{article2_text}

---

Provide a detailed evaluation for each article, highlighting their unique contributions and gaps.
Conclude with a summary of how they compare, which one provides better evidence (if applicable), and how they complement each other."""
