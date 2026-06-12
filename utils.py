from io import BytesIO
from PIL import Image

def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        import easyocr
        import numpy as np
    except Exception:
        return "OCR unavailable (easyocr not installed). Install with: pip install easyocr numpy"
    reader = easyocr.Reader(['en'])
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    arr = np.array(img)
    results = reader.readtext(arr)
    texts = [r[1] for r in results]
    return "\n".join(texts)

def clean_text(text: str) -> str:
    return " ".join(text.split())
