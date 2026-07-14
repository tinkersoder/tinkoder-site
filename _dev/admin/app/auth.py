"""Shared-secret auth gate for write routes.

A single token read from the ADMIN_TOKEN environment variable gates every
route that can modify the working tree, upload media, or touch git
(save draft, publish, revert, discard, media upload). Read-only browsing
(listing pages, viewing content, preview, history) works without logging
in -- the project brief explicitly allows a GET-only "just looking" mode.

Session state is a signed cookie (itsdangerous), not a server-side store:
after POSTing the correct token to /login, the browser holds a cookie
asserting "this browser presented the correct token once". The cookie's
signature is verified on every write request and its payload carries an
issue time, so it expires (SESSION_MAX_AGE) even without an explicit
logout. Nothing here is meant to withstand a hostile network -- this is a
local single-operator tool, not a public login system.
"""
from __future__ import annotations

import hmac
import os
import secrets
from functools import lru_cache

from fastapi import HTTPException, Request, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

COOKIE_NAME = "tinkoder_admin_session"
SESSION_MAX_AGE = 60 * 60 * 12  # 12 hours
_SESSION_PAYLOAD = "authenticated"


@lru_cache(maxsize=1)
def _fallback_secret() -> str:
    # Only used if ADMIN_SECRET_KEY isn't set: sessions won't survive a
    # process restart, but ADMIN_TOKEN (checked on every /login) is what
    # actually gates access, so this is a usability fallback, not a hole.
    return secrets.token_hex(32)


def _secret_key() -> str:
    return os.environ.get("ADMIN_SECRET_KEY") or _fallback_secret()


def admin_token_configured() -> bool:
    return bool(os.environ.get("ADMIN_TOKEN"))


def check_token(submitted: str) -> bool:
    """Constant-time comparison against ADMIN_TOKEN. False if unset."""
    expected = os.environ.get("ADMIN_TOKEN")
    if not expected:
        return False
    return hmac.compare_digest(submitted or "", expected)


def make_session_cookie() -> str:
    serializer = URLSafeTimedSerializer(_secret_key())
    return serializer.dumps(_SESSION_PAYLOAD)


def _session_valid(cookie_value: str | None) -> bool:
    if not cookie_value:
        return False
    serializer = URLSafeTimedSerializer(_secret_key())
    try:
        payload = serializer.loads(cookie_value, max_age=SESSION_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return False
    return payload == _SESSION_PAYLOAD


def is_authenticated(request: Request) -> bool:
    return _session_valid(request.cookies.get(COOKIE_NAME))


def require_auth(request: Request) -> None:
    """FastAPI dependency for write routes: 401s unless the session is valid."""
    if not is_authenticated(request):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
