PROMPT = """
Extract symptom-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., Symptom, Sign, Condition)
  - relation (choose from: caused_by, associated_with, symptom_of,
    risk_factor_for, precedes, follows, exacerbated_by, relieved_by,
    manifestation_of, sign_of, localized_to)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
