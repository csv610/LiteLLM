"""medkit_client - Medical Content Generation with Gemini and Pydantic Schema Support.

A specialized wrapper around Google's Gemini API that provides domain-specific
functionality for generating medical content with guaranteed structured output.
This client extends GeminiClient with medical expertise context and integrates
PydanticPromptGenerator for sophisticated schema-aware prompt engineering.

Provides high-level methods for generating medical documentation, clinical decision
trees, procedure guides, and medical knowledge bases. All outputs are validated
against Pydantic schemas, ensuring data integrity and type safety. Includes
automatic retry logic, temperature optimization for factual medical content,
and support for both text generation and medical image analysis.

QUICK START:
    Generate structured medical content:

        from medkit_client import MedKitClient
        from pydantic import BaseModel, Field

        class ProcedureGuide(BaseModel):
            name: str = Field(description="Procedure name")
            steps: list = Field(description="Step-by-step instructions")
            risks: list = Field(description="Known complications")

        client = MedKitClient()
        guide = client.generate_text(
            prompt="Explain the colonoscopy procedure",
            schema=ProcedureGuide
        )

COMMON USES:
    - Generating standardized medical decision trees
    - Creating procedure guidelines with risk documentation
    - Analyzing medical images with structured output
    - Building medical knowledge bases with validated schemas
    - Generating patient education materials with consistent formatting
    - Creating clinical protocol documentation

KEY FEATURES:
    - Automatic schema-aware prompt generation from Pydantic models
    - Low temperature settings (0.3) for factual medical accuracy
    - Integrated image analysis with base64 encoding
    - Configurable prompt styles (DETAILED, CONCISE, TECHNICAL)
    - Built-in retry logic (max 3 attempts) with exponential backoff
    - JSON response validation against schemas
    - Support for markdown JSON extraction from LLM responses
"""

import base64
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ValidationError

from medkit.core.gemini_client import GeminiClient, ModelConfig, ModelInput
from medkit.utils.pydantic_prompt_generator import PydanticPromptGenerator, PromptStyle
from medkit.utils.storage_config import StorageConfig

logger = logging.getLogger(__name__)


@dataclass
class MedKitConfig(StorageConfig):
    """
    Centralized configuration for MedKit modules.

    Combines storage configuration (from StorageConfig) with standard module
    settings for output, logging, and verbosity control.

    Attributes:
        db_path: Path to LMDB database (inherited from StorageConfig)
        db_capacity_mb: Database capacity in MB (inherited from StorageConfig)
        db_store: Whether to cache results (inherited from StorageConfig)
        db_overwrite: Whether to overwrite cached results (inherited from StorageConfig)
        output_dir: Directory for module output files
        log_file: Path to log file for this module
        verbosity: Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG)

    Example:
        >>> config = MedKitConfig(
        ...     db_path="/path/to/db.lmdb",
        ...     output_dir=Path("outputs"),
        ...     verbosity=3  # INFO level
        ... )
        >>> # Use in a module
        >>> generator = MyModule(config=config)
    """
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    log_file: Optional[Path] = None
    verbosity: int = 2  # Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Validate verbosity level
        if not 0 <= self.verbosity <= 4:
            raise ValueError("verbosity must be between 0 and 4")

        # Call parent validation
        super().__post_init__()


