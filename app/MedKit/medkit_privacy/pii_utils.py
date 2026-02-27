import json
from typing import Dict, List, Optional, Any
from pydantic import BaseModel

# Try to import LiteClient and Config classes from the project's 'lite' package
try:
    from lite.lite_client import LiteClient
    from lite.config import ModelConfig, ModelInput
except (ImportError, ModuleNotFoundError):
    # Fallback/Mock if not available
    from dataclasses import dataclass
    @dataclass
    class ModelConfig:
        model: str
        temperature: float = 0.7
    
    @dataclass
    class ModelInput:
        user_prompt: str = ""
        system_prompt: Optional[str] = None
        response_format: Optional[Any] = None

    class LiteClient:
        def __init__(self, model_config=None): pass
        def generate_text(self, model_input: ModelInput, **kwargs):
            return '{"pii": []}'

class PIIEntity(BaseModel):
    """Represents a single detected PII entity."""
    type: str
    value: str
    start: int
    end: int

class PIIResponse(BaseModel):
    """Container for multiple PII entities, used for structured LLM output."""
    pii: List[PIIEntity]

class PIIDetector:
    """Detects PII using LLM (via LiteClient) for high-accuracy, context-aware identification."""

    def __init__(self, model_config: Optional[ModelConfig] = None):
        # Defaulting to ollama/gemma3 as per project standards
        self.model_config = model_config or ModelConfig(model="ollama/gemma3")
        self.client = LiteClient(model_config=self.model_config)
        self.system_prompt = """
        You are an expert Privacy and Compliance Auditor specializing in both HIPAA Safe Harbor and GDPR (General Data Protection Regulation) standards.
        Analyze the input text and identify ALL Personal Data and Protected Health Information (PHI).
        
        Identify the following categories:
        1. HIPAA 18 Identifiers: Names, all geographical subdivisions smaller than a state (addresses, zip codes), all elements of dates directly related to an individual (DOB, admission/discharge), telephone/fax numbers, emails, SSNs, MRNs, health plan IDs, account numbers, license numbers, vehicle identifiers, device serial numbers, URLs, IP addresses, biometric identifiers, and full-face photos.
        
        2. GDPR Specific Identifiers:
           - Online Identifiers: Cookie IDs, RFID tags, device IDs, and metadata that could identify a user.
           - Indirect Identifiers: Information specific to physical, physiological, genetic, mental, economic, cultural, or social identity that could identify a person in context (e.g., "the only left-handed surgeon at St. Jude's").
        
        3. GDPR Special Categories (Article 9):
           - Racial or ethnic origin.
           - Political opinions or Trade union membership.
           - Religious or philosophical beliefs.
           - Genetic and Biometric data.
           - Data concerning health, sex life, or sexual orientation.
        
        4. Any other unique identifying number, characteristic, or code.
        
        Return ONLY a JSON object with a 'pii' key containing a list of objects:
        {
          "pii": [
            {"type": "NAME", "value": "John Doe", "start": 11, "end": 19},
            {"type": "POLITICAL_OPINION", "value": "Federalist", "start": 30, "end": 40}
          ]
        }
        Use descriptive category names like NAME, CONTACT, LOCATION, DATE, IDENTITY, ONLINE_ID, POLITICAL_OPINION, RELIGIOUS_BELIEF, BIOMETRIC, HEALTH_DATA, or INDIRECT_ID.
        The 'start' and 'end' must be the exact character indices in the input text.
        """

    def detect(self, text: str) -> List[Dict]:
        """Perform PII detection using the LLM with structured Pydantic output."""
        if not text.strip():
            return []

        # Create ModelInput with system prompt and Pydantic response format
        model_input = ModelInput(
            user_prompt=text, 
            system_prompt=self.system_prompt,
            response_format=PIIResponse
        )
        
        try:
            # LiteClient returns a PIIResponse instance
            response = self.client.generate_text(model_input)
            
            entities = []
            if isinstance(response, PIIResponse):
                entities = response.pii
            elif isinstance(response, str):
                data = json.loads(response)
                entities = [PIIEntity(**e) for e in data.get("pii", [])]
            
            # Validation: Ensure values exist in text and indices are correct
            valid_entities = []
            for entity in entities:
                # Sanity check: does the value at start:end match the detected value?
                actual_value = text[entity.start:entity.end]
                if actual_value.strip().lower() == entity.value.strip().lower():
                    valid_entities.append(entity.model_dump())
                else:
                    # If indices are slightly off, try to find the value in the text
                    # (LLMs sometimes struggle with exact indexing)
                    pos = text.find(entity.value)
                    if pos != -1:
                        entity.start = pos
                        entity.end = pos + len(entity.value)
                        valid_entities.append(entity.model_dump())
            
            return valid_entities
        except Exception as e:
            print(f"CRITICAL: LLM PII Detection Failed: {e}")
            return []

class PIIMasker:
    """Masks PII in text using the LLM-based detector."""

    def __init__(self, detector: Optional[PIIDetector] = None):
        self.detector = detector or PIIDetector()

    def mask(self, text: str, placeholder: str = "[{type}]") -> str:
        """Mask all detected PII in text with placeholders."""
        detections = self.detector.detect(text)
        
        # Sort by start index descending to replace without shifting indices
        sorted_detections = sorted(detections, key=lambda x: x["start"], reverse=True)
        
        masked_text = text
        for d in sorted_detections:
            label = placeholder.format(type=d["type"])
            masked_text = masked_text[:d["start"]] + label + masked_text[d["end"]:]
            
        return masked_text
