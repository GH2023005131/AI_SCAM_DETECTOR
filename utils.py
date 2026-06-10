
import re
from io import BytesIO

try:
    import easyocr
    from PIL import Image
    import numpy as np
except ImportError:
    easyocr = None

OCR_AVAILABLE = easyocr is not None


def is_ocr_available() -> bool:
    return OCR_AVAILABLE


def extract_text_from_image(image_bytes: bytes) -> str:
    if easyocr is None:
        return ""

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        reader = easyocr.Reader(["en"], gpu=False)
        raw_result = reader.readtext(np.array(image), detail=0)
        return "\n".join(raw_result).strip()
    except Exception:
        return ""


def clean_text(text: str) -> str:
    normalized = text.replace("\r", " ").replace("\n", " ")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()
