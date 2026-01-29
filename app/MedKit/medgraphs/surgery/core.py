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

# Relation types between surgical entities
Relation = Literal[
    "treats_disease",
    "performed_on_organ",
    "requires_instrument",
    "performed_by_specialist",
    "requires_anesthesia",
    "has_risk",
    "has_benefit",
    "has_complication",
    "requires_preparation",
    "follow_up_by",
    "related_to_surgery",
    "other",
]

# Node/entity types
NodeType = Literal[
    "Surgery",
    "Disease",
    "Organ",
    "BodySystem",
    "Instrument",
    "Specialist",
    "AnesthesiaType",
    "Risk",
    "Benefit",
    "Complication",
    "Preparation",
    "FollowUp",
    "Condition",
    "Other",
]

# Normalization maps
RELATION_ALIASES = {
    "treats": "treats_disease",
    "performed_on": "performed_on_organ",
    "organ": "performed_on_organ",
    "needs_instrument": "requires_instrument",
    "instrument": "requires_instrument",
    "surgeon": "performed_by_specialist",
    "anesthesia": "requires_anesthesia",
    "risk": "has_risk",
    "benefit": "has_benefit",
    "complication": "has_complication",
    "preparation": "requires_preparation",
    "follow_up": "follow_up_by",
    "related": "related_to_surgery",
}

NODE_TYPE_ALIASES = {
    "surgery": "Surgery",
    "operation": "Surgery",
    "procedure": "Surgery",
    "disease": "Disease",
    "condition": "Condition",
    "organ": "Organ",
    "system": "BodySystem",
    "instrument": "Instrument",
    "device": "Instrument",
    "specialist": "Specialist",
    "surgeon": "Specialist",
    "risk": "Risk",
    "benefit": "Benefit",
    "complication": "Complication",
    "anesthesia": "AnesthesiaType",
    "preparation": "Preparation",
    "follow_up": "FollowUp",
}


class Triple(BaseModel):
    """Represents one validated surgical relation."""
    source: str = Field(..., description="Subject entity")
    relation: Relation = Field(..., description="Type of relationship")
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
# 2️⃣ Gemini Surgery Extractor
# =========================
class SurgeryTripletExtractor:
    """Extracts structured triples from unstructured surgical text using Gemini."""

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
                print("⚠️ Skipped invalid triple:", item, "|", e)
        return triples

    def _simulate(self, text: str):
        """Offline mock extractor for testing."""
        t = text.lower()
        triples = []
        if "bypass surgery" in t:
            triples.extend([
                {"source": "Coronary Artery Bypass Surgery", "relation": "treats_disease", "target": "Coronary Artery Disease", "source_type": "Surgery", "target_type": "Disease"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "performed_on_organ", "target": "Heart", "source_type": "Surgery", "target_type": "Organ"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "requires_instrument", "target": "Heart-Lung Machine", "source_type": "Surgery", "target_type": "Instrument"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "performed_by_specialist", "target": "Cardiothoracic Surgeon", "source_type": "Surgery", "target_type": "Specialist"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "requires_anesthesia", "target": "General Anesthesia", "source_type": "Surgery", "target_type": "AnesthesiaType"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "has_risk", "target": "Heart Attack", "source_type": "Surgery", "target_type": "Risk"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "has_complication", "target": "Arrhythmia", "source_type": "Surgery", "target_type": "Complication"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "has_benefit", "target": "Improved Blood Flow", "source_type": "Surgery", "target_type": "Benefit"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "requires_preparation", "target": "Preoperative Fasting", "source_type": "Surgery", "target_type": "Preparation"},
                {"source": "Coronary Artery Bypass Surgery", "relation": "follow_up_by", "target": "Cardiac Rehabilitation", "source_type": "Surgery", "target_type": "FollowUp"},
            ])
        return triples


# =========================
# 3️⃣ Surgery Graph Builder
# =========================
class SurgeryGraphBuilder:
    """Builds and queries the surgical knowledge graph."""

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

    def query_risks(self, surgery: str):
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == surgery.lower() and d.get("relation") == "has_risk"
        ]

    def export_json(self, path: str = "surgery_graph.json"):
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
    """Visualizes the surgical knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Surgery": "#80b1d3",
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
