import os

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from dotenv import load_dotenv


load_dotenv()

# Get Tesseract path from .env
tesseract_path = os.getenv("TESSERACT_PATH")

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    pages = []

    for page_number, page in enumerate(doc):
        text = page.get_text("text").strip()

        # Normal PDF → use its embedded text
        if not text:
            # Scanned/image PDF → render page and use OCR
            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text = pytesseract.image_to_string(image).strip()

        if text:
            pages.append(
                f"[Page {page_number + 1}]\n{text}"
            )

    doc.close()

    return "\n\n".join(pages)