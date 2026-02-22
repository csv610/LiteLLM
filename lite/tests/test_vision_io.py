import pytest
import os
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from lite.vision.io import save_image, get_image_info, save_images_batch, cv2_to_pil, pil_to_cv2

@pytest.fixture
def test_img_path(tmp_path):
    path = tmp_path / "original.jpg"
    img = Image.new("RGB", (100, 100), color="green")
    img.save(path)
    return str(path)

def test_save_image(test_img_path, tmp_path):
    output_path = tmp_path / "saved.png"
    # Save from path
    result = save_image(test_img_path, str(output_path), format="PNG")
    assert result == str(output_path)
    assert Path(result).exists()
    assert Image.open(result).format == "PNG"

def test_save_image_from_pil(tmp_path):
    img = Image.new("RGB", (50, 50), color="blue")
    output = tmp_path / "pil_saved.jpg"
    save_image(img, str(output), format="JPEG")
    assert Path(output).exists()

def test_get_image_info(test_img_path):
    info = get_image_info(test_img_path)
    assert info["width"] == 100
    assert info["height"] == 100
    assert info["format"] == "JPEG"
    assert info["file_size_mb"] >= 0

def test_cv2_pil_conversion():
    # Create OpenCV image (BGR)
    cv_img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv_img[:, :, 2] = 255  # Red in BGR is (0, 0, 255)
    
    pil_img = cv2_to_pil(cv_img)
    assert pil_img.size == (100, 100)
    # Red in RGB is (255, 0, 0)
    assert pil_img.getpixel((0, 0)) == (255, 0, 0)
    
    cv_back = pil_to_cv2(pil_img)
    assert cv_back.shape == (100, 100, 3)
    assert cv_back[0, 0].tolist() == [0, 0, 255]

def test_save_images_batch(test_img_path, tmp_path):
    output_dir = tmp_path / "batch_output"
    images = [test_img_path, test_img_path]
    saved = save_images_batch(images, str(output_dir), filename_prefix="batch")
    
    assert len(saved) == 2
    assert Path(saved[0]).name == "batch_0000.png"
    assert Path(saved[1]).name == "batch_0001.png"
