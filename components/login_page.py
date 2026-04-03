"""
components/login_page.py — Full-page login / signup UI component
"""

import streamlit as st
from src.auth import login_user, register_user

AUTH_CSS = """
<style>
.auth-logo {
    text-align: center;
    margin-bottom: 1.6rem;
}
.auth-logo .icon { font-size: 2.8rem; line-height: 1; }
.auth-logo h2 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800;
    font-size: 1.55rem;
    margin: 0.3rem 0 0.1rem;
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 60%, #fb7185 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.auth-logo p {
    color: #475569;
    font-size: 0.8rem;
    margin: 0;
    letter-spacing: 0.06em;
}
.auth-note {
    text-align: center;
    color: #334155;
    font-size: 0.72rem;
    margin-top: 1.2rem;
    line-height: 1.5;
}
</style>
"""


def render_auth_page() -> bool:
    """
    Render the login / signup page.
    Returns True when the user is authenticated.
    """
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    if st.session_state.get("authenticated"):
        return True

    _, card_col, _ = st.columns([1, 1.4, 1])

    with card_col:
        st.markdown(
            """
            <div class="auth-logo">
                <div class="icon">🛠️</div>
                <h2>AI Dev Copilot</h2>
                <p>YOUR INTELLIGENT CODE COMPANION</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if "auth_tab" not in st.session_state:
            st.session_state.auth_tab = "login"

        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("Log In", use_container_width=True, key="tab_login"):
                st.session_state.auth_tab = "login"
        with tab_col2:
            if st.button("Sign Up", use_container_width=True, key="tab_signup"):
                st.session_state.auth_tab = "signup"

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.auth_tab == "login":
            _render_login_form()
        else:
            _render_signup_form()

        st.markdown(
            '<div class="auth-note">By continuing you agree to our Terms of Service<br>and Privacy Policy.</div>',
            unsafe_allow_html=True,
        )

    return st.session_state.get("authenticated", False)


def _render_login_form() -> None:
    email = st.text_input("Email address", placeholder="you@example.com", key="login_email")
    password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

    if st.button("Log In →", use_container_width=True, key="login_submit"):
        if not email or not password:
            st.warning("Please fill in both fields.")
        else:
            ok, msg, user = login_user(email, password)
            if ok and user:
                st.session_state.authenticated = True
                st.session_state.user = user
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)


def _render_signup_form() -> None:
    name = st.text_input("Full name", placeholder="Jane Smith", key="signup_name")
    email = st.text_input("Email address", placeholder="you@example.com", key="signup_email")
    password = st.text_input("Password (min 6 chars)", type="password", placeholder="••••••••", key="signup_password")
    confirm = st.text_input("Confirm password", type="password", placeholder="••••••••", key="signup_confirm")

    if st.button("Create Account →", use_container_width=True, key="signup_submit"):
        if not email or not password:
            st.warning("Email and password are required.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            ok, msg = register_user(email, name, password)
            if ok:
                st.success(msg)
                st.session_state.auth_tab = "login"
                st.rerun()
            else:
                st.error(msg)
