import os
from pathlib import Path

import cv2
import numpy as np
import pytesseract
from dotenv import load_dotenv


load_dotenv()

# Get Tesseract path from .env
tesseract_path = os.getenv("TESSERACT_PATH")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_image(image_path: str) -> str:
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read the uploaded image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    text = pytesseract.image_to_string(thresh)

    return clean_text(text)


def extract_text_from_image_bytes(data: bytes) -> str:
    image = cv2.imdecode(
        np.frombuffer(data, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise ValueError("Could not decode the uploaded image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    text = pytesseract.image_to_string(thresh)

    return clean_text(text)


def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return "\n".join(lines)