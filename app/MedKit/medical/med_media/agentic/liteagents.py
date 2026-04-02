"""
liteagents.py - Unified for med_media
"""
from .ddg_videos import DuckDuckVideos\nfrom io import BytesIO\nimport requests\nfrom lite.utils import save_model_response\nfrom PIL import Image\nfrom ddgs import DDGS\nfrom app.MedKit.medical.med_media.shared.models import *\nimport logging\nfrom lite.lite_client import LiteClient\nfrom .ddg_images import DuckDuckImages\nfrom pathlib import Path\nimport os\nimport argparse\nfrom lite.config import ModelConfig\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.logging_config import configure_logging\nimport sys\nimport streamlit as st\n\n

class StVideoSearch:
    def __init__(self):
        self.video_searcher = DuckDuckVideos()
        st.session_state.setdefault("videos", [])
        st.session_state.setdefault("selected_title", "")
        st.session_state.setdefault("max_results", 10)

    def search_videos(self, title, max_results):
        if title.strip():
            st.session_state.selected_title = title.strip()
            st.session_state.max_results = max_results
            with st.spinner("Searching for videos..."):
                st.session_state.videos = self.video_searcher.get_urls(
                    st.session_state.selected_title,
                    max_results=st.session_state.max_results,
                )
            if not st.session_state.videos:
                st.info("No videos found for your search. Try a different query.")
        else:
            st.warning("Please enter a valid search query.")

    def show_videos(self):
        if st.session_state.videos:
            for i, video in enumerate(st.session_state.videos):
                if i >= st.session_state.max_results:
                    break
                with st.container():
                    st.markdown(f"### VideoID: {i}")
                    st.markdown(f"### Title: {video['title']}")
                    st.markdown(f"### Duration: {video['duration']}")
                    try:
                        st.video(video["url"])
                    except Exception:
                        st.warning(
                            "This video cannot be embedded. Please use the link above."
                        )

                    st.divider()

                    if st.button(f"Remove Video {i}", key=f"remove_video_{i}"):
                        st.session_state.videos.pop(i)
                        st.rerun()


class UIVideoApp:
    def __init__(self):
        self.app = StVideoSearch()

    def run(self):
        st.title("🔎 DuckDuckGo Video Finder")

        # Step 1: Input title
        title = st.text_input(
            "Enter a video title to search:", value=st.session_state.selected_title
        )

        # Step 2: Select number of results
        max_results = st.slider(
            "Select number of videos to retrieve:",
            min_value=1,
            max_value=50,
            value=st.session_state.max_results,
        )

        # Step 3: Search for videos
        if st.button("Search"):
            self.app.search_videos(title, max_results)

        self.app.show_videos()


if __name__ == "__main__":
    app = UIVideoApp()
    app.run()




class RenderImages:
    def __init__(self):
        self.image_searcher = DuckDuckImages()
        if "last_query" not in st.session_state:
            st.session_state.last_query = ""
        # Initialize object_images in session state
        if "object_images" not in st.session_state:
            st.session_state.object_images = {}

    def display_image(self, query, url):
        width, height = self.image_searcher.fetch_image_size(url)
        if width == 0 and height == 0:
            st.write(f"Could not retrieve image size for {url}.")
            return
        st.image(
            url,
            caption=f"Image - Size: {width}x{height}",
            width="stretch" if self.fit_image else "content",
        )
        if st.button("Remove Image", key=query + url):
            for query, urls in st.session_state.object_images.items():
                if url in urls:
                    st.session_state.object_images[query].remove(url)
            st.rerun()
        st.divider()

    def display_all_images(self):
        for query, urls in st.session_state.object_images.items():
            for url in urls:
                self.display_image(query, url)

    def fetch_object_images(self, query, image_size, num_images):
        st.write(f"Downloading images for {query} ")
        with st.spinner(f"Fetching images for '{query}'..."):
            new_urls = self.image_searcher.get_urls(query, image_size, num_images)
            for url in new_urls:
                self.display_image(query, url)
            st.session_state.object_images[query] = new_urls

    def fetch_all_images(self, query_input, image_size, num_images):
        queries = [q.strip() for q in query_input.split(",") if q.strip()]
        if query_input != st.session_state.last_query:
            st.session_state.last_query = query_input
            st.session_state.object_images = {}

        for q in queries:
            self.fetch_object_images(q, image_size, num_images)

        st.write("All images fetched")
        st.rerun()

    def save_images(self):
        # Create directory for saving images
        os.makedirs("downloaded_images", exist_ok=True)

        # Check if there are any images to save
        if not st.session_state.object_images:
            st.write("No images to save.")
            return

        for query, urls in st.session_state.object_images.items():
            for i, url in enumerate(urls):
                filename = self.image_searcher.download_image(
                    url, "downloaded_images", query, i
                )
                if filename:
                    st.write(f"Saved: {filename}")

    def get_sidebar_options(self):
        size = st.sidebar.selectbox(
            "Select image size:",
            options=["Large", "Medium", "Small", "Wallpaper"],
            index=0,
        )
        max_results = st.sidebar.number_input(
            "images per item:", min_value=1, value=5, step=1
        )
        self.fit_image = st.sidebar.checkbox("Fit Image", value=False)

        # Store the selected size in session state
        st.session_state.image_size = size
        return size, max_results

    def render(self, med_image):
        image_size, max_images_per_item = self.get_sidebar_options()

        # Check if the image size has changed
        if (
            "image_size" not in st.session_state
            or st.session_state.image_size != image_size
        ):
            st.session_state.object_images = {}  # Clear previous images if size changes
            st.session_state.image_size = image_size  # Update the stored image size

        # Image Search
        if st.button("Image Search"):
            st.session_state.query_input = med_image
            self.fetch_all_images(med_image, image_size, max_images_per_item)

        self.display_all_images()

        # Images download and save
        if st.session_state.object_images and st.sidebar.button("Save Images"):
            self.save_images()


