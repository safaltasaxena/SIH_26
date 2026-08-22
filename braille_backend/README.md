# Braille Assistant Backend

Pipeline:

User uploads Image/PDF
        |
        v
OCR / PDF extraction
        |
        v
Text chunks
        |
        v
HuggingFace embeddings
        |
        v
FAISS vector store
        |
        v
LangGraph RAG
        |
        v
Local Ollama LLM
        |
        v
Answer / Summary / Full Text / Explanation
        |
        v
6-dot Braille binary
        |
        +------> JSON response to frontend
        |
        +------> Serial -> Arduino (background)

## 1. Install Python packages

python -m venv .venv

Windows:
.venv\Scripts\activate

Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt

## 2. Install Tesseract

Install Tesseract OCR separately and make sure `tesseract`
is available on PATH.

If Windows cannot find it, set the pytesseract executable path
inside `app/services/ocr_service.py`.

## 3. Install Ollama

Install Ollama, then:

ollama pull qwen3:4b

The LangChain Ollama integration uses the local Ollama server.
No paid LLM API key is required.

## 4. Configure

copy .env.example .env

Change ARDUINO_PORT to your actual Arduino COM port.

For testing without Arduino:

ARDUINO_ENABLED=false

## 5. Run

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/docs

## Main endpoints

POST /api/upload
- Upload image/PDF
- Extract text
- Build embeddings
- Create FAISS vector store
- Return session_id

POST /api/chat
- Send session_id + message
- LangGraph determines action
- RAG retrieves context when needed
- Ollama generates answer
- Answer is converted to Braille
- Binary is returned to frontend
- Same binary is sent to Arduino in background

GET /api/arduino/status
- Check serial connection

POST /api/arduino/send
- Manually send Braille binary to Arduino
