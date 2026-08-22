import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import UPLOAD_DIR
from app.models.schemas import UploadResponse
from app.services.document_service import extract_document_text
from app.services.vector_store_service import build_vector_store
from app.store.session_store import create_session


router = APIRouter(prefix="/api/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tiff",
    ".webp",
    ".pdf",
}


@router.post("", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or "uploaded_file"
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only images and PDF files are supported.",
        )

    session_id = uuid.uuid4().hex

    safe_name = f"{session_id}{extension}"
    file_path = UPLOAD_DIR / safe_name

    data = await file.read()
    file_path.write_bytes(data)

    try:
        text = extract_document_text(str(file_path))
        create_session(session_id, filename, text)
        build_vector_store(session_id, text)

    except Exception as exc:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {exc}",
        )

    return UploadResponse(
        session_id=session_id,
        filename=filename,
        message="Yes! File uploaded successfully. Go ahead and ask.",
        extracted_text=text,
        character_count=len(text),
    )
