"""FastAPI entrypoint wiring content.py / pages.py / git_ops.py / sync.py /
auth.py / media.py into an actual local admin GUI for tinkoder.fi.

Run with:  uv run uvicorn app.main:app --reload   (from _dev/admin/)
See _dev/admin/README.md for required environment variables.

Route map:
    GET  /                          dashboard: page list, dirty/sync status
    GET  /login, POST /login        token -> signed session cookie
    POST /logout
    GET  /page/{slug}                FI/EN side-by-side editor
    POST /page/{slug}/save           write draft edits to disk (no git)   [auth]
    POST /page/{slug}/publish        validate sync, commit + push        [auth]
    POST /page/{slug}/revert         git checkout <rev> -- <file>         [auth]
    POST /page/{slug}/discard        git checkout HEAD -- <file>          [auth]
    POST /media/upload               optimize + save into assets/uploads  [auth]
    GET  /_site/{path:path}          read-only passthrough of the live
                                     working tree, for the preview iframe

Only routes marked [auth] require a valid session (see app.auth). Every
other route is reachable without logging in -- intentional "just looking"
mode per the project brief. /page/*/save, /publish, /revert, /discard and
/media/upload are the only routes that write to disk; /publish is the only
one that touches git remote state (commit + push to origin).
"""
from __future__ import annotations

import itertools
from pathlib import Path

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import auth, content, git_ops, media, pages, sync

ADMIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ADMIN_ROOT / "templates"
STATIC_DIR = ADMIN_ROOT / "static"
UPLOADS_SUBDIR = "assets/uploads"

# Path prefixes that must never be served through the /_site preview
# passthrough, even though it otherwise reads straight off SITE_ROOT.
_PREVIEW_BLOCKED_PREFIXES = ("_dev", ".git", ".github")

_MEDIA_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".js": "application/javascript",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
    ".json": "application/json",
    ".xml": "application/xml",
    ".txt": "text/plain; charset=utf-8",
}

app = FastAPI(title="Tinkoder Admin")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _get_pair_or_404(slug: str) -> pages.PagePair:
    pair = pages.get_pair(slug)
    if pair is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"unknown page slug: {slug}")
    return pair


def _page_status(pair: pages.PagePair) -> dict:
    fi_path, en_path = pages.fi_abs(pair), pages.en_abs(pair)
    fi_dirty = git_ops.is_dirty(fi_path)
    en_dirty = git_ops.is_dirty(en_path)
    sync_ok = True
    if fi_path.is_file() and en_path.is_file():
        result = sync.check_sync(
            fi_path.read_text(encoding="utf-8"), en_path.read_text(encoding="utf-8")
        )
        sync_ok = result.ok
    else:
        sync_ok = False
    return {"pair": pair, "fi_dirty": fi_dirty, "en_dirty": en_dirty, "sync_ok": sync_ok}


def _page_edit_response(
    request: Request,
    pair: pages.PagePair,
    *,
    flash: str | None = None,
    flash_kind: str = "info",
    status_code: int = 200,
) -> HTMLResponse:
    fi_path, en_path = pages.fi_abs(pair), pages.en_abs(pair)
    fi_html = fi_path.read_text(encoding="utf-8")
    en_html = en_path.read_text(encoding="utf-8")
    result = sync.check_sync(fi_html, en_html)
    paired_fields = list(itertools.zip_longest(result.fi_fields, result.en_fields))
    context = {
        "pair": pair,
        "paired_fields": paired_fields,
        "sync_ok": result.ok,
        "sync_issues": result.issues,
        "fi_dirty": git_ops.is_dirty(fi_path),
        "en_dirty": git_ops.is_dirty(en_path),
        "history_fi": git_ops.log_for(fi_path, limit=10),
        "history_en": git_ops.log_for(en_path, limit=10),
        "authenticated": auth.is_authenticated(request),
        "token_configured": auth.admin_token_configured(),
        "flash": flash,
        "flash_kind": flash_kind,
    }
    return templates.TemplateResponse(
        request, "page_edit.html", context, status_code=status_code
    )


