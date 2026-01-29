
PROMPT = """
Extract biomedical knowledge triples from the text below.
Each triple must be a JSON object with:
  - source
  - relation (choose from: treats, has_side_effect, belongs_to_class,
    interacts_with, contraindicated_in, has_active_ingredient, affects_system,
    has_dosage_form, has_route, requires_test, causes, has_mechanism,
    manufactured_by, recommended_dose_for, other)
  - target
Optional: source_type, target_type, confidence

Return only a JSON array.

Text:
"""{text}"""
