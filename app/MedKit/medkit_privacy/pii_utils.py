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
        You are an expert PII (Personally Identifiable Information) detector specializing in HIPAA Safe Harbor de-identification standards.
        Analyze the input text and identify ALL of the following 18 identifiers:
        
        1. Names.
        2. All geographical subdivisions smaller than a state, including street address, city, county, precinct, and zip code. 
           - Special Rule: The initial three digits of a zip code may be retained ONLY if the geographic unit formed by combining all zip codes with the same three initial digits contains more than 20,000 people. Otherwise, the zip code must be treated as PII.
        3. All elements of dates (except year) for dates directly related to an individual, including birth date, admission date, discharge date, and date of death.
           - Special Rule: For individuals age 90 or older, ALL elements of dates (including year) indicative of such age must be identified as PII, except that such ages and elements may be aggregated into a single category of 'age 90 or older'.
        4. Telephone numbers.
        5. Fax numbers.
        6. Email addresses.
        7. Social Security numbers.
        8. Medical record numbers.
        9. Health plan beneficiary numbers.
        10. Account numbers.
        11. Certificate/license numbers.
        12. Vehicle identifiers and serial numbers, including license plate numbers.
        13. Device identifiers and serial numbers.
        14. Web Universal Resource Locators (URLs).
        15. Internet Protocol (IP) address numbers.
        16. Biometric identifiers, including finger and voice prints.
        17. Full face photographic images and any comparable images.
        18. Any other unique identifying number, characteristic, or code, except as permitted by the HIPAA Safe Harbor for re-identification (e.g., a code assigned by the investigator).
        
        Return the data in the specified JSON format. The 'start' and 'end' must be exact character indices.
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
