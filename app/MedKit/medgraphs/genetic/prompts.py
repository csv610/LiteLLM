PROMPT = """
Extract genetic relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., Gene, Protein, Variant)
  - relation (choose from: encodes, interacts_with, mutation_associated_with,
    regulates, located_on_chromosome, variant_of, part_of_pathway, biomarker_for,
    inherits_as, expressed_in)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
