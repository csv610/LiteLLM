"""
Agno-powered Agentic Dictionary Builder
Uses multi-agent collaboration with Agno to build the medical dictionary.
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
    from agno.agent import Agent
    from agno.models.ollama import Ollama
except ImportError:
    print("Agno or Ollama model not found. Please install agno and ollama: pip install agno ollama")
    sys.exit(1)

try:
    from dictionary_builder import load_terms_from_file
except ImportError:
    from med_dictionary.dictionary_builder import load_terms_from_file

class AgnoDictionaryBuilder:
    """Multi-agent approach for dictionary building using Agno."""

    def __init__(self, model_id: str = "gemma3:latest"):
        self.model = Ollama(id=model_id, host="http://127.0.0.1:11434")
        
        # 1. Researcher: Verification Phase
        self.researcher = Agent(
            model=self.model,
            description="You are a meticulous medical researcher.",
            instructions=[
                "Determine if a given term is a formally recognized medical term.",
                "Think step-by-step about its origin, clinical use, and documentation.",
                "End your reasoning with [YES] if it's a medical term, or [NO] if it's not."
            ]
        )
        
        # 2. Writer: Drafting Phase
        self.writer = Agent(
            model=self.model,
            description="You are a medical dictionary writer.",
            instructions=[
                "Write a draft definition for the medical term based on research provided.",
                "Rules: Concise, factual, 2-3 sentences max.",
                "Do NOT start with 'is' or 'refers to'.",
                "Focus only on the medical description."
            ]
        )
        
        # 3. Editor: Critique & Refinement Phase
        self.editor = Agent(
            model=self.model,
            description="You are an expert medical editor.",
            instructions=[
                "Review and refine the drafted definition.",
                "Ensure it's concise (2-3 sentences).",
                "Ensure it does NOT start with the term itself or 'is'.",
                "Ensure it's professional and factual.",
                "Output ONLY the final definition text."
            ]
        )

        self.output_file = Path(__file__).parent.parent / "outputs" / "dictionary_agno.json"
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

    def process_term(self, term: str) -> Optional[str]:
        """Runs the multi-agent workflow for a single term."""
        
        # Step 1: Verification
        research_resp = self.researcher.run(f"Research and verify the term: '{term}'")
        reasoning = research_resp.content if research_resp else ""
        
        if not reasoning or "[YES]" not in reasoning.upper():
            return None

        # Step 2: Drafting
        draft_resp = self.writer.run(f"Draft a definition for '{term}' based on this research: {reasoning}")
        draft = draft_resp.content if draft_resp else ""
        
        if not draft:
            return None

        # Step 3: Refinement
        refine_resp = self.editor.run(f"Refine this definition for '{term}': {draft}")
        final_definition = refine_resp.content if refine_resp else ""
        
        return final_definition.strip() if final_definition else None

    def build(self, input_data: str):
        input_path = Path(input_data)
        if input_path.exists():
            terms = load_terms_from_file(input_path)
        else:
            # Assume it's a comma-separated list or single term
            terms = [t.strip() for t in input_data.split(",") if t.strip()]

        new_terms = [t for t in terms if t.lower() not in self.existing_terms]
        
        for term in tqdm(new_terms, desc="Agno Processing"):
            definition = self.process_term(term)
            if definition:
                self.definitions.append({"term": term, "definition": definition})
                self.save()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build medical dictionary with Agno agents.")
    parser.add_argument("--input", type=str, required=True, help="Input file path or comma-separated terms.")
    args = parser.parse_args()
    
    builder = AgnoDictionaryBuilder()
    builder.build(args.input)
