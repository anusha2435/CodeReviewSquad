import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm import get_llm, build_messages

INTENTS = ["debug", "style", "explain", "test", "full_review"]

SYSTEM = """Classify the user's request about a code snippet.
intent must be one of: debug, style, explain, test, full_review.
- debug: find or fix bugs and errors
- style: readability, naming, lint, conventions
- explain: explain what the code does
- test: write or run tests
- full_review: general review, or unclear
retrieve: yes if coding guidelines or docs would help, no for a plain explanation.
Reply in exactly this format, nothing else:
intent: <word>
retrieve: <yes or no>"""


def route(request: str, code: str):
    """Returns (intent, use_rag)."""
    if not request.strip():
        return "full_review", True          # no request -> do everything
    try:
        chain = (ChatPromptTemplate.from_messages(
            build_messages(SYSTEM, "Request: {request}\n\nCode (start):\n{code}"))
            | get_llm() | StrOutputParser())
        out = chain.invoke({"request": request, "code": code[:500]}).lower()
        intent = re.search(r"intent:\s*(\w+)", out).group(1)
        use_rag = "retrieve: no" not in out
        return (intent if intent in INTENTS else "full_review"), use_rag
    except Exception:
        return "full_review", True          # safe fallback