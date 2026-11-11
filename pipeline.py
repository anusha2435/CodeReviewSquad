import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import MAX_FIX_ROUNDS
from llm import get_llm, build_messages
from prompts import PROMPTS
from retriever import retrieve
from router import route
from tools import static_report, run_code, run_tests

# which agents run for each intent, in order
PLAN = {
    "debug": ["bugs", "fix"],
    "style": ["style", "fix"],
    "explain": ["explain"],
    "test": ["tests"],
    "full_review": ["bugs", "style", "fix", "tests"],
}
# which knowledge_base folder each agent reads
CATEGORY = {"bugs": "debugging", "style": "style", "tests": "testing", "explain": "general"}


def run_agent(name: str, **variables) -> str:
    system, human = PROMPTS[name]
    chain = (ChatPromptTemplate.from_messages(build_messages(system, human))
             | get_llm() | StrOutputParser())
    return chain.invoke(variables)


def extract_code(text: str) -> str:
    blocks = re.findall(r"```(?:python)?\n(.*?)```", text, re.S)
    return max(blocks, key=len).strip() if blocks else text.strip()


def _guide(use_rag, step, code, request):
    if not use_rag:
        return "None"
    try:
        return retrieve(f"{request} {code[:400]}", CATEGORY[step]) or "None"
    except Exception:
        return "None"        # e.g. ChromaDB not ingested yet


def review(code: str, request: str = "", log=print) -> dict:
    result = {}
    intent, use_rag = route(request, code)
    result["intent"] = intent
    log(f"Router: intent = **{intent}**, retrieval = {use_rag}")
    steps = PLAN[intent]

    static = static_report(code)

    if "bugs" in steps:
        log("🐞 Bug-Finder working...")
        run = run_code(code)
        report = f"Syntax/flake8:\n{static}\n\nExecution output:\n{run['output'] or '(no output)'}"
        result["bugs"] = run_agent("bugs", code=code, tool_report=report,
                                   guidelines=_guide(use_rag, "bugs", code, request))

    if "style" in steps:
        log("🎨 Style/Lint agent working...")
        result["style"] = run_agent("style", code=code, tool_report=static,
                                    guidelines=_guide(use_rag, "style", code, request))

    if "explain" in steps:
        log("📖 Explaining code...")
        result["explanation"] = run_agent("explain", code=code,
                                          guidelines=_guide(use_rag, "explain", code, request))

    current = code
    if "fix" in steps:
        log("🧯 Fixer rewriting code...")
        out = run_agent("fix", code=code, bugs=result.get("bugs", "n/a"),
                        style=result.get("style", "n/a"), failures="none")
        current = extract_code(out)
        result["fixed_code"] = current

    if "tests" in steps:
        log("🧪 Test-Writer generating and running tests...")
        tests = extract_code(run_agent("tests", code=current,
                                       guidelines=_guide(use_rag, "tests", code, request)))
        res = run_tests(current, tests)
        rounds = 0
        while not res["ok"] and "fix" in steps and rounds < MAX_FIX_ROUNDS:
            rounds += 1
            log(f"🔁 Tests failed, fixer retry {rounds}/{MAX_FIX_ROUNDS}...")
            out = run_agent("fix", code=current, bugs=result.get("bugs", "n/a"),
                            style=result.get("style", "n/a"), failures=res["output"])
            current = extract_code(out)
            result["fixed_code"] = current
            res = run_tests(current, tests)
        result.update(tests=tests, test_output=res["output"],
                      tests_passed=res["ok"], fix_rounds=rounds)

    log("✅ Done")
    return result