
PROMPT = """
Extract pharmacological relationships as JSON triples.
Each triple must include:
  - source
  - relation (choose from: binds_to, inhibits, activates, modulates, metabolized_by,
    eliminated_by, converted_to, targets_receptor, affects_pathway, induces_enzyme,
    inhibits_enzyme, upregulates, downregulates, causes_effect, other)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
"""{text}"""
"
