PROMPT = """
Extract disease-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: caused_by, risk_factor, complication, symptom_of,
    treated_with, prevents, affects_organ, genetic_basis, epidemiological_link,
    differential_diagnosis, mechanism_of, associated_with)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
