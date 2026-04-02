class PromptBuilder:
    """Builder class for creating prompts for herbal information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for herbal information generation."""
        return """You are a professional herbal pharmacology expert with knowledge of medicinal plants, phytochemistry, and clinical research.

Your task is to generate accurate, neutral, and structured information about herbs based on established traditional use and available scientific evidence.

Rules:
- Write in a formal, medical-style tone.
- Do NOT use promotional, exaggerated, or spiritual language.
- Clearly distinguish traditional use from scientifically studied effects.
- If reliable evidence is lacking, explicitly state that.
- Do NOT include any preamble, disclaimer, or self-referential statements.
- Do NOT give personal advice.
- Output must be factual, cautious, and suitable for educational or clinical reference.
"""

    @staticmethod
    def create_user_prompt(herb: str) -> str:
        """Create the user prompt for herbal information generation."""
        return f"Generate a structured herbal monograph for: {herb}"

    @staticmethod
    def create_compliance_auditor_prompts(herb: str, content: str) -> tuple[str, str]:
        """Create prompts for the JSON Compliance Auditor."""
        system = (
            "You are a Senior Herbal Safety & Compliance Auditor. Your role is to "
            "audit herbal monographs for accuracy, dangerous claims, and missing "
            "drug interaction warnings. Output a structured JSON report identifying "
            "any unsubstantiated cures or critical safety omissions."
        )
        user = (
            f"Audit the following herbal information for '{herb}' and output a "
            f"structured JSON report:\n\n{content}"
        )
        return system, user

    @staticmethod
    def create_output_synthesis_prompts(herb: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Herbal Monograph Editor. Your role is to take raw "
            "botanical and pharmacological data and a structured safety audit, "
            "then synthesize them into a FINAL, polished, and safe Markdown monograph. "
            "You MUST apply all safety fixes identified in the audit and ensure "
            "all drug interactions are clearly highlighted."
        )
        user = (
            f"Synthesize the final herbal monograph for: '{herb}'\n\n"
            f"HERBAL DATA:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown monograph. Ensure it is accurate, professional, "
            "and 100% compliant with evidence-based safety standards."
        )
        return system, user
