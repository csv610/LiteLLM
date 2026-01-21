import sys
import json
import argparse
import logging
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from logging_util import setup_logging

# Configure logging
log_file = Path(__file__).parent / "logs" / "medicine_info.log"
logger = setup_logging(str(log_file))

class MedicineInfo(BaseModel):
    name: str = Field(..., description="The generic name of the medicine.")
    brand_name: str = Field(..., description="The common brand name for the medicine.")
    alternative_names: list[str] = Field(default=[], description="Other generic names, synonyms, or brand names for the medicine.")
    description: str = Field(..., description="A brief description of how the medicine works and its primary uses.")
    history: str = Field(..., description="A brief history of the medicine including the approval date from medical uses.")
    active_ingredient: str = Field(..., description="The main chemical component of the medicine.")
    chemical_formula: str = Field(default="", description="The molecular or chemical formula of the medicine.")
    uses: list[str] = Field(..., description="A list of medical conditions the medicine is used to treat.")
    dosage_information: str = Field(default="", description="Recommended doses, frequency, and administration method.")
    side_effects: list[str] = Field(..., description="A list of common side effects associated with the medicine.")
    contraindications: list[str] = Field(default=[], description="Medical conditions or circumstances where the medicine should not be used.")
    drug_interactions: list[str] = Field(default=[], description="Other drugs or substances that may interact with this medicine.")
    warnings: list[str] = Field(default=[], description="Serious warnings and precautions for this medicine.")
    storage_instructions: str = Field(default="", description="How to properly store and handle the medicine.")
    cost_information: str = Field(default="", description="Approximate cost, price ranges, or insurance coverage information.")
    availability_status: str = Field(default="", description="OTC vs prescription status and regional availability.")
    manufacturer: str = Field(default="", description="The pharmaceutical company that produces this medicine.")


class MedicineResponse(BaseModel):
    medicine: MedicineInfo


def create_client(model: str, temperature: float = 0.2) -> LiteClient:
    """Create and return a configured LiteClient instance."""
    try:
        model_config = ModelConfig(model=model, temperature=temperature)
        client = LiteClient(model_config=model_config)
        logger.info(f"Client created with model: {model}, temperature: {temperature}")
        return client
    except Exception as e:
        logger.error(f"Failed to create client: {e}")
        raise


def generate_prompt(medicine: str) -> str:
    """Generate the prompt for medicine information query."""
    prompt = f"Provide detailed information about the medicine {medicine}."
    logger.debug(f"Generated prompt: {prompt}")
    return prompt


def fetch_medicine_data(client: LiteClient, medicine: str) -> str | None:
    """Fetch medicine information from the API."""
    try:
        prompt = generate_prompt(medicine)
        model_input = ModelInput(user_prompt=prompt, response_format=MedicineResponse)
        response_content = client.generate_text(model_input=model_input)

        if not isinstance(response_content, str):
            logger.error("Expected string response from model")
            return None

        logger.info(f"Successfully fetched data for medicine: {medicine}")
        return response_content
    except Exception as e:
        logger.error(f"Failed to fetch medicine data: {e}")
        return None


def parse_response(response_content: str) -> dict | None:
    """Parse JSON response content."""
    try:
        data = json.loads(response_content)
        logger.debug("Successfully parsed JSON response")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        return None


def save_result(medicine: str, data: dict, output_dir: Path = None) -> Path | None:
    """Save medicine information to a JSON file."""
    try:
        if output_dir is None:
            output_dir = Path(__file__).parent / "outputs"

        output_dir.mkdir(exist_ok=True)
        filename = medicine.lower().replace(" ", "_")
        output_file = output_dir / f"{filename}.json"

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

        logger.info(f"Medicine information saved to {output_file}")
        print(f"Medicine information saved to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Failed to save result: {e}")
        return None


def cli(medicine: str, model: str, temperature: float = 0.2):
    """Main CLI function to fetch and save medicine information."""
    try:
        client = create_client(model, temperature)
        response_content = fetch_medicine_data(client, medicine)

        if response_content is None:
            print("Error: Failed to fetch medicine information")
            return

        data = parse_response(response_content)

        if data is None:
            print("Error: Failed to parse response")
            return

        output_file = save_result(medicine, data)

        if output_file is None:
            print("Error: Failed to save results")
    except Exception as e:
        logger.error(f"Unexpected error in cli: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch detailed medicine information using AI"
    )
    parser.add_argument(
        "medicine",
        help="The name of the medicine to fetch information about"
    )
    parser.add_argument(
        "-m", "--model",
        default="gemini/gemini-2.5-flash",
        help="The model to use for generating medicine information (default: gemini/gemini-2.5-flash)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.2,
        help="Temperature for model response (default: 0.2)"
    )

    args = parser.parse_args()
    cli(args.medicine, args.model, args.temperature)
