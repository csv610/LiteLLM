# =========================
# Imports
# =========================
import json
from typing import List, Literal, Optional

import matplotlib.pyplot as plt
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


class TripleList(BaseModel):
    """Container for a list of triples."""

    triples: List[Triple]


# =========================
# 2️⃣ Gemini Triplet Extractor
# =========================
class MedicineTripletExtractor:
    """Uses LiteClient or fallback simulation to extract biomedical triples."""

    def __init__(self, model_name: str = "ollama/gemma3"):
        self.model_name = model_name
        self.client = None

        if LiteClient is not None:
            config = ModelConfig(model=self.model_name)
            self.client = LiteClient(model_config=config)
        else:
            print("⚠️ 'lite' package not installed. Using offline mode.")

    def extract(self, text: str) -> List[Triple]:
        if self.client is not None:
            model_input = ModelInput(
                user_prompt=text,
                system_prompt=prompts.PROMPT,
                response_format=TripleList,
            )
            try:
                response = self.client.generate_text(model_input=model_input)
                # LiteClient with response_format returns the Pydantic object directly
                if isinstance(response, TripleList):
                    return response.triples
                elif isinstance(response, str):
                    # Fallback if it somehow returns a string
                    data = json.loads(response)
                    if isinstance(data, list):
                        return [Triple(**item) for item in data]
                    elif isinstance(data, dict) and "triples" in data:
                        return [Triple(**item) for item in data["triples"]]
            except Exception as e:
                print(f"⚠️ Extraction failed: {e}. Falling back to simulation.")

        return [Triple(**item) for item in self._simulate(text)]

    def _simulate(self, text: str):
        """Fallback for offline testing."""
        t = text.lower()
        if "paracetamol" in t:
            return [
                {
                    "source": "Paracetamol",
                    "relation": "treats",
                    "target": "Fever",
                    "source_type": "Drug",
                    "target_type": "Disease",
                },
                {
                    "source": "Paracetamol",
                    "relation": "treats",
                    "target": "Pain",
                    "source_type": "Drug",
                    "target_type": "Symptom",
                },
                {
                    "source": "Paracetamol",
                    "relation": "has_side_effect",
                    "target": "Liver toxicity",
                    "source_type": "Drug",
                    "target_type": "SideEffect",
                },
                {
                    "source": "Paracetamol",
                    "relation": "contraindicated_in",
                    "target": "Liver disease",
                    "source_type": "Drug",
                    "target_type": "Condition",
                },
                {
                    "source": "Paracetamol",
                    "relation": "belongs_to_class",
                    "target": "Analgesic",
                    "source_type": "Drug",
                    "target_type": "DrugClass",
                },
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
            self.G.add_edge(
                t.source, t.target, relation=t.relation, confidence=t.confidence
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

    def export_dot(self, path: str):
        """Exports the graph to a Graphviz .dot file."""
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
