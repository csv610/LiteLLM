Armacology Knowledge Graph Builder
------------------------------------
Builds a structured graph of pharmacological relationships:
Drugs, targets, receptors, enzymes, pathways, and mechanisms.

Author: ChatGPT (for Chaman Singh Verma)
"""

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
# 1️⃣ Define Schema
# =========================

# Relation (edge) types
Relation = Literal[
    "binds_to",
    "inhibits",
    "activates",
    "modulates",
    "metabolized_by",
    "eliminated_by",
    "converted_to",
    "targets_receptor",
    "affects_pathway",
    "induces_enzyme",
    "inhibits_enzyme",
    "upregulates",
    "downregulates",
    "causes_effect",
    "other",
]

# Node (entity) types
NodeType = Literal[
    "Drug",
    "Target",
    "Receptor",
    "Enzyme",
    "Transporter",
    "Pathway",
    "Metabolite",
    "Mechanism",
    "Effect",
    "BodySystem",
    "Organ",
    "Other",
]

RELATION_ALIASES = {
    "acts_on": "binds_to",
    "binds": "binds_to",
    "stimulates": "activates",
    "blocks": "inhibits",
    "inhibitor_of": "inhibits",
    "activator_of": "activates",
    "modulator": "modulates",
    "metabolized": "metabolized_by",
    "eliminated": "eliminated_by",
    "induces": "induces_enzyme",
    "inhibits_enzyme": "inhibits_enzyme",
    "affects": "affects_pathway",
    "targets": "targets_receptor",
    "causes": "causes_effect",
}

NODE_TYPE_ALIASES = {
    "drug": "Drug",
    "compound": "Drug",
    "target": "Target",
    "receptor": "Receptor",
    "enzyme": "Enzyme",
    "pathway": "Pathway",
    "metabolite": "Metabolite",
    "mechanism": "Mechanism",
    "effect": "Effect",
    "organ": "Organ",
    "system": "BodySystem",
    "transporter": "Transporter",
}


class Triple(BaseModel):
    """Validated pharmacology triple."""
    source: str = Field(..., description="Pharmacological entity")
    relation: Relation = Field(..., description="Relationship type")
    target: str = Field(..., description="Linked entity")
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
# 2️⃣ LLM Extractor (Gemini / Offline)
# =========================
class PharmacologyTripletExtractor:
    """Extracts pharmacology triples using Gemini or offline fallback."""

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
Extract pharmacological relationships as JSON triples.
Each triple must include:
  - source
  - relation (choose from: binds_to, inhibits, activates, modulates, metabolized_by,
    eliminated_by, converted_to, targets_receptor, affects_pathway, induces_enzyme,
    inhibits_enzyme, upregulates, downregulates, causes_effect, other)
  - target
Optional: source_type, target_type, confidence
Return a JSON array only.

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
        """Offline simulation."""
        t = text.lower()
        triples = []
        if "paracetamol" in t:
            triples.extend([
                {"source": "Paracetamol", "relation": "inhibits", "target": "Cyclooxygenase Enzyme", "source_type": "Drug", "target_type": "Enzyme"},
                {"source": "Paracetamol", "relation": "causes_effect", "target": "Pain Relief", "source_type": "Drug", "target_type": "Effect"},
                {"source": "Paracetamol", "relation": "causes_effect", "target": "Fever Reduction", "source_type": "Drug", "target_type": "Effect"},
                {"source": "Paracetamol", "relation": "metabolized_by", "target": "Liver", "source_type": "Drug", "target_type": "Organ"},
                {"source": "Paracetamol", "relation": "affects_pathway", "target": "Prostaglandin Synthesis", "source_type": "Drug", "target_type": "Pathway"},
                {"source": "Paracetamol", "relation": "eliminated_by", "target": "Kidney", "source_type": "Drug", "target_type": "Organ"},
            ])
        return triples


# =========================
# 3️⃣ Graph Builder
# =========================
class PharmacologyGraphBuilder:
    """Builds and queries the pharmacology knowledge graph."""

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_targets(self, drug: str):
        """Find biological targets of a drug."""
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == drug.lower() and d.get("relation") in ["binds_to", "inhibits", "activates"]
        ]

    def query_effects(self, drug: str):
        """Find effects caused by a drug."""
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == drug.lower() and d.get("relation") == "causes_effect"
        ]

    def export_json(self, path: str = "pharmacology_graph.json"):
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
    """Visualizes the pharmacology knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Drug": "#8dd3c7",
            "Target": "#bebada",
            "Receptor": "#80b1d3",
            "Enzyme": "#b3de69",
            "Pathway": "#fccde5",
            "Metabolite": "#fdb462",
            "Mechanism": "#bc80bd",
            "Effect": "#fb8072",
            "Organ": "#ffffb3",
            "BodySystem": "#ccebc5",
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


# =========================
# 5️⃣ Runner
# =========================
if __name__ == "__main__":
    text = """
    Paracetamol is an analgesic and antipyretic drug.
    It inhibits the cyclooxygenase enzyme, reducing prostaglandin synthesis.
    This leads to pain relief and fever reduction.
    Paracetamol is metabolized by the liver and eliminated through the kidneys.
    """

    extractor = PharmacologyTripletExtractor()  # Uses GEMINI_API_KEY from environment
    triples = extractor.extract(text)

    print("✅ Extracted Pharmacology Triples:")
    for t in triples:
        print(t.dict())

    builder = PharmacologyGraphBuilder()
    builder.add_triples(triples)

    print("🔹 Targets of Paracetamol:", builder.query_targets("Paracetamol"))
    print("🔹 Effects of Paracetamol:", builder.query_effects("Paracetamol"))

    builder.export_json("pharmacology_graph.json")

    visualizer = GraphVisualizer(builder.G)
    visualizer.show()
xilla Examination 

