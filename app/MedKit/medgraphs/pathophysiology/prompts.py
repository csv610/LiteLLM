PROMPT = """
Extract pathophysiological relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., Mechanism, Trigger, Symptom)
  - relation (choose from: triggers, leads_to, exacerbates, inhibits,
    characterized_by, mechanism_of, resultant_effect, cellular_impact,
    systemic_response, associated_pathway)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
