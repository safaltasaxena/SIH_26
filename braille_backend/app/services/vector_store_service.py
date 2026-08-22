from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.core.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    VECTOR_DIR,
)
from app.store.session_store import set_vector_store


_embeddings = None


def get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    return _embeddings


def build_vector_store(session_id: str, text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    documents = [
        Document(
            page_content=chunk,
            metadata={"session_id": session_id},
        )
        for chunk in splitter.split_text(text)
    ]

    if not documents:
        raise ValueError("Document did not produce any chunks.")

    store = FAISS.from_documents(documents, get_embeddings())

    session_dir = VECTOR_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    store.save_local(str(session_dir))

    set_vector_store(session_id, store)

    return store


def load_vector_store(session_id: str):
    session_dir = VECTOR_DIR / session_id

    if not session_dir.exists():
        return None

    store = FAISS.load_local(
        str(session_dir),
        get_embeddings(),
        allow_dangerous_deserialization=True,
    )

    set_vector_store(session_id, store)
    return store


def get_vector_store(session_id: str):
    from app.store.session_store import get_session

    session = get_session(session_id)

    if session and session.vector_store is not None:
        return session.vector_store

    return load_vector_store(session_id)
