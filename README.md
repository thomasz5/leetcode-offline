## Offline LeetCode workflow with a local LLM in Cursor

This repo is set up to let you:
- Use a fully offline LLM in Cursor for coding help
- Scaffold new LeetCode problems quickly
- Write and run tests locally with `pytest`

### 1) Run a local LLM (pick one)

- Option A — Ollama (recommended on macOS with Apple Silicon)
  1. Install: `brew install ollama`
  2. Start the service: `ollama serve` (usually starts on `http://localhost:11434`)
  3. Pull a good code model (pick one that fits your RAM/VRAM):
     - `ollama pull qwen2.5-coder:7b`
     - `ollama pull qwen2.5-coder:14b`
     - `ollama pull llama3.1:8b`
     - `ollama pull codellama:7b-instruct`

- Option B — LM Studio (GUI)
  1. Download LM Studio, open it, and download a coding model (e.g., Qwen2.5 Coder or Code Llama)
  2. In LM Studio, start the Local Server (OpenAI compatible). Note the Base URL and port it shows

### 2) Point Cursor to your local model

In Cursor: Settings → Models → Add Provider → OpenAI Compatible
- Base URL:
  - Ollama: `http://localhost:11434/v1`
  - LM Studio: use the base URL it shows (e.g., `http://localhost:1234/v1`)
- API Key: any non-empty string (local servers usually ignore it)
- Default Model: match the model you pulled (e.g., `qwen2.5-coder:14b`)

Tip: You can create a "Local" provider and set it as default for Chat, Composer, and Inline.

### 3) Python test workflow

Create a venv and install deps:

```bash
cd /Users/Thomas/PROJECT/Leetcode
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q
```

### 4) Generate a new problem scaffold

Create a new problem (will create `problems/<slug>.py` and `tests/test_<slug>.py`):

```bash
python scripts/new_problem.py --name "two-sum" --title "Two Sum"
```

Then, fill in `solve(...)` and flesh out `tests/test_two-sum.py` with real cases.

### 4b) Verify your attempt against targeted tests

Place your solution attempt in `attempt/<name>.py` using a `class Solution` with the expected method name (e.g., `rotate`, `romanToInt`, etc.). Then run:

```bash
python scripts/verify_attempt.py --name "rotate"
```

This runs targeted sanity tests (and uses the matching reference in `question-answer/` if present to align method names).

### 5) Suggested prompts for quality answers (offline)

- "Given this problem description (pasted), propose the function signature and identify edge cases. Return only the signature and a bulleted list of edge cases."
- "Write `pytest` tests for the edge cases above. Return only the tests in valid Python."
- "Implement `solve(...)` to pass the tests. Return only the code for `problems/<slug>.py`."
- "Analyze time and space complexity. Return just Big-O for best/average/worst if relevant."

Keep the model grounded by always:
- Providing the exact file path and function to edit
- Asking for code-only when you want a drop-in edit
- Running `pytest` after edits and iterating

### 6) Notes

- Running completely offline: keep Cursor in local-only mode by using the OpenAI-compatible provider that points to your local server. Avoid cloud providers in settings if you want strict offline.
- Model sizing: If 14B is too heavy, try 7B variants. If you have plenty of RAM/VRAM, 14B often gives stronger coding performance.
- Language choice: This scaffold uses Python for speed and clarity. You can extend the generator for other languages.


