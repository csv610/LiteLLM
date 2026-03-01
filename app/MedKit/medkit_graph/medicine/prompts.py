PROMPT = """
Extract medicine-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., DrugName, Ingredient, Class)
  - relation (choose from: mechanism_of_action, therapeutic_class, adverse_effect,
    treats, contraindication, dose_related_to, interact_with, metabolis_by,
    available_as, biomarker_indication)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
