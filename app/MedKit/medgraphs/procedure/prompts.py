
PROMPT = """
Extract medical procedure triples from the following text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: treats_disease, used_for_diagnosis, performed_on,
    requires_instrument, performed_by_specialist, has_risk, has_benefit,
    has_complication, requires_anesthesia, requires_preparation,
    follow_up_by, related_to_procedure, other)
  - target
Optional: source_type, target_type, confidence
Return only a JSON array.

Text:
"""{text}"""
