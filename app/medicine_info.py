import sys
import json
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


class MedicineInfo(BaseModel):
    name: str = Field(..., description="The generic name of the medicine.")
    brand_name: str = Field(..., description="The common brand name for the medicine.")
    description: str = Field(..., description="A brief description of how the medicine works and its primary uses.")
    history: str = Field(..., description="A brief history of the medicine including the approval date from medical uses.")
    active_ingredient: str = Field(..., description="The main chemical component of the medicine.")
    uses: list[str] = Field(..., description="A list of medical conditions the medicine is used to treat.")
    side_effects: list[str] = Field(..., description="A list of common side effects associated with the medicine.")


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

    # Parse and print the formatted JSON output
    if isinstance(response_content, str):
        data = json.loads(response_content)
        print(json.dumps(data, indent=4))
    else:
        print("Error: Expected string response from model")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python medicine_info.py <medicine_name>")
        sys.exit(1)
    medicine = sys.argv[1]
    cli(medicine)
