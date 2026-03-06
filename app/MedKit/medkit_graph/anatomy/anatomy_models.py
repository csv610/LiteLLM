from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
import anatomy_prompts as prompts

try:
    from lite import LiteClient
    from lite.config import ModelConfig, ModelInput
except ImportError:
    LiteClient = None
    ModelConfig = None
    ModelInput = None

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
    "common_disease",
    "rare_disease",
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
    "Disease",
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
    "has_common_disease": "common_disease",
    "has_rare_disease": "rare_disease",
    "common_disease": "common_disease",
    "rare_disease": "rare_disease",
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


class TripleList(BaseModel):
    """Container for a list of triples."""
    triples: List[Triple]


# =========================
# 2️⃣ Anatomy Extractor
# =========================
class AnatomyTripletExtractor:
    """Extracts anatomy triples using LiteClient or offline simulation."""

    def __init__(self, model_name: str = "gemini-2.0-flash"):
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
                user_prompt=prompts.PROMPT.format(text=text),
                system_prompt="You are an anatomy expert extractor.",
                response_format=TripleList
            )
            return self._call_client(model_input, text)

        return [Triple(**item) for item in self._simulate(text)]

    def generate_from_name(self, anatomy_name: str) -> List[Triple]:
        """Directly generates anatomical triples for a given name using LLM."""
        if self.client is not None:
            model_input = ModelInput(
                user_prompt=prompts.GENERATION_PROMPT.format(anatomy_name=anatomy_name),
                system_prompt="You are an anatomy expert.",
                response_format=TripleList
            )
            return self._call_client(model_input, anatomy_name)
        
        return [Triple(**item) for item in self._simulate(anatomy_name)]

    def _call_client(self, model_input: "ModelInput", fallback_text: str) -> List[Triple]:
        try:
            response = self.client.generate_text(model_input=model_input)
            if isinstance(response, TripleList):
                return response.triples
            elif isinstance(response, str):
                data = json.loads(response)
                if isinstance(data, list):
                    return [Triple(**item) for item in data]
                elif isinstance(data, dict) and "triples" in data:
                    return [Triple(**item) for item in data["triples"]]
        except Exception as e:
            print(f"⚠️ LLM call failed: {e}. Falling back to simulation.")
        
        return [Triple(**item) for item in self._simulate(fallback_text)]

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
                {"source": "Heart", "relation": "common_disease", "target": "Coronary Artery Disease", "source_type": "Organ", "target_type": "Disease"},
                {"source": "Heart", "relation": "rare_disease", "target": "Cardiac Amyloidosis", "source_type": "Organ", "target_type": "Disease"},
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

    def export_dot(self, anatomy: str):
        """Export the graph as a DOT file for Graphviz."""
        os.makedirs("outputs", exist_ok=True)
        path = f"outputs/{anatomy.lower().replace(' ', '_')}.dot"
        
        lines = ["digraph G {", '  node [style=filled, fontname="Arial"];']
        
        # Add nodes with colors
        color_map = {
            "Organ": "#8dd3c7", "BodySystem": "#80b1d3", "Vessel": "#bebada",
            "Nerve": "#fb8072", "Bone": "#fdb462", "Muscle": "#b3de69",
            "Cavity": "#bc80bd", "Region": "#fccde5", "Tissue": "#ffffb3",
            "Cell": "#ccebc5", "Disease": "#ffed6f", "Other": "#d9d9d9",
        }
        
        for n, d in self.G.nodes(data=True):
            node_type = d.get("type", "Other")
            color = color_map.get(node_type, "#d9d9d9")
            lines.append(f'  "{n}" [fillcolor="{color}", label="{n}\n({node_type})"];')
            
        # Add edges
        for u, v, d in self.G.edges(data=True):
            rel = d.get("relation", "other")
            lines.append(f'  "{u}" -> "{v}" [label="{rel}"];')
            
        lines.append("}")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ Graph exported to {path}")

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
            "Disease": "#ffed6f",
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
