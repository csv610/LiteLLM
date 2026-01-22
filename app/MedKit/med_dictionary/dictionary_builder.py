"""
Dictionary Builder

Encapsulates functionality for building and managing dictionary definitions
using LLM-generated content.
"""

import sys
import json
import os
import re
from pathlib import Path
from tqdm import tqdm
from typing import Set

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from logging_util import setup_logging

# Configure logging
log_file = Path(__file__).parent / "logs" / "medical_dictionary.log"
logger = setup_logging(str(log_file))


# Default regex patterns for cleaning conversational text (can be customized via DictConfig)
DEFAULT_CONVERSATIONAL_PATTERNS = [
    r'\n+Would you like.*',
    r'\n+Feel free to.*',
    r'\n+Let me know.*',
    r'\n+Do you have.*',
    r'\n+Is there anything.*',
    r'\n+For more.*',
    r'\n+Please feel.*',
]

# Default regex patterns for detecting and removing term from definition start (can be customized via DictConfig)
DEFAULT_TERM_PREFIX_PATTERNS = [
    r'^\*\*{term}\*\*:\s*',      # **term**:
    r'^\*\*{term}\*\*\s+',        # **term**
    r'^{term}:\s*',                # term:
    r'^{term}\s+',                 # term
]


def sanitize_model_name(model: str) -> str:
    """Sanitize model name for use in file paths.

    Args:
        model: Model name (e.g., 'ollama/gemma3', 'gpt-4')

    Returns:
        Safe filename (e.g., 'ollama_gemma3', 'gpt-4')
    """
    # Replace invalid path characters: / \ : * ? " < > |
    invalid_chars = r'[\\/:\*\?"<>|]'
    sanitized = re.sub(invalid_chars, '_', model)
    return sanitized


# ============================================================================
# DICT CONFIG CLASS
# ============================================================================

class DictConfig:
    """Configuration for dictionary builder with prompt templates and file naming."""

    def __init__(
        self,
        system_prompt_template: str,
        user_prompt_template: str,
        file_name: str,
        output_dir: Path = None,
        conversational_patterns: list = None,
        term_prefix_patterns: list = None,
    ):
        """
        Initialize DictConfig with prompt and file configuration.

        Args:
            system_prompt_template: System prompt template for the LLM (required)
            user_prompt_template: User prompt template with {term} placeholder (required)
            file_name: Base name for the dictionary file (required)
            output_dir: Directory for saving dictionary definitions. Defaults to ./outputs
            conversational_patterns: List of regex patterns to remove from responses.
                Uses defaults if not provided.
            term_prefix_patterns: List of regex patterns for detecting terms at start of definitions.
                Uses defaults if not provided.

        Raises:
            ValueError: If required parameters are missing or invalid
        """
        if not system_prompt_template or not isinstance(system_prompt_template, str) or not system_prompt_template.strip():
            raise ValueError("system_prompt_template must be a non-empty string")

        if not user_prompt_template or not isinstance(user_prompt_template, str) or not user_prompt_template.strip():
            raise ValueError("user_prompt_template must be a non-empty string")

        if not file_name or not isinstance(file_name, str) or not file_name.strip():
            raise ValueError("file_name must be a non-empty string")

        self.system_prompt_template = system_prompt_template
        self.user_prompt_template = user_prompt_template
        self.file_name = file_name
        self.output_dir = output_dir or (Path(__file__).parent / "outputs")
        self.conversational_patterns = conversational_patterns or DEFAULT_CONVERSATIONAL_PATTERNS
        self.term_prefix_patterns = term_prefix_patterns or DEFAULT_TERM_PREFIX_PATTERNS

        logger.debug(
            f"DictConfig initialized: file_name={file_name}, "
            f"output_dir={self.output_dir}"
        )

    def to_dict(self) -> dict:
        """
        Convert configuration to dictionary for serialization.

        Returns:
            Dictionary representation of configuration
        """
        return {
            "system_prompt_template": self.system_prompt_template,
            "user_prompt_template": self.user_prompt_template,
            "file_name": self.file_name,
            "output_dir": str(self.output_dir),
            "conversational_patterns": self.conversational_patterns,
            "term_prefix_patterns": self.term_prefix_patterns,
        }

    @classmethod
    def from_dict(cls, config_dict: dict) -> "DictConfig":
        """
        Create DictConfig from dictionary.

        Args:
            config_dict: Dictionary containing configuration parameters

        Returns:
            DictConfig instance

        Raises:
            ValueError: If required parameters are missing
        """
        required_keys = ["system_prompt_template", "user_prompt_template", "file_name"]
        if not all(key in config_dict for key in required_keys):
            raise ValueError(
                f"system_prompt_template, user_prompt_template, and file_name are required in configuration dictionary"
            )

        return cls(
            system_prompt_template=config_dict["system_prompt_template"],
            user_prompt_template=config_dict["user_prompt_template"],
            file_name=config_dict["file_name"],
            output_dir=Path(config_dict["output_dir"]) if "output_dir" in config_dict else None,
            conversational_patterns=config_dict.get("conversational_patterns"),
            term_prefix_patterns=config_dict.get("term_prefix_patterns"),
        )

    def __repr__(self) -> str:
        """String representation of configuration."""
        return (
            f"DictConfig(file_name='{self.file_name}', "
            f"output_dir='{self.output_dir}')"
        )


