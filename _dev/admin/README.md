# Tinkoder admin GUI

A small, locally-run editing tool for tinkoder.fi's hand-written HTML pages
— **not** a hosted CMS. There's deliberately no GitHub OAuth app, no SaaS
account, no build step: it's a FastAPI process you run on your own machine
that edits the files already in this repo and, when you ask it to, commits
and pushes them like you would by hand.

## Why this exists

The site (`/`, `/en/*.html`) is hand-authored static HTML with no
templating layer — see the repo root `README.md`/`CLAUDE.md`. Editing
copy safely means never touching the header/nav/footer shell, and never
letting the Finnish and English versions of a page drift out of sync
(the site's one hard rule). This tool exists to make that safe and
pleasant without needing to hand-edit HTML or remember the sync rule
yourself.

## What it does

- **Lists every page pair** (`app/pages.py`'s registry) with dirty/clean
  and FI/EN-sync status at a glance.
- **Edits FI and EN side by side** — one row per editable field (text
  fields: headings/paragraphs/links/etc.; attribute fields: `alt`,
  `placeholder`, `data-success`, `data-error`), scoped to each page's
  `<main id="main">` (the shared shell is out of scope by design —
  `app/content.py` explains the extraction approach in detail).
- **Save draft** — writes edits straight to the real `.html` files on
  disk. This is *just* an uncommitted working-tree change; nothing is
  committed or pushed. Refresh/reload any time to see the current
  on-disk state.
- **Preview** — an iframe served from `/_site/...`, which reads the
  current on-disk (draft) content live, including its real `css/`, `js/`
  and `assets/` so it renders close to what will actually ship. It
  refuses to serve anything under `_dev/`, `.git/`, or `.github/`.
- **Publish** — the *only* action that touches git remote state: stages
  the page's FI+EN files (plus any pending uploads under
  `assets/uploads/`), commits, and pushes to `origin`. It is visually
  distinct from Save (amber, dashed border, its own confirm dialog) and
  is **blocked automatically** if the FI/EN sync check fails or if there
  is nothing pending to publish.
- **FI/EN sync validation** (`app/sync.py`) — the safety check that
  matters most. It verifies the two pages still expose the same number
  of editable fields (same shape) and that no field is left blank on one
  side while its counterpart has real content. This runs before every
  publish and is what actually blocks the button, not just a comment.
- **Media upload** — accepts a JPEG/PNG/WebP, downscales it (capped at
  1920px on the long edge, EXIF-orientation aware) via Pillow, and saves
  an optimized copy plus a `.webp` variant into `assets/uploads/`. Copy
  the returned path into a field and Save.
- **Version history / revert** — `git log`/`git show` per page file, with
  a one-click "revert to this revision" that runs `git checkout <rev> --
  <file>` (again, a working-tree change — publish it explicitly if you
  want it live) and a "discard uncommitted changes" shortcut
  (`git checkout HEAD -- <file>`).
- **Auth gate** — a single shared secret (`ADMIN_TOKEN`). Every route that
  writes anything (save, publish, revert, discard, media upload) requires
  a valid session; browsing (page list, viewing content, preview,
  history) works without logging in.

## Running it

```sh
cd _dev/admin
export ADMIN_TOKEN="pick something only you know"
# optional: export ADMIN_SECRET_KEY="..." to keep sessions valid across
# restarts (otherwise a random key is generated per process, and you'll
# just need to log in again after a restart)
uv run uvicorn app.main:app --reload
```

Then open <http://127.0.0.1:8000/>. Log in at `/login` with `ADMIN_TOKEN`
before trying to save, publish, upload, or revert anything.

If `ADMIN_TOKEN` isn't set, the app still runs in read-only ("just
looking") mode — every write route returns 401 and the login page tells
you it's not configured.

## Environment variables

| Variable            | Required | Purpose |
|---------------------|----------|---------|
| `ADMIN_TOKEN`        | Yes, for any write action | Shared secret checked at `/login`. |
| `ADMIN_SECRET_KEY`   | No | Signs the session cookie. Without it, a random key is generated per process (sessions don't survive a restart, but `ADMIN_TOKEN` still gates everything). |

Neither is read from a `.env` file automatically — export them in your
shell, or use `env ADMIN_TOKEN=... uv run uvicorn app.main:app`.

## Running the tests

```sh
cd _dev/admin
uv run pytest
```

Tests never touch the real tinkoder.fi repo or GitHub: `tests/conftest.py`
builds a disposable git repo shaped like the real site (plus its own
disposable bare "origin" remote) per test, and `app/git_ops.py` /
`app/pages.py` are monkeypatched to point at it. The one test that
exercises a real `publish` pushes only to that sandbox remote.

Coverage: field extraction/patching (`test_content.py`), the FI/EN sync
guard specifically (`test_sync.py`), image optimization
(`test_media.py`), the auth gate (`test_auth.py`), git plumbing
(`test_git_ops.py`), and the wired-up FastAPI routes end to end
(`test_main.py`, including that publish is genuinely blocked when pages
are out of sync or there's nothing pending).

## Layout

```
app/
  content.py   field extraction + in-place patching of the raw HTML
  pages.py     registry of FI/EN page pairs
  sync.py      the FI/EN parity check that gates Publish
  git_ops.py   git plumbing: dirty/log/commit+push/revert/discard
  auth.py      shared-secret + signed-cookie session gate
  media.py     Pillow-based resize + WebP generation for uploads
  main.py      FastAPI routes wiring all of the above together
templates/     Jinja2 templates (server-rendered, no JS framework)
static/        admin.css
tests/         pytest suite (see above)
```

## Things it deliberately does not do

- No database, no SQLite, no separate "draft" store — a draft is just an
  uncommitted change to the real file, per `git_ops.py`'s own design.
  There is nothing to gitignore here beyond the usual `.venv`/
  `__pycache__`/`.pytest_cache` (already covered by the repo root
  `.gitignore`).
- No migration of the site to a templating system or CMS data model —
  `content.py` reads and patches the existing hand-written HTML files
  in place, byte-for-byte outside the fields you actually edit.
- No hosted/SaaS anything, no GitHub OAuth app — that's a founder-level
  decision (see repo root `CLAUDE.md`), not something to bake in here.
