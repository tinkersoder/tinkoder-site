from __future__ import annotations

import pytest

from app import git_ops


def test_is_dirty_and_log_for(wired_modules):
    site = wired_modules
    index = site / "index.html"
    assert not git_ops.is_dirty(index)
    log = git_ops.log_for(index)
    assert len(log) == 1
    assert log[0].message == "initial"


def test_commit_and_push_lands_in_origin(wired_modules):
    site = wired_modules
    index = site / "index.html"
    index.write_text(index.read_text(encoding="utf-8") + "\n<!-- edited -->", encoding="utf-8")
    assert git_ops.is_dirty(index)

    hexsha = git_ops.commit_and_push([index], "test: edit index")
    assert not git_ops.is_dirty(index)

    log = git_ops.log_for(index)
    assert log[0].hexsha == hexsha
    assert log[0].message == "test: edit index"


def test_commit_and_push_raises_when_nothing_to_commit(wired_modules):
    site = wired_modules
    index = site / "index.html"
    with pytest.raises(git_ops.GitError):
        git_ops.commit_and_push([index], "no-op")


def test_revert_to_restores_previous_content_uncommitted(wired_modules):
    site = wired_modules
    index = site / "index.html"
    original = index.read_text(encoding="utf-8")
    index.write_text(original + "\nCHANGED", encoding="utf-8")
    git_ops.commit_and_push([index], "test: change")

    log = git_ops.log_for(index)
    initial_rev = log[-1].hexsha  # oldest entry = the "initial" commit

    git_ops.revert_to(index, initial_rev)
    assert index.read_text(encoding="utf-8") == original
    assert git_ops.is_dirty(index)  # restored in the working tree, not committed


def test_discard_changes_restores_head(wired_modules):
    site = wired_modules
    index = site / "index.html"
    original = index.read_text(encoding="utf-8")
    index.write_text(original + "\nSCRATCH", encoding="utf-8")
    git_ops.discard_changes(index)
    assert index.read_text(encoding="utf-8") == original
    assert not git_ops.is_dirty(index)


def test_dirty_files_under_filters_by_prefix(wired_modules):
    site = wired_modules
    uploads = site / "assets" / "uploads"
    uploads.mkdir(parents=True)
    (uploads / "new.jpg").write_bytes(b"fake-bytes")
    (site / "index.html").write_text("changed content", encoding="utf-8")

    dirty = git_ops.dirty_files_under(site / "assets")
    resolved = {p.resolve() for p in dirty}

    # git may report either the individual new file or (if the containing
    # directory is entirely new) the collapsed directory line -- either is
    # fine here since `git add` on a directory recurses into it.
    assert any(
        r == (uploads / "new.jpg").resolve() or r == uploads.resolve()
        for r in resolved
    )
    assert not any(p.name == "index.html" for p in dirty)
