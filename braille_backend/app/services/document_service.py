from pathlib import Path
from .ocr_service import extract_text_from_image
from .pdf_service import extract_text_from_pdf


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def extract_document_text(file_path: str) -> str:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension in IMAGE_EXTENSIONS:
        text = extract_text_from_image(str(path))

    elif extension == ".pdf":
        text = extract_text_from_pdf(str(path))

    else:
        raise ValueError(
            "Unsupported file type. Upload an image or PDF."
        )

    if not text.strip():
        raise ValueError(
            "No readable text was found in the uploaded document."
        )

    return text
