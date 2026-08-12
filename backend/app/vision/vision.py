"""Vision system for screen capture, OCR, and image understanding."""

from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import io
import base64
from PIL import Image, ImageDraw
import pytesseract
import cv2
import numpy as np


class ScreenCapture:
    """Capture and analyze screen content."""

    def __init__(self):
        """Initialize screen capture."""
        pass

    async def capture_screen(self, filepath: Optional[str] = None) -> Optional[Image.Image]:
        """Capture entire screen.
        
        Args:
            filepath: Optional path to save screenshot
            
        Returns:
            PIL Image or None
        """
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            if filepath:
                screenshot.save(filepath)
            return screenshot
        except Exception as e:
            print(f"Failed to capture screen: {e}")
            return None

    async def capture_region(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        filepath: Optional[str] = None,
    ) -> Optional[Image.Image]:
        """Capture screen region.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Region width
            height: Region height
            filepath: Optional path to save screenshot
            
        Returns:
            PIL Image or None
        """
        try:
            import pyautogui
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            if filepath:
                screenshot.save(filepath)
            return screenshot
        except Exception as e:
            print(f"Failed to capture region: {e}")
            return None

    async def capture_window(self, window_title: str) -> Optional[Image.Image]:
        """Capture specific window (Windows only).
        
        Args:
            window_title: Window title
            
        Returns:
            PIL Image or None
        """
        try:
            import pygetwindow
            window = pygetwindow.getWindowsWithTitle(window_title)[0]
            return await self.capture_region(
                window.left,
                window.top,
                window.width,
                window.height,
            )
        except Exception as e:
            print(f"Failed to capture window: {e}")
            return None

    async def image_to_base64(self, image: Image.Image) -> str:
        """Convert image to base64 string.
        
        Args:
            image: PIL Image
            
        Returns:
            Base64 encoded string
        """
        try:
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            return base64.b64encode(buffer.getvalue()).decode()
        except Exception as e:
            print(f"Failed to convert image: {e}")
            return ""

    async def base64_to_image(self, data: str) -> Optional[Image.Image]:
        """Convert base64 string to image.
        
        Args:
            data: Base64 encoded string
            
        Returns:
            PIL Image or None
        """
        try:
            image_data = base64.b64decode(data)
            return Image.open(io.BytesIO(image_data))
        except Exception as e:
            print(f"Failed to convert base64: {e}")
            return None


class OCR:
    """Optical Character Recognition."""

    def __init__(self):
        """Initialize OCR."""
        try:
            # Verify Tesseract is available
            pytesseract.get_tesseract_version()
        except Exception as e:
            print(f"Tesseract not available: {e}")

    async def extract_text(
        self,
        image: Image.Image,
        language: str = "eng",
    ) -> str:
        """Extract text from image using OCR.
        
        Args:
            image: PIL Image
            language: Language code (e.g., 'eng', 'fra')
            
        Returns:
            Extracted text
        """
        try:
            text = pytesseract.image_to_string(
                image,
                lang=language,
            )
            return text.strip()
        except Exception as e:
            print(f"Failed to extract text: {e}")
            return ""

    async def extract_text_with_boxes(
        self,
        image: Image.Image,
        language: str = "eng",
    ) -> List[Dict[str, Any]]:
        """Extract text with bounding boxes.
        
        Args:
            image: PIL Image
            language: Language code
            
        Returns:
            List of text boxes with coordinates
        """
        try:
            data = pytesseract.image_to_data(
                image,
                lang=language,
                output_type=pytesseract.Output.DICT,
            )
            
            results = []
            for i in range(len(data["text"])):
                if int(data["conf"][i]) > 0:  # Confidence > 0
                    results.append({
                        "text": data["text"][i],
                        "x": int(data["left"][i]),
                        "y": int(data["top"][i]),
                        "width": int(data["width"][i]),
                        "height": int(data["height"][i]),
                        "confidence": int(data["conf"][i]),
                    })
            return results
        except Exception as e:
            print(f"Failed to extract text with boxes: {e}")
            return []


