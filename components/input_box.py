"""
components/input_box.py — Code + error input UI component

Now includes a file-upload widget that auto-fills the code text area.
Priority order for code content:
  1. Uploaded file (when a new file is provided)
  2. "Load demo" button
  3. Manual text typed by the user
"""

import streamlit as st
from pathlib import Path

from components.file_upload import render_file_uploader

_SAMPLE_PATH = Path(__file__).parent.parent / "assets" / "sample_code.txt"
_LEVELS = ["Beginner", "Intermediate", "Expert"]


def _load_sample() -> str:
    try:
        return _SAMPLE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def render_input_section() -> tuple[str, str, str]:
    """
    Render the left-panel input controls.
    Returns: (code_input, error_input, level)
    """
    # Level selector
    st.markdown("#### ⚙️ Experience Level")
    level = st.selectbox(
        label="Experience Level",
        options=_LEVELS,
        index=1,
        label_visibility="collapsed",
        help="Controls how detailed and technical the explanation will be.",
    )
    badge_class = {
        "Beginner":     "badge-beginner",
        "Intermediate": "badge-intermediate",
        "Expert":       "badge-expert",
    }.get(level, "badge-intermediate")
    st.markdown(f'<span class="level-badge {badge_class}">{level}</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Code source header row
    col_label, col_btn = st.columns([3, 1])
    with col_label:
        st.markdown("#### 📄 Your Code")
    with col_btn:
        load_sample = st.button("Load demo", use_container_width=True)

    # File uploader
    st.markdown(
        "<p style='color:#475569;font-size:0.78rem;margin:2px 0 6px;'>"
        "📂 Upload a <code>.py</code> or <code>.txt</code> file to auto-fill the box below"
        "</p>",
        unsafe_allow_html=True,
    )
    uploaded_content, uploaded_name = render_file_uploader()

    # Session state init
    if "code_value" not in st.session_state:
        st.session_state.code_value = ""
    if "last_uploaded_name" not in st.session_state:
        st.session_state.last_uploaded_name = ""

    new_file_loaded = (
        uploaded_name and uploaded_name != st.session_state.last_uploaded_name
    )

    if new_file_loaded:
        st.session_state.code_value = uploaded_content
        st.session_state.last_uploaded_name = uploaded_name
        st.toast(f"Loaded {uploaded_name} into the editor", icon="📂")
    elif load_sample:
        st.session_state.code_value = _load_sample()
        st.session_state.last_uploaded_name = ""

    # Source hint label
    if uploaded_name and uploaded_name == st.session_state.last_uploaded_name:
        source_hint = (
            f"<span style='color:#38bdf8;font-size:0.75rem;font-family:JetBrains Mono,monospace;'>"
            f"📂 {uploaded_name}</span>"
        )
    else:
        source_hint = "<span style='color:#334155;font-size:0.75rem;'>✏️ manual input</span>"

    st.markdown(f"<div style='margin-bottom:4px;'>{source_hint}</div>", unsafe_allow_html=True)

    code_input = st.text_area(
        label="Paste your code here",
        value=st.session_state.code_value,
        height=240,
        placeholder="# Paste your Python / JS / TypeScript / Go code here\n# — or upload a .py / .txt file above —",
        label_visibility="collapsed",
        key="code_textarea",
    )
    if not new_file_loaded:
        st.session_state.code_value = code_input

    # Error input
    st.markdown(
        "#### 🚨 Error / Traceback <span style='color:#475569;font-size:0.8rem'>(optional)</span>",
        unsafe_allow_html=True,
    )
    error_input = st.text_area(
        label="Paste error or traceback",
        height=120,
        placeholder="Traceback (most recent call last):\n  ...",
        label_visibility="collapsed",
        key="error_textarea",
    )

    return code_input, error_input, level
