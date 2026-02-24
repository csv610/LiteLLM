PROMPT = """
Extract anatomical relationships as triples from the text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: part_of, connected_to, supplied_by, drained_by,
    innervated_by, located_in, composed_of, adjacent_to, protects, supports,
    associated_with_system, other)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
"""{text}"""
"""
