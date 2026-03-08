import pytest
from PIL import Image
from pathlib import Path
from lite.vision.processing import (
    create_blank_image, 
    square_image, 
    resize_to_dimensions, 
    crop, 
    remove_exif,
    resize_images_to_fit
)

@pytest.fixture
def sample_image_path(tmp_path):
    path = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 50), color="red")
    img.save(path)
    return str(path)

def test_create_blank_image():
    img = create_blank_image(100, 100, color=(255, 0, 0))
    assert img.size == (100, 100)
    assert img.getpixel((0, 0)) == (255, 0, 0)

def test_square_image(sample_image_path):
    # Original is 100x50. Squaring to 200 should result in 200x200
    squared = square_image(sample_image_path, max_size=200, background_color=(0, 0, 0))
    assert squared.size == (200, 200)
    # Background should be black
    assert squared.getpixel((0, 0)) == (0, 0, 0)

def test_resize_to_dimensions(sample_image_path):
    # Resize 100x50 to 50x50
    resized = resized = resize_to_dimensions(sample_image_path, 50, 50)
    assert resized.size == (50, 50)

def test_crop(sample_image_path):
    # Crop a 10x10 area from 100x50
    cropped = crop(sample_image_path, 0, 0, 10, 10)
    assert cropped.size == (10, 10)

def test_remove_exif(sample_image_path):
    # Even if no exif exists, it should return a clean image
    clean = remove_exif(sample_image_path)
    assert clean.size == (100, 50)
    assert "exif" not in clean.info

def test_resize_images_to_fit(tmp_path):
    # Create a large image
    path1 = tmp_path / "large.jpg"
    img = Image.new("RGB", (2000, 2000), color="blue")
    img.save(path1, quality=95)
    
    # This should return paths (either original or temp)
    paths = [str(path1)]
    result_paths = resize_images_to_fit(paths)
    assert len(result_paths) == 1
    assert Path(result_paths[0]).exists()
