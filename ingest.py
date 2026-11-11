import shutil
from pathlib import Path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from config import CHROMA_DIR
from llm import get_embeddings


def main():
    docs = []
    for p in Path("knowledge_base").rglob("*.md"):
        docs.append(Document(
            page_content=p.read_text(encoding="utf-8"),
            metadata={"source": p.name, "category": p.parent.name},
        ))
    if not docs:
        raise SystemExit("No .md files found in knowledge_base/")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=100
    ).split_documents(docs)

    shutil.rmtree(CHROMA_DIR, ignore_errors=True)   # avoids duplicates on re-run
    Chroma.from_documents(
        chunks, get_embeddings(),
        persist_directory=CHROMA_DIR, collection_name="coding_kb",
    )
    print(f"Ingested {len(docs)} files -> {len(chunks)} chunks")


if __name__ == "__main__":
    main()