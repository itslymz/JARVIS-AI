"""Unit tests for vision system."""

import pytest
from PIL import Image
from app.vision.vision import ScreenCapture, OCR, ObjectDetection, ImageAnalyzer


@pytest.fixture
def screen_capture():
    """Create screen capture instance."""
    return ScreenCapture()


@pytest.fixture
def ocr():
    """Create OCR instance."""
    return OCR()


@pytest.fixture
def object_detection():
    """Create object detection instance."""
    return ObjectDetection()


@pytest.fixture
def test_image():
    """Create test image."""
    return Image.new('RGB', (100, 100), color='red')


@pytest.mark.asyncio
async def test_image_to_base64(screen_capture, test_image):
    """Test image to base64 conversion."""
    base64_str = await screen_capture.image_to_base64(test_image)
    assert len(base64_str) > 0


@pytest.mark.asyncio
async def test_base64_to_image(screen_capture):
    """Test base64 to image conversion."""
    test_image = Image.new('RGB', (100, 100), color='red')
    base64_str = await screen_capture.image_to_base64(test_image)
    image = await screen_capture.base64_to_image(base64_str)
    assert image is not None
    assert image.size == (100, 100)


@pytest.mark.asyncio
async def test_detect_edges(object_detection, test_image):
    """Test edge detection."""
    result = await object_detection.detect_edges(test_image)
    assert result is not None


@pytest.mark.asyncio
async def test_highlight_region(object_detection, test_image):
    """Test region highlighting."""
    result = await object_detection.highlight_region(test_image, 10, 10, 20, 20)
    assert result is not None
