
PROMPT = """
Extract structured disease knowledge triples from the following text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: has_symptom, caused_by, risk_factor, treated_by,
    diagnosed_by, leads_to, associated_with, prevented_by, affects_system, other)
  - target
Optional: source_type, target_type, confidence
Return only a JSON array.

Text:
"""{text}"""
