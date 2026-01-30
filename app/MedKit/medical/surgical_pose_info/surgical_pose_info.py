"""Surgical Position Information Generator.

This module contains the core logic for generating comprehensive surgical position information.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.llm_client import LiteClient
from lite.models import ModelInput, ModelOutput
from lite.utils import save_model_response

from .surgical_pose_info_models import SurgicalPoseInfoModel
from .surgical_pose_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)

COMMON_SURGICAL_POSITIONS = [
    "Supine (Dorsal Decubitus)",
    "Dorsal Recumbent",
    "Hips-Flexed Supine",
    "Recumbent",
    "Head-Elevated Supine",
    "Sniffing Position",
    "Trendelenburg Position",
    "Reverse Trendelenburg",
    "Lateral (Right/Left)",
    "Lateral Kidney Position",
    "Lithotomy Position",
    "Prone Position",
    "Jackknife Position",
    "Knee-Chest Position",
    "Sims' Position (Left Lateral)",
    "Fowler's Position",
    "High Fowler's",
    "Semi-Fowler's",
    "Orthopneic Position",
    "Knee-Chest",
    "Lloyd-Davies Position",
    "Kraske Position",
    "Modified Lithotomy",
    "Legs-Elevated Supine",
    "Beach Chair Position",
    "Sitting Position",
    "Lateral Decubitus",
    "Oblique Position",
    "Reverse Trendelenburg with Head Up",
    "Rotational Bed Position",
    "Frog-Leg Position",
    "Cradle Position",
    "Swaddled Supine",
    "Recovery Position",
    "Shock Position",
    "Neutral Spine Immobilization Position"
]


class SurgicalPoseInfoGenerator:
    """Generates comprehensive surgical position information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.pose = None  # Store the position being analyzed
        logger.debug(f"Initialized SurgicalPoseInfoGenerator")

    def generate_text(self, pose: str, structured: bool = False) -> ModelOutput:
        """Generates comprehensive surgical position information."""
        if not pose or not str(pose).strip():
            raise ValueError("Position name cannot be empty")

        # Store the pose for later use in save
        self.pose = pose
        logger.debug(f"Starting surgical position information generation for: {pose}")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(pose)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = SurgicalPoseInfoModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.info("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated surgical position information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical position information: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the surgical position information to a file."""
        if self.pose is None:
            raise ValueError("No position information available. Call generate_text first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.pose.lower().replace(' ', '_')}"
        
        return save_model_response(result, output_dir / base_filename)
