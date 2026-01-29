
PROMPT = """
Extract genetic relationships as JSON triples.
Each triple must include:
  - source
  - relation (one of: encodes, mutated_in, associated_with, expresses, involved_in,
    regulates, interacts_with, participates_in, upregulates, downregulates, linked_to,
    causes, contributes_to, part_of, pathogenic_in, protective_in, other)
  - target
Optional: source_type, target_type, confidence

Text:
"""{text}"""

