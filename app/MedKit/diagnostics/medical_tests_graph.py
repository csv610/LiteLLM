"""Medical Test Knowledge Graph Builder
------------------------------------
- Extracts medical test triples (subject-relation-object) using Gemini
- Validates using Pydantic
- Builds a NetworkX knowledge graph
- Visualizes using Matplotlib

Author: ChatGPT (for Chaman Singh Verma)
"""

# =========================
# Imports
# =========================
from typing import List, Literal, Optional
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, validator
import networkx as nx
import matplotlib.pyplot as plt
import json
from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.core.gemini_client import ModelInput

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig

# Uncomment in production:
# from google import genai


# =========================
# Type Definitions
# =========================
Relation = Literal[
    "measures",
    "detects",
    "diagnoses",
    "monitors",
    "screen_for",
    "related_to_disease",
    "requires_sample",
    "uses_instrument",
    "evaluates_function_of",
    "ordered_for_symptom",
    "follow_up_of",
    "has_reference_range",
    "other",
]

NodeType = Literal["Test", "Biomarker", "Disease", "SampleType", "Instrument", "Organ", "Other"]

RELATION_ALIASES = {
    "measures": "measures",
    "detects": "detects",
    "diagnoses": "diagnoses",
    "monitors": "monitors",
    "screen": "screen_for",
    "screen_for": "screen_for",
    "related": "related_to_disease",
    "related_to_disease": "related_to_disease",
    "sample": "requires_sample",
    "requires_sample": "requires_sample",
    "instrument": "uses_instrument",
    "uses_instrument": "uses_instrument",
    "evaluates": "evaluates_function_of",
    "evaluates_function_of": "evaluates_function_of",
    "symptom": "ordered_for_symptom",
    "ordered_for_symptom": "ordered_for_symptom",
    "follow_up": "follow_up_of",
    "follow_up_of": "follow_up_of",
    "reference": "has_reference_range",
    "has_reference_range": "has_reference_range",
}

NODE_TYPE_ALIASES = {
    "test": "Test",
    "biomarker": "Biomarker",
    "disease": "Disease",
    "sample": "SampleType",
    "sampletype": "SampleType",
    "instrument": "Instrument",
    "organ": "Organ",
    "other": "Other",
}


# =========================
# Configuration
# =========================
@dataclass
class TestGraphConfig(MedKitConfig):
    """
    Configuration for medical_tests_graph.

    Inherits from StorageConfig for LMDB database settings:
    - db_path: Auto-generated path to medical_tests_graph.lmdb
    - db_capacity_mb: Database capacity (default 500 MB)
    - db_store: Whether to cache results (default True)
    - db_overwrite: Whether to refresh cache (default False)
    """
    output_path: Optional[Path] = None
    verbosity: bool = False
    enable_cache: bool = True

    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_tests_graph.lmdb"
            )
        # Call parent validation
        super().__post_init__()
class Triple(BaseModel):
    """Represents one medical test knowledge triple."""
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
# 2️⃣ Gemini Test Extractor
# =========================
class TestTripletExtractor:
    """Uses Gemini (or fallback) to extract structured test knowledge triples."""

    def __init__(self, client=None, model_name: str = "gemini-2.0-flash-thinking-exp"):
        self.client = client
        self.model_name = model_name

    def build_prompt(self, text: str) -> str:
        return f"""
Extract biomedical test knowledge triples from the following text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: measures, detects, diagnoses, monitors,
    screen_for, related_to_disease, requires_sample, uses_instrument,
    evaluates_function_of, ordered_for_symptom, follow_up_of, has_reference_range, other)
  - target
Optional: source_type, target_type, confidence
Return only a JSON array.

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
        """Offline example for testing."""
        t = text.lower()
        triples = []
        if "complete blood count" in t or "cbc" in t:
            triples.extend([
                {"source": "Complete Blood Count", "relation": "measures", "target": "Hemoglobin", "source_type": "Test", "target_type": "Biomarker"},
                {"source": "Complete Blood Count", "relation": "measures", "target": "White blood cell count", "source_type": "Test", "target_type": "Biomarker"},
                {"source": "Complete Blood Count", "relation": "requires_sample", "target": "Blood", "source_type": "Test", "target_type": "SampleType"},
                {"source": "Complete Blood Count", "relation": "uses_instrument", "target": "Hematology analyzer", "source_type": "Test", "target_type": "Instrument"},
                {"source": "Complete Blood Count", "relation": "related_to_disease", "target": "Anemia", "source_type": "Test", "target_type": "Disease"},
                {"source": "Complete Blood Count", "relation": "related_to_disease", "target": "Leukemia", "source_type": "Test", "target_type": "Disease"},
                {"source": "Complete Blood Count", "relation": "evaluates_function_of", "target": "Bone marrow", "source_type": "Test", "target_type": "Organ"},
            ])
        return triples


# =========================
# 3️⃣ Test Graph Builder
# =========================
class TestGraphBuilder:
    """Builds and queries the medical test knowledge graph."""

    def __init__(self):
        self.G = nx.MultiDiGraph()


    def _generate_dbkey(self, *args) -> str:
        """
        Generates a unique database key for a query.

        Args:
            *args: Components to combine for the key.

        Returns:
            A unique database key using SHA256 hashing.
        """
        key_content = ":".join(str(arg).lower().strip() for arg in args)
        return hashlib.sha256(key_content.encode()).hexdigest()

    def add_triples(self, triples: List[Triple]):
        for t in triples:
            self.G.add_node(t.source, type=t.source_type)
            self.G.add_node(t.target, type=t.target_type)
            self.G.add_edge(t.source, t.target, relation=t.relation, confidence=t.confidence)

    def query_measures(self, test: str):
        """Get all biomarkers measured by a given test."""
        return [
            tgt for src, tgt, d in self.G.out_edges(test, data=True)
            if d.get('relation') == 'measures'
        ]

def get_medical_tests_graph(query: str) -> List[dict]:
    """
    Get a medical tests graph for a given query.

    Args:
        query: The query to search for.

    Returns:
        A list of dictionaries representing the graph's edges.
    """
    extractor = TestTripletExtractor()
    triples = extractor.extract(query)
    builder = TestGraphBuilder()
    builder.add_triples(triples)
    return [
        {
            "source": src,
            "target": tgt,
            "relation": d.get("relation"),
            "confidence": d.get("confidence"),
        }
        for src, tgt, d in builder.G.edges(data=True)
    ]
