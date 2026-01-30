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
        """Create the user prompt for herbal information generation.

        Args:
            herb: The name of the herb to generate information for.
        """
        return f"""
Generate a structured herbal monograph for: {herb}

Include the following sections:

1. Botanical Name and Family  
2. Common Names  
3. Parts Used  
4. Active Compounds (major phytochemicals)  
5. Traditional Uses (Ayurveda, TCM, Western herbalism if applicable)  
6. Pharmacological Actions (mechanisms where known)  
7. Modern Scientific Evidence (human, animal, or in vitro)  
8. Common Preparations and Dosage Forms (not prescriptions)  
9. Safety Profile  
10. Contraindications  
11. Drug Interactions  
12. Pregnancy and Lactation Safety  
13. Toxicity and Overdose Risk  

Formatting rules:
- Use clear section headings.
- Use complete, medically precise sentences.
- Do not invent clinical evidence.
- If data is unknown or insufficient, write: "Insufficient reliable data available."
"""