if __name__ == "__main__":
    st.title("DuckDuckGo Image Search")
    med_image = st.text_input("Search Medical Images: ", "Give an image of lazy eye")
    app = RenderImages()
    app.render(med_image)


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .med_media import MedicalMediaGenerator
except (ImportError, ValueError):
    from medical.med_media.agentic.med_media import MedicalMediaGenerator

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="MedKit Media CLI - Search, download, and analyze medical media."
    )

    # Global arguments
    parser.add_argument(
        "-m", "--model", default="ollama/gemma3", help="Model to use for AI analysis."
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        default="outputs/media",
        help="Output directory for results.",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output (JSON)."
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Media tool subcommands"
    )

    # Image Download
    images_p = subparsers.add_parser(
        "images", help="Search and download medical images"
    )
    images_p.add_argument(
        "query", help="Search query (e.g., 'acne vulgaris', 'heart anatomy')"
    )
    images_p.add_argument(
        "-n", "--num", type=int, default=3, help="Number of images to download"
    )
    images_p.add_argument(
        "--size",
        choices=["Small", "Medium", "Large", "Wallpaper"],
        default="Medium",
        help="Image size filter",
    )

    # Video Search
    videos_p = subparsers.add_parser("videos", help="Search for medical videos")
    videos_p.add_argument(
        "query",
        help="Search query (e.g., 'laparoscopic surgery', 'diabetes education')",
    )
    videos_p.add_argument(
        "-n", "--num", type=int, default=5, help="Number of results to list"
    )

    # Caption Generation
    caption_p = subparsers.add_parser(
        "caption", help="Generate professional medical caption"
    )
    caption_p.add_argument("topic", help="Topic for the caption")
    caption_p.add_argument(
        "-t",
        "--type",
        default="image",
        choices=["image", "x-ray", "mri", "ct", "pathology"],
        help="Media type context",
    )

    # Summary Generation
    summary_p = subparsers.add_parser(
        "summary", help="Generate medical summary for educational content"
    )
    summary_p.add_argument("topic", help="Topic for the summary")
    summary_p.add_argument(
        "-t",
        "--type",
        default="video",
        choices=["video", "article", "lecture"],
        help="Media type context",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(
        log_file="medkit_media.log", verbosity=args.verbosity, enable_console=True
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = ModelConfig(model=args.model, temperature=0.2)
    generator = MedicalMediaGenerator(model_config)

    try:
        if args.command == "images":
            print(
                f"🔍 Searching and downloading {args.num} images for: {args.query}..."
            )
            downloaded = generator.download_images(
                args.query, args.num, args.size, output_dir / "images"
            )
            for path in downloaded:
                print(f"✓ Saved: {path}")

        elif args.command == "videos":
            print(f"🔍 Searching for medical videos: {args.query}...")
            results = generator.search_videos(args.query, args.num)
            if not results:
                print("No videos found.")
            else:
                for res in results:
                    print(f"- {res['title']} ({res['duration']}): {res['url']}")

        elif args.command == "caption":
            print(f"✍️ Generating caption for {args.type}: {args.topic}...")
            res = generator.generate_caption(
                args.topic, args.type, structured=args.structured
            )
            if res:
                path = generator.save(res, output_dir, suffix="caption")
                print(f"✓ Caption generated and saved to: {path}")

        elif args.command == "summary":
            print(f"✍️ Generating summary for {args.type}: {args.topic}...")
            res = generator.generate_summary(
                args.topic, args.type, structured=args.structured
            )
            if res:
                path = generator.save(res, output_dir, suffix="summary")
                print(f"✓ Summary generated and saved to: {path}")

    except Exception as e:
        logger.error(f"Error executing command '{args.command}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


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



logger = logging.getLogger(__name__)

# Default timeout for requests
DEFAULT_TIMEOUT = 10
IMAGE_VALIDATION_TIMEOUT = 5


class DuckDuckImages:
    """Search and download images from DuckDuckGo."""

    def fetch_image_size(self, url):
        """
        Fetch image dimensions from a URL.

        Args:
            url: Image URL

        Returns:
            Tuple of (width, height) or (0, 0) if unable to fetch
        """
        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            return img.size
        except Exception as e:
            logger.warning(f"Failed to fetch image size from {url}: {e}")
            return (0, 0)

    def get_urls(self, query, size, max_results):
        """
        Search DuckDuckGo for image URLs matching the query.

        Args:
            query: Search query string
            size: Image size filter (e.g., 'Large', 'Medium', 'Small')
            max_results: Maximum number of URLs to return

        Returns:
            List of valid image URLs
        """
        image_urls = []
        try:
            kwargs = {"max_results": max_results * 2}
            if size:
                kwargs["size"] = size

            with DDGS() as ddgs:
                for result in ddgs.images(query, **kwargs):
                    url = result.get("image")
                    if not url:
                        continue

                    if self.is_valid_image_url(url):
                        image_urls.append(url)
                        if len(image_urls) >= max_results:
                            break
        except Exception as e:
            logger.error(f"Error searching for images with query '{query}': {e}")

        return image_urls

    def download_image(self, url, save_dir, query, index):
        """
        Download and save an image from a URL.

        Args:
            url: Image URL
            save_dir: Directory to save the image
            query: Search query (used in filename)
            index: Image index (used in filename)

        Returns:
            Filename if successful, None otherwise
        """
        try:
            os.makedirs(save_dir, exist_ok=True)

            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))

            # Validate image format
            ext = img.format
            if not ext:
                logger.warning(f"Could not determine format for image from {url}")
                return None

            ext = ext.lower()
            safe_query = "_".join(query.lower().split())
            filename = f"{safe_query}_{index + 1}.{ext}"
            filepath = os.path.join(save_dir, filename)

            img.save(filepath)
            logger.info(f"Successfully saved image: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Failed to download image from {url}: {e}")
            return None

    def is_valid_image_url(self, url):
        """
        Validate that a URL points to a valid image.

        Args:
            url: URL to validate

        Returns:
            True if URL is a valid image, False otherwise
        """
        try:
            response = requests.head(
                url, allow_redirects=True, timeout=IMAGE_VALIDATION_TIMEOUT
            )
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            return content_type.startswith("image/")
        except Exception as e:
            logger.debug(f"Image URL validation failed for {url}: {e}")
            return False



logger = logging.getLogger(__name__)


class DuckDuckVideos:
    def get_urls(self, query, max_results=10):
        video_urls = []
        try:
            with DDGS() as ddgs:
                for result in ddgs.videos(query, max_results=max_results):
                    url = (
                        result.get("url")
                        or result.get("content")
                        or result.get("image")
                    )
                    if not url:
                        continue
                    video_urls.append(
                        {
                            "url": url,
                            "title": result.get("title", "No title"),
                            "duration": result.get("duration", "N/A"),
                        }
                    )
                    if len(video_urls) >= max_results:
                        break
        except Exception as e:
            try:
                import streamlit as st

                st.error(f"Error during video search: {e}")
            except (ImportError, RuntimeError):
                logger.error(f"Error during video search: {e}")
        return self.sort_by_duration(video_urls)

    def _duration_to_seconds(self, duration_str):
        if duration_str == "N/A" or not duration_str:
            return float("inf")

        parts = duration_str.split(":")
        try:
            parts = [int(p) for p in parts]
            if len(parts) == 3:  # HH:MM:SS
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:  # MM:SS
                return parts[0] * 60 + parts[1]
            elif len(parts) == 1:  # SS
                return parts[0]
        except (ValueError, TypeError):
            return float("inf")
        return float("inf")

    def sort_by_duration(self, videos):
        return sorted(videos, key=lambda x: self._duration_to_seconds(x["duration"]))

