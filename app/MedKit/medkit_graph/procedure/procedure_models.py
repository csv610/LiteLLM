# =========================
# Imports
# =========================
import json
import os
from typing import List, Literal, Optional

import matplotlib.pyplot as plt
import networkx as nx
import procedure_prompts as prompts
from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from pydantic import BaseModel, Field, field_validator

# =========================
# 1️⃣ Pydantic Models
# =========================

# ---- Canonical edge (relation) types ----
Relation = Literal[
    "treats_disease",
    "used_for_diagnosis",
    "performed_on",
    "requires_instrument",
    "performed_by_specialist",
    "has_risk",
    "has_benefit",
    "has_complication",
    "has_contraindication",
    "requires_anesthesia",
    "requires_preparation",
    "follow_up_by",
    "related_to_procedure",
    "other",
]

# ---- Node (entity) types ----
NodeType = Literal[
    "Procedure",
    "Disease",
    "Organ",
    "BodySystem",
    "Instrument",
    "Specialist",
    "Risk",
    "Benefit",
    "Complication",
    "AnesthesiaType",
    "Preparation",
    "FollowUp",
    "Condition",
    "Contraindication",
    "Other",
]

# ---- Normalization dictionaries ----
RELATION_ALIASES = {
    "treats": "treats_disease",
    "used_for": "used_for_diagnosis",
    "diagnose": "used_for_diagnosis",
    "performed": "performed_on",
    "needs_instrument": "requires_instrument",
    "instrument": "requires_instrument",
    "specialist": "performed_by_specialist",
    "risk": "has_risk",
    "benefit": "has_benefit",
    "complication": "has_complication",
    "anesthesia": "requires_anesthesia",
    "preparation": "requires_preparation",
    "follow_up": "follow_up_by",
    "related": "related_to_procedure",
    "contraindication": "has_contraindication",
}

NODE_TYPE_ALIASES = {
    "procedure": "Procedure",
    "surgery": "Procedure",
    "operation": "Procedure",
    "test": "Procedure",
    "disease": "Disease",
    "condition": "Condition",
    "organ": "Organ",
    "system": "BodySystem",
    "instrument": "Instrument",
    "device": "Instrument",
    "implant": "Instrument",
    "surgeon": "Specialist",
    "doctor": "Specialist",
    "risk": "Risk",
    "benefit": "Benefit",
    "complication": "Complication",
    "anesthesia": "AnesthesiaType",
    "anesthesia_type": "AnesthesiaType",
    "preparation": "Preparation",
    "follow_up": "FollowUp",
    "contraindication": "Contraindication",
}


class Triple(BaseModel):
    """Represents one validated medical procedure relation."""

    source: str = Field(..., description="Subject entity")
    relation: Relation = Field(..., description="Relation type")
    target: str = Field(..., description="Object entity")
    source_type: NodeType = "Other"
    target_type: NodeType = "Other"
    confidence: Optional[float] = None

    @field_validator("source", "target")
    @classmethod
    def not_empty_entity(cls, v):
        if not v or not v.strip():
            raise ValueError("Entity name cannot be empty")
        return v.strip()

    @field_validator("relation", mode="before")
    @classmethod
    def normalize_relation(cls, v):
        if not v:
            return "other"
        rv = str(v).strip().lower().replace(" ", "_")
        if rv in RELATION_ALIASES:
            rv = RELATION_ALIASES[rv]

        # Case-insensitive match for Relation literal
        allowed = {t.lower(): t for t in Relation.__args__}
        if rv in allowed:
            return allowed[rv]
        return "other"

    @field_validator("source_type", "target_type", mode="before")
    @classmethod
    def normalize_node_type(cls, v):
        if not v:
            return "Other"

        val = str(v).strip()

        # 1. Clean key for alias lookup
        alias_key = val.lower().replace(" ", "_")
        if alias_key in NODE_TYPE_ALIASES:
            return NODE_TYPE_ALIASES[alias_key]

        # 2. Case-insensitive and space-insensitive match for NodeType literal
        allowed_types = {t.lower().replace("_", ""): t for t in NodeType.__args__}
        key = val.lower().replace(" ", "").replace("_", "")

        if key in allowed_types:
            return allowed_types[key]

        return "Other"


class TripleList(BaseModel):
    triples: List[Triple]


# =========================
# 3️⃣ Procedure Graph Builders
# =========================


