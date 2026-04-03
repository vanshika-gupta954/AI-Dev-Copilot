"""
src/utils.py — Formatting and parsing helpers
"""

import re
from dataclasses import dataclass, field


@dataclass
class ParsedResponse:
    """Structured container for the five output sections."""
    explanation: str = ""
    issues: str = ""
    root_cause: str = ""
    fix: str = ""
    best_practices: str = ""
    raw: str = ""


# Maps section header text → field name on ParsedResponse
_SECTION_MAP: dict[str, str] = {
    "Code Explanation": "explanation",
    "Issues Found":     "issues",
    "Root Cause":       "root_cause",
    "Fix":              "fix",
    "Best Practices":   "best_practices",
}

# Regex that matches any of the five H2 headings (emoji-prefixed or plain)
_SECTION_RE = re.compile(
    r"^##\s+(?:[^\w]*)?\s*(" + "|".join(re.escape(k) for k in _SECTION_MAP) + r")",
    re.MULTILINE,
)


def parse_structured_response(raw: str) -> ParsedResponse:
    """
    Parse the model's Markdown output into a ParsedResponse.

    Falls back gracefully — if a section is missing the field stays empty.
    """
    result = ParsedResponse(raw=raw)

    matches = list(_SECTION_RE.finditer(raw))
    if not matches:
        # Nothing parsed — store everything in explanation so it's still shown
        result.explanation = raw
        return result

    for idx, match in enumerate(matches):
        section_name = match.group(1)
        field_name = _SECTION_MAP.get(section_name)
        if not field_name:
            continue

        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(raw)
        content = raw[start:end].strip()
        setattr(result, field_name, content)

    return result


def sanitise_markdown(text: str) -> str:
    """
    Light sanitisation — strip leading/trailing blank lines.
    Streamlit renders Markdown natively so we don't need to escape.
    """
    return text.strip()


def word_count(text: str) -> int:
    """Return the approximate word count of a string."""
    return len(text.split())