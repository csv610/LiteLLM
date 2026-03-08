import os
import pytest
import numpy as np
from PIL import Image
from lite.vision.processing import (
    create_random_image,
    create_gradient_image,
    resize_images_to_fit,
    resize_to_max_size,
    convert_format,
    auto_orient,
    crop,
    square_image,
    resize_to_dimensions,
    create_blank_image,
    remove_exif
)

def test_remove_exif_extended(sample_image):
    # Test with real file path
    result = remove_exif(sample_image)
    assert isinstance(result, Image.Image)

def test_resize_to_max_size_units(sample_image):
    # Test KB unit
    img_kb = resize_to_max_size(sample_image, 10, size_unit="KB")
    assert isinstance(img_kb, Image.Image)
    
    # Test invalid unit fallback
    img_fallback = resize_to_max_size(sample_image, 1, size_unit="INVALID")
    assert isinstance(img_fallback, Image.Image)


@pytest.fixture
def sample_image(tmp_path):
    path = tmp_path / "sample.jpg"
    img = Image.new('RGB', (100, 100), color='red')
    img.save(path)
    return str(path)

def test_create_blank_image_extended():
    img = create_blank_image(10, 10, color="random", image_mode="RGB")
    assert img.size == (10, 10)
    img_l = create_blank_image(10, 10, color="random", image_mode="L")
    assert img_l.mode == "L"
    img_rgba = create_blank_image(10, 10, color="random", image_mode="RGBA")
    assert img_rgba.mode == "RGBA"

def test_create_random_image():
    img = create_random_image(10, 10, image_mode="RGB")
    assert img.size == (10, 10)
    assert img.mode == "RGB"
    img_l = create_random_image(10, 10, image_mode="L")
    assert img_l.mode == "L"
    img_rgba = create_random_image(10, 10, image_mode="RGBA")
    assert img_rgba.mode == "RGBA"

def test_create_gradient_image():
    img_h = create_gradient_image(10, 10, (0,0,0), (255,255,255), direction="horizontal")
    assert img_h.size == (10, 10)
    img_v = create_gradient_image(10, 10, (0,0,0), (255,255,255), direction="vertical")
    assert img_v.size == (10, 10)
    img_d = create_gradient_image(10, 10, (0,0,0), (255,255,255), direction="diagonal")
    assert img_d.size == (10, 10)

def test_resize_images_to_fit_no_resize(sample_image):
    # Small image should stay as is
    paths = [sample_image]
    result = resize_images_to_fit(paths)
    assert result == paths

def test_square_image_extended(sample_image):
    # Test top-left position
    img = square_image(sample_image, 200, (0,0,0), position="top-left")
    assert img.size == (200, 200)
    # Test resizing in square_image
    img_small = square_image(sample_image, 50, (0,0,0))
    assert img_small.size == (50, 50)

def test_resize_to_dimensions_extended(sample_image):
    img = resize_to_dimensions(sample_image, 200, 100)
    assert img.size == (200, 100)

def test_convert_format(sample_image):
    data = convert_format(sample_image, "PNG")
    assert len(data) > 0
    # Check if it's actually a PNG
    img = Image.open(io.BytesIO(data))
    assert img.format == "PNG"

import io

def test_auto_orient(sample_image):
    # Hard to test actual rotation without real EXIF, but can test the call
    img = auto_orient(sample_image)
    assert isinstance(img, Image.Image)

def test_crop_extended(sample_image):
    img = crop(sample_image, 0, 0, 50, 50)
    assert img.size == (50, 50)

def test_resize_to_max_size_mb(sample_image):
    # Test with very small limit to trigger compression
    img = resize_to_max_size(sample_image, 0.001, size_unit="MB")
    assert isinstance(img, Image.Image)
    
    # Test with GB unit
    img_gb = resize_to_max_size(sample_image, 0.000001, size_unit="GB")
    assert isinstance(img_gb, Image.Image)

def test_resize_to_max_size_no_compress(sample_image):
    # Large limit should not compress
    img = resize_to_max_size(sample_image, 100, size_unit="MB")
    assert isinstance(img, Image.Image)
