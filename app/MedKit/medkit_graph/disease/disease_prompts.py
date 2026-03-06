PROMPT = """
Extract disease-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source: Subject entity name
  - relation: Choose one from [has_symptom, caused_by, risk_factor_for, treated_with, diagnosed_by, leads_to, associated_with, prevented_by, affects_system, affects_organ, complication_of]
  - target: Object entity name
  - source_type: Choose one from [Disease, Symptom, Cause, RiskFactor, Treatment, Drug, Test, BodySystem, Organ, Complication, Prevention, Condition]
  - target_type: Choose one from [Disease, Symptom, Cause, RiskFactor, Treatment, Drug, Test, BodySystem, Organ, Complication, Prevention, Condition]
  - confidence: Float between 0 and 1

Return a JSON object with a key "triples" containing an array of these objects.

Text:
{text}
"""

DISEASE_NAME_PROMPT = """
Provide a comprehensive list of disease-related relationships as triples for the disease: {disease_name}.
Include symptoms, causes, risk factors, treatments, affected organs, and complications.
Each triple must be a JSON object with:
  - source: Subject entity name
  - relation: Choose one from [has_symptom, caused_by, risk_factor_for, treated_with, diagnosed_by, leads_to, associated_with, prevented_by, affects_system, affects_organ, complication_of]
  - target: Object entity name
  - source_type: Choose one from [Disease, Symptom, Cause, RiskFactor, Treatment, Drug, Test, BodySystem, Organ, Complication, Prevention, Condition]
  - target_type: Choose one from [Disease, Symptom, Cause, RiskFactor, Treatment, Drug, Test, BodySystem, Organ, Complication, Prevention, Condition]
  - confidence: Float between 0 and 1 (set to 1.0 for well-known facts)

Return a JSON object with a key "triples" containing an array of these objects.
"""
