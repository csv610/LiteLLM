# =========================
# Imports
# =========================
import json
import os
from typing import List, Literal, Optional

import medicine_prompts as prompts
import networkx as nx
from pydantic import BaseModel, Field, validator

try:
    from lite import LiteClient
    from lite.config import ModelConfig, ModelInput
except ImportError:
    LiteClient = None
    ModelConfig = None
    ModelInput = None


# =========================
# 1️⃣ Pydantic Models
# =========================
Relation = Literal[
    "treats",
    "has_side_effect",
    "belongs_to_class",
    "has_atc_classification",
    "has_therapeutic_class",
    "has_pharmacological_class",
    "interacts_with",
    "contraindicated_in",
    "has_active_ingredient",
    "affects_system",
    "has_dosage_form",
    "has_route",
    "requires_test",
    "causes",
    "has_mechanism",
    "manufactured_by",
    "recommended_dose_for",
    "safe_for_breastfeeding",
    "contraindicated_in_breastfeeding",
    "safe_for_children",
    "contraindicated_in_children",
    "safe_for_elderly",
    "contraindicated_in_elderly",
    "has_restriction",
    "approved_by",
    "approved_on",
    "other",
]

NodeType = Literal[
    "Drug",
    "DrugClass",
    "ATCClass",
    "ActiveIngredient",
    "Disease",
    "Symptom",
    "SideEffect",
    "DosageForm",
    "Condition",
    "BodySystem",
    "Mechanism",
    "Route",
    "Manufacturer",
    "ClinicalTest",
    "Contraindication",
    "LactationContext",
    "AgeGroup",
    "Restriction",
    "RegulatoryAgency",
    "Date",
    "Other",
]

RELATION_ALIASES = {
    "treat": "treats",
    "treats_for": "treats",
    "side_effect": "has_side_effect",
    "adverse_effect": "has_side_effect",
    "belongs_to": "belongs_to_class",
    "is_a": "belongs_to_class",
    "atc": "has_atc_classification",
    "atc_code": "has_atc_classification",
    "therapeutic_class": "has_therapeutic_class",
    "pharmacological_class": "has_pharmacological_class",
    "interaction": "interacts_with",
    "interacts": "interacts_with",
    "contraindicated": "contraindicated_in",
    "active_ingredient": "has_active_ingredient",
    "affects": "affects_system",
    "dosage_form": "has_dosage_form",
    "mechanism": "has_mechanism",
    "manufacturer": "manufactured_by",
    "dose_for": "recommended_dose_for",
    "breastfeeding_safe": "safe_for_breastfeeding",
    "lactation_safe": "safe_for_breastfeeding",
    "child_safe": "safe_for_children",
    "pediatric_safe": "safe_for_children",
    "elderly_safe": "safe_for_elderly",
    "geriatric_safe": "safe_for_elderly",
    "fda_approved": "approved_by",
    "approval_date": "approved_on",
}

NODE_TYPE_ALIASES = {
    "medicine": "Drug",
    "drug": "Drug",
    "medication": "Drug",
    "class": "DrugClass",
    "drug_class": "DrugClass",
    "disease": "Disease",
    "disorder": "Disease",
    "condition": "Condition",
    "symptom": "Symptom",
    "side_effect": "SideEffect",
    "side effect": "SideEffect",
    "form": "DosageForm",
    "system": "BodySystem",
    "mechanism": "Mechanism",
    "manufacturer": "Manufacturer",
    "route": "Route",
}


class Triple(BaseModel):
    """Represents one biomedical relation."""

    source: str = Field(..., description="Subject entity", alias="subject")
    relation: Relation = Field(..., description="Relation type", alias="predicate")
    target: str = Field(..., description="Object entity", alias="object")
    source_type: NodeType = Field("Other", alias="subject_type")
    target_type: NodeType = Field("Other", alias="object_type")
    evidence: Optional[str] = Field(None, description="Brief medical justification or reference")

    class Config:
        populate_by_name = True

    @validator("source", "target")
    def not_empty_entity(cls, v):
        if not v or not v.strip():
            raise ValueError("Entity name cannot be empty")
        return v.strip()

    @validator("relation", pre=True)
    def normalize_relation(cls, v):
        if not v:
            return "other"
        rv = str(v).strip().lower().replace(" ", "_")
        if rv in RELATION_ALIASES:
            rv = RELATION_ALIASES[rv]
        allowed = set(Relation.__args__)
        return rv if rv in allowed else "other"

    @validator("source_type", "target_type", pre=True)
    def normalize_node_type(cls, v):
        if not v:
            return "Other"
        key = str(v).strip().lower().replace(" ", "_")
        if key.capitalize() in NodeType.__args__:
            return key.capitalize()
        if key in NODE_TYPE_ALIASES:
            return NODE_TYPE_ALIASES[key]
        return "Other"


