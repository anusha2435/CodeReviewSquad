import difflib
import streamlit as st
import config
from pipeline import review
from tools import sandbox_status

st.set_page_config(page_title="Code Review & Debug Squad", layout="wide")
st.title("🛠️ Code Review & Debug Squad")

with st.sidebar:
    provider = st.selectbox(
        "LLM provider",
        options=("ollama", "gemini"),
        index=("ollama", "gemini").index(config.LLM_PROVIDER),
        key="llm_provider",
    )
    config.LLM_PROVIDER = st.session_state["llm_provider"]
    provider = config.LLM_PROVIDER
    model = config.OLLAMA_MODEL if provider == "ollama" else config.GEMINI_MODEL
    st.write(f"**LLM:** {provider} / {model}")
    st.write(f"**Sandbox:** {sandbox_status()}")
    st.caption("Supports Python code only.")

uploaded = st.file_uploader("Upload a .py file (optional)", type=["py"])
default = uploaded.read().decode("utf-8") if uploaded else ""
code = st.text_area("Paste your Python code", value=default, height=300)
request = st.text_input("What do you want? (optional)",
                        placeholder="e.g. 'find bugs', 'write tests', 'explain this'. Blank = full review")

if st.button("Run review", type="primary"):
    if not code.strip():
        st.warning("Please paste some code first.")
    else:
        config.LLM_PROVIDER = st.session_state["llm_provider"]
        with st.status("Crew is working...", expanded=True) as status:
            result = review(code, request, log=st.write)
            status.update(label="Done", state="complete")
        st.session_state["result"] = result
        st.session_state["code"] = code

result = st.session_state.get("result")
if result:
    sections = [("🐞 Bugs", "bugs"), ("🎨 Style", "style"), ("🧯 Fixed code", "fixed_code"),
                ("🧪 Tests", "tests"), ("📖 Explanation", "explanation")]
    available = [(t, k) for t, k in sections if k in result]
    st.caption(f"Detected intent: {result['intent']}")
    for tab, (title, key) in zip(st.tabs([t for t, _ in available]), available):
        with tab:
            if key == "fixed_code":
                diff = "\n".join(difflib.unified_diff(
                    st.session_state["code"].splitlines(), result[key].splitlines(),
                    "original", "fixed", lineterm=""))
                st.subheader("Diff")
                st.code(diff or "No changes", language="diff")
                st.subheader("Full fixed code")
                st.code(result[key], language="python")
                st.download_button("Download fixed.py", result[key], "fixed.py")
            elif key == "tests":
                st.code(result[key], language="python")
                if result.get("tests_passed"):
                    st.success("All tests passed")
                else:
                    st.error("Some tests failed")
                st.code(result["test_output"])
                st.download_button("Download test_fixed.py", result[key], "test_fixed.py")
            else:
                st.markdown(result[key])