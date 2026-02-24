
PROMPT = """
Extract surgical knowledge triples from the following text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: treats_disease, performed_on_organ,
    requires_instrument, performed_by_specialist, requires_anesthesia,
    has_risk, has_benefit, has_complication, requires_preparation,
    follow_up_by, related_to_surgery, other)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
"""{text}"""
