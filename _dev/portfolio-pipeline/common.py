"""Shared paths and state log for the portfolio pipeline."""
import json
from pathlib import Path

PORTFOLIO_DIR = Path("/mnt/ssdintenso/portfolio")
REJECTED_DIR = PORTFOLIO_DIR / "_rejected"
STAGED_DIR = PORTFOLIO_DIR / "_staged"
STAGED_IG_DIR = STAGED_DIR / "instagram"
STAGED_WEB_DIR = STAGED_DIR / "website"
ARCHIVE_DIR = PORTFOLIO_DIR / "_archive"
OUTBOX_DIR = PORTFOLIO_DIR / "_outbox" / "instagram"
STATE_DIR = PORTFOLIO_DIR / "_state"
STATE_FILE = STATE_DIR / "processed.json"

SOURCE_EXTS = {".jpg", ".jpeg", ".png", ".heic"}


def ensure_dirs():
    for d in (REJECTED_DIR, STAGED_IG_DIR, STAGED_WEB_DIR, ARCHIVE_DIR, OUTBOX_DIR, STATE_DIR):
        d.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def save_state(state: dict):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def new_source_files() -> list[Path]:
    """Files sitting directly in the portfolio root that haven't been logged yet."""
    state = load_state()
    files = []
    for p in sorted(PORTFOLIO_DIR.iterdir()):
        if p.is_file() and p.suffix.lower() in SOURCE_EXTS and p.name not in state:
            files.append(p)
    return files
