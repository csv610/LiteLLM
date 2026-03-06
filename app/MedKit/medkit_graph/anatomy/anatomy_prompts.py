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

GENERATION_PROMPT = """
Generate a comprehensive set of anatomical relationships for the given anatomy name as triples.
Provide details about its system, blood supply (arterial and venous), nerve supply, location (cavity/region),
adjacent structures, composition, and associated diseases (common and rare).
Return a JSON object with a 'triples' key containing an array of triple objects.

Each triple object must have:
  - source (the anatomy entity)
  - relation (choose from: part_of, connected_to, supplied_by, drained_by,
    innervated_by, located_in, composed_of, adjacent_to, protects, supports,
    associated_with_system, common_disease, rare_disease, other)
  - target (the related entity)
Optional: source_type (choose from: Organ, Tissue, BodySystem, Vessel, Nerve, Bone, Muscle, Cavity, Region, Cell, Disease, Other),
          target_type (same as source_type),
          confidence

Anatomy Name:
{anatomy_name}
"""
