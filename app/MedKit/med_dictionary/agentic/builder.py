"""
Agentic Dictionary Builder
A multi-step, iterative way to build the dictionary with reasoning, drafting, and refinement.
"""

import json
import logging
from pathlib import Path
from typing import List, Optional
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

class AgenticDictionaryBuilder:
    """Multi-step agentic approach for dictionary building."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.prompt_builder = MedicalDictionaryPromptBuilder()
        self.output_file = Path(__file__).parent.parent / "outputs" / "dictionary_agentic.json"
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

    def process_term_agentic(self, term: str) -> Optional[str]:
        """Runs the multi-step agentic workflow for a single term."""
        
        # Step 1: Verification Phase (Is it a medical term?)
        verify_prompt = (
            f"Determine if '{term}' is a formally recognized medical term. "
            "Think step-by-step about its origin, clinical use, and documentation. "
            "End your reasoning with [YES] if it's a medical term, or [NO] if it's not."
        )
        
        reasoning = self.client.generate_text(
            ModelInput(
                user_prompt=verify_prompt,
                system_prompt="You are a meticulous medical researcher."
            )
        )
        
        if not reasoning or "[YES]" not in reasoning.upper():
            return "Not a medically recognized term."

        # Step 2: Drafting Phase
        draft_prompt = (
            f"Based on your reasoning: '{reasoning}', write a draft definition for '{term}'. "
            "Follow these rules: Concise, factual, 2-3 sentences max. "
            "Do NOT start with '{term} is' or '{term} refers to'. "
            "Focus only on the medical description."
        )
        
        draft = self.client.generate_text(
            ModelInput(
                user_prompt=draft_prompt,
                system_prompt="You are a medical dictionary writer."
            )
        )
        
        if not draft:
            return None

        # Step 3: Critique & Refinement Phase
        refine_prompt = (
            f"Review this drafted definition for '{term}':\n\n'{draft}'\n\n"
            "Constraints:\n"
            "1. Must be concise (2-3 sentences).\n"
            "2. Must NOT start with the term itself or 'is'.\n"
            "3. Must be professional and factual.\n\n"
            "Refine the definition to ensure it perfectly matches these constraints. "
            "Output ONLY the final definition text."
        )
        
        final_definition = self.client.generate_text(
            ModelInput(
                user_prompt=refine_prompt,
                system_prompt="You are an expert medical editor."
            )
        )
        
        return final_definition.strip() if final_definition else None

    def build(self, input_data: str):
        input_path = Path(input_data)
        if input_path.exists():
            terms = load_terms_from_file(input_path)
        else:
            terms = [input_data]

        new_terms = [t for t in terms if t.lower() not in self.existing_terms]
        
        for term in tqdm(new_terms, desc="Agentic Processing"):
            definition = self.process_term_agentic(term)
            if definition:
                self.definitions.append({"term": term, "definition": definition})
                self.save()
