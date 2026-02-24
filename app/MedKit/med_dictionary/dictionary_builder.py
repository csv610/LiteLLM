"""
Dictionary Builder
Encapsulates functionality for building and managing dictionary definitions using LLM content.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional
from tqdm import tqdm

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
try:
    from .medical_dictionary_prompts import MedicalDictionaryPromptBuilder
except (ImportError, ValueError):
    from medical_dictionary_prompts import MedicalDictionaryPromptBuilder

# Logging setup
log_file = Path(__file__).parent / "logs" / "medical_dictionary.log"
configure_logging(str(log_file))
logger = logging.getLogger(__name__)

def load_terms_from_file(file_path: Path) -> List[str]:
    """
    Loads terms from a given file path.
    Supports .txt (one term per line), .csv (first column), and .json (list of strings or dict keys).
    """
    terms = []
    if not file_path.exists():
        logger.warning(f"File not found: {file_path}")
        return []

    try:
        if file_path.suffix == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                terms = [line.strip() for line in f if line.strip()]
        elif file_path.suffix == '.csv':
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        terms.append(row[0].strip()) # Assume first column contains the term
        elif file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    terms = [item.strip() for item in data if isinstance(item, str) and item.strip()]
                elif isinstance(data, dict):
                    terms = [key.strip() for key in data.keys() if key.strip()]
        else:
            logger.warning(f"Unsupported file type for loading terms: {file_path.suffix}")

    except Exception as e:
        logger.error(f"Error loading terms from {file_path}: {e}")
    
    return terms


class DictionaryBuilder:
    """Core logic for building dictionaries via LLM."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.prompt_builder = MedicalDictionaryPromptBuilder()
        
        # Set default values since DictConfig is no longer used
        safe_model = model_config.model.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        self.output_file = Path(__file__).parent / "outputs" / f"dictionary_{safe_model}.json"
        
        self.definitions = self._load_definitions()
        self.existing_terms = {d.get("term", "").lower() for d in self.definitions}

    def _load_definitions(self) -> List[dict]:
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load definitions: {e}")
        return []

    def save(self) -> bool:
        """Save definitions to JSON file."""
        try:
            sorted_defs = sorted(self.definitions, key=lambda x: x.get("term", "").lower())
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_defs, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to save: {e}")
            return False

    def generate_text(self, input_data: str) -> int:
        """Process input (term or file) and build dictionary definitions."""
        input_path = Path(input_data)
        if input_path.exists() and input_path.suffix in ('.json', '.txt', '.csv'):
            # Load terms from file, preserving original case
            terms = set()
            for t in load_terms_from_file(input_path):
                if t.strip():  # Only add non-empty terms
                    terms.add(t.strip())
        else:
            # Single term input, preserve original case
            terms = {input_data.strip()} if input_data.strip() else set()

        # Use lowercase for comparison with existing terms
        new_terms = sorted([term for term in terms if term.lower() not in self.existing_terms])
        if not new_terms:
            print(f"\nAll {len(terms)} terms already exist.")
            return 0

        print(f"\nAdding {len(new_terms)} new terms...")
        saved_count = 0
        temp_definitions = []
        temp_output_file = self.output_file.parent / f"temp_{self.output_file.name}"

        # Ensure temp file is empty or created
        with open(temp_output_file, 'w', encoding='utf-8') as f:
            pass # Truncate or create file

        for term in tqdm(new_terms, desc="Processing"):
            try:
                raw_response = self.client.generate_text(ModelInput(
                    user_prompt=self.prompt_builder.create_user_prompt(term),
                    system_prompt=self.prompt_builder.create_system_prompt()
                ))
                
                if raw_response and raw_response.strip():
                    # Create definition and dump to temp file immediately
                    new_definition = {"term": term, "definition": raw_response.strip()}
                    temp_definitions.append(new_definition)
                    with open(temp_output_file, 'a', encoding='utf-8') as f:
                        json.dump(new_definition, f, ensure_ascii=False)
                        f.write('\n')
                    
                    saved_count += 1

            except Exception as e:
                logger.error(f"Error processing '{term}': {e}")
        
        # Merge temporary definitions with main definitions once complete
        if temp_definitions:
            self.definitions.extend(temp_definitions)
            if self.save():
                print(f"Merged {len(temp_definitions)} new terms into the main dictionary.")
            else:
                logger.error("Failed to save merged dictionary.")
        
        # Clean up temporary file
        if temp_output_file.exists():
            os.remove(temp_output_file)

        print(f"\nCompleted: {saved_count}/{len(new_terms)} added. Total: {len(self.definitions)}")
        return saved_count
