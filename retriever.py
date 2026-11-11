from langchain_chroma import Chroma
from config import CHROMA_DIR
from llm import get_embeddings


def retrieve(query: str, category: str | None = None, k: int = 4) -> str:
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings(),
        collection_name="coding_kb",
    )
    flt = {"category": category} if category else None
    docs = db.similarity_search(query, k=k, filter=flt)
    return "\n\n".join(d.page_content for d in docs)