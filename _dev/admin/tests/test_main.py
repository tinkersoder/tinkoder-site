"""Integration tests against the real FastAPI app, wired to a disposable
sandbox repo (see conftest.py) -- never the real tinkoder.fi checkout, and
the one test that exercises a real publish pushes to a disposable bare
'origin', never GitHub.
"""
from __future__ import annotations

import io

from fastapi.testclient import TestClient
from PIL import Image

from app.content import extract_fields
from app.main import app


def _client() -> TestClient:
    return TestClient(app)


def _login(client: TestClient, monkeypatch, token: str = "s3cret") -> TestClient:
    monkeypatch.setenv("ADMIN_TOKEN", token)
    resp = client.post("/login", data={"token": token, "next": "/"}, follow_redirects=False)
    assert resp.status_code == 303
    return client


def test_dashboard_lists_pages(wired_modules):
    resp = _client().get("/")
    assert resp.status_code == 200
    assert "Test Page" in resp.text


def test_page_edit_readonly_without_login(wired_modules):
    resp = _client().get("/page/etusivu")
    assert resp.status_code == 200
    assert "Log in" in resp.text


def test_page_edit_unknown_slug_is_404(wired_modules):
    resp = _client().get("/page/does-not-exist")
    assert resp.status_code == 404


def test_save_requires_auth(wired_modules):
    resp = _client().post("/page/etusivu/save", data={})
    assert resp.status_code == 401


def test_publish_requires_auth(wired_modules):
    resp = _client().post("/page/etusivu/publish")
    assert resp.status_code == 401


def test_revert_requires_auth(wired_modules):
    resp = _client().post("/page/etusivu/revert", data={"lang": "fi", "revision": "HEAD"})
    assert resp.status_code == 401


def test_media_upload_requires_auth(wired_modules):
    resp = _client().post("/media/upload", files={"file": ("x.png", b"data", "image/png")})
    assert resp.status_code == 401


def test_login_wrong_token_rejected(wired_modules, monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN", "correct")
    resp = _client().post("/login", data={"token": "wrong", "next": "/"})
    assert resp.status_code == 401
    assert "Incorrect token" in resp.text


def test_save_edits_then_publish_flow(wired_modules, monkeypatch):
    client = _client()
    _login(client, monkeypatch)
    site = wired_modules

    fi_fields = extract_fields((site / "index.html").read_text(encoding="utf-8"))
    en_fields = extract_fields((site / "en" / "index.html").read_text(encoding="utf-8"))
    h1_fi = next(f for f in fi_fields if f.tag == "h1")
    h1_en = next(f for f in en_fields if f.tag == "h1")

    resp = client.post(
        "/page/etusivu/save",
        data={f"fi_{h1_fi.index}": "Uusi otsikko", f"en_{h1_en.index}": "New title"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert "saved=1" in resp.headers["location"]
    assert "Uusi otsikko" in (site / "index.html").read_text(encoding="utf-8")
    assert "New title" in (site / "en" / "index.html").read_text(encoding="utf-8")

    resp = client.post("/page/etusivu/publish", follow_redirects=False)
    assert resp.status_code == 303
    assert "published=" in resp.headers["location"]

    from app import git_ops
    assert not git_ops.is_dirty(site / "index.html")
    assert not git_ops.is_dirty(site / "en" / "index.html")


def test_publish_blocked_when_out_of_sync(wired_modules, monkeypatch):
    client = _client()
    _login(client, monkeypatch)
    site = wired_modules

    en_path = site / "en" / "index.html"
    en_html = en_path.read_text(encoding="utf-8")
    broken = en_html.replace("<h1>Title</h1>", "<h1></h1>")
    en_path.write_text(broken, encoding="utf-8")

    resp = client.post("/page/etusivu/publish")
    assert resp.status_code == 409
    assert "out of sync" in resp.text.lower()

    from app import git_ops
    assert git_ops.is_dirty(en_path)  # nothing was committed/pushed


def test_publish_blocked_with_nothing_pending(wired_modules, monkeypatch):
    client = _client()
    _login(client, monkeypatch)
    resp = client.post("/page/etusivu/publish")
    assert resp.status_code == 400
    assert "nothing to publish" in resp.text.lower()


def test_media_upload_end_to_end(wired_modules, monkeypatch):
    client = _client()
    _login(client, monkeypatch)
    buf = io.BytesIO()
    Image.new("RGB", (500, 500), (10, 20, 30)).save(buf, "PNG")
    resp = client.post("/media/upload", files={"file": ("test.png", buf.getvalue(), "image/png")})
    assert resp.status_code == 200
    data = resp.json()
    assert data["primary"].startswith("/assets/uploads/")
    assert data["webp"].endswith(".webp")


def test_preview_passthrough_serves_html_and_blocks_dev_paths(wired_modules):
    client = _client()
    resp = client.get("/_site/index.html")
    assert resp.status_code == 200
    assert "main" in resp.text.lower()

    resp2 = client.get("/_site/_dev/admin/app/main.py")
    assert resp2.status_code == 404
