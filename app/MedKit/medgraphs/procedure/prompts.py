PROMPT = """
Extract procedure-related relationships as triples from the text.
Each triple must be a JSON object with:
  - source (e.g., Procedure, Tool, Specialty)
  - relation (choose from: indicated_for, contraindication, performed_on,
    uses_tool, step_of, complication_of, therapeutic_benefit, diagnostic_accuracy,
    associated_specialty, post_op_care)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

Text:
{text}
"""
