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

# Relation (edge) types
Relation = Literal[
    "part_of",
    "connected_to",
    "supplied_by",
    "drained_by",
    "innervated_by",
    "located_in",
    "composed_of",
    "adjacent_to",
    "protects",
    "supports",
    "associated_with_system",
    "other",
]

# Node (entity) types
NodeType = Literal[
    "Organ",
    "Tissue",
    "BodySystem",
    "Vessel",
    "Nerve",
    "Bone",
    "Muscle",
    "Cavity",
    "Region",
    "Cell",
    "Other",
]

# Normalization dictionaries
RELATION_ALIASES = {
    "is_part_of": "part_of",
    "connected": "connected_to",
    "blood_supply": "supplied_by",
    "venous_drainage": "drained_by",
    "nerve_supply": "innervated_by",
    "in": "located_in",
    "made_of": "composed_of",
    "near": "adjacent_to",
    "protects": "protects",
    "supports": "supports",
    "belongs_to_system": "associated_with_system",
}

NODE_TYPE_ALIASES = {
    "organ": "Organ",
    "tissue": "Tissue",
    "system": "BodySystem",
    "vessel": "Vessel",
    "artery": "Vessel",
    "vein": "Vessel",
    "nerve": "Nerve",
    "bone": "Bone",
    "muscle": "Muscle",
    "cavity": "Cavity",
    "region": "Region",
    "cell": "Cell",
}


class Triple(BaseModel):
    """Validated anatomical triple."""
    source: str = Field(..., description="Anatomical entity")
    relation: Relation = Field(..., description="Relationship type")
    target: str = Field(..., description="Linked anatomical entity")
    source_type: NodeType = "Other"
    target_type: NodeType = "Other"
    confidence: Optional[float] = None

    @validator("source", "target")
    def not_empty(cls, v):
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
        key = str(v).strip().lower().replace(" ", "")
        if key.capitalize() in NodeType.__args__:
            return key.capitalize()
        if key in NODE_TYPE_ALIASES:
            return NODE_TYPE_ALIASES[key]
        return "Other"


# =========================
# 2️⃣ Gemini Extractor
# =========================
class AnatomyTripletExtractor:
    """Extracts anatomy triples using Gemini or offline simulation."""

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
        """Offline simulation for testing."""
        t = text.lower()
        triples = []
        if "heart" in t:
            triples.extend([
                {"source": "Heart", "relation": "part_of", "target": "Circulatory System", "source_type": "Organ", "target_type": "BodySystem"},
                {"source": "Heart", "relation": "supplied_by", "target": "Coronary Arteries", "source_type": "Organ", "target_type": "Vessel"},
                {"source": "Heart", "relation": "drained_by", "target": "Cardiac Veins", "source_type": "Organ", "target_type": "Vessel"},
                {"source": "Heart", "relation": "innervated_by", "target": "Vagus Nerve", "source_type": "Organ", "target_type": "Nerve"},
                {"source": "Heart", "relation": "located_in", "target": "Thoracic Cavity", "source_type": "Organ", "target_type": "Cavity"},
                {"source": "Heart", "relation": "adjacent_to", "target": "Lungs", "source_type": "Organ", "target_type": "Organ"},
                {"source": "Rib Cage", "relation": "protects", "target": "Heart", "source_type": "Bone", "target_type": "Organ"},
                {"source": "Diaphragm", "relation": "supports", "target": "Heart", "source_type": "Muscle", "target_type": "Organ"},
            ])
        return triples


# =========================
# 3️⃣ Graph Builder
# =========================
class AnatomyGraphBuilder:
    """Builds and queries the anatomy knowledge graph."""

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_part_of(self, organ: str):
        """Find the system or region an organ belongs to."""
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == organ.lower() and d.get("relation") == "part_of"
        ]

    def query_connections(self, organ: str):
        """Find adjacent or connected organs."""
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == organ.lower() and d.get("relation") in ["connected_to", "adjacent_to"]
        ]

    def export_json(self, path: str = "anatomy_graph.json"):
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
    """Visualizes the anatomy knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Organ": "#8dd3c7",
            "BodySystem": "#80b1d3",
            "Vessel": "#bebada",
            "Nerve": "#fb8072",
            "Bone": "#fdb462",
            "Muscle": "#b3de69",
            "Cavity": "#bc80bd",
            "Region": "#fccde5",
            "Tissue": "#ffffb3",
            "Cell": "#ccebc5",
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
