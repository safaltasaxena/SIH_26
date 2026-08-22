from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.arduino_service import send_to_arduino
from app.services.braille_service import (
    binary_to_unicode,
    convert_text_to_braille,
)
from app.services.rag_graph import run_rag
from app.store.session_store import get_session


router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
):
    session = get_session(request.session_id)

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Upload the document again.",
        )

    try:
        action, answer = run_rag(
            request.session_id,
            request.message,
        )

        braille_binary, unsupported = convert_text_to_braille(answer)
        braille_unicode = binary_to_unicode(braille_binary)

        # Hardware communication happens after the HTTP response is prepared.
        background_tasks.add_task(
            send_to_arduino,
            braille_binary,
        )

        warning = None

        if unsupported:
            preview = ", ".join(unsupported[:10])
            warning = (
                "Some characters are not currently in the Braille mapping "
                f"and were shown as '?': {preview}"
            )

        return ChatResponse(
            session_id=request.session_id,
            action=action,
            answer=answer,
            braille_binary=braille_binary,
            braille_unicode=braille_unicode,
            sent_to_arduino=True,
            warning=warning,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {exc}",
        )