class ObjectDetection:
    """Detect objects and windows in images."""

    def __init__(self):
        """Initialize object detection."""
        pass

    async def detect_edges(
        self,
        image: Image.Image,
        threshold1: int = 100,
        threshold2: int = 200,
    ) -> Image.Image:
        """Detect edges in image using Canny edge detection.
        
        Args:
            image: PIL Image
            threshold1: Lower threshold
            threshold2: Upper threshold
            
        Returns:
            Edge detection result as PIL Image
        """
        try:
            # Convert PIL to OpenCV format
            cv_image = cv2.cvtColor(
                np.array(image),
                cv2.COLOR_RGB2BGR,
            )
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, threshold1, threshold2)
            
            # Convert back to PIL
            return Image.fromarray(edges)
        except Exception as e:
            print(f"Failed to detect edges: {e}")
            return image

    async def detect_contours(
        self,
        image: Image.Image,
        min_area: int = 100,
    ) -> List[Dict[str, Any]]:
        """Detect contours (shapes) in image.
        
        Args:
            image: PIL Image
            min_area: Minimum area to consider
            
        Returns:
            List of contours with bounds
        """
        try:
            # Convert PIL to OpenCV format
            cv_image = cv2.cvtColor(
                np.array(image),
                cv2.COLOR_RGB2BGR,
            )
            
            # Convert to grayscale and threshold
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Find contours
            contours, _ = cv2.findContours(
                binary,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE,
            )
            
            results = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > min_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    results.append({
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": int(area),
                    })
            
            return results
        except Exception as e:
            print(f"Failed to detect contours: {e}")
            return []

    async def find_template(
        self,
        haystack: Image.Image,
        needle: Image.Image,
        threshold: float = 0.8,
    ) -> Optional[Dict[str, Any]]:
        """Find template image within larger image.
        
        Args:
            haystack: Large image to search in
            needle: Template to find
            threshold: Match threshold (0-1)
            
        Returns:
            Match result with coordinates or None
        """
        try:
            # Convert to OpenCV format
            haystack_cv = cv2.cvtColor(
                np.array(haystack),
                cv2.COLOR_RGB2BGR,
            )
            needle_cv = cv2.cvtColor(
                np.array(needle),
                cv2.COLOR_RGB2BGR,
            )
            
            # Match template
            result = cv2.matchTemplate(haystack_cv, needle_cv, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                h, w = needle_cv.shape[:2]
                return {
                    "x": int(max_loc[0]),
                    "y": int(max_loc[1]),
                    "width": w,
                    "height": h,
                    "confidence": float(max_val),
                }
            return None
        except Exception as e:
            print(f"Failed to find template: {e}")
            return None

    async def highlight_region(
        self,
        image: Image.Image,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2,
    ) -> Image.Image:
        """Highlight region on image.
        
        Args:
            image: PIL Image
            x: X coordinate
            y: Y coordinate
            width: Width
            height: Height
            color: RGB color tuple
            thickness: Line thickness
            
        Returns:
            Modified image
        """
        try:
            draw = ImageDraw.Draw(image)
            draw.rectangle(
                [(x, y), (x + width, y + height)],
                outline=color,
                width=thickness,
            )
            return image
        except Exception as e:
            print(f"Failed to highlight region: {e}")
            return image


class ImageAnalyzer:
    """Analyze and understand images."""

    def __init__(self):
        """Initialize image analyzer."""
        self.screen_capture = ScreenCapture()
        self.ocr = OCR()
        self.object_detection = ObjectDetection()

    async def analyze_screenshot(self) -> Dict[str, Any]:
        """Analyze current screenshot.
        
        Returns:
            Analysis results
        """
        try:
            # Capture screen
            screenshot = await self.screen_capture.capture_screen()
            if not screenshot:
                return {}
            
            # Extract text
            text = await self.ocr.extract_text(screenshot)
            
            # Detect objects
            contours = await self.object_detection.detect_contours(screenshot)
            
            return {
                "text": text,
                "objects": contours,
                "width": screenshot.width,
                "height": screenshot.height,
            }
        except Exception as e:
            print(f"Failed to analyze screenshot: {e}")
            return {}

    async def analyze_image(self, filepath: str) -> Dict[str, Any]:
        """Analyze image file.
        
        Args:
            filepath: Path to image file
            
        Returns:
            Analysis results
        """
        try:
            image = Image.open(filepath)
            
            # Extract text
            text = await self.ocr.extract_text(image)
            
            # Detect objects
            contours = await self.object_detection.detect_contours(image)
            
            return {
                "text": text,
                "objects": contours,
                "width": image.width,
                "height": image.height,
            }
        except Exception as e:
            print(f"Failed to analyze image: {e}")
            return {}
