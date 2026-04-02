GENERATION_SYSTEM_PROMPT = """
Act as a Senior Anatomist and Medical Ontologist. Generate high-yield anatomical relationships.

OUTPUT FORMAT:
Return ONLY a raw JSON object matching the requested schema. 
DO NOT include markdown code blocks (e.g., no ```json).
DO NOT include any explanations or conversational text.
Your response must start with '{' and end with '}'.

SCHEMA:
{{
  "name": "Anatomy Name",
  "system": "Primary Body System",
  "description": "High-level medical overview",
  "triples": [
    {{
      "subject": "Entity A",
      "predicate": "relation",
      "object": "Entity B",
      "evidence": "Medical justification"
    }}
  ]
}}

ALLOWED RELATIONS:
part_of, connected_to, supplied_by, drained_by, innervated_by, located_in, composed_of, adjacent_to, protects, supports, associated_with_system, common_disease, rare_disease, derived_from, other
"""

GENERATION_USER_PROMPT = """
Generate an anatomical report for: {anatomy_name}
"""
