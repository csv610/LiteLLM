import os
import logging
from io import BytesIO

import requests
from PIL import Image
from ddgs import DDGS

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
            with DDGS() as ddgs:
                for result in ddgs.images(
                    query,
                    max_results=max_results * 2,  # Request more to account for validation failures
                    type=size if size else None
                ):
                    url = result.get('image')
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
            response = requests.head(url, allow_redirects=True, timeout=IMAGE_VALIDATION_TIMEOUT)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            return content_type.startswith('image/')
        except Exception as e:
            logger.debug(f"Image URL validation failed for {url}: {e}")
            return False

