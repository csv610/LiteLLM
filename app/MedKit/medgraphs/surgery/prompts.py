PROMPT = """
Extract surgery-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., Surgery, Anesthesia, Equipment)
  - relation (choose from: indicated_for, contraindication, performed_in_position,
    uses_equipment, step_of, complication_of, therapeutic_benefit, surgical_approach,
    associated_specialty, post_op_care, requires_anesthesia)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
