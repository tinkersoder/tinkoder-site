"""Shared fixtures: a disposable git repo shaped like the real site, with
its own disposable bare 'origin' remote, so tests can exercise commit +
push for real without ever touching the actual tinkoder.fi repository.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

FI_HTML = """<!DOCTYPE html>
<html lang="fi">
<head><meta charset="utf-8"><title>Testisivu</title>
<link rel="stylesheet" href="css/styles.css">
</head>
<body>
<header>shared shell, out of scope</header>
<main id="main">
  <h1>Otsikko</h1>
  <p>Testiteksti suomeksi. <a href="/yhteys.html">Ota yhteyttä</a></p>
</main>
<footer>shared shell</footer>
<script src="js/script.js"></script>
</body>
</html>
"""

EN_HTML = """<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Test page</title>
<link rel="stylesheet" href="../css/styles.css">
</head>
<body>
<header>shared shell, out of scope</header>
<main id="main">
  <h1>Title</h1>
  <p>Test text in English. <a href="/en/contact.html">Get in touch</a></p>
</main>
<footer>shared shell</footer>
<script src="../js/script.js"></script>
</body>
</html>
"""


def _git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    assert proc.returncode == 0, f"git {args} failed: {proc.stderr}"
    return proc.stdout


@pytest.fixture
def site_repo(tmp_path: Path) -> Path:
    site = tmp_path / "site"
    origin = tmp_path / "origin.git"
    site.mkdir()
    (site / "css").mkdir()
    (site / "js").mkdir()
    (site / "assets").mkdir()
    (site / "en").mkdir()

    (site / "index.html").write_text(FI_HTML, encoding="utf-8")
    (site / "en" / "index.html").write_text(EN_HTML, encoding="utf-8")
    (site / "css" / "styles.css").write_text("body{}", encoding="utf-8")
    (site / "js" / "script.js").write_text("// noop", encoding="utf-8")
    # Git doesn't track empty directories -- commit a placeholder so
    # assets/ itself is a tracked path, matching the real repo (where
    # assets/ already has committed content). Otherwise a brand new
    # assets/uploads/ subtree collapses git's untracked-file reporting
    # up to "assets" itself rather than "assets/uploads/...".
    (site / "assets" / ".gitkeep").write_text("", encoding="utf-8")

    _git(site, "init", "-q", "-b", "main")
    _git(site, "config", "user.email", "test@example.com")
    _git(site, "config", "user.name", "Test")
    _git(site, "add", "-A")
    _git(site, "commit", "-q", "-m", "initial")

    _git(tmp_path, "init", "-q", "--bare", str(origin))
    _git(site, "remote", "add", "origin", str(origin))
    _git(site, "push", "-q", "-u", "origin", "main")

    return site


@pytest.fixture
def wired_modules(site_repo: Path, monkeypatch) -> Path:
    """Point the admin app's pages/git_ops modules at the sandbox repo
    instead of the real tinkoder.fi checkout, for the duration of a test."""
    from app import git_ops, pages

    test_pair = pages.PagePair("etusivu", "Test Page", "index.html", "en/index.html")
    monkeypatch.setattr(pages, "SITE_ROOT", site_repo)
    monkeypatch.setattr(pages, "PAGE_PAIRS", [test_pair])
    monkeypatch.setattr(git_ops, "SITE_ROOT", site_repo)
    return site_repo
