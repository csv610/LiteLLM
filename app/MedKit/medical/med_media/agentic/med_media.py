import logging
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .ddg_images import DuckDuckImages
    from .ddg_videos import DuckDuckVideos
    from .med_media_models import (
        MediaCaptionModel,
        MediaSummaryModel,
        ModelOutput,
    )
    from .med_media_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.med_media.agentic.ddg_images import DuckDuckImages
    from medical.med_media.agentic.ddg_videos import DuckDuckVideos
    from medical.med_media.agentic.med_media_models import (
        MediaCaptionModel,
        MediaSummaryModel,
        ModelOutput,
    )
    from medical.med_media.agentic.med_media_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalMediaGenerator:
    """Generates medical media information, downloads content, and provides AI analysis."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.image_searcher = DuckDuckImages()
        self.video_searcher = DuckDuckVideos()
        self.last_topic = None

    def download_images(
        self,
        query: str,
        num_images: int = 3,
        size: str = "Medium",
        output_dir: Path = Path("outputs/images"),
    ):
        """Search and download medical images."""
        logger.info(f"Searching for images: {query}")
        urls = self.image_searcher.get_urls(query, size, num_images)
        downloaded = []
        for i, url in enumerate(urls):
            filename = self.image_searcher.download_image(
                url, str(output_dir), query, i
            )
            if filename:
                downloaded.append(output_dir / filename)
        return downloaded

    def search_videos(self, query: str, max_results: int = 5):
        """Search for medical videos (returns metadata/URLs)."""
        logger.info(f"Searching for videos: {query}")
        return self.video_searcher.get_urls(query, max_results)

    def generate_caption(
        self, topic: str, media_type: str = "image", structured: bool = False
    ) -> ModelOutput:
        """Generate a 3-tier professional medical caption."""
        self.last_topic = topic
        logger.info(f"Starting 3-tier caption generation for: {topic}")

        try:
            # 1. Specialist Stage (JSON)
            spec_input = ModelInput(
                system_prompt=PromptBuilder.create_system_prompt(),
                user_prompt=PromptBuilder.create_caption_prompt(topic, media_type),
                response_format=MediaCaptionModel if structured else None,
            )
            spec_res = self.client.generate_text(spec_input)
            spec_json = spec_res.data.model_dump_json(indent=2) if structured else spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            audit_sys, audit_usr = PromptBuilder.create_accuracy_auditor_prompts(topic, spec_json)
            audit_res = self.client.generate_text(ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None
            ))
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown)
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(topic, spec_json, audit_json)
            final_res = self.client.generate_text(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )
        except Exception as e:
            logger.error(f"✗ 3-tier Caption generation failed: {e}")
            raise

    def generate_summary(
        self, topic: str, media_type: str = "video", structured: bool = False
    ) -> ModelOutput:
        """Generate a 3-tier medical summary."""
        self.last_topic = topic
        logger.info(f"Starting 3-tier summary generation for: {topic}")

        try:
            # 1. Specialist Stage (JSON)
            spec_input = ModelInput(
                system_prompt=PromptBuilder.create_system_prompt(),
                user_prompt=PromptBuilder.create_summary_prompt(topic, media_type),
                response_format=MediaSummaryModel if structured else None,
            )
            spec_res = self.client.generate_text(spec_input)
            spec_json = spec_res.data.model_dump_json(indent=2) if structured else spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            audit_sys, audit_usr = PromptBuilder.create_accuracy_auditor_prompts(topic, spec_json)
            audit_res = self.client.generate_text(ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None
            ))
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown)
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(topic, spec_json, audit_json)
            final_res = self.client.generate_text(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )
        except Exception as e:
            logger.error(f"✗ 3-tier Summary generation failed: {e}")
            raise

    def save(
        self, result: ModelOutput, output_dir: Path, suffix: str = "analysis"
    ) -> Path:
        """Saves the AI analysis to a file."""
        if not self.last_topic:
            filename = "media_analysis"
        else:
            filename = f"{self.last_topic.lower().replace(' ', '_')}_{suffix}"

        return save_model_response(result, output_dir / filename)
