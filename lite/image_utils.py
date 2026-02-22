"""Compatibility layer for image utilities.

This module is deprecated. Use the 'lite.vision' package instead.
"""

import logging
from .vision import (
    IMAGE_MIME_TYPE,
    MAX_IMAGE_SIZE_MB,
    MAX_IMAGE_SIZE_BYTES,
    MAX_TOTAL_IMAGE_PAYLOAD_MB,
    MAX_TOTAL_IMAGE_PAYLOAD_BYTES,
    MIN_IMAGE_DIMENSION,
    is_valid_image,
    is_valid_size,
    is_valid_dimensions,
    encode_to_base64,
    b64_to_pil,
    pil_to_b64,
    cv2_to_pil,
    pil_to_cv2,
    get_image_info,
    save_image,
    save_images_batch,
    create_blank_image,
    create_random_image,
    create_gradient_image,
    resize_images_to_fit,
    square_image,
    resize_to_dimensions,
    convert_format,
    crop,
    auto_orient,
    remove_exif,
    resize_to_max_size,
    collect_images,
    collect_images_with_info,
)

logger = logging.getLogger(__name__)

class ImageUtils:
    """Compatibility class for vision utilities."""
    
    IMAGE_MIME_TYPE = IMAGE_MIME_TYPE
    
    @staticmethod
    def encode_to_base64(image_path: str) -> str:
        return encode_to_base64(image_path)

    @staticmethod
    def is_valid_image(path):
        return is_valid_image(path)

    @staticmethod
    def is_valid_size(path):
        return is_valid_size(path)

    @staticmethod
    def is_valid_dimensions(path):
        return is_valid_dimensions(path)

    @staticmethod
    def create_blank_image(*args, **kwargs):
        return create_blank_image(*args, **kwargs)

    @staticmethod
    def create_random_image(*args, **kwargs):
        return create_random_image(*args, **kwargs)

    @staticmethod
    def create_gradient_image(*args, **kwargs):
        return create_gradient_image(*args, **kwargs)

    @staticmethod
    def resize_images_to_fit(image_paths):
        return resize_images_to_fit(image_paths)

    @staticmethod
    def square_image(*args, **kwargs):
        return square_image(*args, **kwargs)

    @staticmethod
    def resize_to_dimensions(*args, **kwargs):
        return resize_to_dimensions(*args, **kwargs)

    @staticmethod
    def convert_format(*args, **kwargs):
        return convert_format(*args, **kwargs)

    @staticmethod
    def crop(*args, **kwargs):
        return crop(*args, **kwargs)

    @staticmethod
    def b64_to_pil(b64_string):
        return b64_to_pil(b64_string)

    @staticmethod
    def pil_to_b64(*args, **kwargs):
        return pil_to_b64(*args, **kwargs)

    @staticmethod
    def cv2_to_pil(cv_image):
        return cv2_to_pil(cv_image)

    @staticmethod
    def pil_to_cv2(image):
        return pil_to_cv2(image)

    @staticmethod
    def get_image_info(image_path):
        return get_image_info(image_path)

    @staticmethod
    def save_image(*args, **kwargs):
        return save_image(*args, **kwargs)

    @staticmethod
    def save_images_batch(*args, **kwargs):
        return save_images_batch(*args, **kwargs)

    @staticmethod
    def auto_orient(image_path):
        return auto_orient(image_path)

    @staticmethod
    def remove_exif(image_path):
        return remove_exif(image_path)

    @staticmethod
    def resize_to_max_size(*args, **kwargs):
        return resize_to_max_size(*args, **kwargs)

    @staticmethod
    def collect_images(*args, **kwargs):
        return collect_images(*args, **kwargs)

    @staticmethod
    def collect_images_with_info(*args, **kwargs):
        return collect_images_with_info(*args, **kwargs)
