import logging
from typing import List, Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Medication(BaseModel):
    """Structured data for a single medication."""

    name: str = Field(description="Name of the medication")
    dosage: str = Field(description="Dosage of the medication (e.g., 500mg)")
    frequency: str = Field(
        description="Frequency of administration (e.g., BID, TID, Once daily)"
    )
    route: str = Field(description="Route of administration (e.g., Oral, Topical, IV)")
    duration: str = Field(description="Duration of treatment (e.g., 7 days, 1 month)")


class PrescriptionData(BaseModel):
    """Structured data for a medical prescription."""

    medications: List[Medication] = Field(description="List of medications prescribed")
    prescriber: str = Field(
        description="Name of the prescribing doctor or healthcare professional"
    )
    patient_name: str = Field(description="Name of the patient")
    date_prescribed: str = Field(description="Date the prescription was issued")


class PrescriptionExtractor:
    """Extracts prescription data from an image using LiteClient."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initializes the PrescriptionExtractor with a LiteClient.

        Args:
            config: Optional ModelConfig. If not provided, a default gemini-1.5-flash config is used.
        """
        if config is None:
            config = ModelConfig(model="ollama/gemma3:12b", temperature=0.2)

        self.client = LiteClient(config)

    def extract(self, image_path: str) -> PrescriptionData:
        """
        Extracts prescription details from an image.

        Args:
            image_path: Path to the prescription image file.

        Returns:
            PrescriptionData: Extracted and structured prescription details.

        Raises:
            Exception: If extraction fails.
        """
        logger.info(f"Extracting prescription data from image: {image_path}")

        # Comprehensive prompt for extraction
        prompt = (
            "Extract all available prescription details from the provided image. "
            "Ensure you capture all medications with their dosage, frequency, route, "
            "and duration. Also capture the prescriber's name, patient's name, "
            "and the date prescribed. If any field is not clearly visible, return 'Not specified'."
        )

        model_input = ModelInput(
            user_prompt=prompt, image_path=image_path, response_format=PrescriptionData
        )

        try:
            logger.debug("Calling LiteClient for structured extraction...")
            result = self.client.generate_text(model_input=model_input)

            if result and result.data:
                logger.info("✓ Successfully extracted prescription data")
                return result.data

            # If structured data is not available, we could attempt to parse the markdown
            # but for now we expect structured data as per LiteClient capability.
            if result and result.markdown:
                logger.warning("Model returned markdown instead of structured data.")
                # Basic parsing or error handling could go here.

            raise ValueError(
                "Failed to extract structured prescription data from the image."
            )

        except Exception as e:
            logger.error(f"✗ Error during prescription extraction: {e}")
            raise
