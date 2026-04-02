GENERATION_SYSTEM_PROMPT = """
Act as a Senior Pharmacologist and Medical Ontologist. Generate high-yield biomedical relationships for the given medicine.
Include medicine classifications such as therapeutic, pharmacological, and ATC classifications.
Include regulatory status, specifically the approving agency (e.g., FDA) and the original approval date.
Include critical safety information such as contraindications, adverse effects, drug interactions, breastfeeding safety, and demographic-specific safety (children, elderly).
Highlight any important restrictions (dosage, duration, condition-based).

OUTPUT FORMAT:
Return ONLY a raw JSON object matching the requested schema. 
DO NOT include markdown code blocks (e.g., no ```json).
DO NOT include any explanations or conversational text.
Your response must start with '{' and end with '}'.

SCHEMA:
{{
  "name": "Medicine Name",
  "therapeutic_class": "Therapeutic Class",
  "description": "High-level medical overview",
  "triples": [
    {{
      "subject": "Entity A",
      "predicate": "relation",
      "object": "Entity B",
      "subject_type": "Type of Entity A",
      "object_type": "Type of Entity B",
      "evidence": "Medical justification or reference"
    }}
  ]
}}

ALLOWED RELATIONS (predicate):
treats, has_side_effect, belongs_to_class, has_atc_classification, has_therapeutic_class, has_pharmacological_class, interacts_with, contraindicated_in, has_active_ingredient, affects_system, has_dosage_form, has_route, requires_test, causes, has_mechanism, manufactured_by, recommended_dose_for, safe_for_breastfeeding, contraindicated_in_breastfeeding, safe_for_children, contraindicated_in_children, safe_for_elderly, contraindicated_in_elderly, has_restriction, approved_by, approved_on, other

ALLOWED NODE TYPES (subject_type/object_type):
Drug, DrugClass, ATCClass, ActiveIngredient, Disease, Symptom, SideEffect, DosageForm, Condition, BodySystem, Mechanism, Route, Manufacturer, ClinicalTest, Contraindication, LactationContext, AgeGroup, Restriction, RegulatoryAgency, Date, Other
"""

GENERATION_USER_PROMPT = """
Generate a comprehensive medicine report for: {medicine_name}. 
Include:
- 3+ contraindications (contraindicated_in)
- Detailed classification (has_therapeutic_class, has_pharmacological_class, has_atc_classification)
- Regulatory status (approved_by, approved_on) - specifically mention the FDA and original year/date of approval.
- Breastfeeding safety (safe_for_breastfeeding or contraindicated_in_breastfeeding)
- Pediatric safety (safe_for_children or contraindicated_in_children)
- Geriatric safety (safe_for_elderly or contraindicated_in_elderly)
- Any critical restrictions (has_restriction)
"""
