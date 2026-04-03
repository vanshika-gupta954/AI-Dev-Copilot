"""
AI Dev Copilot — Main Streamlit Application
"""

import streamlit as st
from dotenv import load_dotenv

from components.login_page import render_auth_page
from components.input_box import render_input_section
from components.output_box import render_output_section
from src.llm import get_copilot_response
from src.utils import parse_structured_response

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Dev Copilot",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;800&display=swap');

    html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
    code, pre, .stTextArea textarea { font-family: 'JetBrains Mono', monospace !important; }

    .stApp { background-color: #0d0f14; color: #e2e8f0; }

    /* Header */
    .copilot-header {
        display: flex; align-items: center; gap: 14px;
        padding: 1.6rem 0 0.4rem 0;
    }
    .copilot-header .icon { font-size: 2.6rem; line-height: 1; }
    .copilot-header h1 {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800; font-size: 2.1rem; margin: 0;
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 60%, #fb7185 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .copilot-header p { color: #64748b; font-size: 0.85rem; margin: 0; letter-spacing: 0.06em; text-transform: uppercase; }

    /* User avatar chip */
    .user-chip {
        display: inline-flex; align-items: center; gap: 8px;
        background: #111520; border: 1px solid #1e2533;
        border-radius: 20px; padding: 5px 14px 5px 8px;
        font-size: 0.8rem; color: #94a3b8;
    }
    .user-chip .avatar {
        width: 26px; height: 26px; border-radius: 50%;
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 700; color: #0d0f14;
    }

    .section-divider { border: none; border-top: 1px solid #1e2533; margin: 1rem 0; }

    /* Level badge */
    .level-badge {
        display: inline-block; padding: 3px 12px; border-radius: 20px;
        font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em;
        text-transform: uppercase; margin-left: 6px;
    }
    .badge-beginner   { background: #064e3b; color: #34d399; }
    .badge-intermediate { background: #1e3a8a; color: #60a5fa; }
    .badge-expert     { background: #4c1d95; color: #c084fc; }

    /* Expanders */
    .stExpander { border: 1px solid #1e2533 !important; border-radius: 10px !important; background: #111520 !important; margin-bottom: 10px; }
    .stExpander summary { font-family: 'Syne', sans-serif !important; font-weight: 600 !important; color: #94a3b8 !important; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8, #818cf8) !important;
        color: #0d0f14 !important; border: none !important;
        font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
        font-size: 0.95rem !important; letter-spacing: 0.04em !important;
        padding: 0.55rem 2rem !important; border-radius: 8px !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.85 !important; }

    /* Text areas */
    .stTextArea textarea {
        background: #111520 !important; color: #e2e8f0 !important;
        border: 1px solid #1e2533 !important; border-radius: 8px !important;
        font-size: 0.82rem !important;
    }
    .stTextArea textarea:focus { border-color: #38bdf8 !important; box-shadow: 0 0 0 2px rgba(56,189,248,0.15) !important; }

    /* Select box */
    .stSelectbox > div > div {
        background: #111520 !important; border: 1px solid #1e2533 !important;
        color: #e2e8f0 !important; border-radius: 8px !important;
    }

    .stAlert { border-radius: 8px !important; font-size: 0.85rem !important; }
    .stSpinner { color: #38bdf8 !important; }

    .footer { text-align: center; color: #334155; font-size: 0.75rem; padding: 2rem 0 1rem; letter-spacing: 0.04em; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state defaults ─────────────────────────────────────────────────────
for key, default in [
    ("authenticated", False),
    ("user", None),
    ("result", None),
    ("parsed", None),
    ("loading", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Auth gate ──────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    render_auth_page()
    st.stop()

# ── App shell (authenticated users only) ──────────────────────────────────────
user = st.session_state.user or {}
user_name = user.get("name", "User")
user_initial = user_name[0].upper()

# Top bar
header_col, spacer, user_col = st.columns([5, 1, 2])

with header_col:
    st.markdown(
        """
        <div class="copilot-header">
            <span class="icon">🛠️</span>
            <div>
                <h1>AI Dev Copilot</h1>
                <p>Paste code · drop an error · get expert guidance instantly</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with user_col:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="user-chip">
            <div class="avatar">{user_initial}</div>
            <span>{user_name}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Sign out", key="signout"):
        for k in ("authenticated", "user", "result", "parsed",
                  "code_value", "last_uploaded_name"):
            st.session_state.pop(k, None)
        st.rerun()

st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

# ── Main layout ────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    code_input, error_input, level = render_input_section()

    run_clicked = st.button("⚡ Analyse Code", use_container_width=True)

    if run_clicked:
        if not code_input.strip():
            st.warning("Please paste or upload some code before analysing.")
        else:
            st.session_state.loading = True
            with st.spinner("Consulting your AI copilot…"):
                try:
                    raw = get_copilot_response(
                        code=code_input,
                        error=error_input,
                        level=level,
                    )
                    st.session_state.result = raw
                    st.session_state.parsed = parse_structured_response(raw)
                except Exception as exc:
                    st.error(f"API error: {exc}")
            st.session_state.loading = False

with right_col:
    if st.session_state.parsed:
        render_output_section(st.session_state.parsed, level)
    else:
        st.markdown(
            """
            <div style="
                height:360px; display:flex; flex-direction:column;
                align-items:center; justify-content:center;
                border:1px dashed #1e2533; border-radius:12px;
                color:#334155; font-size:0.9rem; gap:10px;
            ">
                <span style="font-size:2.5rem">🤖</span>
                <span>Your analysis will appear here</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">AI Dev Copilot · Powered by Claude via OpenRouter</div>',
    unsafe_allow_html=True,
)
