# =========================
# Prompt Constants
# =========================

PROMPT_TEMPLATE = """
Extract procedure-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source: Subject entity name
  - relation: Type of relation (choose from: treats_disease, used_for_diagnosis, performed_on, requires_instrument, performed_by_specialist, has_risk, has_benefit, has_complication, requires_anesthesia, requires_preparation, follow_up_by, related_to_procedure, other)
  - target: Object entity name
  - source_type: Type of source node (choose from: Procedure, Disease, Organ, BodySystem, Instrument, Specialist, Risk, Benefit, Complication, AnesthesiaType, Preparation, FollowUp, Condition, Other)
  - target_type: Type of target node (choose from: Procedure, Disease, Organ, BodySystem, Instrument, Specialist, Risk, Benefit, Complication, AnesthesiaType, Preparation, FollowUp, Condition, Other)
  - confidence: Float between 0 and 1

Return a JSON object with a key "triples" containing an array of these objects.

Text:
{text}
"""

NAME_PROMPT_TEMPLATE = """
Provide detailed information about the medical procedure '{procedure_name}' as a list of relationship triples.
Each triple must be a JSON object with:
  - source: Subject entity name
  - relation: Type of relation (choose from: treats_disease, used_for_diagnosis, performed_on, requires_instrument, performed_by_specialist, has_risk, has_benefit, has_complication, requires_anesthesia, requires_preparation, follow_up_by, related_to_procedure, other)
  - target: Object entity name
  - source_type: Type of source node (choose from: Procedure, Disease, Organ, BodySystem, Instrument, Specialist, Risk, Benefit, Complication, AnesthesiaType, Preparation, FollowUp, Condition, Other)
  - target_type: Type of target node (choose from: Procedure, Disease, Organ, BodySystem, Instrument, Specialist, Risk, Benefit, Complication, AnesthesiaType, Preparation, FollowUp, Condition, Other)
  - confidence: Float between 0 and 1 (use your best estimate)

Provide at least 5-10 triples to cover different aspects like what it treats, risks, instruments used, specialist, etc.
Return a JSON object with a key "triples" containing an array of these objects.
"""

# =========================
# Prompt Builder
# =========================

class PromptBuilder:
    """Standardized builder for medical procedure LLM prompts."""

    @staticmethod
    def build_extraction_prompt(text: str) -> str:
        """Creates a prompt for extracting triples from raw medical text."""
        return PROMPT_TEMPLATE.format(text=text)

    @staticmethod
    def build_name_prompt(procedure_name: str) -> str:
        """Creates a prompt for generating a procedure graph from a name."""
        return NAME_PROMPT_TEMPLATE.format(procedure_name=procedure_name)
