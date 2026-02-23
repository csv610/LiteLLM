class MedicalDictionaryPromptBuilder:
    """Class to manage and build prompts for the medical dictionary definitions."""

    def __init__(self):
        self.system_prompt = (
            "You are a medical dictionary specialist. "
            "Provide a definition ONLY if the term is a formally recognized medical term "
            "found in established medical literature (e.g., standard medical textbooks, "
            "peer-reviewed journals, or recognized medical references). "
            "If the term is not recognized with high confidence, output exactly: "
            "'Not a medically recognized term.' "
            "Do not guess. Do not infer meaning from similarity. "
            "Do not fabricate definitions. "
            "Write concise, neutral, factual definitions in clear, everyday language. "
            "Avoid unnecessary medical jargon, but use essential technical terms if required "
            "for accuracy. "
            "Do not include conversational text, commentary, explanations about uncertainty, "
            "or formatting beyond the definition itself."
        )

        self.user_prompt_template = (
            "Define '{term}' only if it is a formally recognized medical term. "
            "Exclude abbreviations, acronyms, slang, brand names, incomplete fragments, "
            "and non-medical terms. "
            "If it is not a valid medical term, output exactly: "
            "'Not a medically recognized term.' "
            "Write a concise medical dictionary-style definition (maximum 2–3 sentences). "
            "Begin immediately with a direct description of the medical concept. "
            "Do NOT begin with the term name or phrases like '{term} is', "
            "'This term refers to', or similar constructions. "
            "Do NOT include pronunciation, etymology, examples, usage notes, or extra commentary. "
            "Output only the definition text and nothing else."
        )

    def create_system_prompt(self) -> str:
        """Returns the system prompt."""
        return self.system_prompt

    def create_user_prompt(self, term: str) -> str:
        """Returns the formatted user prompt for a specific term."""
        return self.user_prompt_template.format(term=term)
