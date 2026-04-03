#  AI Dev Copilot

> Paste code. Drop an error. Get expert-level debugging guidance — instantly.

AI Dev Copilot is a production-ready Streamlit application that sends your code (and optional error traceback) to Claude via the OpenRouter API and returns a structured, five-section analysis tailored to your experience level.

---

## Features

| Feature | Detail |
|---|---|
| **Code input** | Syntax-highlighted-ready text area with a demo loader |
| **Error input** | Optional traceback / error message box |
| **Experience levels** | Beginner · Intermediate · Expert — controls depth & tone |
| **Structured output** | Five clearly separated sections (see below) |
| **Model-agnostic** | Works with any OpenRouter model; defaults to Claude 3.5 Sonnet |

### Output Sections

1. **📖 Code Explanation** — what the code does
2. **🐛 Issues Found** — numbered list of problems
3. **🔍 Root Cause** — the underlying reason for the bug
4. **✅ Fix** — corrected code + change explanation
5. **💡 Best Practices** — actionable recommendations

---

##  Project Structure

```
ai-dev-copilot/
├── app.py                  # Streamlit UI entry point
├── requirements.txt
├── README.md
├── .env                    # API key (git-ignored)
│
├── src/
│   ├── __init__.py
│   ├── llm.py              # OpenRouter API call logic
│   ├── prompts.py          # System & user prompt templates
│   └── utils.py            # Response parser + helpers
│
├── components/
│   ├── __init__.py
│   ├── input_box.py        # Code + error input component
│   └── output_box.py       # Structured response display
│
└── assets/
    └── sample_code.txt     # Demo code for quick testing
```

---

##  Quick Start

### 1 — Clone & enter the directory

```bash
git clone https://github.com/your-org/ai-dev-copilot.git
cd ai-dev-copilot
```

### 2 — Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Configure your API key

Edit `.env` and replace the placeholder with your real key:

```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet   # optional override
```

Get a free OpenRouter key at <https://openrouter.ai/keys>.

### 5 — Run the app

```bash
streamlit run app.py
```

Open <http://localhost:8501> in your browser.

---

##  Configuration

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENROUTER_API_KEY` |  Yes | — | Your OpenRouter API key |
| `OPENROUTER_MODEL` | No | `anthropic/claude-3.5-sonnet` | Any OpenRouter model string |

---

##  Security Notes

- `.env` is **never** committed to version control (add it to `.gitignore`).
- API calls are made server-side; your key is never exposed to the browser.

---

##  Dependencies

- [Streamlit](https://streamlit.io/) ≥ 1.35
- [Requests](https://docs.python-requests.org/) ≥ 2.31
- [python-dotenv](https://pypi.org/project/python-dotenv/) ≥ 1.0

---

##  Contributing

Pull requests welcome. Please open an issue first to discuss what you'd like to change.

