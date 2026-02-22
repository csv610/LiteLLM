"""Core constants and internal helper functions for vision utilities."""

import logging
import tempfile
import urllib.request
import urllib.error
from pathlib import Path
from typing import Tuple, Literal, Union
from urllib.parse import urlparse
from PIL import Image

logger = logging.getLogger(__name__)

# API constraints
MAX_IMAGE_SIZE_MB = 50
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024
MAX_TOTAL_IMAGE_PAYLOAD_MB = 50
MAX_TOTAL_IMAGE_PAYLOAD_BYTES = MAX_TOTAL_IMAGE_PAYLOAD_MB * 1024 * 1024
MIN_IMAGE_DIMENSION = 32  # Minimum 32x32 pixels

IMAGE_MIME_TYPE = "image/jpeg"

def _convert_to_rgb(img: Image.Image) -> Image.Image:
    """
    Convert PIL image to RGB mode, handling transparency and palettes.
    """
    if img.mode in ("RGBA", "LA", "P"):
        rgb_img = Image.new("RGB", img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        return rgb_img
    elif img.mode != "RGB":
        return img.convert("RGB")
    return img

def _is_url(path: str) -> bool:
    """
    Check if a string is a valid HTTP(S) URL.
    """
    try:
        parsed = urlparse(path)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False

def _download_from_url(url: str) -> str:
    """
    Download image from URL to a temporary file.
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")

        path = parsed.path.lower()
        if path.endswith('.jpg') or path.endswith('.jpeg'):
            suffix = '.jpg'
        elif path.endswith('.png'):
            suffix = '.png'
        elif path.endswith('.webp'):
            suffix = '.webp'
        elif path.endswith('.gif'):
            suffix = '.gif'
        else:
            suffix = '.jpg'

        temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        temp_path = temp_file.name
        temp_file.close()

        logger.info(f"Downloading image from {url}")
        urllib.request.urlretrieve(url, temp_path)
        return temp_path

    except urllib.error.URLError as e:
        raise ValueError(f"Failed to download image from {url}: {e}")
    except Exception as e:
        raise ValueError(f"Error downloading image from {url}: {e}")

def _validate_file_exists(file_path: str) -> Path:
    """Validate that a file exists and return Path object."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path

def _validate_directory_exists(directory_path: str) -> Path:
    """Validate that a directory exists and is a directory."""
    directory = Path(directory_path)
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")
    return directory
