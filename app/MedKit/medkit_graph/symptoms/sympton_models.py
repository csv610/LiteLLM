# =========================
# Imports
# =========================
import json
import os
from typing import List, Literal, Optional

import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel, Field, field_validator

try:
    from . import sympton_prompts as prompts
except ImportError:
    import sympton_prompts as prompts

try:
    from google import genai
except ImportError:
    genai = None

try:
    from lite.config import ModelConfig, ModelInput
    from lite.lite_client import LiteClient
except ImportError:
    LiteClient = None
    ModelInput = None
    ModelConfig = None

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

    @field_validator("source", "target")
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Entity cannot be empty")
        return v.strip()

    @field_validator("relation", mode="before")
    @classmethod
    def normalize_relation(cls, v):
        if not v:
            return "other"
        rv = str(v).strip().lower().replace(" ", "_")
        if rv in RELATION_ALIASES:
            rv = RELATION_ALIASES[rv]
        allowed = set(Relation.__args__)
        return rv if rv in allowed else "other"

    @field_validator("source_type", "target_type", mode="before")
    @classmethod
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
    triples: List[Triple]


# =========================
# 2️⃣ LLM Extractor (LiteClient)
# =========================
class SymptomTripletExtractor:
    """Extracts symptom knowledge triples using LiteClient."""

    def __init__(self, model_name: str = "ollama/gemma3"):
        self.model_name = model_name
        self.lite_client = None

        if LiteClient:
            config = ModelConfig(model=model_name)
            self.lite_client = LiteClient(model_config=config)
        else:
            print("⚠️ LiteClient not found. Using offline mode.")

    def build_prompt(self, text: str) -> str:
        return prompts.PROMPT.format(text=text)

    def extract(self, text: str) -> List[Triple]:
        if self.lite_client is not None:
            model_input = ModelInput(
                user_prompt=self.build_prompt(text), response_format=TripleList
            )
            try:
                # Use generate_text which returns the parsed Pydantic model
                response = self.lite_client.generate_text(model_input=model_input)
                if isinstance(response, TripleList):
                    return response.triples
                elif isinstance(response, str):
                    # Fallback if it returns a string
                    raw_list = json.loads(response)
                    # Check if it's a list or a dict with 'triples' key
                    if isinstance(raw_list, dict) and "triples" in raw_list:
                        return [Triple(**item) for item in raw_list["triples"]]
                    return [Triple(**item) for item in raw_list]
            except Exception as e:
                print(f"⚠️ Error during extraction: {e}")
                return self._simulate(text)
        else:
            return self._simulate(text)

    def _simulate(self, text: str):
        """Offline fallback for testing."""
        symptom = "Symptom"
        if "fever" in text.lower():
            symptom = "Fever"
        elif "cough" in text.lower():
            symptom = "Cough"

        triples = [
            Triple(
                source=symptom,
                relation="associated_with_disease",
                target="Common Cold",
                source_type="Symptom",
                target_type="Disease",
            ),
            Triple(
                source=symptom,
                relation="affects_body_part",
                target="Respiratory System",
                source_type="Symptom",
                target_type="BodyPart",
            ),
            Triple(
                source=symptom,
                relation="treated_with_drug",
                target="General Medicine",
                source_type="Symptom",
                target_type="Drug",
            ),
            Triple(
                source=symptom,
                relation="has_severity",
                target="Mild",
                source_type="Symptom",
                target_type="Severity",
            ),
        ]
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
            self.G.add_edge(
                t.source, t.target, relation=t.relation, confidence=t.confidence
            )

    def query_diseases(self, symptom: str):
        return [
            tgt
            for src, tgt, d in self.G.edges(data=True)
            if src.lower() == symptom.lower()
            and d.get("relation") in ["associated_with_disease", "indicates_disease"]
        ]

    def query_treatments(self, symptom: str):
        return [
            tgt
            for src, tgt, d in self.G.edges(data=True)
            if src.lower() == symptom.lower()
            and d.get("relation") in ["treated_with_drug", "treated_with_procedure"]
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
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(
            path
        ) else None
        with open(path, "w", encoding="utf-8") as f:
            json.dump(triples, f, indent=2)
        print(f"✅ Graph exported to {path}")

    def export_dot(self, path: str):
        """Export the graph in DOT format."""
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(
            path
        ) else None
        with open(path, "w", encoding="utf-8") as f:
            f.write("digraph SymptomGraph {\n")
            f.write("  node [shape=box, style=rounded, fontname=Arial];\n")
            for n, d in self.G.nodes(data=True):
                ntype = d.get("type", "Other")
                f.write(f'  "{n}" [label="{n}\\n({ntype})"];\n')
            for u, v, d in self.G.edges(data=True):
                rel = d.get("relation", "other")
                f.write(f'  "{u}" -> "{v}" [label="{rel}"];\n')
            f.write("}\n")
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


class ModelOutput(BaseModel):
    """Standardized artifact envelope for the application."""
    data: Optional[Any] = None      # Tier 1: Specialists Facts (JSON Object)
    markdown: Optional[str] = None  # Tier 3: Final Synthesized Report (Markdown String)
    metadata: Optional[dict] = Field(default_factory=dict) # Tier 2: Process Artifacts (Audit/Reasoning)
