"""Thin wrappers around `git` for draft/publish/version-history operations.

Drafts are just uncommitted working-tree changes to the real site files --
no separate draft store. Publishing stages specific files, commits, and
pushes to `origin`. Version history and revert shell out to `git log` /
`git checkout` on individual files, per the project brief.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .pages import SITE_ROOT


class GitError(RuntimeError):
    pass


def _run(args: list[str], cwd: Path | None = None) -> str:
    # `cwd` resolves against the *current* module-level SITE_ROOT at call
    # time, not a default bound once at function-definition time -- a
    # `cwd: Path = SITE_ROOT` default would freeze in whatever SITE_ROOT
    # was when this module was first imported, silently ignoring any later
    # reassignment (e.g. tests monkeypatching git_ops.SITE_ROOT to a
    # sandbox repo would have no effect, and commands would keep running
    # against the real site checkout).
    proc = subprocess.run(
        ["git", *args], cwd=cwd or SITE_ROOT, capture_output=True, text=True,
    )
    if proc.returncode != 0:
        raise GitError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def relpath(abs_path: Path) -> str:
    return str(abs_path.resolve().relative_to(SITE_ROOT.resolve()))


def is_dirty(abs_path: Path) -> bool:
    """True if the file has uncommitted changes (modified, staged, or untracked)."""
    out = _run(["status", "--porcelain", "--", relpath(abs_path)])
    return bool(out.strip())


def diff_stat(abs_path: Path) -> str:
    """Unified diff of working tree vs HEAD for a single file (empty if unchanged)."""
    try:
        return _run(["diff", "HEAD", "--", relpath(abs_path)])
    except GitError:
        return ""


@dataclass
class Commit:
    hexsha: str
    short: str
    date: str
    message: str


def log_for(abs_path: Path, limit: int = 20) -> list[Commit]:
    """git log for a single file, newest first."""
    fmt = "%H%x1f%h%x1f%ad%x1f%s"
    out = _run([
        "log", f"-{limit}", f"--date=format:%Y-%m-%d %H:%M",
        f"--pretty=format:{fmt}", "--", relpath(abs_path),
    ])
    commits = []
    for line in out.splitlines():
        if not line:
            continue
        hexsha, short, date, msg = line.split("\x1f", 3)
        commits.append(Commit(hexsha, short, date, msg))
    return commits


def show_at(abs_path: Path, revision: str) -> str:
    """Contents of a file at a specific revision."""
    return _run(["show", f"{revision}:{relpath(abs_path)}"])


def revert_to(abs_path: Path, revision: str) -> None:
    """Restore a file's working-tree content to a previous revision (uncommitted)."""
    _run(["checkout", revision, "--", relpath(abs_path)])


def discard_changes(abs_path: Path) -> None:
    """Discard uncommitted working-tree changes to a file, restoring HEAD's version."""
    _run(["checkout", "HEAD", "--", relpath(abs_path)])


def current_branch() -> str:
    return _run(["rev-parse", "--abbrev-ref", "HEAD"]).strip()


def status_porcelain() -> list[tuple[str, str]]:
    """All pending changes in the repo as (status_code, relpath) pairs."""
    out = _run(["status", "--porcelain"])
    result = []
    for line in out.splitlines():
        if not line:
            continue
        code, path = line[:2].strip(), line[3:]
        result.append((code, path))
    return result


def dirty_files_under(subdir: Path) -> list[Path]:
    """Absolute paths of every pending change (modified/staged/untracked)
    whose relpath falls inside `subdir` -- used to sweep newly uploaded
    media into a publish alongside the page files that reference them."""
    rel_prefix = relpath(subdir)
    out = []
    for _code, path in status_porcelain():
        if path == rel_prefix or path.startswith(rel_prefix + "/"):
            out.append(SITE_ROOT / path)
    return out


def commit_and_push(paths: list[Path], message: str) -> str:
    """Stage exactly `paths`, commit, and push to origin. Returns the new commit hexsha.

    Raises GitError if there is nothing to commit or if push fails --
    callers should treat push failure as needing manual follow-up (the
    commit itself will have succeeded and is not rolled back).
    """
    rels = [relpath(p) for p in paths]
    if not rels:
        raise GitError("no files given to commit")
    _run(["add", "--", *rels])
    staged = _run(["diff", "--cached", "--name-only"])
    if not staged.strip():
        raise GitError("nothing staged to commit (files may already match HEAD)")
    _run(["commit", "-m", message])
    hexsha = _run(["rev-parse", "HEAD"]).strip()
    branch = current_branch()
    _run(["push", "origin", branch])
    return hexsha
