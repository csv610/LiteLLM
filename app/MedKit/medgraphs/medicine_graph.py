# =========================
# Imports
# =========================
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator
import networkx as nx
import matplotlib.pyplot as plt
import json
import os

try:
    from google import genai
except ImportError:
    genai = None


# =========================
# 1️⃣ Pydantic Models
# =========================
Relation = Literal[
    "treats",
    "has_side_effect",
    "belongs_to_class",
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
    "other",
]

NodeType = Literal[
    "Drug",
    "DrugClass",
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
    "Other",
]

RELATION_ALIASES = {
    "treat": "treats",
    "treats_for": "treats",
    "side_effect": "has_side_effect",
    "adverse_effect": "has_side_effect",
    "belongs_to": "belongs_to_class",
    "is_a": "belongs_to_class",
    "interaction": "interacts_with",
    "interacts": "interacts_with",
    "contraindicated": "contraindicated_in",
    "active_ingredient": "has_active_ingredient",
    "affects": "affects_system",
    "dosage_form": "has_dosage_form",
    "mechanism": "has_mechanism",
    "manufacturer": "manufactured_by",
    "dose_for": "recommended_dose_for",
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
    source: str = Field(..., description="Subject entity")
    relation: Relation = Field(..., description="Relation type")
    target: str = Field(..., description="Object entity")
    source_type: NodeType = "Other"
    target_type: NodeType = "Other"
    confidence: Optional[float] = None

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


# =========================
# 2️⃣ Gemini Triplet Extractor
# =========================
class MedicineTripletExtractor:
    """Uses Gemini or fallback simulation to extract biomedical triples."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.client = None

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and genai is not None:
            self.client = genai.Client(api_key=api_key)
        elif api_key and genai is None:
            print("⚠️ GEMINI_API_KEY set but google.genai not installed. Using offline mode.")

    def build_prompt(self, text: str) -> str:
        return f"""
Extract biomedical knowledge triples from the text below.
Each triple must be a JSON object with:
  - source
  - relation (choose from: treats, has_side_effect, belongs_to_class,
    interacts_with, contraindicated_in, has_active_ingredient, affects_system,
    has_dosage_form, has_route, requires_test, causes, has_mechanism,
    manufactured_by, recommended_dose_for, other)
  - target
Optional: source_type, target_type, confidence

Return only a JSON array.

Text:
\"\"\"{text}\"\"\"
"""

    def extract(self, text: str) -> List[Triple]:
        raw_list = None
        if self.client is not None:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.build_prompt(text),
                config={"response_mime_type": "application/json"},
            )
            try:
                raw_list = response.parsed
            except Exception:
                try:
                    raw_list = json.loads(response.text)
                except Exception:
                    raw_list = []
        else:
            raw_list = self._simulate(text)

        triples = []
        for item in raw_list:
            try:
                triples.append(Triple(**item))
            except Exception as e:
                print("⚠️ Skipped invalid triple:", item, "|", e)
        return triples

    def _simulate(self, text: str):
        """Fallback for offline testing."""
        t = text.lower()
        if "paracetamol" in t:
            return [
                {"source": "Paracetamol", "relation": "treats", "target": "Fever", "source_type": "Drug", "target_type": "Disease"},
                {"source": "Paracetamol", "relation": "treats", "target": "Pain", "source_type": "Drug", "target_type": "Symptom"},
                {"source": "Paracetamol", "relation": "has_side_effect", "target": "Liver toxicity", "source_type": "Drug", "target_type": "SideEffect"},
                {"source": "Paracetamol", "relation": "contraindicated_in", "target": "Liver disease", "source_type": "Drug", "target_type": "Condition"},
                {"source": "Paracetamol", "relation": "belongs_to_class", "target": "Analgesic", "source_type": "Drug", "target_type": "DrugClass"},
            ]
        return []


# =========================
# 3️⃣ Graph Builder
# =========================
class MedicineGraphBuilder:
    """Builds and queries the medicine knowledge graph."""

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_treats(self, disease: str):
        return [
            src for src, tgt, d in self.G.edges(data=True)
            if tgt.lower() == disease.lower() and d.get("relation") == "treats"
        ]

    def query_side_effects(self, drug: str):
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == drug.lower() and d.get("relation") == "has_side_effect"
        ]

    def export_json(self, path: str = "medicine_graph.json"):
        triples = [
            {
                "source": u,
                "relation": d.get("relation"),
                "target": v,
                "source_type": self.G.nodes[u].get("type"),
                "target_type": self.G.nodes[v].get("type"),
                "confidence": d.get("confidence"),
            }
            for u, v, d in self.G.edges(data=True)
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(triples, f, indent=2)
        print(f"✅ Graph exported to {path}")


# =========================
# 4️⃣ Graph Visualizer
# =========================
class GraphVisualizer:
    """Visualizes the medicine knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Drug": "#8dd3c7",
            "Disease": "#fb8072",
            "SideEffect": "#ffffb3",
            "DrugClass": "#bebada",
            "Condition": "#80b1d3",
            "Other": "#fdb462",
        }

        node_colors = [
            color_map.get(self.G.nodes[n].get("type", "Other"), "#fdb462")
            for n in self.G.nodes()
        ]

        nx.draw(
            self.G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=2200,
            font_size=9,
            font_weight="bold",
            arrows=True,
        )
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()


# =========================
# 5️⃣ Main Runner
# =========================
if __name__ == "__main__":
    text = """
    Paracetamol is an analgesic and antipyretic used to treat fever and mild pain.
    It may cause liver toxicity and is contraindicated in patients with liver disease.
    """

    extractor = MedicineTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted & validated triples:")
    for t in triples:
        print(t.dict())

    builder = MedicineGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Drugs that treat Fever:", builder.query_treats("Fever"))
    print("🔹 Side effects of Paracetamol:", builder.query_side_effects("Paracetamol"))

    builder.export_json("medicine_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()

