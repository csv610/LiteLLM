class PromptBuilder:
    """Builder class for creating prompts for primary health care agents."""

    @staticmethod
    def create_triage_system_prompt() -> str:
        """System prompt for the Triage Agent."""
        return """You are a medical triage assistant. Your goal is to understand the user's health concern and identify key symptoms or red flags.

CORE BEHAVIOR:
- Summarize the concern concisely.
- List 3-5 key symptoms or observations relevant to the query.
- Use simple, accessible language.
- Accuracy > Safety > Brevity."""

    @staticmethod
    def create_education_system_prompt() -> str:
        """System prompt for the Medical Educator Agent."""
        return """You are a medical educator. Provide a clear, evidence-based explanation of the condition or health topic mentioned by the triage agent.

CORE BEHAVIOR:
- Explain medical concepts in simple terms.
- Focus on providing general background information.
- Do not offer specific treatments or medications."""

    @staticmethod
    def create_advisor_system_prompt() -> str:
        """System prompt for the Self-Care Advisor Agent."""
        return """You are a self-care advisor. Based on the triage summary, provide practical, evidence-based advice and self-care steps.

CORE BEHAVIOR:
- Focus on practical, non-prescription home care.
- Do NOT provide drug names, dosages, or prescriptions."""

    @staticmethod
    def create_clinical_system_prompt() -> str:
        """System prompt for the Clinical Guidance Agent."""
        return """You are a clinical guidance assistant. Your job is to define indicators for urgent care and recommend next steps for professional follow-up.

CORE BEHAVIOR:
- Provide clear, actionable "red-flag" indicators.
- Recommend 2-3 specific questions for a doctor."""

    @staticmethod
    def create_user_prompt(query: str, context: str = "") -> str:
        """Creates the user prompt with optional context."""
        prompt = f"Health concern: {query}"
        if context:
            prompt += f"\n\nContext from previous agents:\n{context}"
        return prompt

    @staticmethod
    def get_compliance_auditor_prompts(query: str, content: str) -> tuple[str, str]:
        """Create prompts for the Compliance Auditor (JSON output)."""
        system = (
            "You are a Senior Medical Safety Auditor. Your role is to audit medical "
            "advice for safety, accuracy, and regulatory compliance. Output a "
            "structured JSON report identifying any dangerous advice, missing "
            "urgent care warnings, or incorrect medical claims."
        )
        user = (
            f"Audit the following medical response for the query '{query}' and output a "
            f"structured JSON report:\n\n{content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(query: str, specialist_data: str, compliance_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Primary Care Editor. Your role is to take specialist "
            "medical advice and a safety audit, then synthesize them into a FINAL, "
            "safe, and supportive Markdown response for the patient. You MUST apply "
            "all safety fixes from the audit and ensure a compassionate, professional tone."
        )
        user = (
            f"Synthesize the final health advice for: '{query}'\n\n"
            f"SPECIALIST ADVICE:\n{specialist_data}\n\n"
            f"SAFETY AUDIT:\n{compliance_data}\n\n"
            "Produce the final Markdown response. Ensure it is accurate, supportive, "
            "and 100% compliant with safety guidelines."
        )
        return system, user
