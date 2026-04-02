"""
Non-Agentic Dictionary Builder
A simple, direct way to build the dictionary with a single LLM call per term.
"""

import json
import logging
from pathlib import Path
from typing import List
from tqdm import tqdm
import sys
import os

# Add the project roots to sys.path to support imports
project_root = Path(__file__).parent.parent
litellm_root = project_root.parent.parent.parent
for path in [project_root, project_root.parent, litellm_root]:
    if str(path) not in sys.path:
        sys.path.append(str(path))

try:
    from lite.config import ModelConfig, ModelInput
    from lite.lite_client import LiteClient
    from dictionary_builder import load_terms_from_file
    from medical_dictionary_prompts import MedicalDictionaryPromptBuilder
except ImportError:
    # Fallback for local imports if needed
    from med_dictionary.dictionary_builder import load_terms_from_file
    from med_dictionary.medical_dictionary_prompts import MedicalDictionaryPromptBuilder
    from lite.config import ModelConfig, ModelInput
    from lite.lite_client import LiteClient

class NonAgenticDictionaryBuilder:
    """Direct, single-prompt approach for dictionary building."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.prompt_builder = MedicalDictionaryPromptBuilder()
        self.output_file = Path(__file__).parent.parent / "outputs" / "dictionary_nonagentic.json"
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.definitions = self._load_definitions()
        self.existing_terms = {d.get("term", "").lower() for d in self.definitions}

    def _load_definitions(self) -> List[dict]:
        if self.output_file.exists():
            try:
                with open(self.output_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save(self):
        sorted_defs = sorted(self.definitions, key=lambda x: x.get("term", "").lower())
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(sorted_defs, f, indent=2, ensure_ascii=False)

    def build(self, input_data: str):
        input_path = Path(input_data)
        if input_path.exists():
            terms = load_terms_from_file(input_path)
        else:
            terms = [input_data]

        new_terms = [t for t in terms if t.lower() not in self.existing_terms]
        
        for term in tqdm(new_terms, desc="Non-Agentic Processing"):
            response = self.client.generate_text(
                ModelInput(
                    user_prompt=self.prompt_builder.create_user_prompt(term),
                    system_prompt=self.prompt_builder.create_system_prompt(),
                )
            )
            if response:
                self.definitions.append({"term": term, "definition": response.strip()})
                self.save()
