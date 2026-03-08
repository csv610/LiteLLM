import os
import pytest
import numpy as np
import base64
import io
from PIL import Image
from lite.vision.io import (
    b64_to_pil,
    pil_to_b64,
    cv2_to_pil,
    pil_to_cv2,
    get_image_info,
    save_image,
    save_images_batch,
    encode_to_base64
)

@pytest.fixture
def sample_pil():
    return Image.new('RGB', (100, 100), color='red')

@pytest.fixture
def sample_cv2():
    # Red in BGR, ensure uint8
    return (np.zeros((100, 100, 3), dtype=np.uint8) + np.array([0, 0, 255], dtype=np.uint8)).astype(np.uint8)

def test_b64_pil_conversion(sample_pil):
    b64_str = pil_to_b64(sample_pil)
    assert b64_str.startswith("data:image/jpeg;base64,")
    
    pil_img = b64_to_pil(b64_str)
    assert pil_img.size == (100, 100)
    
    # Test without data URI
    b64_raw = pil_to_b64(sample_pil, include_data_uri=False)
    assert not b64_raw.startswith("data:")
    pil_img_raw = b64_to_pil(b64_raw)
    assert pil_img_raw.size == (100, 100)

def test_cv2_pil_conversion_extended(sample_cv2):
    pil_img = cv2_to_pil(sample_cv2)
    assert pil_img.size == (100, 100)
    assert pil_img.mode == "RGB"
    
    cv2_img = pil_to_cv2(pil_img)
    assert cv2_img.shape == (100, 100, 3)
    # Check BGR: red was (0,0,255), after conversion should be same
    assert np.all(cv2_img[0,0] == [0, 0, 255])

def test_cv2_pil_rgba():
    rgba_cv2 = np.zeros((10, 10, 4), dtype=np.uint8)
    pil_img = cv2_to_pil(rgba_cv2)
    assert pil_img.mode == "RGBA"
    
    cv2_img = pil_to_cv2(pil_img)
    assert cv2_img.shape == (10, 10, 4)

def test_cv2_pil_grayscale():
    gray_cv2 = np.zeros((10, 10), dtype=np.uint8)
    pil_img = cv2_to_pil(gray_cv2)
    assert pil_img.mode == "L"
    
    cv2_img = pil_to_cv2(pil_img)
    assert len(cv2_img.shape) == 2

def test_save_image_types(sample_pil, sample_cv2, tmp_path):
    # PIL input
    p1 = tmp_path / "p1.png"
    save_image(sample_pil, str(p1), input_type="pil")
    assert p1.exists()
    
    # CV2 input
    p2 = tmp_path / "p2.jpg"
    save_image(sample_cv2, str(p2), input_type="cv2", format="JPG")
    assert p2.exists()
    
    # Base64 input
    b64_str = pil_to_b64(sample_pil)
    p3 = tmp_path / "p3.png"
    save_image(b64_str, str(p3), input_type="base64")
    assert p3.exists()

def test_save_image_auto_detect(sample_pil, tmp_path):
    p = tmp_path / "auto.png"
    save_image(sample_pil, str(p))
    assert p.exists()

def test_get_image_info_error():
    with pytest.raises(Exception):
        get_image_info("nonexistent.jpg")

@pytest.fixture
def real_image_file(tmp_path):
    p = tmp_path / "real.jpg"
    img = Image.new('RGB', (100, 100), color='blue')
    img.save(p)
    return str(p)

def test_encode_to_base64_file(real_image_file):
    b64 = encode_to_base64(real_image_file)
    assert b64.startswith("data:image/jpeg;base64,")

def test_save_images_batch_extended(sample_pil, tmp_path):
    output_dir = tmp_path / "batch"
    paths = save_images_batch([sample_pil, sample_pil], str(output_dir), filename_prefix="test")
    assert len(paths) == 2
    assert os.path.exists(paths[0])
    assert "test_0000.png" in paths[0]
