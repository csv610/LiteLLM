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
# 1️⃣ Define Schema with Pydantic
# =========================

# Relation (edge) types
Relation = Literal[
    "associated_with_disease",
    "affects_body_part",
    "caused_by_condition",
    "indicates_disease",
    "diagnosed_by_test",
    "treated_with_drug",
    "treated_with_procedure",
    "has_severity",
    "has_duration",
    "co_occurs_with",
    "risk_factor_for",
    "other",
]

# Node (entity) types
NodeType = Literal[
    "Symptom",
    "Disease",
    "Condition",
    "BodyPart",
    "BodySystem",
    "Test",
    "Drug",
    "Procedure",
    "Severity",
    "Duration",
    "RiskFactor",
    "Other",
]

# Normalization dictionaries
RELATION_ALIASES = {
    "associated": "associated_with_disease",
    "caused_by": "caused_by_condition",
    "indicates": "indicates_disease",
    "affects": "affects_body_part",
    "diagnosed_by": "diagnosed_by_test",
    "treated_by": "treated_with_drug",
    "treated_with": "treated_with_drug",
    "treated_with_procedure": "treated_with_procedure",
    "severity": "has_severity",
    "duration": "has_duration",
    "co_occurs": "co_occurs_with",
    "risk_factor": "risk_factor_for",
}

NODE_TYPE_ALIASES = {
    "symptom": "Symptom",
    "sign": "Symptom",
    "disease": "Disease",
    "condition": "Condition",
    "bodypart": "BodyPart",
    "organ": "BodyPart",
    "system": "BodySystem",
    "test": "Test",
    "investigation": "Test",
    "drug": "Drug",
    "medicine": "Drug",
    "procedure": "Procedure",
    "severity": "Severity",
    "duration": "Duration",
    "riskfactor": "RiskFactor",
}


class Triple(BaseModel):
    """Validated knowledge triple for medical symptoms."""
    source: str = Field(..., description="Subject entity (e.g. Symptom)")
    relation: Relation = Field(..., description="Relation type")
    target: str = Field(..., description="Object entity (e.g. Disease)")
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
# 2️⃣ LLM Extractor (Gemini or Offline)
# =========================
class SymptomTripletExtractor:
    """Extracts symptom knowledge triples using Gemini."""

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
        """Offline fallback for testing."""
        t = text.lower()
        triples = []
        if "fever" in t:
            triples.extend([
                {"source": "Fever", "relation": "associated_with_disease", "target": "Infection", "source_type": "Symptom", "target_type": "Disease"},
                {"source": "Fever", "relation": "indicates_disease", "target": "Malaria", "source_type": "Symptom", "target_type": "Disease"},
                {"source": "Fever", "relation": "affects_body_part", "target": "Whole Body", "source_type": "Symptom", "target_type": "BodyPart"},
                {"source": "Fever", "relation": "has_severity", "target": "Mild to High", "source_type": "Symptom", "target_type": "Severity"},
                {"source": "Fever", "relation": "has_duration", "target": "Few hours to several days", "source_type": "Symptom", "target_type": "Duration"},
                {"source": "Fever", "relation": "diagnosed_by_test", "target": "Blood Test", "source_type": "Symptom", "target_type": "Test"},
                {"source": "Fever", "relation": "treated_with_drug", "target": "Paracetamol", "source_type": "Symptom", "target_type": "Drug"},
                {"source": "Fever", "relation": "risk_factor_for", "target": "Dehydration", "source_type": "Symptom", "target_type": "RiskFactor"},
            ])
        return triples


# =========================
# 3️⃣ Graph Builder
# =========================
class SymptomGraphBuilder:
    """Builds and queries the symptom knowledge graph."""

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_diseases(self, symptom: str):
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == symptom.lower() and d.get("relation") in ["associated_with_disease", "indicates_disease"]
        ]

    def query_treatments(self, symptom: str):
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == symptom.lower() and d.get("relation") in ["treated_with_drug", "treated_with_procedure"]
        ]

    def export_json(self, path: str = "symptom_graph.json"):
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
    """Visualizes the symptom knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Symptom": "#8dd3c7",
            "Disease": "#fb8072",
            "BodyPart": "#bebada",
            "Test": "#80b1d3",
            "Drug": "#b3de69",
            "Procedure": "#fdb462",
            "Severity": "#fccde5",
            "Duration": "#bc80bd",
            "RiskFactor": "#ffffb3",
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
