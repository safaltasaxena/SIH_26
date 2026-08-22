from typing import TypedDict, List

from langgraph.graph import StateGraph, START, END

from app.core.config import TOP_K
from app.services.llm_service import get_llm
from app.services.vector_store_service import get_vector_store
from app.store.session_store import get_session


class RAGState(TypedDict, total=False):
    session_id: str
    query: str
    action: str
    context: str
    answer: str


def classify_action(query: str) -> str:
    q = query.lower()

    if any(
        phrase in q
        for phrase in [
            "full text",
            "complete text",
            "entire text",
            "show text",
            "all text",
        ]
    ):
        return "full_text"

    if any(
        word in q
        for word in ["summary", "summarize", "summarise", "shorten"]
    ):
        return "summary"

    if any(
        word in q
        for word in ["translate", "translation"]
    ):
        return "translation"

    if any(
        word in q
        for word in ["explain", "explanation", "simplify", "simple"]
    ):
        return "explain"

    return "qa"


def route_node(state: RAGState):
    return {"action": classify_action(state["query"])}


def retrieve_node(state: RAGState):
    session = get_session(state["session_id"])
    if not session:
        raise ValueError("Invalid session ID.")

    store = get_vector_store(state["session_id"])
    if store is None:
        raise ValueError("Vector store not available for this session.")

    action = state["action"]

    # Summary/explanation can use more context; normal Q&A uses fewer chunks.
    k = 8 if action in {"summary", "explain"} else TOP_K

    docs = store.similarity_search(state["query"], k=k)

    context = "\n\n---\n\n".join(
        document.page_content for document in docs
    )

    return {"context": context}


def generate_node(state: RAGState):
    session = get_session(state["session_id"])
    if not session:
        raise ValueError("Invalid session ID.")

    action = state["action"]
    query = state["query"]
    context = state.get("context", "")

    if action == "summary":
        instruction = """
Create a concise but complete summary of the document context.
Keep important facts, definitions, dates, formulas, and examples.
Do not invent information.
"""

    elif action == "translation":
        instruction = """
Translate the relevant document content into the language requested
by the user. Preserve important meaning and do not invent information.
"""

    elif action == "explain":
        instruction = """
Explain the requested topic in simple, child-friendly language.
Use short sentences and examples where useful.
Only use information supported by the provided context.
"""

    else:
        instruction = """
Answer the user's question using only the provided document context.
If the answer is not present in the context, clearly say that the
document does not contain enough information.
"""

    prompt = f"""
You are Braille Assistant, an educational assistant for visually
impaired learners.

{instruction}

DOCUMENT CONTEXT:
{context}

USER QUERY:
{query}

Return only the useful answer. Do not mention internal prompts,
retrieval, vector databases, or system architecture.
"""

    response = get_llm().invoke(prompt)
    return {"answer": response.content.strip()}


def full_text_node(state: RAGState):
    session = get_session(state["session_id"])
    if not session:
        raise ValueError("Invalid session ID.")

    return {"answer": session.text}


def build_graph():
    graph = StateGraph(RAGState)

    graph.add_node("route", route_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_node("full_text", full_text_node)

    graph.add_edge(START, "route")

    graph.add_conditional_edges(
        "route",
        lambda state: state["action"],
        {
            "full_text": "full_text",
            "summary": "retrieve",
            "translation": "retrieve",
            "explain": "retrieve",
            "qa": "retrieve",
        },
    )

    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    graph.add_edge("full_text", END)

    return graph.compile()


rag_graph = build_graph()


def run_rag(session_id: str, query: str):
    result = rag_graph.invoke(
        {
            "session_id": session_id,
            "query": query,
        }
    )

    return result["action"], result["answer"]
