PROMPT = """
Extract pharmacological relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., Drug, Target, Receptor)
  - relation (choose from: binds_to, agonist_for, antagonist_at, metabolizes,
    inhibits, activates, distributed_to, absorbed_by, excreted_through,
    effective_concentration, side_effect_of)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
