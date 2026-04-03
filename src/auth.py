"""
src/auth.py — Authentication helpers (email / password)

Users are persisted to users.json so accounts survive Streamlit reruns.
"""

import hashlib
import hmac
import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional

_DB_PATH = Path(__file__).parent.parent / "users.json"


def _load_db() -> dict:
    if _DB_PATH.exists():
        try:
            return json.loads(_DB_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_db(db: dict) -> None:
    _DB_PATH.write_text(json.dumps(db, indent=2), encoding="utf-8")


def _hash_password(password: str, salt: str) -> str:
    return hmac.new(salt.encode(), password.encode(), hashlib.sha256).hexdigest()


def _new_salt() -> str:
    return secrets.token_hex(16)


def register_user(email: str, name: str, password: str) -> tuple[bool, str]:
    """Register a new user. Returns (success, message)."""
    email = email.strip().lower()
    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    db = _load_db()
    if email in db:
        return False, "An account with this email already exists."

    salt = _new_salt()
    db[email] = {
        "email": email,
        "name": name.strip() or email.split("@")[0],
        "password_hash": _hash_password(password, salt),
        "salt": salt,
        "provider": "email",
        "created_at": datetime.utcnow().isoformat(),
    }
    _save_db(db)
    return True, "Account created! You can now log in."


def login_user(email: str, password: str) -> tuple[bool, str, Optional[dict]]:
    """Verify email + password. Returns (success, message, user_dict | None)."""
    email = email.strip().lower()
    db = _load_db()
    user = db.get(email)
    if not user:
        return False, "No account found for this email.", None

    expected = _hash_password(password, user["salt"])
    if not hmac.compare_digest(expected, user["password_hash"]):
        return False, "Incorrect password.", None

    return True, f"Welcome back, {user['name']}!", user
