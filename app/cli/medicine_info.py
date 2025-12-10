import sys
import json
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


def cli(medicine):
    """Fetch medicine information using LiteClient."""
    model = "gemini/gemini-2.5-flash"

    model_config = ModelConfig(model=model, temperature=0.2)
    client = LiteClient(model_config=model_config)

    prompt = f"Provide detailed information about the medicine {medicine}."
    model_input = ModelInput(user_prompt=prompt, response_format=MedicineResponse)

    response_content = client.generate_text(model_input=model_input)

    # Parse and save the formatted JSON output
    if isinstance(response_content, str):
        data = json.loads(response_content)
        output_file = f"{medicine}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Medicine information saved to {output_file}")
    else:
        print("Error: Expected string response from model")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python medicine_info.py <medicine_name>")
        sys.exit(1)
    medicine = sys.argv[1]
    cli(medicine)
