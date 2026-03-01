class PromptBuilder:
    """Class to manage and build LLM prompts for medical article summarization."""

    @staticmethod
    def get_chunk_summary_prompt(text: str) -> str:
        """
        Build a prompt for summarizing a chunk of text.

        Args:
            text: The text chunk to summarize.

        Returns:
            The formatted prompt string.
        """
        return f"""Summarize the following medical text chunk concisely, focusing on key medical facts and findings.

Text Chunk:
{text}"""

    @staticmethod
    def get_final_summary_prompt(chunk_summaries: list[str]) -> str:
        """
        Build a prompt for the final combined summary.

        Args:
            chunk_summaries: List of individual chunk summaries.

        Returns:
            The formatted prompt string.
        """
        summaries_text = "\n\n".join([f"Chunk {i+1}: {s}" for i, s in enumerate(chunk_summaries)])
        return f"""Synthesize the following summaries from different parts of a medical article into a single, cohesive, and comprehensive summary. 
The final summary should flow logically and cover all important aspects mentioned in the chunks.

Chunk Summaries:
{summaries_text}"""
