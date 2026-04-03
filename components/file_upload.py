"""
components/file_upload.py — File upload widget for .py and .txt files

Reads the uploaded file and returns its text content so the caller
can pre-fill the code text area.  Falls back gracefully on decode errors.
"""

import streamlit as st

_ALLOWED_TYPES = ["py", "txt"]
_MAX_SIZE_BYTES = 500_000  # 500 KB — sensible cap for a code file


def render_file_uploader() -> tuple[str, str]:
    """
    Render the file-upload widget.

    Returns:
        (file_content, file_name)
        Both are empty strings when no file is uploaded or the file is invalid.
    """
    st.markdown(
        """
        <style>
        /* Upload zone */
        [data-testid="stFileUploader"] {
            background: #0d0f14 !important;
            border: 1px dashed #1e2533 !important;
            border-radius: 10px !important;
            padding: 0.4rem 0.8rem !important;
        }
        [data-testid="stFileUploader"]:hover {
            border-color: #38bdf8 !important;
        }
        [data-testid="stFileUploadDropzone"] {
            background: transparent !important;
        }
        /* File chip shown after upload */
        .file-chip {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: #0d3350;
            border: 1px solid #38bdf8;
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 0.78rem;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            margin-top: 6px;
        }
        .file-chip .size {
            color: #475569;
            font-size: 0.7rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        label="Upload a .py or .txt file",
        type=_ALLOWED_TYPES,
        accept_multiple_files=False,
        label_visibility="collapsed",
        key="code_file_upload",
        help="Upload a Python or plain-text file to auto-fill the code box.",
    )

    if uploaded is None:
        return "", ""

    # Size guard
    uploaded.seek(0, 2)          # seek to end
    size = uploaded.tell()
    uploaded.seek(0)             # reset

    if size > _MAX_SIZE_BYTES:
        st.error(
            f"File is too large ({size / 1024:.0f} KB). "
            f"Maximum allowed: {_MAX_SIZE_BYTES // 1024} KB."
        )
        return "", ""

    # Decode
    try:
        content = uploaded.read().decode("utf-8")
    except UnicodeDecodeError:
        try:
            uploaded.seek(0)
            content = uploaded.read().decode("latin-1")
        except Exception:
            st.error("Could not decode the file. Please ensure it is a UTF-8 text file.")
            return "", ""

    # File name badge
    ext_icon = "🐍" if uploaded.name.endswith(".py") else "📄"
    size_str = f"{size / 1024:.1f} KB" if size >= 1024 else f"{size} B"
    st.markdown(
        f'<div class="file-chip">'
        f'{ext_icon} {uploaded.name}'
        f'<span class="size">{size_str}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    return content, uploaded.name
