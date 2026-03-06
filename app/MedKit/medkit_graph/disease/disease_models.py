from typing import List, Literal, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, field_validator
import json
import os
import sys

# Add lite package path
lite_path = "/Users/csv610/Projects/LiteLLM/lite"
if lite_path not in sys.path:
    sys.path.append(lite_path)

try:
    import disease_prompts as prompts
except ImportError:
    from . import disease_prompts as prompts

try:
    from lite import LiteClient
    from lite.config import ModelConfig, ModelInput
except ImportError:
    LiteClient = None
    ModelConfig = None
    ModelInput = None


# ---- Canonical edge (relation) types ----
Relation = Literal[
    "has_symptom",
    "caused_by",
    "risk_factor_for",
    "treated_with",
    "diagnosed_by",
    "leads_to",
    "associated_with",
    "prevented_by",
    "affects_system",
    "affects_organ",
    "complication_of",
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
    "Organ",
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
    "risk": "risk_factor_for",
    "risk_factor": "risk_factor_for",
    "factor": "risk_factor_for",
    "treatment": "treated_with",
    "treated_by": "treated_with",
    "managed_by": "treated_with",
    "diagnosis": "diagnosed_by",
    "diagnosed_with": "diagnosed_by",
    "lead_to": "leads_to",
    "complication": "complication_of",
    "associated": "associated_with",
    "prevented_with": "prevented_by",
    "affects": "affects_system",
    "affects_organ": "affects_organ",
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
    "organ": "Organ",
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

    @field_validator("source", "target")
    @classmethod
    def not_empty_entity(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Entity name cannot be empty")
        return v.strip()

    @field_validator("relation", mode="before")
    @classmethod
    def normalize_relation(cls, v: Any) -> str:
        if not v:
            return "other"
        rv = str(v).strip().lower().replace(" ", "_")
        if rv in RELATION_ALIASES:
            rv = RELATION_ALIASES[rv]
        allowed = set(Relation.__args__)
        return rv if rv in allowed else "other"

    @field_validator("source_type", "target_type", mode="before")
    @classmethod
    def normalize_node_type(cls, v: Any) -> str:
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
# 2️⃣ Disease Extractor
# =========================
class DiseaseTripletExtractor:
    """Uses LiteClient to extract structured disease knowledge triples."""

    def __init__(self, model_name: str = "gemini/gemini-2.0-flash"):
        self.model_name = model_name
        self.client = None

        if LiteClient is not None:
            self.client = LiteClient(ModelConfig(model=self.model_name))
        else:
            print("⚠️ lite package not installed. Using offline mode.")

    def build_prompt(self, text: str) -> str:
        return prompts.PROMPT.format(text=text)

    def extract(self, text: str) -> List[Triple]:
        if self.client is not None:
            model_input = ModelInput(
                user_prompt=self.build_prompt(text),
                response_format=TripleList
            )
            try:
                response = self.client.generate_text(model_input)
                if isinstance(response, TripleList):
                    return response.triples
                elif isinstance(response, str):
                    # Fallback if it returns a string
                    data = json.loads(response)
                    if isinstance(data, list):
                        return [Triple(**t) for t in data]
                    elif isinstance(data, dict) and "triples" in data:
                        return [Triple(**t) for t in data["triples"]]
            except Exception as e:
                print(f"⚠️ Error during extraction: {e}")
                return self._simulate_as_triples(text)
        
        return self._simulate_as_triples(text)

    def extract_by_name(self, disease_name: str) -> List[Triple]:
        """Directly generates triples from a disease name."""
        if self.client is not None:
            model_input = ModelInput(
                user_prompt=prompts.DISEASE_NAME_PROMPT.format(disease_name=disease_name),
                response_format=TripleList
            )
            try:
                response = self.client.generate_text(model_input)
                if isinstance(response, TripleList):
                    return response.triples
                elif isinstance(response, str):
                    # Fallback if it returns a string
                    data = json.loads(response)
                    if isinstance(data, list):
                        return [Triple(**t) for t in data]
                    elif isinstance(data, dict) and "triples" in data:
                        return [Triple(**t) for t in data["triples"]]
            except Exception as e:
                print(f"⚠️ Error during generation for '{disease_name}': {e}")
                return self._simulate_as_triples(disease_name)
        
        return self._simulate_as_triples(disease_name)

    def _simulate_as_triples(self, text: str) -> List[Triple]:
        return [Triple(**t) for t in self._simulate(text)]

    def _simulate(self, text: str):
        """Offline example for demonstration."""
        t = text.lower()
        triples = []
        if "diabetes" in t:
            triples.extend([
                {"source": "Diabetes Mellitus", "relation": "has_symptom", "target": "Increased thirst", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Diabetes Mellitus", "relation": "has_symptom", "target": "Frequent urination", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Diabetes Mellitus", "relation": "risk_factor_for", "target": "Obesity", "source_type": "Disease", "target_type": "RiskFactor"},
                {"source": "Diabetes Mellitus", "relation": "treated_with", "target": "Insulin", "source_type": "Disease", "target_type": "Drug"},
                {"source": "Diabetes Mellitus", "relation": "diagnosed_by", "target": "Blood sugar test", "source_type": "Disease", "target_type": "Test"},
                {"source": "Diabetes Mellitus", "relation": "leads_to", "target": "Kidney failure", "source_type": "Disease", "target_type": "Complication"},
                {"source": "Kidney failure", "relation": "complication_of", "target": "Diabetes Mellitus", "source_type": "Complication", "target_type": "Disease"},
                {"source": "Diabetes Mellitus", "relation": "affects_organ", "target": "Pancreas", "source_type": "Disease", "target_type": "Organ"},
            ])
        if "malaria" in t:
             triples.extend([
                {"source": "Malaria", "relation": "has_symptom", "target": "Fever", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Malaria", "relation": "has_symptom", "target": "Chills", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Malaria", "relation": "has_symptom", "target": "Headache", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Malaria", "relation": "has_symptom", "target": "Nausea", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Malaria", "relation": "has_symptom", "target": "Vomiting", "source_type": "Disease", "target_type": "Symptom"},
                {"source": "Malaria", "relation": "caused_by", "target": "Plasmodium parasites", "source_type": "Disease", "target_type": "Cause"},
                {"source": "Malaria", "relation": "caused_by", "target": "Infected female Anopheles mosquitoes", "source_type": "Disease", "target_type": "Cause"},
                {"source": "Malaria", "relation": "treated_with", "target": "Artemisinin-based combination therapy", "source_type": "Disease", "target_type": "Treatment"},
                {"source": "Malaria", "relation": "affects_organ", "target": "Liver", "source_type": "Disease", "target_type": "Organ"},
                {"source": "Malaria", "relation": "affects_organ", "target": "Red blood cells", "source_type": "Disease", "target_type": "Organ"},
                {"source": "Cerebral malaria", "relation": "complication_of", "target": "Malaria", "source_type": "Complication", "target_type": "Disease"},
                {"source": "Standing water", "relation": "risk_factor_for", "target": "Malaria", "source_type": "RiskFactor", "target_type": "Disease"},
            ])
        return triples


# =========================
# 3️⃣ Disease Graph Builder
# =========================
class DiseaseGraphBuilder:
    """Builds an in-memory disease knowledge graph (Simplified without NetworkX)."""

    def __init__(self):
        self.nodes = {} # name -> type
        self.edges = [] # List of dicts

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.nodes[t.source] = t.source_type
            self.nodes[t.target] = t.target_type
            self.edges.append({
                "source": t.source,
                "target": t.target,
                "relation": t.relation,
                "confidence": t.confidence
            })

    def query_symptoms(self, disease: str):
        return [
            e["target"] for e in self.edges
            if e["source"].lower() == disease.lower() and e["relation"] == "has_symptom"
        ]

    def query_treatments(self, disease: str):
        return [
            e["target"] for e in self.edges
            if e["source"].lower() == disease.lower() and e["relation"] == "treated_with"
        ]

    def export_json(self, path: str = "disease_graph.json"):
        triples = [
            {
                "source": e["source"],
                "relation": e["relation"],
                "target": e["target"],
                "source_type": self.nodes.get(e["source"]),
                "target_type": self.nodes.get(e["target"]),
                "confidence": e.get("confidence"),
            }
            for e in self.edges
        ]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(triples, f, indent=2)
        print(f"✅ Graph exported to {path}")

    def export_dot(self, disease_name: str, folder: str = "outputs"):
        """Exports the graph to a DOT file for visualization."""
        os.makedirs(folder, exist_ok=True)
        filename = f"{disease_name.lower().replace(' ', '_')}.dot"
        path = os.path.join(folder, filename)
        
        color_map = {
            "Disease": "#fb8072",
            "Symptom": "#ffffb3",
            "RiskFactor": "#8dd3c7",
            "Treatment": "#bebada",
            "Drug": "#80b1d3",
            "Test": "#bebada",
            "Organ": "#ccebc5",
            "Complication": "#fdb462",
            "Prevention": "#b3de69",
            "Other": "#d9d9d9",
        }

        dot_lines = ["digraph G {", "    rankdir=LR;", "    node [shape=box, style=filled, fontname=\"Arial\"];"]
        
        # Add nodes with colors
        for node, ntype in self.nodes.items():
            color = color_map.get(ntype, "#d9d9d9")
            label = f"{node}\\n({ntype})"
            dot_lines.append(f"    \"{node}\" [fillcolor=\"{color}\", label=\"{label}\"];")
        
        # Add edges
        for e in self.edges:
            dot_lines.append(f"    \"{e['source']}\" -> \"{e['target']}\" [label=\"{e['relation']}\"];")
        
        dot_lines.append("}")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(dot_lines))
        print(f"✅ Graph exported to {path}")


# =========================
# 4️⃣ Visualization
# =========================
class GraphVisualizer:
    """Prints the disease knowledge graph (Simplified without NetworkX/Matplotlib)."""

    def __init__(self, builder: DiseaseGraphBuilder):
        self.builder = builder

    def show(self):
        print("\n--- Disease Knowledge Graph ---")
        for e in self.builder.edges:
            print(f"({e['source']}: {self.builder.nodes.get(e['source'])}) --[{e['relation']}]--> ({e['target']}: {self.builder.nodes.get(e['target'])})")
