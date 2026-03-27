import os
from typing import List, Literal, Optional

import matplotlib.pyplot as plt
import networkx as nx
from pydantic import BaseModel, Field, field_validator

try:
    from . import anatomy_prompts as prompts
except ImportError:
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
    "derived_from",
    "other",
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
    "originated_from": "derived_from",
    "embryological_origin": "derived_from",
}


class Triple(BaseModel):
    """Validated anatomical triple with clinical context."""

    source: str = Field(..., description="Anatomical entity", alias="subject")
    relation: Relation = Field(..., description="Relationship type", alias="predicate")
    target: str = Field(..., description="Linked anatomical entity", alias="object")
    evidence: Optional[str] = Field(
        None, description="Brief medical justification or reference"
    )

    class Config:
        populate_by_name = True

    @field_validator("source", "target")
    @classmethod
    def not_empty(cls, v):
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
        allowed = set(Relation.__args__)
        return rv if rv in allowed else "other"


class AnatomyReport(BaseModel):
    """Full structured anatomical report."""

    name: str = Field(..., description="Name of the anatomy")
    system: str = Field(..., description="Primary body system")
    description: str = Field(..., description="High-level medical description")
    triples: List[Triple] = Field(..., description="List of anatomical triples")


# =========================
# 2️⃣ Graph Builder
# =========================
class AnatomyKnowledgeGraph:
    """Builds and queries the anatomy knowledge graph using LLM."""

    def __init__(self, model_config: Optional["ModelConfig"] = None):
        self.G = nx.MultiDiGraph()
        self.model_config = model_config
        self.client = None
        self.last_report = None

        if LiteClient is not None:
            if self.model_config is None:
                self.model_config = ModelConfig(
                    model="ollama_chat/gemma3:27b-cloud", temperature=0.0
                )
            self.client = LiteClient(model_config=self.model_config)
        else:
            print("⚠️ 'lite' package not installed. Using offline mode.")

    def build_from_name(self, anatomy_name: str):
        """Generates a structured anatomical report and builds the graph."""
        if not self.client:
            raise RuntimeError("LLM client not initialized.")

        model_input = ModelInput(
            user_prompt=prompts.GENERATION_USER_PROMPT.format(
                anatomy_name=anatomy_name
            ),
            system_prompt=prompts.GENERATION_SYSTEM_PROMPT,
            response_format=AnatomyReport,
        )
        report = self._ask_llm(model_input)

        self.last_report = report
        self.add_triples(report.triples)
        return report.triples

    def _ask_llm(self, model_input: "ModelInput") -> AnatomyReport:
        # Rely on LiteClient's native Pydantic validation
        return self.client.generate_text(model_input=model_input)

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source)
            self.G.add_node(t.target)
            self.G.add_edge(t.source, t.target, relation=t.relation)

    def query_part_of(self, organ: str):
        """Find the system or region an organ belongs to."""
        return [
            tgt
            for src, tgt, d in self.G.edges(data=True)
            if src.lower() == organ.lower() and d.get("relation") == "part_of"
        ]

    def query_connections(self, organ: str):
        """Find adjacent or connected organs."""
        return [
            tgt
            for src, tgt, d in self.G.edges(data=True)
            if src.lower() == organ.lower()
            and d.get("relation") in ["connected_to", "adjacent_to"]
        ]

    def export_dot(self, anatomy: str):
        """Export the graph as a DOT file for Graphviz."""
        os.makedirs("outputs", exist_ok=True)
        path = f"outputs/{anatomy.lower().replace(' ', '_')}.dot"

        lines = [
            "digraph G {",
            '  node [style=filled, fontname="Arial", fillcolor="#d9d9d9"];',
        ]

        # Add nodes
        for n in self.G.nodes():
            lines.append(f'  "{n}" [label="{n}"];')

        # Add edges
        for u, v, d in self.G.edges(data=True):
            rel = d.get("relation", "other")
            lines.append(f'  "{u}" -> "{v}" [label="{rel}"];')

        lines.append("}")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"✅ Graph exported to {path}")

    def export_json(self, path: str = "anatomy_graph.json"):
        """Export the full report including metadata and triples to JSON."""
        if not self.last_report:
            print("⚠️ No report to export.")
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.last_report.model_dump_json(indent=2))

        print(f"✅ Full report exported to {path}")


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

        nx.draw(
            self.G,
            pos,
            with_labels=True,
            node_color="#d9d9d9",
            node_size=2200,
            font_size=9,
            font_weight="bold",
            arrows=True,
        )
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        plt.show()