class MedicineReport(BaseModel):
    """Container for a structured medicine report."""

    name: str = Field(..., description="Name of the medicine")
    therapeutic_class: str = Field(..., description="Therapeutic class of the medicine")
    description: str = Field(..., description="High-level medical overview")
    triples: List[Triple] = Field(..., description="List of biomedical triples")


# =========================
# 2️⃣ Graph Builder
# =========================
class MedicineKnowledgeGraph:
    """Builds and queries the medicine knowledge graph using LLM."""

    def __init__(self, model_config: Optional["ModelConfig"] = None):
        self.G = nx.MultiDiGraph()
        self.model_config = model_config
        self.client = None
        self.last_report = None

        if LiteClient is not None:
            if self.model_config is None:
                self.model_config = ModelConfig(
                    model="ollama/gemma3", temperature=0.0
                )
            self.client = LiteClient(model_config=self.model_config)
        else:
            raise ImportError("'lite' package is required for MedicineKnowledgeGraph.")

    def build_from_medicine(self, medicine_name: str):
        """Generates a structured medicine report and builds the graph."""
        model_input = ModelInput(
            user_prompt=prompts.GENERATION_USER_PROMPT.format(medicine_name=medicine_name),
            system_prompt=prompts.GENERATION_SYSTEM_PROMPT,
            response_format=MedicineReport,
        )
        report = self.client.generate_text(model_input=model_input)
        if isinstance(report, MedicineReport):
            self.last_report = report
            self.add_triples(report.triples)
            return report.triples
        else:
            raise ValueError(f"Expected MedicineReport, got {type(report)}")

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(
                t.source, t.target, relation=t.relation, evidence=t.evidence
            )

    def query_treats(self, disease: str):
        return [
            src
            for src, tgt, d in self.G.edges(data=True)
            if tgt.lower() == disease.lower() and d.get("relation") == "treats"
        ]

    def query_side_effects(self, drug: str):
        return [
            tgt
            for src, tgt, d in self.G.edges(data=True)
            if src.lower() == drug.lower() and d.get("relation") == "has_side_effect"
        ]

    def export_json(self, path: str = "medicine_graph.json"):
        if not self.last_report:
            print("⚠️ No report to export.")
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.last_report.model_dump_json(indent=2, by_alias=True))
        print(f"✅ Graph exported to {path}")

    def export_dot(self, medicine: str):
        """Exports the graph to a Graphviz .dot file."""
        os.makedirs("outputs", exist_ok=True)
        path = f"outputs/{medicine.lower().replace(' ', '_')}.dot"

        with open(path, "w", encoding="utf-8") as f:
            f.write("digraph G {\n")
            f.write("  rankdir=LR;\n")
            f.write('  node [style=filled, shape=rect, fontname="Arial"];\n')

            color_map = {
                "Drug": "#8dd3c7",
                "Disease": "#fb8072",
                "SideEffect": "#ffffb3",
                "DrugClass": "#bebada",
                "Condition": "#80b1d3",
                "Other": "#fdb462",
            }

            for n, d in self.G.nodes(data=True):
                node_type = d.get("type", "Other")
                color = color_map.get(node_type, "#fdb462")
                f.write(
                    f'  "{n}" [fillcolor="{color}", label="{n}\\n({node_type})"];\n'
                )

            for u, v, d in self.G.edges(data=True):
                rel = d.get("relation", "other")
                f.write(f'  "{u}" -> "{v}" [label="{rel}"];\n')
            f.write("}\n")
        print(f"✅ Graph exported to {path}")
