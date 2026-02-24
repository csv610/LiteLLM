import logging
from pathlib import Path
from typing import List, Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

# Import utils
from utils.ddg_images import DuckDuckImages
from utils.ddg_videos import DuckDuckVideos

from .med_media_models import MedicalMediaModel, MediaCaptionModel, MediaSummaryModel, ModelOutput
from .med_media_prompts import PromptBuilder

logger = logging.getLogger(__name__)

class MedicalMediaGenerator:
    """Generates medical media information, downloads content, and provides AI analysis."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.image_searcher = DuckDuckImages()
        self.video_searcher = DuckDuckVideos()
        self.last_topic = None

    def download_images(self, query: str, num_images: int = 3, size: str = "Medium", output_dir: Path = Path("outputs/images")):
        """Search and download medical images."""
        logger.info(f"Searching for images: {query}")
        urls = self.image_searcher.get_urls(query, size, num_images)
        downloaded = []
        for i, url in enumerate(urls):
            filename = self.image_searcher.download_image(url, str(output_dir), query, i)
            if filename:
                downloaded.append(output_dir / filename)
        return downloaded

    def search_videos(self, query: str, max_results: int = 5):
        """Search for medical videos (returns metadata/URLs)."""
        logger.info(f"Searching for videos: {query}")
        return self.video_searcher.get_urls(query, max_results)

    def generate_caption(self, topic: str, media_type: str = "image", structured: bool = False) -> ModelOutput:
        """Generate a professional medical caption for a topic."""
        self.last_topic = topic
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_caption_prompt(topic, media_type),
            response_format=MediaCaptionModel if structured else None
        )
        return self.client.generate_text(model_input)

    def generate_summary(self, topic: str, media_type: str = "video", structured: bool = False) -> ModelOutput:
        """Generate a medical summary for a topic."""
        self.last_topic = topic
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_summary_prompt(topic, media_type),
            response_format=MediaSummaryModel if structured else None
        )
        return self.client.generate_text(model_input)

    def save(self, result: ModelOutput, output_dir: Path, suffix: str = "analysis") -> Path:
        """Saves the AI analysis to a file."""
        if not self.last_topic:
            filename = "media_analysis"
        else:
            filename = f"{self.last_topic.lower().replace(' ', '_')}_{suffix}"
        
        return save_model_response(result, output_dir / filename)