class BaseProcedureGraphBuilder:
    """Base class for building medical procedure graphs."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.G = nx.MultiDiGraph()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(
                t.source, t.target, relation=t.relation, confidence=t.confidence
            )

    def query_treats(self, disease: str):
        return [
            src
            for src, tgt, d in self.G.edges(data=True)
            if tgt.lower() == disease.lower() and d.get("relation") == "treats_disease"
        ]

    def export_json(self, path: str = "procedure_graph.json"):
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
        """Exports the graph to a DOT file."""
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(
            path
        ) else None
        with open(path, "w", encoding="utf-8") as f:
            f.write("digraph G {\n")
            f.write('  node [shape=box, style=filled, fontname="Arial"];\n')

            # Add nodes with colors
            color_map = {
                "Procedure": "#80b1d3",
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

            for node, data in self.G.nodes(data=True):
                ntype = data.get("type", "Other")
                color = color_map.get(ntype, "#d9d9d9")
                f.write(
                    f' "{node}" [fillcolor="{color}", label="{node}\\n({ntype})"];\n'
                )

            # Add edges
            for u, v, data in self.G.edges(data=True):
                rel = data.get("relation", "related_to")
                f.write(f' "{u}" -> "{v}" [label="{rel}"];\n')

            f.write("}\n")
        print(f"✅ Graph exported to {path}")


class ProcedureGraphBuilder(BaseProcedureGraphBuilder):
    """Builds the procedure knowledge graph from a procedure name."""

    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)
        self.client = LiteClient(model_config=self.model_config)

    def build(self, procedure_name: str) -> List[Triple]:
        """Builds graph from scratch using LLM based on procedure name."""
        model_input = ModelInput(
            user_prompt=prompts.PromptBuilder.build_name_prompt(procedure_name),
            response_format=TripleList,
        )
        try:
            response: TripleList = self.client.generate_text(model_input)
            triples = response.triples
        except Exception as e:
            print(
                f"⚠️ Graph build failed for '{procedure_name}': {e}. Using offline mode."
            )
            triples = self._simulate_name(procedure_name)

        if triples:
            self.add_triples(triples)
        return triples

    def _simulate_name(self, name: str) -> List[Triple]:
        """Offline fallback for name-based graph building."""
        t = name.lower()
        triples = []
        if "appendectomy" in t:
            triples.extend(
                [
                    Triple(
                        source="Appendectomy",
                        relation="treats_disease",
                        target="Appendicitis",
                        source_type="Procedure",
                        target_type="Disease",
                    ),
                    Triple(
                        source="Appendectomy",
                        relation="performed_on",
                        target="Appendix",
                        source_type="Procedure",
                        target_type="Organ",
                    ),
                    Triple(
                        source="Appendectomy",
                        relation="has_risk",
                        target="Infection",
                        source_type="Procedure",
                        target_type="Risk",
                    ),
                    Triple(
                        source="Appendectomy",
                        relation="requires_instrument",
                        target="Scalpel",
                        source_type="Procedure",
                        target_type="Instrument",
                    ),
                    Triple(
                        source="Appendectomy",
                        relation="performed_by_specialist",
                        target="Surgeon",
                        source_type="Procedure",
                        target_type="Specialist",
                    ),
                ]
            )
        elif "colonoscopy" in t:
            triples.extend(
                [
                    Triple(
                        source="Colonoscopy",
                        relation="used_for_diagnosis",
                        target="Colon Cancer",
                        source_type="Procedure",
                        target_type="Disease",
                    ),
                    Triple(
                        source="Colonoscopy",
                        relation="performed_on",
                        target="Colon",
                        source_type="Procedure",
                        target_type="Organ",
                    ),
                    Triple(
                        source="Colonoscopy",
                        relation="requires_instrument",
                        target="Colonoscope",
                        source_type="Procedure",
                        target_type="Instrument",
                    ),
                    Triple(
                        source="Colonoscopy",
                        relation="has_risk",
                        target="Perforation",
                        source_type="Procedure",
                        target_type="Risk",
                    ),
                    Triple(
                        source="Colonoscopy",
                        relation="performed_by_specialist",
                        target="Gastroenterologist",
                        source_type="Procedure",
                        target_type="Specialist",
                    ),
                ]
            )
        return triples


# =========================
# 4️⃣ Visualization
# =========================
class GraphVisualizer:
    """Visualizes the procedure knowledge graph."""

    def __init__(self, graph: nx.MultiDiGraph):
        self.G = graph

    def show(self, figsize=(10, 8)):
        plt.figure(figsize=figsize)
        pos = nx.spring_layout(self.G, k=0.6, iterations=40)
        edge_labels = nx.get_edge_attributes(self.G, "relation")

        color_map = {
            "Procedure": "#80b1d3",
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
