import argparse
from pathlib import Path

# Add parent directories to path for imports

from logging_util import setup_logging
from lite.config import ModelConfig
from dictionary_builder import (
    DictionaryBuilder,
    DictConfig,
)

# Configure logging
log_file = Path(__file__).parent / "logs" / "medical_dictionary.log"
logger = setup_logging(str(log_file))


# ============================================================================
# MEDICAL DICTIONARY CONFIGURATION
# ============================================================================

# Medical system prompt
MEDICAL_SYSTEM_PROMPT = (
    "You are a medical dictionary expert. Provide a dictionary definition ONLY if the term "
    "is medically recognized - no conversational text, no follow-up questions, no extra "
    "commentary. Be concise and professional. Format the response as a clear medical "
    "dictionary entry."
)

# Medical user prompt template
MEDICAL_USER_PROMPT_TEMPLATE = (
    "Define '{term}' only if it is a medically recognized full term (not an abbreviation, "
    "acronym, or slang). If it is not a valid medical term, output exactly: "
    "'Not a medically recognized term.' "
    "Write the definition in formal medical dictionary style: concise, neutral, factual. "
    "Do NOT include pronunciation, etymology, examples, or usage notes. "
    "Do NOT repeat the term name at the start of the definition. "
    "Output only the definition text and nothing else."
)


# ============================================================================
# MAIN CLI FUNCTION
# ============================================================================

def build_med_dict(input_data: str, model: str):
    """Main CLI function to fetch and save medical term definitions.

    Workflow:
    (1) process_input: Get input_terms as a set
    (2) Identify new terms not in existing_terms
    (3) process_and_save_terms: Fetch, clean, and save definitions incrementally

    Args:
        input_data: Medical term or file path to JSON/text file containing terms
        model: The LLM model to use for generating definitions

    Input data can be:
    - A single medical term (string)
    - Path to a JSON file containing a dictionary of terms
    - Path to a text file with one term per line
    """
    try:
        # Create model config
        model_config = ModelConfig(model=model)

        # Create dictionary config with medical prompts
        config = DictConfig(
            system_prompt_template=MEDICAL_SYSTEM_PROMPT,
            user_prompt_template=MEDICAL_USER_PROMPT_TEMPLATE,
            file_name="medical_dictionary",
        )

        # Create and run builder with both config and model_config
        builder = DictionaryBuilder(config, model_config)
        builder.build(input_data)

    except Exception as e:
        logger.error(f"Unexpected error in build_med_dict: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch medical dictionary definitions using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "input",
        help="Medical term, or path to JSON/text file containing terms"
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="The model to use for generating definitions (default: ollama/gemma3)"
    )

    args = parser.parse_args()
    build_med_dict(args.input, args.model)
