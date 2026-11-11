# Code Review & Debug Squad

A small multi-agent tool that reviews Python code the way a little engineering team would. You paste your code, and different AI agents find bugs, check style, fix the code, and write tests that are actually run to check the fix.

This is my project for Assignment 2.

## Why I made this

Students rarely get quick feedback on their code, and teachers can't check hundreds of submissions by hand. This tool gives fast, organised feedback so students can learn from their mistakes.

## What it does

You give it some Python code. It gives you back:

- a list of **bugs** (logic errors, edge cases, things that could crash)
- a **style review** (naming, readability, PEP 8)
- a **fixed version** of your code (with a diff so you can see what changed)
- **test cases** (pytest) that were run on the fixed code, with pass/fail results
- an **explanation** of the code, if you ask for one

## The agents

| Agent | What it does |
|---|---|
| Router | Reads your request and decides what you want: debug, style, explain, test, or a full review |
| Bug-Finder | Finds logic errors, edge-case failures and runtime risks |
| Style/Lint Agent | Checks naming, readability and Python conventions |
| Fixer | Rewrites the code to fix the problems found |
| Test-Writer | Writes pytest tests and runs them in the sandbox to check the fixed code |

If the tests fail, the Fixer gets the error messages and tries again (up to the retry limit I set).

## How it works

```
Your code + request
      │
   Router (what do you want?)
      │
   RAG: looks up coding guidelines in ChromaDB
      │
   Bug-Finder → Style Agent → Fixer → Test-Writer
                                          │
                              tests run inside Docker
      │
   Results shown in Streamlit tabs
```

**Agentic RAG:** I wrote short guideline notes (PEP 8, common bugs, edge cases, pytest tips) and stored them in ChromaDB. The router decides whether the guidelines are needed, and each agent only pulls notes from its own topic (style, debugging or testing).

**Sandbox:** Any code that gets run (your code, and the generated tests) runs inside a Docker container with no internet, a read-only file system, and memory/CPU limits. So bad or infinite-loop code can't harm my computer.

## Tech stack

- Frontend: Streamlit
- Backend: Python
- LLM: Google Gemini API or a local Ollama model
- LangChain: prompt templates and LCEL chains
- Vector DB: ChromaDB
- Tools: flake8, ast (syntax check), pytest, Docker

## Project structure

```
code-review-squad/
├── app.py              # Streamlit app
├── pipeline.py         # runs the agents in order
├── router.py           # works out the intent
├── prompts.py          # prompts for all agents
├── tools.py            # flake8 + Docker sandbox
├── llm.py              # picks the LLM and embeddings
├── config.py           # settings
├── ingest.py           # loads notes into ChromaDB
├── retriever.py        # searches ChromaDB
├── test_sandbox.py     # checks the sandbox is really isolated
├── Dockerfile.sandbox  # image used for the sandbox
├── requirements.txt
├── samples/            # buggy code I used for testing
└── knowledge_base/     # guideline notes (style, debugging, testing, general)
```

## How to set it up

You need: Python 3.11 or 3.12, Docker Desktop, and either Ollama or a Gemini API key from https://aistudio.google.com.

1. **Open a terminal in the project folder and make a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   (On Mac/Linux use `source venv/bin/activate`.)

2. **Install the packages**
   ```
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** in the project folder:
   ```
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=qwen2.5-coder:3b
   EMBED_MODEL=nomic-embed-text
   SANDBOX_TIMEOUT=15
   MAX_FIX_ROUNDS=1
   ```
   To use Gemini instead, set:
   ```
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=your-key-here
   GEMINI_MODEL=gemini-2.5-flash
   GEMINI_EMBED_MODEL=gemini-embedding-001
   SANDBOX_TIMEOUT=15
   MAX_FIX_ROUNDS=1
   ```
   If a model name doesn't work, copy the exact name from Google AI Studio.

4. **Start Docker Desktop** and wait until it says it is running.

5. **Build the sandbox image** (only once)
   ```
   docker build -f Dockerfile.sandbox -t squad-sandbox .
   ```

6. **Check the sandbox works**
   ```
   python test_sandbox.py
   ```
   Network access and file writing should both be blocked, and the infinite loop should time out.

7. **Load the guideline notes into ChromaDB**
   ```
   python ingest.py
   ```

8. **Run the app**
   ```
   streamlit run app.py
   ```
   Open http://localhost:8501 in your browser.
   The sidebar lets you choose Gemini or Ollama for each review.

## How to use it

1. Paste your Python code (or upload a `.py` file).
2. Type what you want, or leave it blank for a full review. Examples:
   - `find bugs`
   - `only check style`
   - `write tests`
   - `explain this code`
3. Click **Run review** and watch each agent work.
4. Look through the tabs: Bugs, Style, Fixed code, Tests, Explanation.

## Example

Input code with an empty-list crash, a mutable default argument and an off-by-one loop:

```python
def average(nums):
    total = 0
    for n in nums:
        total += n
    return total / len(nums)

def add_item(item, items=[]):
    items.append(item)
    return items

def GetMax(l):
    m = l[0]
    for i in range(1, len(l) + 1):
        if l[i] > m:
            m = l[i]
    return m
```

The tool found the division by zero, the mutable default, the off-by-one and the empty/None input problems. It also pointed out the bad names (`GetMax`, `l`). The fixed code passed all 8 generated tests inside Docker.

## My test results

I tested the tool on several snippets where I put in bugs on purpose.

| Snippet | Bugs I planted | Bugs found | False alarms | Tests passed |
|---|---|---|---|---|
| sample1 | 4 | 4 | 0 | Yes |
| sample2 | | | | |
| sample3 | | | | |
| sample4 | | | | |
| sample5 | | | | |

(Fill in with your own numbers.)

Screenshots are in the `screenshots/` folder, and the sandbox proof is in `sandbox_output.txt`.

## Limitations

- Only works for **Python** code.
- The AI can miss bugs or sometimes report things that aren't really bugs.
- The generated tests can also be wrong, so a "passed" result is a good sign but not a guarantee.
- The Fixer can rename functions when the style agent asks for it.
- The free Gemini API has rate limits, so very fast repeated runs can give a 429 error.
- Free API requests may be used by Google, so don't paste private code.
- Reviews take around a minute because several AI calls run one after another.

## Things I'd add next

- Support for other languages like Java or C++
- A security-check agent
- Review many student files at once (batch mode) for teachers
- Better scoring of the fixes

## Troubleshooting

| Problem | What to do |
|---|---|
| "Cannot connect to the Docker daemon" | Start Docker Desktop and wait for it to finish loading |
| Sidebar says "image missing" | Run the `docker build` command from step 5 |
| 429 error from the API | Wait a minute and try again |
| Retrieval gives nothing | Run `python ingest.py` again |
| Changed the LLM provider and got a dimension error | Delete the `chroma_db` folder and run `python ingest.py` again |

## Credits

Built with Streamlit, LangChain, ChromaDB, Docker, flake8 and pytest. The guideline notes are summaries I wrote based on PEP 8, PEP 257 and the pytest documentation.