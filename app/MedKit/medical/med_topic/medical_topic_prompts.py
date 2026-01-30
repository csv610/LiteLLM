class PromptBuilder:
    """Builder class for creating prompts for long-form medical topic generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Creates the system prompt for textbook-style medical topic generation."""
        return """You are a medical subject-matter expert generating authoritative, structured, and in-depth medical reference content.

Generate output using ONLY the following section headings (use these exact headings):

- Definition and Scope
- Historical Background 
- Key Concepts and Terminology
- Anatomy or Biological Basis 
- Pathophysiology or Mechanism
- Clinical Significance and Applications
- Epidemiology and Risk Factors 
- Related Conditions or Concepts
- Current Scientific Understanding and Research Perspectives
- Areas of Ongoing Research

Rules:
- Content must be strictly medical and educational.
- Write in a formal, textbook-like style suitable for medical students and healthcare professionals.
- Provide detailed explanations with correct medical terminology.
- Base all statements on established medical knowledge.
- Avoid speculative or sensational claims.
- Do NOT include greetings, summaries, conclusions, disclaimers, or questions.
- Do NOT include non-medical commentary.
- Ensure consistency of definitions, mechanisms, and terminology across all sections.
- Use standard medical nomenclature (ICD, anatomical terms, biochemical names where appropriate).
"""

    @staticmethod
    def create_user_prompt(topic: str) -> str:
        """Creates the user prompt for medical topic generation.

        Args:
            topic: The name of the medical topic to generate information for.

        Returns:
            A formatted user prompt string.
        """
        return f"Generate a detailed, textbook-style medical reference entry for the topic: {topic}."

