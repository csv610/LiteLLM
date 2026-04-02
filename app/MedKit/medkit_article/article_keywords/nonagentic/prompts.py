class PromptBuilder:
    """Class to manage and build LLM prompts for medical keyword extraction."""

    @staticmethod
    def get_keyword_extraction_prompt(text: str) -> str:
        """
        Build a prompt for medical keyword extraction.

        Args:
            text: The text to extract keywords from.

        Returns:
            The formatted prompt string.
        """
        return f"""Extract all medical keywords and important terms from this text.
Return ONLY medical terminology including:
- Diseases, medical conditions, and syndromes
- Symptoms and clinical findings
- Medications, drugs, and herbal supplements
- Surgical procedures and treatments
- Medical tests, diagnostic tests, and imaging findings
- Anatomical terms

Focus on specific medical terms, not generic descriptions. Be precise and clinical.

Text:
{text}"""
