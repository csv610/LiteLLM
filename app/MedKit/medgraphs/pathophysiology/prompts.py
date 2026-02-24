
PROMPT = """
Extract pathophysiology triplets from the following biomedical text.
Each triple must include:
- source
- relation (one of: causes, leads_to, results_in, mediated_by, associated_with,
  triggered_by, worsens, complicates, alleviated_by, regulated_by, linked_to,
  part_of, predisposes_to, mechanism_of, other)
- target
Optional: source_type, target_type, confidence

Return JSON array only.

Text:
"""{text}"""
"
