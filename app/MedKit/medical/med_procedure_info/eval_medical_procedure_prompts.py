
class PromptBuilder:
    """Builder class for creating prompts for medical procedure evaluation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure evaluation."""
        return (
            "You are a Senior Medical Editor and Review Board member. "
            "Your task is to critically review medical procedure documentation for accuracy, "
            "safety, completeness, and adherence to highest medical standards. "
            "You MUST return ONLY a raw JSON object. "
            "NO Markdown code blocks. NO preamble. NO postamble. "
            "The output must start with '{' and end with '}'. "
            "Prioritize patient safety and flag any inaccuracies or missing critical information. "
            "Your evaluation should be constructive but rigorous."
        )

    @staticmethod
    def create_user_prompt(procedure_name: str, content: str) -> str:
        """Create the user prompt for evaluating procedure information."""
        return f"""
Critically review the following medical procedure information for "{procedure_name}".

Content to Review:
-------------------
{content}
-------------------

Conduct a comprehensive evaluation covering:

1. Medical Accuracy: Are the anatomical and procedural details correct?
2. Safety & Risks: Are contraindications, risks, and warning signs clearly stated?
3. Completeness: Is any critical phase (prep, procedure, recovery) missing?
4. Evidence-Base: Does it align with standard modern medical practices?
5. Clarity: Is it understandable while maintaining professional precision?

Provide a structured evaluation with scores and specific recommendations for improvement.
"""
