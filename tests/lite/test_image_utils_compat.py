import pytest
from unittest.mock import patch, MagicMock
from lite.image_utils import ImageUtils

@patch("lite.image_utils.encode_to_base64")
def test_image_utils_encode(mock_encode):
    ImageUtils.encode_to_base64("test.jpg")
    mock_encode.assert_called_with("test.jpg")

@patch("lite.image_utils.is_valid_image")
def test_image_utils_validate(mock_valid):
    ImageUtils.is_valid_image("test.jpg")
    mock_valid.assert_called_with("test.jpg")

@patch("lite.image_utils.is_valid_size")
def test_image_utils_is_valid_size(mock):
    ImageUtils.is_valid_size("test.jpg")
    mock.assert_called_with("test.jpg")

@patch("lite.image_utils.is_valid_dimensions")
def test_image_utils_is_valid_dimensions(mock):
    ImageUtils.is_valid_dimensions("test.jpg")
    mock.assert_called_with("test.jpg")

@patch("lite.image_utils.create_blank_image")
def test_image_utils_create(mock_create):
    ImageUtils.create_blank_image(10, 10)
    mock_create.assert_called_with(10, 10)

@patch("lite.image_utils.create_random_image")
def test_image_utils_create_random(mock):
    ImageUtils.create_random_image(10, 10)
    mock.assert_called_with(10, 10)

@patch("lite.image_utils.create_gradient_image")
def test_image_utils_create_gradient(mock):
    ImageUtils.create_gradient_image(10, 10, (0,0,0), (255,255,255))
    mock.assert_called_with(10, 10, (0,0,0), (255,255,255))

@patch("lite.image_utils.resize_images_to_fit")
def test_image_utils_resize(mock_resize):
    ImageUtils.resize_images_to_fit(["a.jpg"])
    mock_resize.assert_called_with(["a.jpg"])

@patch("lite.image_utils.square_image")
def test_image_utils_square(mock):
    ImageUtils.square_image("test.jpg", 100)
    mock.assert_called_with("test.jpg", 100)

@patch("lite.image_utils.resize_to_dimensions")
def test_image_utils_resize_dim(mock):
    ImageUtils.resize_to_dimensions("test.jpg", 100, 100)
    mock.assert_called_with("test.jpg", 100, 100)

@patch("lite.image_utils.convert_format")
def test_image_utils_convert(mock):
    ImageUtils.convert_format("test.jpg", "PNG")
    mock.assert_called_with("test.jpg", "PNG")

@patch("lite.image_utils.crop")
def test_image_utils_crop(mock):
    ImageUtils.crop("test.jpg", 0, 0, 10, 10)
    mock.assert_called_with("test.jpg", 0, 0, 10, 10)

@patch("lite.image_utils.b64_to_pil")
def test_image_utils_b64_pil(mock):
    ImageUtils.b64_to_pil("data")
    mock.assert_called_with("data")

@patch("lite.image_utils.cv2_to_pil")
def test_image_utils_cv2_pil(mock):
    ImageUtils.cv2_to_pil(None)
    mock.assert_called_with(None)

@patch("lite.image_utils.pil_to_cv2")
def test_image_utils_pil_cv2(mock):
    ImageUtils.pil_to_cv2(None)
    mock.assert_called_with(None)

@patch("lite.image_utils.save_image")
def test_image_utils_save(mock_save):
    ImageUtils.save_image("data", "out.png")
    mock_save.assert_called_with("data", "out.png")

@patch("lite.image_utils.save_images_batch")
def test_image_utils_save_batch(mock):
    ImageUtils.save_images_batch(["data"], "dir")
    mock.assert_called_with(["data"], "dir")

@patch("lite.image_utils.auto_orient")
def test_image_utils_auto_orient(mock):
    ImageUtils.auto_orient("test.jpg")
    mock.assert_called_with("test.jpg")

@patch("lite.image_utils.remove_exif")
def test_image_utils_remove_exif(mock):
    ImageUtils.remove_exif("test.jpg")
    mock.assert_called_with("test.jpg")

@patch("lite.image_utils.resize_to_max_size")
def test_image_utils_resize_max(mock):
    ImageUtils.resize_to_max_size("test.jpg", 1.0)
    mock.assert_called_with("test.jpg", 1.0)

@patch("lite.image_utils.collect_images")
def test_image_utils_collect(mock):
    ImageUtils.collect_images("dir")
    mock.assert_called_with("dir")

@patch("lite.image_utils.collect_images_with_info")
def test_image_utils_collect_info(mock):
    ImageUtils.collect_images_with_info("dir")
    mock.assert_called_with("dir")

def test_image_utils_mime():
    assert ImageUtils.IMAGE_MIME_TYPE == "image/jpeg"

@patch("lite.image_utils.get_image_info")
def test_image_utils_info(mock_info):
    ImageUtils.get_image_info("test.jpg")
    mock_info.assert_called_with("test.jpg")

@patch("lite.image_utils.pil_to_b64")
def test_image_utils_pil_b64(mock_conv):
    mock_img = MagicMock()
    ImageUtils.pil_to_b64(mock_img)
    mock_conv.assert_called_with(mock_img)
