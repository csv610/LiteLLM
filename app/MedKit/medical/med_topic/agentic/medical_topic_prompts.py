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
        """Creates the user prompt for medical topic generation."""
        return f"Generate a detailed, textbook-style medical reference entry for the topic: {topic}."

    @staticmethod
    def get_topic_auditor_prompts(topic: str, topic_content: str) -> tuple[str, str]:
        """Create prompts for the Topic Compliance Auditor (JSON output)."""
        system = (
            "You are a Senior Medical Editor and Compliance Auditor. Your role is to "
            "audit medical textbook-style content for accuracy, formal tone, and "
            "completeness. Output a structured JSON report identifying any "
            "factual errors, tone violations, or missing mandatory sections."
        )
        user = (
            f"Audit the following medical reference entry for the topic '{topic}' and "
            f"output a structured JSON report:\n\n{topic_content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(topic: str, topic_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Textbook Editor. Your role is to take raw "
            "specialist data and a structured quality audit, then synthesize them into "
            "a FINAL, polished, and authoritative Markdown reference entry. "
            "You MUST apply all fixes identified in the audit and ensure a "
            "perfectly formal, professional tone throughout."
        )
        user = (
            f"Synthesize the final medical reference entry for '{topic}'.\n\n"
            f"TOPIC DATA:\n{topic_data}\n\n"
            f"QUALITY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown entry. Ensure it is accurate, comprehensive, "
            "and follows the required textbook structure."
        )
        return system, user