def _safe_site_path(rel_path: str) -> Path:
    rel = Path(rel_path)
    if rel.is_absolute() or ".." in rel.parts:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if rel.parts and (rel.parts[0].startswith(".") or rel.parts[0] in _PREVIEW_BLOCKED_PREFIXES):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    root = pages.SITE_ROOT.resolve()
    full = (root / rel).resolve()
    try:
        full.relative_to(root)
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not full.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return full


# --------------------------------------------------------------------------
# dashboard + auth
# --------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    rows = [_page_status(p) for p in pages.PAGE_PAIRS]
    return templates.TemplateResponse(request, "index.html", {
        "rows": rows,
        "authenticated": auth.is_authenticated(request),
        "token_configured": auth.admin_token_configured(),
    })


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request, next: str = "/"):
    return templates.TemplateResponse(request, "login.html", {
        "next": next, "error": None,
        "token_configured": auth.admin_token_configured(),
    })


@app.post("/login")
def login_submit(request: Request, token: str = Form(...), next: str = Form("/")):
    if not auth.check_token(token):
        return templates.TemplateResponse(
            request,
            "login.html",
            {
                "next": next,
                "error": "Incorrect token." if auth.admin_token_configured()
                         else "ADMIN_TOKEN is not configured on the server -- writes are disabled.",
                "token_configured": auth.admin_token_configured(),
            },
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    resp = RedirectResponse(url=next or "/", status_code=status.HTTP_303_SEE_OTHER)
    resp.set_cookie(
        auth.COOKIE_NAME, auth.make_session_cookie(),
        httponly=True, samesite="lax", max_age=auth.SESSION_MAX_AGE,
    )
    return resp


@app.post("/logout")
def logout():
    resp = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie(auth.COOKIE_NAME)
    return resp


# --------------------------------------------------------------------------
# page editor
# --------------------------------------------------------------------------

@app.get("/page/{slug}", response_class=HTMLResponse)
def page_edit(request: Request, slug: str):
    pair = _get_pair_or_404(slug)
    flash = None
    if request.query_params.get("saved"):
        flash, kind = "Draft saved locally (not published).", "success"
    elif request.query_params.get("published"):
        flash, kind = f"Published as commit {request.query_params['published']}.", "success"
    elif request.query_params.get("reverted"):
        flash, kind = f"Reverted to {request.query_params['reverted']}.", "success"
    elif request.query_params.get("discarded"):
        flash, kind = "Discarded uncommitted changes.", "success"
    else:
        kind = "info"
    return _page_edit_response(request, pair, flash=flash, flash_kind=kind)


@app.post("/page/{slug}/save")
async def page_save(request: Request, slug: str, _auth: None = Depends(auth.require_auth)):
    pair = _get_pair_or_404(slug)
    form = await request.form()

    fi_edits: dict[int, str] = {}
    en_edits: dict[int, str] = {}
    for key, value in form.multi_items():
        if key.startswith("fi_"):
            fi_edits[int(key[3:])] = str(value)
        elif key.startswith("en_"):
            en_edits[int(key[3:])] = str(value)

    fi_path, en_path = pages.fi_abs(pair), pages.en_abs(pair)
    try:
        if fi_edits:
            fi_html = fi_path.read_text(encoding="utf-8")
            new_fi = content.apply_edits(fi_html, fi_edits)
            if new_fi != fi_html:
                fi_path.write_text(new_fi, encoding="utf-8")
        if en_edits:
            en_html = en_path.read_text(encoding="utf-8")
            new_en = content.apply_edits(en_html, en_edits)
            if new_en != en_html:
                en_path.write_text(new_en, encoding="utf-8")
    except ValueError as exc:
        return _page_edit_response(
            request, pair, flash=f"Save failed: {exc}", flash_kind="error",
            status_code=status.HTTP_409_CONFLICT,
        )

    return RedirectResponse(url=f"/page/{slug}?saved=1", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/page/{slug}/publish")
def page_publish(request: Request, slug: str, _auth: None = Depends(auth.require_auth)):
    pair = _get_pair_or_404(slug)
    fi_path, en_path = pages.fi_abs(pair), pages.en_abs(pair)
    fi_html = fi_path.read_text(encoding="utf-8")
    en_html = en_path.read_text(encoding="utf-8")

    result = sync.check_sync(fi_html, en_html)
    if not result.ok:
        issues = "; ".join(result.issues)
        return _page_edit_response(
            request, pair,
            flash=f"Publish blocked -- Finnish and English are out of sync: {issues}",
            flash_kind="error", status_code=status.HTTP_409_CONFLICT,
        )

    paths = [fi_path, en_path]
    uploads_dir = pages.SITE_ROOT / UPLOADS_SUBDIR
    if uploads_dir.exists():
        paths += git_ops.dirty_files_under(uploads_dir)

    if not any(git_ops.is_dirty(p) for p in paths):
        return _page_edit_response(
            request, pair, flash="Nothing to publish -- no pending changes.",
            flash_kind="error", status_code=status.HTTP_400_BAD_REQUEST,
        )

    message = f"content: update {pair.title} ({pair.slug})"
    try:
        hexsha = git_ops.commit_and_push(paths, message)
    except git_ops.GitError as exc:
        return _page_edit_response(
            request, pair, flash=f"Publish failed: {exc}", flash_kind="error",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    return RedirectResponse(
        url=f"/page/{slug}?published={hexsha[:8]}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/page/{slug}/revert")
def page_revert(
    request: Request, slug: str, lang: str = Form(...), revision: str = Form(...),
    _auth: None = Depends(auth.require_auth),
):
    pair = _get_pair_or_404(slug)
    if lang not in ("fi", "en"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "lang must be 'fi' or 'en'")
    target = pages.fi_abs(pair) if lang == "fi" else pages.en_abs(pair)
    try:
        git_ops.revert_to(target, revision)
    except git_ops.GitError as exc:
        return _page_edit_response(
            request, pair, flash=f"Revert failed: {exc}", flash_kind="error",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )
    return RedirectResponse(
        url=f"/page/{slug}?reverted={revision[:8]}", status_code=status.HTTP_303_SEE_OTHER
    )


@app.post("/page/{slug}/discard")
def page_discard(
    request: Request, slug: str, lang: str = Form(...),
    _auth: None = Depends(auth.require_auth),
):
    pair = _get_pair_or_404(slug)
    if lang not in ("fi", "en"):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "lang must be 'fi' or 'en'")
    target = pages.fi_abs(pair) if lang == "fi" else pages.en_abs(pair)
    try:
        git_ops.discard_changes(target)
    except git_ops.GitError as exc:
        return _page_edit_response(
            request, pair, flash=f"Discard failed: {exc}", flash_kind="error",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )
    return RedirectResponse(url=f"/page/{slug}?discarded=1", status_code=status.HTTP_303_SEE_OTHER)


# --------------------------------------------------------------------------
# media upload
# --------------------------------------------------------------------------

@app.post("/media/upload")
async def media_upload(file: UploadFile = File(...), _auth: None = Depends(auth.require_auth)):
    data = await file.read()
    dest_dir = pages.SITE_ROOT / UPLOADS_SUBDIR
    try:
        saved = media.optimize_and_save(data, file.filename or "upload", file.content_type or "", dest_dir)
    except media.UnsupportedImageError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc))

    root = pages.SITE_ROOT.resolve()
    return {
        "primary": "/" + str(saved.primary_path.resolve().relative_to(root)),
        "webp": "/" + str(saved.webp_path.resolve().relative_to(root)),
        "width": saved.width,
        "height": saved.height,
    }


# --------------------------------------------------------------------------
# preview passthrough -- read-only, reflects on-disk draft state live
# --------------------------------------------------------------------------

@app.get("/_site/{rel_path:path}")
def preview_asset(rel_path: str):
    full = _safe_site_path(rel_path)
    media_type = _MEDIA_TYPES.get(full.suffix.lower(), "application/octet-stream")
    return FileResponse(str(full), media_type=media_type)
