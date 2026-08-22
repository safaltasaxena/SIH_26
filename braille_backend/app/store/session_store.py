from dataclasses import dataclass, field
import json
from typing import Dict, Optional, Any

from app.core.config import SESSION_DIR


@dataclass
class SessionData:
    session_id: str
    filename: str
    text: str
    vector_store: Any = None


_sessions: Dict[str, SessionData] = {}


def create_session(session_id: str, filename: str, text: str) -> SessionData:
    session = SessionData(
        session_id=session_id,
        filename=filename,
        text=text,
    )
    _sessions[session_id] = session
    session_file = SESSION_DIR / f"{session_id}.json"
    session_file.write_text(
        json.dumps({"session_id": session_id, "filename": filename, "text": text}),
        encoding="utf-8",
    )
    return session


def get_session(session_id: str) -> Optional[SessionData]:
    session = _sessions.get(session_id)
    if session is not None:
        return session

    session_file = SESSION_DIR / f"{session_id}.json"
    if not session_file.is_file():
        return None

    try:
        data = json.loads(session_file.read_text(encoding="utf-8"))
        session = SessionData(
            session_id=data["session_id"],
            filename=data["filename"],
            text=data["text"],
        )
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return None

    _sessions[session_id] = session
    return session


def set_vector_store(session_id: str, vector_store: Any) -> None:
    if session_id in _sessions:
        _sessions[session_id].vector_store = vector_store
