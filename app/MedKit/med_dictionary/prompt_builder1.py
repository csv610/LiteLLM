"""
Prompt Builder for Medical Dictionary.
"""

class PromptBuilder:
    """Class to manage and build prompts for the medical dictionary."""

    def __init__(self):
        self.system_prompt = (
            "You are a medical dictionary expert. Provide a dictionary definition ONLY if the term "
            "is medically recognized - no conversational text, no follow-up questions, no extra "
            "commentary. Be concise and professional. Format the response as a clear medical "
            "dictionary entry. Use simple, everyday language and avoid complex medical jargon "
            "where possible."
        )
        self.user_prompt_template = (
            "Define '{term}' only if it is a medically recognized full term (not an abbreviation, "
            "acronym, or slang). If it is not a valid medical term, output exactly: "
            "'Not a medically recognized term.' "
            "Write the definition in a simple, easy-to-understand medical dictionary style: concise, neutral, factual. "
            "Avoid specialized medical terms and jargon unless absolutely necessary for accuracy. "
            "Start the definition immediately with a description of the condition. "
            "Do NOT include the term name or phrases like '{term} is', 'This term refers to', or 'A condition where' at the beginning. "
            "Example: Instead of 'Eczema is a skin condition...', write 'A skin condition...'. "
            "Do NOT include pronunciation, etymology, examples, or usage notes. "
            "Output only the definition text and nothing else."
        )

    def build_system_prompt(self) -> str:
        """Returns the system prompt."""
        return self.system_prompt

    def build_user_prompt(self, term: str) -> str:
        """Returns the formatted user prompt for a specific term."""
        return self.user_prompt_template.format(term=term)
