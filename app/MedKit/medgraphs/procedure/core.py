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
# 1️⃣ Pydantic Models
# =========================

# ---- Canonical edge (relation) types ----
Relation = Literal[
    "treats_disease",
    "used_for_diagnosis",
    "performed_on",
    "requires_instrument",
    "performed_by_specialist",
    "has_risk",
    "has_benefit",
    "has_complication",
    "requires_anesthesia",
    "requires_preparation",
    "follow_up_by",
    "related_to_procedure",
    "other",
]

# ---- Node (entity) types ----
NodeType = Literal[
    "Procedure",
    "Disease",
    "Organ",
    "BodySystem",
    "Instrument",
    "Specialist",
    "Risk",
    "Benefit",
    "Complication",
    "AnesthesiaType",
    "Preparation",
    "FollowUp",
    "Condition",
    "Other",
]

# ---- Normalization dictionaries ----
RELATION_ALIASES = {
    "treats": "treats_disease",
    "used_for": "used_for_diagnosis",
    "diagnose": "used_for_diagnosis",
    "performed": "performed_on",
    "needs_instrument": "requires_instrument",
    "instrument": "requires_instrument",
    "specialist": "performed_by_specialist",
    "risk": "has_risk",
    "benefit": "has_benefit",
    "complication": "has_complication",
    "anesthesia": "requires_anesthesia",
    "preparation": "requires_preparation",
    "follow_up": "follow_up_by",
    "related": "related_to_procedure",
}

NODE_TYPE_ALIASES = {
    "procedure": "Procedure",
    "surgery": "Procedure",
    "operation": "Procedure",
    "test": "Procedure",
    "disease": "Disease",
    "condition": "Condition",
    "organ": "Organ",
    "system": "BodySystem",
    "instrument": "Instrument",
    "device": "Instrument",
    "surgeon": "Specialist",
    "doctor": "Specialist",
    "risk": "Risk",
    "benefit": "Benefit",
    "complication": "Complication",
    "anesthesia": "AnesthesiaType",
    "preparation": "Preparation",
    "follow_up": "FollowUp",
}


class Triple(BaseModel):
    """Represents one validated medical procedure relation."""
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
# 2️⃣ Gemini Procedure Extractor
# =========================
class ProcedureTripletExtractor:
    """Uses Gemini (or fallback) to extract structured procedure triples."""

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
        """Offline fallback for testing."""
        t = text.lower()
        triples = []
        if "appendectomy" in t:
             triples.extend([
                 {"source": "Appendectomy", "relation": "treats_disease", "target": "Appendicitis", "source_type": "Procedure", "target_type": "Disease"},
                 {"source": "Appendectomy", "relation": "performed_on", "target": "Appendix", "source_type": "Procedure", "target_type": "Organ"},
                 {"source": "Appendectomy", "relation": "has_risk", "target": "Infection", "source_type": "Procedure", "target_type": "Risk"},
             ])
        return triples

# =========================
# 3️⃣ Procedure Graph Builder
# =========================
class ProcedureGraphBuilder:
    """Builds and queries the procedure knowledge graph."""

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
            if tgt.lower() == disease.lower() and d.get("relation") == "treats_disease"
        ]

    def export_json(self, path: str = "procedure_graph.json"):
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
    """Visualizes the procedure knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Procedure": "#80b1d3",
            "Disease": "#fb8072",
            "Organ": "#8dd3c7",
            "Instrument": "#bebada",
            "Specialist": "#b3de69",
            "Risk": "#fccde5",
            "Benefit": "#bc80bd",
            "Complication": "#fdb462",
            "AnesthesiaType": "#ffffb3",
            "Preparation": "#ccebc5",
            "FollowUp": "#ffed6f",
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