def _read_file_terms(file_path: Path) -> list | None:
    """
    Helper function to read terms from either JSON or text file.

    Args:
        file_path: Path to the file

    Returns:
        List of terms or None if file cannot be read
    """
    # Try JSON first
    terms = read_json_file(file_path)
    if terms is not None:
        return terms

    # Try text file
    terms = read_text_file(file_path)
    if terms is not None:
        return terms

    return None


def read_text_file(file_path: Path) -> list | None:
    """Read terms from a plain text file (one term per line). Returns list of terms."""
    try:
        with open(file_path, 'r') as f:
            terms = [line.strip() for line in f if line.strip()]

        if not terms:
            logger.warning(f"Text file {file_path} is empty")
            return None

        logger.info(f"Read {len(terms)} terms from text file: {file_path}")
        return terms
    except Exception as e:
        logger.warning(f"Failed to read text file: {e}")
        return None


def read_json_file(file_path: Path) -> list | None:
    """Read terms from a JSON file (dictionary or list). Returns list of terms."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        if not isinstance(data, (dict, list)):
            logger.warning(f"File {file_path} does not contain a dictionary or list")
            return None

        # Extract terms from dict or list
        if isinstance(data, dict):
            all_terms = list(data.keys())
        else:  # list
            all_terms = []
            for item in data:
                if isinstance(item, str):
                    all_terms.append(item)
                elif isinstance(item, dict):
                    term = item.get("term")
                    if term:  # Only add if term exists and is non-empty
                        all_terms.append(term)

        logger.info(f"Read {len(all_terms)} terms from JSON file: {file_path}")
        return all_terms

    except json.JSONDecodeError:
        logger.warning(f"File {file_path} is not valid JSON")
        return None
    except Exception as e:
        logger.error(f"Failed to read JSON file: {e}")
        return None


def definition_starts_with_term(
    term: str, definition: str, term_prefix_patterns: list = None
) -> bool:
    """
    Check if definition starts with the term itself.

    Args:
        term: The term to check for
        definition: The definition text to check
        term_prefix_patterns: List of regex patterns for term prefixes. Uses defaults if None

    Returns:
        True if definition starts with the term, False otherwise
    """
    if not term or not definition:
        return False

    patterns = term_prefix_patterns or DEFAULT_TERM_PREFIX_PATTERNS
    escaped_term = re.escape(term)
    for pattern_template in patterns:
        pattern = pattern_template.format(term=escaped_term)
        if re.match(pattern, definition, re.IGNORECASE):
            return True
    return False


def remove_term_from_definition(
    term: str, definition: str, term_prefix_patterns: list = None
) -> str:
    """
    Remove redundant term from the start of definition.

    Args:
        term: The term to remove
        definition: The definition text
        term_prefix_patterns: List of regex patterns for term prefixes. Uses defaults if None

    Returns:
        Definition with term removed from start
    """
    if not term or not definition:
        return definition

    patterns = term_prefix_patterns or DEFAULT_TERM_PREFIX_PATTERNS
    escaped_term = re.escape(term)
    cleaned = definition

    for pattern_template in patterns:
        pattern = pattern_template.format(term=escaped_term)
        cleaned = re.sub(pattern, '', cleaned, count=1, flags=re.IGNORECASE)
        if cleaned != definition:
            break

    # Capitalize first letter if it's lowercase
    if cleaned and cleaned[0].islower():
        cleaned = cleaned[0].upper() + cleaned[1:]

    return cleaned


def parse_response(response_content: str, conversational_patterns: list = None) -> str | None:
    """
    Parse and clean response content by removing conversational text.

    Args:
        response_content: The response text to parse
        conversational_patterns: List of regex patterns for conversational text. Uses defaults if None

    Returns:
        Cleaned response text or None if invalid
    """
    try:
        if not response_content:
            return None

        patterns = conversational_patterns or DEFAULT_CONVERSATIONAL_PATTERNS
        cleaned = response_content
        for pattern in patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)

        # Strip excess whitespace while preserving internal formatting
        cleaned = cleaned.strip()

        # Remove multiple consecutive blank lines
        cleaned = re.sub(r'\n\n\n+', '\n\n', cleaned)

        # Replace single newlines with spaces to prevent word breaks
        # while preserving double newlines for paragraph breaks
        cleaned = re.sub(r'(?<!\n)\n(?!\n)', ' ', cleaned)

        # Normalize multiple spaces to single space
        cleaned = re.sub(r' +', ' ', cleaned)

        logger.debug("Successfully parsed and cleaned response")
        return cleaned if cleaned else None
    except Exception as e:
        logger.error(f"Failed to parse response: {e}")
        return None


def fetch_definition(
    client: LiteClient,
    term: str,
    config: DictConfig,
) -> str | None:
    """
    Fetch term definition from the API.

    Args:
        client: LiteClient instance for making API calls
        term: The term to define
        config: DictConfig instance with prompt templates

    Returns:
        Definition text or None if failed
    """
    try:
        user_prompt = config.user_prompt_template.format(term=term)
        model_input = ModelInput(user_prompt=user_prompt, system_prompt=config.system_prompt_template)
        response_content = client.generate_text(model_input=model_input)

        if not isinstance(response_content, str):
            logger.error("Expected string response from model")
            return None

        logger.info(f"Successfully fetched definition for term: {term}")
        return response_content
    except Exception as e:
        logger.error(f"Failed to fetch definition for term '{term}': {e}")
        return None


# ============================================================================
# DICTIONARY BUILDER CLASS
# ============================================================================

class DictionaryBuilder:
    """Encapsulates dictionary building functionality (domain-agnostic)."""

    def __init__(self, config: DictConfig, model_config: ModelConfig):
        """
        Initialize the DictionaryBuilder.

        Args:
            config: DictConfig object with prompts and file configuration (required)
            model_config: ModelConfig instance with model and temperature settings (required)

        Raises:
            ValueError: If config or model_config is invalid or missing
        """
        if not isinstance(config, DictConfig):
            raise ValueError("config must be a DictConfig instance")

        if not isinstance(model_config, ModelConfig):
            raise ValueError("model_config must be a ModelConfig instance")

        self.config = config
        self.model_config = model_config

        # Set up instance variables from config
        self.config.output_dir.mkdir(exist_ok=True)
        self.client = LiteClient(model_config=model_config)
        self.definitions = self.load_definitions()
        self.existing_terms = {d.get("term", "").lower() for d in self.definitions}
        logger.info(f"DictionaryBuilder initialized with model: {model_config.model}")

    def _get_definitions_file(self) -> Path:
        """Get the path to the definitions file for this configuration."""
        safe_model = sanitize_model_name(self.model_config.model)
        filename = f"{self.config.file_name}_{safe_model}.json"
        return self.config.output_dir / filename

    def load_definitions(self) -> list:
        """Load existing dictionary definitions from JSON file."""
        try:
            json_file = self._get_definitions_file()

            if json_file.exists():
                with open(json_file, 'r') as f:
                    definitions = json.load(f)
                    logger.info(f"Loaded {len(definitions)} definitions from {json_file}")
                    return definitions

            logger.info(f"No existing definitions file found at {json_file}")
            return []
        except Exception as e:
            logger.error(f"Failed to load definitions: {e}")
            return []

    def save_definitions(self) -> bool:
        """Save current definitions to JSON file."""
        try:
            json_file = self._get_definitions_file()

            sorted_definitions = sorted(self.definitions, key=lambda x: x.get("term", "").lower())
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_definitions, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            logger.info(f"Saved {len(sorted_definitions)} definitions to {json_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save definitions: {e}")
            return False

    def process_input(self, input_data: str | Path) -> Set[str]:
        """
        (1) Process input and return a set of terms.

        Args:
            input_data: Can be a file path (JSON/text) or a single term string

        Returns:
            Set of terms (lowercase)
        """
        input_data_str = str(input_data).strip()
        input_path = Path(input_data_str)

        # Check if it's an existing file first
        file_extensions = ('.json', '.txt', '.csv')
        if input_path.exists() and input_data_str.lower().endswith(file_extensions):
            terms = _read_file_terms(input_path)
            if terms:
                logger.info(f"Loaded {len(terms)} terms from file: {input_path}")
                return set(t.lower() for t in terms)
            else:
                logger.warning(f"File {input_path} exists but contains no terms")
                return set()

        # If it looks like a file but doesn't exist, warn but treat as term
        if input_data_str.lower().endswith(file_extensions):
            logger.warning(f"Input looks like file but doesn't exist, treating as term: {input_data_str}")

        # Process as a single term
        if input_data_str:
            logger.info(f"Processing input as single term: {input_data_str}")
            return {input_data_str.lower()}

        logger.warning("No valid input provided")
        return set()

    def process_and_save_terms(self, new_terms: Set[str]) -> int:
        """
        (4-5) Process new terms incrementally: fetch, clean, and save one at a time.

        Args:
            new_terms: Set of new terms to process

        Returns:
            Count of successfully saved terms
        """
        saved_count = 0
        sorted_terms = sorted(new_terms)

        for term in tqdm(sorted_terms, desc="Processing terms", unit="term"):
            try:
                # Fetch definition from LLM
                raw_response = fetch_definition(self.client, term, self.config)
                if not raw_response:
                    logger.warning(f"Failed to fetch definition for term: {term}")
                    continue

                # Clean response using conversational patterns
                parsed_content = parse_response(
                    raw_response, self.config.conversational_patterns
                )
                if parsed_content is None:
                    logger.warning(f"Failed to parse response for '{term}'")
                    continue

                # Remove term from definition if present using term prefix patterns
                if definition_starts_with_term(
                    term, parsed_content, self.config.term_prefix_patterns
                ):
                    parsed_content = remove_term_from_definition(
                        term, parsed_content, self.config.term_prefix_patterns
                    )

                # Validate definition has content
                if not parsed_content or not parsed_content.strip():
                    logger.warning(f"Definition for '{term}' is empty after cleaning")
                    continue

                # Check for duplicates (case-insensitive)
                if term.lower() in self.existing_terms:
                    logger.info(f"Term '{term}' already exists in dictionary, skipping")
                    continue

                # Append to definitions
                new_entry = {"term": term, "definition": parsed_content}
                self.definitions.append(new_entry)
                self.existing_terms.add(term.lower())

                # Save immediately to file
                if self.save_definitions():
                    logger.info(f"Saved definition for '{term}'")
                    saved_count += 1
                else:
                    # Remove the entry from definitions if save failed
                    self.definitions.pop()
                    self.existing_terms.discard(term.lower())

            except Exception as e:
                logger.error(f"Error processing term '{term}': {e}")
                continue

        logger.info(f"Successfully processed {saved_count}/{len(new_terms)} definitions")
        return saved_count

    def build(self, input_data: str) -> int:
        """
        Main method to build the dictionary.

        Workflow:
        (1) process_input: Get input_terms as a set
        (2) Identify new terms not in existing_terms
        (3) process_and_save_terms: Fetch, clean, and save definitions incrementally

        Args:
            input_data: Term, or path to JSON/text file containing terms

        Returns:
            Count of successfully processed terms
        """
        try:
            # Step 1: Process input to get input_terms as a set
            input_terms = self.process_input(input_data)
            if not input_terms:
                logger.error("No valid input provided")
                return 0

            # Step 2: Identify new terms
            logger.info(f"Retrieved {len(self.existing_terms)} existing terms from dictionary")
            new_items = input_terms - self.existing_terms
            logger.info(f"Found {len(new_items)} new terms out of {len(input_terms)} input terms")

            if not new_items:
                logger.info(f"All {len(input_terms)} terms already exist in dictionary")
                print(f"\nAll {len(input_terms)} terms already exist in dictionary")
            else:
                print(f"\nNew terms to be added ({len(new_items)}):")
                for term in sorted(new_items):
                    print(f"  - {term}")
                print()

                # Step 3: Process and save terms incrementally
                saved_count = self.process_and_save_terms(new_items)
                logger.info(f"Completed: {saved_count}/{len(new_items)} terms processed successfully")
                print(f"\nCompleted: {saved_count}/{len(new_items)} terms processed successfully")
                return saved_count

            # Print total items in dictionary (final dictionary state after processing)
            logger.info(f"Total items in dictionary: {len(self.definitions)}")
            print(f"\nTotal items in dictionary: {len(self.definitions)}")
            return 0

        except Exception as e:
            logger.error(f"Unexpected error in build: {e}")
            return 0
