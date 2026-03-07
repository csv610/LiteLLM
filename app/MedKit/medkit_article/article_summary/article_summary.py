"""Summarize medical articles using chunked processing for long documents."""

import json
import logging
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.logging_config import configure_logging

try:
    from .article_summary_models import ChunkSummary, FinalSummary
    from .article_summary_prompts import PromptBuilder
except (ImportError, ValueError):
    from article_summary_models import ChunkSummary, FinalSummary
    from article_summary_prompts import PromptBuilder

# Setup logging
log_file = Path(__file__).parent / "logs" / "summarization.log"
log_file.parent.mkdir(exist_ok=True)
configure_logging(log_file=str(log_file))
logger = logging.getLogger(__name__)


class ArticleSummarizer:
    """Summarize long articles by chunking them and combining the results."""

    def __init__(self, model: str = "ollama/gemma3"):
        """
        Initialize the ArticleSummarizer.

        Args:
            model: LiteClient model to use for summarization
        """
        self.model = model

        try:
            model_config = ModelConfig(model=model, temperature=0.2)
            self.client = LiteClient(model_config=model_config)
            logger.info(f"Client created with model: {model}")
        except Exception as e:
            logger.error(f"Failed to create client: {e}")
            raise

    def _extract_text_from_object(self, obj) -> str:
        """Recursively extract all text values from nested objects."""
        texts = []
        if isinstance(obj, dict):
            for value in obj.values():
                texts.append(self._extract_text_from_object(value))
        elif isinstance(obj, list):
            for item in obj:
                texts.append(self._extract_text_from_object(item))
        elif isinstance(obj, str):
            texts.append(obj)
        return " ".join(filter(None, texts))

    def load_file(self, file_path: str) -> list[dict]:
        """Auto-detect and parse file based on extension."""
        path = Path(file_path).expanduser()
        ext = path.suffix.lower()

        if ext == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = []
            if isinstance(data, list):
                for i, item in enumerate(data):
                    items.append(
                        {"id": str(i + 1), "text": self._extract_text_from_object(item)}
                    )
            else:
                items.append({"id": "1", "text": self._extract_text_from_object(data)})
            return items
        else:
            # Default for .txt, .md, etc.
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return [{"id": "1", "text": content}]

    def _chunk_text(
        self, text: str, chunk_size: int = 100000, overlap_ratio: float = 0.1
    ) -> list[str]:
        """Split text into chunks with specified overlap."""
        if not text:
            return []

        overlap_size = int(chunk_size * overlap_ratio)
        step_size = max(1, chunk_size - overlap_size)

        chunks = []
        for i in range(0, len(text), step_size):
            chunk = text[i : i + chunk_size]
            chunks.append(chunk)
            if i + chunk_size >= len(text):
                break

        logger.info(
            f"Split text into {len(chunks)} chunks with size {chunk_size} and overlap {overlap_size}"
        )
        return chunks

    def summarize_article(
        self, text: str, chunk_size: int = 100000, overlap_ratio: float = 0.1
    ) -> str:
        """Summarize a long article using chunking."""
        chunks = self._chunk_text(
            text, chunk_size=chunk_size, overlap_ratio=overlap_ratio
        )

        if not chunks:
            return ""

        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            try:
                logger.info(f"Summarizing chunk {i + 1}/{len(chunks)}")
                prompt = PromptBuilder.get_chunk_summary_prompt(chunk)
                model_input = ModelInput(
                    user_prompt=prompt, response_format=ChunkSummary
                )
                response = self.client.generate_text(model_input=model_input)
                chunk_summaries.append(response.summary)
            except Exception as e:
                logger.error(f"Error summarizing chunk {i + 1}: {e}")

        if not chunk_summaries:
            return "Failed to generate chunk summaries."

        if len(chunk_summaries) == 1:
            return chunk_summaries[0]

        try:
            logger.info("Generating final summary from chunks...")
            prompt = PromptBuilder.get_final_summary_prompt(chunk_summaries)
            model_input = ModelInput(user_prompt=prompt, response_format=FinalSummary)
            final_response = self.client.generate_text(model_input=model_input)
            return final_response.summary
        except Exception as e:
            logger.error(f"Error generating final summary: {e}")
            return " ".join(chunk_summaries)
