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

Relation = Literal[
    "encodes",
    "mutated_in",
    "associated_with",
    "expresses",
    "involved_in",
    "regulates",
    "interacts_with",
    "participates_in",
    "upregulates",
    "downregulates",
    "linked_to",
    "causes",
    "contributes_to",
    "part_of",
    "pathogenic_in",
    "protective_in",
    "other",
]

NodeType = Literal[
    "Gene",
    "Protein",
    "Variant",
    "Disease",
    "Pathway",
    "Mechanism",
    "Cell",
    "Organ",
    "Trait",
    "Molecule",
    "Other",
]

RELATION_ALIASES = {
    "codes_for": "encodes",
    "encoded_in": "encodes",
    "mutated": "mutated_in",
    "mutation_in": "mutated_in",
    "linked": "linked_to",
    "connected_to": "linked_to",
    "associated": "associated_with",
    "participates": "participates_in",
    "involved": "involved_in",
    "causes": "causes",
    "leads_to": "causes",
    "affects": "regulates",
    "interacts": "interacts_with",
}

NODE_TYPE_ALIASES = {
    "gene": "Gene",
    "protein": "Protein",
    "variant": "Variant",
    "mutation": "Variant",
    "disease": "Disease",
    "pathway": "Pathway",
    "mechanism": "Mechanism",
    "trait": "Trait",
    "cell": "Cell",
    "organ": "Organ",
    "molecule": "Molecule",
}


class Triple(BaseModel):
    source: str
    relation: Relation
    target: str
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
# 2️⃣ LLM Triplet Extractor
# =========================
class GeneticsTripletExtractor:
    """Extracts genetic and molecular relationships using Gemini or offline simulation."""

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
        """Offline fallback."""
        t = text.lower()
        triples = []
        if "brca1" in t:
            triples.extend([
                {"source": "BRCA1", "relation": "encodes", "target": "BRCA1 Protein", "source_type": "Gene", "target_type": "Protein"},
                {"source": "BRCA1", "relation": "mutated_in", "target": "Breast Cancer", "source_type": "Gene", "target_type": "Disease"},
                {"source": "BRCA1 Protein", "relation": "involved_in", "target": "DNA Repair Pathway", "source_type": "Protein", "target_type": "Pathway"},
                {"source": "BRCA1", "relation": "associated_with", "target": "Ovarian Cancer", "source_type": "Gene", "target_type": "Disease"},
                {"source": "BRCA1 Variant", "relation": "pathogenic_in", "target": "Hereditary Breast Cancer", "source_type": "Variant", "target_type": "Disease"},
            ])
        return triples


# =========================
# 3️⃣ Graph Builder
# =========================
class GeneticsGraphBuilder:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def find_disease_genes(self, disease: str):
        """Return all genes linked to a disease."""
        return [
            src for src, tgt, d in self.G.edges(data=True)
            if tgt.lower() == disease.lower() and self.G.nodes[src].get("type") == "Gene"
        ]

    def find_gene_pathways(self, gene: str):
        """Return pathways involving a gene."""
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == gene.lower() and d.get("relation") in ["involved_in", "participates_in"]
        ]

    def export_json(self, path="genetics_graph.json"):
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
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Gene": "#8dd3c7",
            "Protein": "#bebada",
            "Variant": "#fdb462",
            "Disease": "#fb8072",
            "Pathway": "#80b1d3",
            "Mechanism": "#b3de69",
            "Trait": "#fccde5",
            "Molecule": "#bc80bd",
            "Cell": "#ccebc5",
            "Organ": "#ffffb3",
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