class MedKitClient(GeminiClient):
    """
    Extended GeminiClient for medical content generation and image analysis.

    Inherits all retry logic and error handling from GeminiClient.
    """

    def __init__(self, model_name: str = "gemini-2.5-flash", **kwargs):
        """
        Initialize MedKitClient with optimized configuration.

        Args:
            model_name: Gemini model to use
            **kwargs: Additional arguments passed to GeminiClient
        """
        logger.info(f"Initializing MedKitClient with model: {model_name}")
        config = ModelConfig(
            model_name=model_name,
            max_retries=3,
            initial_delay=1.0,
            temperature=0.3,
        )
        logger.debug(f"MedKitClient config: max_retries=3, initial_delay=1.0s, temperature=0.3")
        super().__init__(config=config, **kwargs)
        logger.info("MedKitClient initialized successfully")

    def generate_text(
        self,
        prompt: str,
        schema: type[BaseModel],
        sys_prompt: str = None,
    ) -> BaseModel:
        """
        Generate structured text with schema validation.

        Args:
            prompt: User prompt describing the task
            schema: Pydantic model for structured output
            sys_prompt: System prompt for context (optional)

        Returns:
            Validated Pydantic model instance with generated data
        """
        schema_name = schema.__name__
        logger.info(f"Starting text generation with schema: {schema_name}")
        logger.debug(f"Prompt length: {len(prompt)} chars, System prompt provided: {sys_prompt is not None}")

        try:
            # Generate schema-aware prompt from Pydantic schema
            logger.debug(f"Generating schema-aware prompt for {schema_name}")
            generator = PydanticPromptGenerator(
                schema,
                style=PromptStyle.DETAILED,
                include_examples=True,
                validate_schema=True,
            )
            schema_prompt = generator.generate_prompt()
            logger.debug(f"Schema prompt generated, length: {len(schema_prompt)} chars")

            user_prompt = f"{prompt}\n\n{schema_prompt}"

            model_input = ModelInput(
                user_prompt=user_prompt,
                sys_prompt=sys_prompt,
                response_schema=schema,
            )

            logger.debug(f"Calling generate_content for schema: {schema_name}")
            result = self.generate_content(model_input)
            logger.info(f"Successfully generated text with schema: {schema_name}")
            return result

        except ValidationError as e:
            logger.error(f"Schema validation failed for {schema_name}: {e.error_count()} errors", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Text generation failed for schema {schema_name}: {type(e).__name__}: {str(e)}", exc_info=True)
            raise

    def analyze_image(
        self,
        image_data: str,
        schema: type[BaseModel],
        prompt: str,
        sys_prompt: Optional[str] = None,
        mime_type: str = "image/jpeg",
        temperature: float = 0.3,
    ) -> BaseModel:
        """
        General-purpose image analysis with structured output.

        Args:
            image_data: Base64 encoded image data
            schema: Pydantic model for structured output
            prompt: User prompt describing the analysis task
            sys_prompt: System prompt for context (optional)
            mime_type: MIME type of the image (default: image/jpeg)
            temperature: Model temperature for response (default: 0.3 for accurate extraction)

        Returns:
            Validated Pydantic model instance with extracted/analyzed data
        """
        schema_name = schema.__name__
        logger.info(f"Starting image analysis with schema: {schema_name}, mime_type: {mime_type}, temperature: {temperature}")
        logger.debug(f"Image data size: {len(image_data)} chars (base64), System prompt provided: {sys_prompt is not None}")

        try:
            from google import genai

            # Prepare the image part
            logger.debug(f"Decoding base64 image data")
            image_part = genai.types.Part.from_bytes(
                data=base64.b64decode(image_data),
                mime_type=mime_type
            )

            # Create content with image and prompt
            contents = [
                genai.types.Content(
                    role="user",
                    parts=[image_part, genai.types.Part(text=prompt)]
                )
            ]

            # Prepare config
            config_params = {
                'temperature': temperature,
                'response_mime_type': 'application/json'
            }
            if sys_prompt:
                config_params['system_instruction'] = sys_prompt
            logger.debug(f"Config prepared: {list(config_params.keys())}")
            config = genai.types.GenerateContentConfig(**config_params)

            # Generate response
            logger.debug(f"Calling Gemini API for image analysis")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )

            # Parse response
            result_text = response.text
            logger.debug(f"API response received, length: {len(result_text)} chars")

            try:
                logger.debug(f"Attempting direct JSON parsing")
                extracted_json = json.loads(result_text)
                logger.debug(f"JSON parsed successfully")
            except json.JSONDecodeError as parse_error:
                logger.warning(f"Direct JSON parsing failed, attempting markdown extraction")
                # Try to extract JSON from markdown if needed
                if "```json" in result_text:
                    logger.debug(f"Found ```json block, extracting")
                    json_str = result_text.split("```json")[1].split("```")[0].strip()
                    extracted_json = json.loads(json_str)
                    logger.debug(f"Successfully extracted JSON from ```json block")
                elif "```" in result_text:
                    logger.debug(f"Found ``` block, extracting")
                    json_str = result_text.split("```")[1].split("```")[0].strip()
                    extracted_json = json.loads(json_str)
                    logger.debug(f"Successfully extracted JSON from ``` block")
                else:
                    logger.error(f"Could not find JSON or markdown blocks in response")
                    raise ValueError(f"Could not parse image analysis result: {result_text}") from parse_error

            # Validate against schema
            logger.debug(f"Validating extracted JSON against schema: {schema_name}")
            result = schema(**extracted_json)
            logger.info(f"Successfully analyzed image and validated with schema: {schema_name}")
            return result

        except ValidationError as e:
            logger.error(f"Schema validation failed for {schema_name}: {e.error_count()} errors", exc_info=True)
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed in image analysis: {str(e)}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Image analysis failed for schema {schema_name}: {type(e).__name__}: {str(e)}", exc_info=True)
            raise
