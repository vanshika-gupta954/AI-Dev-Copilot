"""
components/input_box.py — Code + error input UI component
"""

import streamlit as st
from pathlib import Path


_SAMPLE_PATH = Path(__file__).parent.parent / "assets" / "sample_code.txt"
_LEVELS = ["Beginner", "Intermediate", "Expert"]


def _load_sample() -> str:
    """Load demo code from assets, silently return empty string on failure."""
    try:
        return _SAMPLE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def render_input_section() -> tuple[str, str, str]:
    """
    Render the left-panel input controls.

    Returns:
        (code_input, error_input, level)
    """
    # ── Level selector ─────────────────────────────────────────────────────────
    st.markdown("#### ⚙️ Experience Level")
    level = st.selectbox(
        label="Experience Level",
        options=_LEVELS,
        index=1,
        label_visibility="collapsed",
        help="Controls how detailed and technical the explanation will be.",
    )

    badge_class = {
        "Beginner": "badge-beginner",
        "Intermediate": "badge-intermediate",
        "Expert": "badge-expert",
    }.get(level, "badge-intermediate")

    st.markdown(
        f'<span class="level-badge {badge_class}">{level}</span>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Code input ─────────────────────────────────────────────────────────────
    col_label, col_btn = st.columns([3, 1])
    with col_label:
        st.markdown("#### 📄 Your Code")
    with col_btn:
        load_sample = st.button("Load demo", use_container_width=True)

    sample = _load_sample() if load_sample else ""

    # Preserve user's own text between reruns; only override when button clicked
    if "code_value" not in st.session_state or load_sample:
        st.session_state.code_value = sample

    code_input = st.text_area(
        label="Paste your code here",
        value=st.session_state.code_value,
        height=260,
        placeholder="# Paste your Python / JS / TypeScript / Go … code here",
        label_visibility="collapsed",
        key="code_textarea",
    )
    st.session_state.code_value = code_input

    # ── Error input ────────────────────────────────────────────────────────────
    st.markdown("#### 🚨 Error / Traceback <span style='color:#475569;font-size:0.8rem'>(optional)</span>", unsafe_allow_html=True)
    error_input = st.text_area(
        label="Paste error or traceback",
        height=130,
        placeholder="Traceback (most recent call last):\n  ...",
        label_visibility="collapsed",
        key="error_textarea",
    )

    return code_input, error_input, level