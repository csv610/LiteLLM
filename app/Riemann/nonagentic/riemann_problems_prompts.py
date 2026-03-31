"""
riemann_problems_prompts.py - PromptBuilder class for Riemann Theory Guide
"""

class PromptBuilder:
    """Builder class for creating Riemann theory prompts."""

    @staticmethod
    def get_system_prompt() -> str:
        """Get the system prompt for Riemann theory generation."""
        return """You are an expert mathematical historian and mathematician specializing in Bernhard Riemann's work.
Your task is to provide accurate, rigorous, and well-structured information about Riemann's theories.

Fundamental Principles:
1. Historical Precision: Accurately contextualize work. BE EXTREMELY CAREFUL with publication titles and dates (e.g., do not confuse Riemann's papers with Gauss's books).
2. Mathematical Rigor: Use precise terminology in technical sections.
3. Depth and Clarity: Maintain technical depth while ensuring conceptual clarity.
4. Fact-Checking: Verify all cross-references between mathematicians and their respective works before outputting."""

    @staticmethod
    def get_user_prompt(theory_name: str) -> str:
        """Get the user prompt for a specific Riemann theory or concept."""
        return f"""Provide a comprehensive and rigorous analysis of the theory or concept: "{theory_name}".

Your analysis must include these specific sections:
1. **Layperson Explanation**: Explain the core idea to someone with NO mathematical background. Avoid words like "function," "zeroes," or "tensor" if possible. Use grounded analogies (e.g., music, architecture, maps, or nature) to describe the "vibe" and goal of the theory.
2. **The Bigger Picture & Intuition**: Explain the theory's core concept in an intuitive way for a student, showing how it fits into the broader landscape of mathematics.
3. **Riemann's Motivation**: Clearly identify the specific mathematical or physical problems Riemann was trying to solve (the "Why").
4. **Common Misconceptions**: List and DEBUNK at least two common myths, misunderstandings, or errors in how this theory is often taught or understood (e.g., "A common misconception is... in reality...").
5. **Rigorous Definition**: A precise mathematical or conceptual formulation.
6. **Limitations**: Critically assess the boundaries of the theory and what it does NOT address.
7. **Modern Developments**: Detail how the theory has been refined or generalized since Riemann's time.
8. **Counterfactual Analysis**: Speculate on how modern science would be different today if this idea had never been developed.
9. **Historical & Key Elements**: Accurate origins, specific publication titles, and significant properties.

Ensure the response is factual, dense in technical sections, and captures the intellectual spirit of Riemann's original inquiries."""

    @staticmethod
    def get_summary_prompt(available_theories: list[str]) -> str:
        """Get the user prompt for generating a summary of available Riemann theories."""
        theories_str = "\n".join([f"- {t}" for t in available_theories[:20]])
        if len(available_theories) > 20:
            theories_str += f"\n... and {len(available_theories) - 20} more."

        return f"""Provide a concise expert summary of these Riemann-related concepts:

{theories_str}

Categorize these by field (e.g., Analysis, Differential Geometry, Number Theory) and highlight the overarching legacy of Riemann's contributions to modern mathematics."""
