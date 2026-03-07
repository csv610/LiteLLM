"""
Medical Term Classifier
Classifies medical terms into categories and subcategories using LLM.
"""

import json
import logging
import argparse
from pathlib import Path
from typing import List

from tqdm import tqdm
from lite.logging_config import configure_logging
# Logging setup
log_file = Path(__file__).parent / "logs" / "medical_term_classify.log"
configure_logging(str(log_file), enable_console=False)
logger = logging.getLogger(__name__)

# Suppress LiteLLM logging to console
logging.getLogger("litellm").setLevel(logging.WARNING)
logging.getLogger("LiteLLM").setLevel(logging.WARNING)


from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from med_dictionary.medical_classification_prompts import MedicalClassificationPromptBuilder


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
                        terms.append(row[0].strip())
        elif file_path.suffix == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    terms = [item.strip() for item in data if isinstance(item, str) and item.strip()]
                elif isinstance(data, dict):
                    terms = [key.strip() for key in data.keys() if key.strip()]
    except Exception as e:
        logger.error(f"Error loading terms from {file_path}: {e}")
    
    return terms

class MedicalTermClassifier:
    """Core logic for classifying medical terms via LLM."""

    def __init__(self, model_config: ModelConfig, output_file: Path = None):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.prompt_builder = MedicalClassificationPromptBuilder()
        
        self.output_file = output_file or (Path(__file__).parent / "outputs" / "classified.json")
        logger.info(f"Using output file: {self.output_file}")
        
        self.classifications = self._load_classifications()
        self.existing_terms = {c.get("term", "").lower() for c in self.classifications}

    def _load_classifications(self) -> List[dict]:
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load classifications: {e}")
        return []

    def save(self) -> bool:
        """Save classifications to JSON file."""
        try:
            sorted_data = sorted(self.classifications, key=lambda x: x.get("term", "").lower())
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Classifications saved to {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save to {self.output_file}: {e}")
            return False

    def _extract_json(self, text: str) -> dict:
        """Extracts and parses JSON from a string, handling markdown blocks."""
        import re
        
        # Try to find JSON block in markdown
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        else:
            # Fallback: try to find anything that looks like a JSON object
            json_match = re.search(r'(\{.*\})', text, re.DOTALL)
            if json_match:
                text = json_match.group(1)

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}. Original text: {text}")
            return {}

    def classify(self, input_data: str) -> int:
        """Process input (term or file) and classify medical terms."""
        input_path = Path(input_data)
        if input_path.exists() and input_path.suffix in ('.json', '.txt', '.csv'):
            terms = set(load_terms_from_file(input_path))
        else:
            terms = {input_data.strip()} if input_data.strip() else set()

        new_terms = sorted([term for term in terms if term.lower() not in self.existing_terms])
        if not new_terms:
            logger.info(f"All {len(terms)} terms already classified.")
            return 0

        logger.info(f"Classifying {len(new_terms)} new terms...")
        saved_count = 0

        for term in tqdm(new_terms, desc="Processing terms"):
            try:
                raw_response = self.client.generate_text(ModelInput(
                    user_prompt=self.prompt_builder.create_user_prompt(term),
                    system_prompt=self.prompt_builder.create_system_prompt()
                ))
                
                if raw_response and raw_response.strip():
                    classification_data = self._extract_json(raw_response)
                    
                    if classification_data and "category" in classification_data and "subcategory" in classification_data:
                        classification_data["term"] = term
                        self.classifications.append(classification_data)
                        saved_count += 1
                        
                        # Save periodically
                        if saved_count % 5 == 0:
                            self.save()
                    else:
                        logger.error(f"Invalid classification data for '{term}': {raw_response}")
            except Exception as e:
                logger.error(f"Error processing '{term}': {e}")
        
        self.save()
        logger.info(f"Completed: {saved_count}/{len(new_terms)} classified. Total: {len(self.classifications)}. Results saved to: {self.output_file}")
        return saved_count

def main():
    parser = argparse.ArgumentParser(description="Classify medical terms into categories and subcategories.")
    parser.add_argument("input", help="Medical term, or path to JSON/text file containing terms")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="The model to use (default: ollama/gemma3)")

    args = parser.parse_args()
    
    try:
        model_config = ModelConfig(model=args.model)
        classifier = MedicalTermClassifier(model_config)
        classifier.classify(input_data=args.input)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
   main()
