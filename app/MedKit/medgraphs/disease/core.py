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


# ---- Canonical edge (relation) types ----
Relation = Literal[
    "has_symptom",
    "caused_by",
    "risk_factor",
    "treated_by",
    "diagnosed_by",
    "leads_to",
    "associated_with",
    "prevented_by",
    "affects_system",
    "other",
]

# ---- Node (entity) types ----
NodeType = Literal[
    "Disease",
    "Symptom",
    "Cause",
    "RiskFactor",
    "Treatment",
    "Drug",
    "Test",
    "BodySystem",
    "Complication",
    "Prevention",
    "Condition",
    "Other",
]

# ---- Aliases for normalization ----
RELATION_ALIASES = {
    "symptom": "has_symptom",
    "shows": "has_symptom",
    "results_from": "caused_by",
    "caused": "caused_by",
    "risk": "risk_factor",
    "factor": "risk_factor",
    "treatment": "treated_by",
    "treated_with": "treated_by",
    "managed_by": "treated_by",
    "diagnosis": "diagnosed_by",
    "diagnosed_with": "diagnosed_by",
    "lead_to": "leads_to",
    "complication": "leads_to",
    "associated": "associated_with",
    "prevented_with": "prevented_by",
    "affects": "affects_system",
}

NODE_TYPE_ALIASES = {
    "disease": "Disease",
    "condition": "Condition",
    "symptom": "Symptom",
    "sign": "Symptom",
    "cause": "Cause",
    "factor": "RiskFactor",
    "risk": "RiskFactor",
    "treatment": "Treatment",
    "therapy": "Treatment",
    "drug": "Drug",
    "medicine": "Drug",
    "test": "Test",
    "examination": "Test",
    "system": "BodySystem",
    "complication": "Complication",
    "prevention": "Prevention",
}


class Triple(BaseModel):
    """Represents one disease knowledge triple."""
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
# 2️⃣ Gemini Disease Extractor
# =========================
class DiseaseTripletExtractor:
    """Uses Gemini (or fallback) to extract structured disease knowledge triples."""

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
        """Offline example for demonstration."""
        t = text.lower()
        triples = []
        if "diabetes" in t:
            triples.extend([
                {"source": "Diabetes Mellitus", "relation": "has_symptom", "target": "Increased thirst", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Diabetes Mellitus", "relation": "has_symptom", "target": "Frequent urination", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Diabetes Mellitus", "relation": "risk_factor", "target": "Obesity", "source_type": "Disease", "target_type": "RiskFactor"},
                {"source": "Diabetes Mellitus", "relation": "treated_by", "target": "Insulin", "source_type": "Disease", "target_type": "Drug"},
                {"source": "Diabetes Mellitus", "relation": "diagnosed_by", "target": "Blood sugar test", "source_type": "Disease", "target_type": "Test"},
                {"source": "Diabetes Mellitus", "relation": "leads_to", "target": "Kidney failure", "source_type": "Disease", "target_type": "Complication"},
            ])
        return triples


# =========================
# 3️⃣ Disease Graph Builder
# =========================
class DiseaseGraphBuilder:
    """Builds an in-memory disease knowledge graph."""

    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_symptoms(self, disease: str):
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == disease.lower() and d.get("relation") == "has_symptom"
        ]

    def query_treatments(self, disease: str):
        return [
            tgt for src, tgt, d in self.G.edges(data=True)
            if src.lower() == disease.lower() and d.get("relation") == "treated_by"
        ]

    def export_json(self, path: str = "disease_graph.json"):
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
    """Visualizes the disease knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Disease": "#fb8072",
            "Symptom": "#ffffb3",
            "RiskFactor": "#8dd3c7",
            "Drug": "#80b1d3",
            "Test": "#bebada",
            "Complication": "#fdb462",
            "Other": "#b3de69",
        }

        node_colors = [
            color_map.get(self.G.nodes[n].get("type", "Other"), "#b3de69")
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
