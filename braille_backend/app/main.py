from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.arduino import router as arduino_router


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    description=(
        "Backend for an AI-powered Braille Assistant: "
        "file upload -> OCR/PDF extraction -> RAG -> LLM -> "
        "Braille binary -> Arduino."
    ),
)

# Frontend will run on a different port/domain during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your frontend URL in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(arduino_router)


@app.get("/")
def root():
    return {
        "message": "Braille Assistant backend is running.",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
