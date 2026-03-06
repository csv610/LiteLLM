PROMPT = """
Extract anatomical relationships as triples from the text.
Return a JSON object with a 'triples' key containing an array of triple objects.
Each triple object must have:
  - source
  - relation (choose from: part_of, connected_to, supplied_by, drained_by,
    innervated_by, located_in, composed_of, adjacent_to, protects, supports,
    associated_with_system, common_disease, rare_disease, other)
  - target
Optional: source_type (choose from: Organ, Tissue, BodySystem, Vessel, Nerve, Bone, Muscle, Cavity, Region, Cell, Disease, Other),
          target_type (same as source_type),
          confidence

Text:
{text}
"""
