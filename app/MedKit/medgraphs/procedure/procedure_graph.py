l Procedure Knowledge Graph Builder
-----------------------------------------
- Extracts procedure triples (subject–relation–object) using Gemini
- Validates with Pydantic
- Builds a NetworkX knowledge graph
- Visualizes using Matplotlib

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
    "surgeon": "Specialist",
    "doctor": "Specialist",
    "risk": "Risk",
    "benefit": "Benefit",
    "complication": "Complication",
    "anesthesia": "AnesthesiaType",
    "preparation": "Preparation",
    "follow_up": "FollowUp",
}


class Triple(BaseModel):
    """Represents one validated medical procedure relation."""
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
# 2️⃣ Gemini Procedure Extractor
# =========================
class ProcedureTripletExtractor:
    """Uses Gemini (or fallback) to extract structured procedure triples."""

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
Extract medical procedure triples from the following text.
Each triple must be a JSON object with:
  - source
  - relation (choose from: treats_disease, used_for_diagnosis, performed_on,
    requires_instrument, performed_by_specialist, has_risk, has_benefit,
    has_complication, requires_anesthesia, requires_preparation,
    follow_up_by, related_to_procedure, other)
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
        """Offline fallback for testing."""
        t = text.lower()
        triples = []
        if "appendectomy" in

