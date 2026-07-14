from __future__ import annotations

from app import auth


def test_check_token_false_when_unset(monkeypatch):
    monkeypatch.delenv("ADMIN_TOKEN", raising=False)
    assert not auth.admin_token_configured()
    assert not auth.check_token("anything")
    assert not auth.check_token("")


def test_check_token_matches_env_var(monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN", "s3cret")
    assert auth.admin_token_configured()
    assert auth.check_token("s3cret")
    assert not auth.check_token("wrong")
    assert not auth.check_token("")


def test_session_cookie_round_trip(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY", "test-secret-key")
    cookie = auth.make_session_cookie()
    assert auth._session_valid(cookie)


def test_session_cookie_rejects_tampering(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY", "test-secret-key")
    cookie = auth.make_session_cookie()
    assert not auth._session_valid(cookie + "tampered")
    assert not auth._session_valid(None)
    assert not auth._session_valid("")


def test_session_cookie_rejects_wrong_secret(monkeypatch):
    monkeypatch.setenv("ADMIN_SECRET_KEY", "secret-a")
    cookie = auth.make_session_cookie()
    monkeypatch.setenv("ADMIN_SECRET_KEY", "secret-b")
    assert not auth._session_valid(cookie)
