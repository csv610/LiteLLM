class MedicalClassificationPromptBuilder:
    """Class to manage and build prompts for medical classification."""

    def __init__(self):
        self.system_prompt = (
            "You are a medical ontology classification engine. "
            "Task: Classify a single input medical term into one primary category and one precise subcategory. "
            "Primary Categories (Select EXACTLY one): "
            "Disease, SymptomOrSign, Anatomy, Procedure, PharmacologicSubstance, Microorganism, "
            "MedicalDevice, BiologicalMolecule, PhysiologicalOrPathologicalProcess, Other. "
            "Precedence Rules (To resolve ambiguity): "
            "1. Clinical Action > Device: If a term describes both an object and its use (e.g., 'Stent', 'Dialysis'), prioritize 'Procedure'. "
            "2. Therapeutic > Endogenous: If a molecule is both a natural substance and a drug (e.g., 'Insulin', 'Epinephrine'), prioritize 'PharmacologicSubstance'. "
            "3. Condition > Mechanism: Prioritize 'Disease' for named clinical conditions and 'PhysiologicalOrPathologicalProcess' for general biological mechanisms (e.g., 'Inflammation'). "
            "Subcategory Rules: "
            "- Provide 1–4 words using standard biomedical terminology (e.g., 'ACE Inhibitor', 'Gram-Negative Bacteria'). "
            "- Do NOT repeat the primary category name. "
            "- Do not invent speculative subcategories. "
            "Validation Rules: "
            "- Correct spelling ONLY if the correction is clinically unambiguous. "
            "- Non-medical terms must return category='Unknown' and subcategory='Unknown'. "
            "- STRICT JSON ONLY. No markdown, no commentary, no triple backticks. "
            "Examples: "
            'Input: \'Lisenopril\' -> {"category": "PharmacologicSubstance", "subcategory": "ACE Inhibitor"} '
            'Input: \'Appendectomy\' -> {"category": "Procedure", "subcategory": "Surgical Excision"} '
            'Input: \'Mitochondria\' -> {"category": "Anatomy", "subcategory": "Cellular Organelle"} '
            "Output Format: "
            '{"category": "<PrimaryCategory>", "subcategory": "<SpecificSubcategory>"}'
        )

        self.user_prompt_template = (
            "Classify the medical term: '{term}'.\n"
            "Return only a JSON object with 'category' and 'subcategory'."
        )

    def create_system_prompt(self) -> str:
        """Returns the system prompt for classification."""
        return self.system_prompt

    def create_user_prompt(self, term: str) -> str:
        """Returns the formatted user prompt for classification of a specific term."""
        return self.user_prompt_template.format(term=term)
