# =========================
# Imports
# =========================
from typing import List, Literal, Optional, Any
from pydantic import BaseModel, Field, validator
import networkx as nx
import json
import os
import surgery_prompts as prompts

try:
    from lite.lite_client import LiteClient
    from lite.config import ModelConfig, ModelInput
except ImportError:
    LiteClient = None
    ModelConfig = None
    ModelInput = None


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

class TripleList(BaseModel):
    triples: List[Triple]

# =========================
# 2️⃣ LiteClient Surgery Extractor
# =========================
class SurgeryTripletExtractor:
    """Extracts structured triples from unstructured surgical text using LiteClient."""

    def __init__(self, model_name: str = "gemini/gemini-2.0-flash"):
        self.model_name = model_name
        self.client = None

        if LiteClient is not None:
            config = ModelConfig(model=self.model_name)
            self.client = LiteClient(model_config=config)
        else:
            print("⚠️ LiteClient not found. Using offline mode.")

    def build_prompt(self, text: str) -> str:
        return prompts.PROMPT.format(text=text)

    def extract(self, text: str) -> List[Triple]:
        if self.client is not None:
            model_input = ModelInput(
                user_prompt=self.build_prompt(text),
                response_format=TripleList
            )
            try:
                response: TripleList = self.client.generate_text(model_input)
                return response.triples
            except Exception as e:
                print(f"❌ Extraction failed: {e}. Falling back to simulation.")
                return [Triple(**item) for item in self._simulate(text)]
        else:
            return [Triple(**item) for item in self._simulate(text)]

    def _simulate(self, text: str):
        """Offline mock extractor for testing."""
        t = text.lower()
        triples = []
        if "bypass surgery" in t or "cabg" in t:
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

    def export_dot(self, surgery_name: str, output_dir: str = "outputs"):
        """Exports the graph to a .dot file in the specified directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        safe_name = surgery_name.replace(" ", "_").lower()
        path = os.path.join(output_dir, f"{safe_name}.dot")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'digraph "{surgery_name}" {{\n')
            f.write('    rankdir=LR;\n')
            f.write('    node [shape=box, style=filled, color=lightblue];\n')
            for u, v, d in self.G.edges(data=True):
                relation = d.get("relation", "related_to")
                f.write(f'    "{u}" -> "{v}" [label="{relation}"];\n')
            f.write("}\n")
        print(f"✅ Graph exported to {path}")
