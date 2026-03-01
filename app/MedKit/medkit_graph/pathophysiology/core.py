# =========================
# Imports
# =========================
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import prompts

try:
    from google import genai
except ImportError:
    genai = None


# =========================
# 1️⃣ Schema
# =========================

# Relation (edge) types
Relation = Literal[
    "causes",
    "leads_to",
    "results_in",
    "mediated_by",
    "associated_with",
    "triggered_by",
    "worsens",
    "complicates",
    "alleviated_by",
    "regulated_by",
    "linked_to",
    "part_of",
    "predisposes_to",
    "mechanism_of",
    "other",
]

# Node (entity) types
NodeType = Literal[
    "Cause",
    "Mechanism",
    "Pathway",
    "Molecule",
    "Disease",
    "Symptom",
    "Process",
    "Organ",
    "Cell",
    "System",
    "Treatment",
    "Other",
]

RELATION_ALIASES = {
    "leads": "leads_to",
    "induces": "causes",
    "triggers": "triggered_by",
    "mediated": "mediated_by",
    "associated": "associated_with",
    "part": "part_of",
    "results": "results_in",
    "linked": "linked_to",
    "worsens": "worsens",
    "alleviated": "alleviated_by",
    "regulates": "regulated_by",
}

NODE_TYPE_ALIASES = {
    "cause": "Cause",
    "mechanism": "Mechanism",
    "pathway": "Pathway",
    "disease": "Disease",
    "symptom": "Symptom",
    "organ": "Organ",
    "system": "System",
    "cell": "Cell",
    "molecule": "Molecule",
    "process": "Process",
    "treatment": "Treatment",
}


class Triple(BaseModel):
    source: str = Field(..., description="Source entity in the pathophysiology relationship")
    relation: Relation = Field(..., description="Type of biological relationship")
    target: str = Field(..., description="Target entity in the relationship")
    source_type: NodeType = "Other"
    target_type: NodeType = "Other"
    confidence: Optional[float] = None

    @validator("source", "target")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Entity cannot be empty")
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
    def normalize_type(cls, v):
        if not v:
            return "Other"
        key = str(v).strip().lower().replace(" ", "")
        if key.capitalize() in NodeType.__args__:
            return key.capitalize()
        if key in NODE_TYPE_ALIASES:
            return NODE_TYPE_ALIASES[key]
        return "Other"


# =========================
# 2️⃣ LLM Triplet Extractor
# =========================
class PathophysiologyTripletExtractor:
    """Extracts cause–mechanism–disease–symptom triplets using Gemini or offline fallback."""

    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.client = None

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and genai is not None:
            self.client = genai.Client(api_key=api_key)
        elif api_key and genai is None:
            print("⚠️ GEMINI_API_KEY set but google.genai not installed. Using offline mode.")

    def build_prompt(self, text: str) -> str:
        return prompts.PROMPT.format(text=text)

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
                raw_list = json.loads(response.text)
        else:
            raw_list = self._simulate(text)

        triples = []
        for item in raw_list:
            try:
                triples.append(Triple(**item))
            except Exception as e:
                print("⚠️ Invalid triple skipped:", item, "|", e)
        return triples

    def _simulate(self, text: str):
        """Offline fallback examples."""
        t = text.lower()
        triples = []
        if "inflammation" in t:
            triples.extend([
                {"source": "Inflammation", "relation": "causes", "target": "Cytokine Release", "source_type": "Process", "target_type": "Mechanism"},
                {"source": "Cytokine Release", "relation": "leads_to", "target": "Fever", "source_type": "Mechanism", "target_type": "Symptom"},
                {"source": "Inflammation", "relation": "associated_with", "target": "Tissue Damage", "source_type": "Process", "target_type": "Symptom"},
                {"source": "Infection", "relation": "causes", "target": "Inflammation", "source_type": "Cause", "target_type": "Process"},
                {"source": "Fever", "relation": "alleviated_by", "target": "Paracetamol", "source_type": "Symptom", "target_type": "Treatment"},
            ])
        return triples


# =========================
# 3️⃣ Graph Builder
# =========================
class PathophysiologyGraphBuilder:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_path(self, start: str, end: str):
        """Find any causal path between two entities."""
        try:
            return nx.shortest_path(self.G, start, end)
        except Exception:
            return None

    def find_symptoms(self, disease: str):
        """Find all symptoms caused by a disease."""
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == disease.lower() and d.get("target_type") == "Symptom"
        ]

    def export_json(self, path="pathophysiology_graph.json"):
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
# 4️⃣ Visualization
# =========================
class GraphVisualizer:
    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.7, iterations=50)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Cause": "#fb8072",
            "Mechanism": "#80b1d3",
            "Pathway": "#8dd3c7",
            "Disease": "#bebada",
            "Symptom": "#fdb462",
            "Organ": "#b3de69",
            "System": "#fccde5",
            "Treatment": "#bc80bd",
            "Process": "#ffffb3",
            "Molecule": "#ccebc5",
            "Other": "#d9d9d9",
        }

        node_colors = [
            color_map.get(self.G.nodes[n].get("type", "Other"), "#d9d9d9")
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
