# def build_prompt(code, error, level):
#     return f"""
# You are a senior software engineer.

# Analyze the following:

# CODE:
# {code}

# ERROR:
# {error}

# User Level: {level}

# Return in this format:

# 📘 Code Explanation:
# ...

# 🔍 Issues Found:
# ...

# 💥 Root Cause:
# ...

# ✅ Fix:
# ...

# 🚀 Best Practices:
# ...
# """

"""
src/prompts.py — All prompt templates (clean separation from business logic)
"""

# ── Level descriptions injected into the system prompt ─────────────────────────
LEVEL_GUIDANCE: dict[str, str] = {
    "Beginner": (
        "The user is a beginner. Use plain English, avoid jargon, "
        "give analogies where helpful, and keep explanations short and friendly."
    ),
    "Intermediate": (
        "The user has working knowledge of programming. "
        "Use correct technical terminology, reference language idioms, "
        "and explain the 'why' behind fixes concisely."
    ),
    "Expert": (
        "The user is an expert developer. Be precise and concise. "
        "Reference RFCs, language specs, algorithmic complexity, or design patterns "
        "where relevant. Skip hand-holding."
    ),
}


def build_system_prompt(level: str) -> str:
    """
    Return the system prompt tailored to the chosen experience level.

    Args:
        level: One of 'Beginner', 'Intermediate', 'Expert'.
    """
    guidance = LEVEL_GUIDANCE.get(level, LEVEL_GUIDANCE["Intermediate"])

    return f"""You are AI Dev Copilot, an elite software-engineering assistant.
Your job is to analyse code and/or error messages and return a structured, actionable response.

{guidance}

──────────────────────────────────────────────
RESPONSE FORMAT — you MUST follow this exactly:
──────────────────────────────────────────────

## 📖 Code Explanation
<A clear explanation of what the code does, written for the target level.>

## 🐛 Issues Found
<A numbered list of problems identified in the code or revealed by the error.
If no issues, write "No issues detected.">

## 🔍 Root Cause
<The underlying reason for the bug/error, or why the code may behave unexpectedly.
If no error was provided, describe any latent risks.>

## ✅ Fix
<A corrected version of the code (or the relevant section) in a fenced code block,
followed by a brief explanation of every change made.>

## 💡 Best Practices
<Three to five concrete, actionable best-practice recommendations relevant to this code.>

──────────────────────────────────────────────
Rules:
- Always include all five sections, even if brief.
- Code blocks must use triple backticks with a language tag (e.g. ```python).
- Do not add sections beyond the five listed above.
- Adapt tone and depth strictly to the experience level specified.
"""


def build_user_prompt(code: str, error: str) -> str:
    """
    Build the user turn from the supplied code and optional error string.

    Args:
        code:  The code snippet to analyse.
        error: Optional error message / traceback (may be empty).
    """
    parts = [f"### Code\n```\n{code.strip()}\n```"]

    if error and error.strip():
        parts.append(f"### Error / Traceback\n```\n{error.strip()}\n```")
    else:
        parts.append("### Error / Traceback\n_None provided — please review the code for potential issues._")

    parts.append("Please analyse the above and provide your structured response.")
    return "\n\n".join(parts)