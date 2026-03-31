import sqlite_utils
import hashlib
import json
from pathlib import Path
from typing import Optional, Any
from .drug_disease_interaction_models import DrugDiseaseInteractionModel, ModelOutput

class InteractionCache:
    """SQLite-based cache for drug-disease interaction results."""
    
    def __init__(self, db_path: str = "interaction_cache.db"):
        self.db = sqlite_utils.Database(db_path)
        self.table = self.db.table("interactions", pk="id")
    
    def _generate_key(self, medicine: str, condition: str, age: Optional[int], severity: Optional[str]) -> str:
        """Generate a unique key based on inputs."""
        key_str = f"{medicine.lower()}|{condition.lower()}|{age}|{severity}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def get(self, medicine: str, condition: str, age: Optional[int], severity: Optional[str]) -> Optional[ModelOutput]:
        """Retrieve a cached result if it exists."""
        key = self._generate_key(medicine, condition, age, severity)
        try:
            row = self.table.get(key)
        except sqlite_utils.db.NotFoundError:
            return None
        
        if row:
            # Reconstruct ModelOutput from JSON
            data_dict = json.loads(row["data"])
            markdown = row["markdown"]
            
            # Reconstruct pydantic model
            interaction_data = DrugDiseaseInteractionModel(**data_dict) if data_dict else None
            return ModelOutput(data=interaction_data, markdown=markdown)
        return None

    def set(self, medicine: str, condition: str, age: Optional[int], severity: Optional[str], result: ModelOutput):
        """Store a result in the cache."""
        key = self._generate_key(medicine, condition, age, severity)
        data_json = json.dumps(result.data.dict()) if result.data else None
        
        self.table.insert({
            "id": key,
            "medicine": medicine.lower(),
            "condition": condition.lower(),
            "age": age,
            "severity": severity,
            "data": data_json,
            "markdown": result.markdown
        }, replace=True)
