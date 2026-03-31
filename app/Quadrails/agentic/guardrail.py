#!/usr/bin/env python3
"""
Guardrail System - Analyzes text and images for safety violations.
Uses LiteClient to perform content moderation.
"""

import asyncio
import hashlib
import logging
import re
from pathlib import Path
from typing import Any, Dict, Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from .guardrail_models import GuardrailResponse, ImageGuardrailResponse, PreprocessingError, AnalysisError
from .guardrail_prompts import PromptBuilder

logger = logging.getLogger(__name__)


def configure_module_logging() -> None:
    """Configure module logging explicitly instead of at import time."""
    logging_config.configure_logging(str(Path(__file__).parent / "logs" / "guardrail.log"))


class BaseGuardrailAgent:
    """Shared functionality for guardrail agents."""

    def __init__(self, config: Optional[ModelConfig] = None, max_length: int = 4000):
        """Initialize the agent."""
        self.config = config or ModelConfig(model="ollama/gemma3", temperature=0.1)
        self.client = LiteClient(self.config)
        self.max_length = max_length
        self._cache: Dict[str, Any] = {}

    def _get_cache_key(self, data: str) -> str:
        """Generate a stable hash for caching."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _preprocess_text(self, text: str) -> str:
        """Clean and truncate input text."""
        try:
            if not text:
                return ""
            text = "".join(ch for ch in text if ord(ch) >= 32 or ch in "\n\r\t")
            text = re.sub(r'\s+', ' ', text).strip()
            if len(text) > self.max_length:
                text = text[:self.max_length]
            return text
        except Exception as e:
            raise PreprocessingError(f"Pre-processing failed: {str(e)}")


class TextGuardrailAgent(BaseGuardrailAgent):
    """Agent responsible for text safety analysis."""

    async def analyze_text(self, text: str, use_cache: bool = True) -> GuardrailResponse:
        """Asynchronously analyze text for safety violations."""
        cleaned_text = self._preprocess_text(text)
        if not cleaned_text:
            raise PreprocessingError("Input text is empty after pre-processing.")

        cache_key = self._get_cache_key(cleaned_text)
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        try:
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=PromptBuilder.get_user_prompt(cleaned_text),
                response_format=GuardrailResponse
            )

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.client.generate, model_input)

            if isinstance(response, GuardrailResponse):
                response.text = cleaned_text
                if use_cache:
                    self._cache[cache_key] = response
                return response
            else:
                raise AnalysisError("No structured output received from model.")
        except AnalysisError:
            raise
        except Exception as e:
            raise AnalysisError(f"Analysis failed: {str(e)}")


class ImageGuardrailAgent(BaseGuardrailAgent):
    """Agent responsible for image safety analysis."""

    def _get_image_cache_key(self, path: Path) -> str:
        """Cache based on file identity and content metadata, not just path."""
        resolved_path = path.resolve()
        stats = resolved_path.stat()
        cache_input = f"{resolved_path}:{stats.st_size}:{stats.st_mtime_ns}"
        return self._get_cache_key(cache_input)

    async def analyze_image(self, image_path: str, use_cache: bool = True) -> ImageGuardrailResponse:
        """Asynchronously analyze an image for safety violations."""
        path = Path(image_path)
        if not path.exists():
            raise PreprocessingError(f"Image file not found: {image_path}")

        cache_key = self._get_image_cache_key(path)
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        try:
            logger.info(f"Starting async image analysis: {image_path}")

            # Using image_path directly in ModelInput as per lite/config.py
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_image_system_prompt(),
                user_prompt=PromptBuilder.get_image_user_prompt(),
                image_path=str(path.absolute()),
                response_format=ImageGuardrailResponse
            )

            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, self.client.generate, model_input)

            if isinstance(response, ImageGuardrailResponse):
                response.image_path = str(path.absolute())
                if use_cache:
                    self._cache[cache_key] = response
                return response
            else:
                raise AnalysisError("No structured output received for image analysis.")
        except AnalysisError:
            raise
        except Exception as e:
            logger.error(f"Image analysis error: {str(e)}")
            raise AnalysisError(f"Image analysis failed: {str(e)}")


class GuardrailAnalyzer:
    """Coordinator that routes work to the text or image guardrail agent."""

    def __init__(self, config: Optional[ModelConfig] = None, max_length: int = 4000):
        configure_module_logging()
        self.text_agent = TextGuardrailAgent(config=config, max_length=max_length)
        self.image_agent = ImageGuardrailAgent(config=config, max_length=max_length)

    async def analyze_text(self, text: str, use_cache: bool = True) -> GuardrailResponse:
        """Delegate text analysis to the text guardrail agent."""
        return await self.text_agent.analyze_text(text, use_cache=use_cache)

    async def analyze_image(self, image_path: str, use_cache: bool = True) -> ImageGuardrailResponse:
        """Delegate image analysis to the image guardrail agent."""
        return await self.image_agent.analyze_image(image_path, use_cache=use_cache)

    @staticmethod
    def display_results(result: Any):
        """Display analysis results (Text or Image)."""
        if not result:
            print("\n❌ Error: No analysis result available.")
            return

        is_image = isinstance(result, ImageGuardrailResponse)
        
        print(f"\n{'='*80}")
        print(f"GUARDRAIL {'IMAGE ' if is_image else ''}ANALYSIS RESULTS")
        print(f"{'='*80}")
        
        if is_image:
            print(f"\nIMAGE PATH: {result.image_path}")
        else:
            print(f"\nINPUT TEXT: \"{result.text[:100]}{'...' if len(result.text) > 100 else ''}\"")
            
        print(f"\nOVERALL SAFETY: {'✅ SAFE' if result.is_safe else '⚠️  FLAGGED'}")
        print(f"\nSUMMARY: {result.summary}")
        
        if result.flagged_categories:
            print("\nFLAGGED CATEGORIES:")
            for category_result in result.flagged_categories:
                print(f"  - {category_result.category.value.upper()}:")
                print(f"    Confidence: {category_result.score:.2f}")
                print(f"    Reasoning: {category_result.reasoning}")
        else:
            print("\nNO SAFETY VIOLATIONS DETECTED.")
            
        print(f"\n{'='*80}\n")
