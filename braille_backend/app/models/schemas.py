from pydantic import BaseModel, Field
from typing import List, Optional


class UploadResponse(BaseModel):
    session_id: str
    filename: str
    message: str
    extracted_text: str
    character_count: int


class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    session_id: str
    action: str
    answer: str
    braille_binary: List[List[int]]
    braille_unicode: str
    sent_to_arduino: bool
    warning: Optional[str] = None


class ArduinoRequest(BaseModel):
    braille_binary: List[List[int]]
