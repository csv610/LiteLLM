# =========================
# Prompt Constants
# =========================

NAME_PROMPT_TEMPLATE = """
Provide a medically rigorous and detailed knowledge graph for the medical procedure '{procedure_name}'.
The graph must be suitable for a professional medical board review.

Guidelines:
1. **Clinical Depth**: Include specific anatomical structures (e.g., instead of 'Knee', use 'Femur', 'Tibia', 'Patellar tendon'), specific surgical instruments/implants, and precise medical conditions.
2. **Nuance**: Include common and severe risks, benefits, specific anesthesia types (e.g., 'Spinal Anesthesia'), detailed patient preparation steps, and follow-up care.
3. **Accuracy**: Use standard medical terminology (SNOMED-CT or ICD-10 style concepts).
4. **Volume**: Provide at least 15-20 triples to ensure comprehensive coverage across different domains (anatomy, risk, specialist, etc.).

Each triple must be a JSON object with:
  - source: Subject entity name
  - relation: Type of relation (choose from: treats_disease, used_for_diagnosis, performed_on, requires_instrument, performed_by_specialist, has_risk, has_benefit, has_complication, has_contraindication, requires_anesthesia, requires_preparation, follow_up_by, related_to_procedure, other)
  - target: Object entity name
  - source_type: Type of source node (choose from: Procedure, Disease, Organ, BodySystem, Instrument, Specialist, Risk, Benefit, Complication, AnesthesiaType, Preparation, FollowUp, Condition, Contraindication, Other)
  - target_type: Type of target node (choose from: Procedure, Disease, Organ, BodySystem, Instrument, Specialist, Risk, Benefit, Complication, AnesthesiaType, Preparation, FollowUp, Condition, Contraindication, Other)
  - confidence: Float between 0 and 1 (use your best estimate)

Return a JSON object with a key "triples" containing an array of these objects.
"""

# =========================
# Prompt Builder
# =========================


class PromptBuilder:
    """Standardized builder for medical procedure LLM prompts."""

    @staticmethod
    def build_name_prompt(procedure_name: str) -> str:
        """Creates a prompt for generating a procedure graph from a name."""
        return NAME_PROMPT_TEMPLATE.format(procedure_name=procedure_name)
