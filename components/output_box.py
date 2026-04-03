"""
components/output_box.py — Structured response display component
"""

import streamlit as st

from src.utils import ParsedResponse, sanitise_markdown, word_count


# ── Section metadata ──────────────────────────────────────────────────────────
_SECTIONS = [
    {
        "field":   "explanation",
        "title":   "📖 Code Explanation",
        "color":   "#38bdf8",
        "default": True,
    },
    {
        "field":   "issues",
        "title":   "🐛 Issues Found",
        "color":   "#fb7185",
        "default": True,
    },
    {
        "field":   "root_cause",
        "title":   "🔍 Root Cause",
        "color":   "#f97316",
        "default": True,
    },
    {
        "field":   "fix",
        "title":   "✅ Fix",
        "color":   "#34d399",
        "default": True,
    },
    {
        "field":   "best_practices",
        "title":   "💡 Best Practices",
        "color":   "#c084fc",
        "default": False,
    },
]


def _section_card(title: str, content: str, color: str, expanded: bool) -> None:
    """Render one collapsible section card."""
    with st.expander(title, expanded=expanded):
        if content.strip():
            st.markdown(sanitise_markdown(content))
        else:
            st.info("No content returned for this section.")


def render_output_section(parsed: ParsedResponse, level: str) -> None:
    """
    Render all five output sections plus a quick-stats header.

    Args:
        parsed: ParsedResponse dataclass with section content.
        level:  Experience level string (for display).
    """
    # ── Stats row ──────────────────────────────────────────────────────────────
    total_words = word_count(parsed.raw)
    issues_detected = (
        "None detected" if "no issues" in parsed.issues.lower() else "Found"
    )

    st.markdown("#### 🧠 Analysis Results")

    m1, m2, m3 = st.columns(3)
    m1.metric("Level", level)
    m2.metric("Response Size", f"{total_words} words")
    m3.metric("Issues", issues_detected)

    st.markdown("<hr style='border-color:#1e2533;margin:0.8rem 0'>", unsafe_allow_html=True)

    # ── Section cards ─────────────────────────────────────────────────────────
    for meta in _SECTIONS:
        content = getattr(parsed, meta["field"], "")
        _section_card(
            title=meta["title"],
            content=content,
            color=meta["color"],
            expanded=meta["default"],
        )

    # ── Raw copy option ────────────────────────────────────────────────────────
    with st.expander("📋 Raw response", expanded=False):
        st.code(parsed.raw, language="markdown")
