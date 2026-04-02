#!/usr/bin/env python3
"""
Guardrail System - Analyzes text and images for safety violations using 3-tier approach.
"""

import asyncio
import hashlib
import logging
import re
import sys
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from app.Quadrails.shared.models import GuardrailResponse, ImageGuardrailResponse, PreprocessingError, AnalysisError, ModelOutput
from app.Quadrails.shared.prompts import PromptBuilder

logger = logging.getLogger(__name__)
sys.modules.setdefault("guardrail", sys.modules[__name__])


def configure_module_logging() -> None:
    """Configure module logging explicitly."""
    logging_config.configure_logging(str(Path(__file__).parent / "logs" / "guardrail.log"))


class BaseGuardrailAgent:
    """Shared functionality for guardrail agents."""

    def __init__(self, config: Optional[ModelConfig] = None, max_length: int = 4000):
        self.config = config or ModelConfig(model="ollama/gemma3", temperature=0.1)
        self.client = LiteClient(self.config)
        self.max_length = max_length
        self._cache: Dict[str, Any] = {}

    def _get_cache_key(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _preprocess_text(self, text: str) -> str:
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

    async def analyze_text(self, text: str, use_cache: bool = True) -> ModelOutput:
        """Asynchronously analyze text using 3-tier artifact approach."""
        cleaned_text = self._preprocess_text(text)
        if not cleaned_text:
            raise PreprocessingError("Input text is empty after pre-processing.")

        cache_key = self._get_cache_key(cleaned_text)
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        try:
            # Tier 1: Specialist Analysis (JSON)
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=PromptBuilder.get_user_prompt(cleaned_text),
                response_format=GuardrailResponse
            )

            loop = asyncio.get_event_loop()
            spec_res = await loop.run_in_executor(None, self.client.generate_text, model_input)
            spec_data: GuardrailResponse = spec_res.data
            spec_data.text = cleaned_text

            # Tier 3: Output Synthesis (Markdown Closer)
            synth_prompt = f"Synthesize a professional safety audit report for the following text analysis.\n\nDATA:\n{spec_data.model_dump_json(indent=2)}"
            synth_input = ModelInput(
                system_prompt="You are a Lead Safety Compliance Editor. Synthesize raw guardrail data into a clear Markdown report with Verdict and Severity sections.",
                user_prompt=synth_prompt,
                response_format=None
            )
            final_markdown_res = await loop.run_in_executor(None, self.client.generate_text, synth_input)
            final_markdown = final_markdown_res.markdown

            output = ModelOutput(
                data=spec_data,
                markdown=final_markdown,
                metadata={"type": "text_guardrail", "raw_cleaned_text": cleaned_text}
            )

            if use_cache:
                self._cache[cache_key] = output
            return output
        except Exception as e:
            raise AnalysisError(f"Text analysis failed: {str(e)}")


class ImageGuardrailAgent(BaseGuardrailAgent):
    """Agent responsible for image safety analysis."""

    def _get_image_cache_key(self, path: Path) -> str:
        resolved_path = path.resolve()
        stats = resolved_path.stat()
        cache_input = f"{resolved_path}:{stats.st_size}:{stats.st_mtime_ns}"
        return self._get_cache_key(cache_input)

    async def analyze_image(self, image_path: str, use_cache: bool = True) -> ModelOutput:
        """Asynchronously analyze an image using 3-tier artifact approach."""
        path = Path(image_path)
        if not path.exists():
            raise PreprocessingError(f"Image file not found: {image_path}")

        cache_key = self._get_image_cache_key(path)
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        try:
            # Tier 1: Specialist Analysis (JSON)
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_image_system_prompt(),
                user_prompt=PromptBuilder.get_image_user_prompt(),
                image_path=str(path.absolute()),
                response_format=ImageGuardrailResponse
            )

            loop = asyncio.get_event_loop()
            spec_res = await loop.run_in_executor(None, self.client.generate_text, model_input)
            spec_data: ImageGuardrailResponse = spec_res.data
            spec_data.image_path = str(path.absolute())

            # Tier 3: Output Synthesis (Markdown Closer)
            synth_prompt = f"Synthesize a professional image safety audit report.\n\nDATA:\n{spec_data.model_dump_json(indent=2)}"
            synth_input = ModelInput(
                system_prompt="You are a Lead Visual Safety Editor. Synthesize raw image guardrail data into a clear Markdown report with Verdict and Category sections.",
                user_prompt=synth_prompt,
                response_format=None
            )
            final_markdown_res = await loop.run_in_executor(None, self.client.generate_text, synth_input)
            final_markdown = final_markdown_res.markdown

            output = ModelOutput(
                data=spec_data,
                markdown=final_markdown,
                metadata={"type": "image_guardrail", "image_path": str(path.absolute())}
            )

            if use_cache:
                self._cache[cache_key] = output
            return output
        except Exception as e:
            raise AnalysisError(f"Image analysis failed: {str(e)}")


class GuardrailAnalyzer:
    """Coordinator that routes work to the text or image guardrail agent."""

    def __init__(self, config: Optional[ModelConfig] = None, max_length: int = 4000):
        configure_module_logging()
        self.text_agent = TextGuardrailAgent(config=config, max_length=max_length)
        self.image_agent = ImageGuardrailAgent(config=config, max_length=max_length)

    async def analyze_text(self, text: str, use_cache: bool = True) -> ModelOutput:
        return await self.text_agent.analyze_text(text, use_cache=use_cache)

    async def analyze_image(self, image_path: str, use_cache: bool = True) -> ModelOutput:
        return await self.image_agent.analyze_image(image_path, use_cache=use_cache)

    @staticmethod
    def display_results(output: ModelOutput):
        """Display synthesized Markdown results."""
        if not output or not output.markdown:
            print("\n❌ Error: No analysis result available.")
            return

        print(f"\n{'='*80}")
        print(f"GUARDRAIL ANALYSIS REPORT")
        print(f"{'='*80}")
        print(output.markdown)
        print(f"\n{'='*80}\n")
