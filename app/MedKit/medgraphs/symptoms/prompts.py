
PROMPT = """
Extract symptom knowledge triples from the text below.
Each triple must be a JSON object with:
  - source
  - relation (choose from: associated_with_disease, caused_by_condition, indicates_disease,
    affects_body_part, diagnosed_by_test, treated_with_drug, treated_with_procedure,
    has_severity, has_duration, co_occurs_with, risk_factor_for, other)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
"""{text}"""
