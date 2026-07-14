from __future__ import annotations

import pytest

from app.content import MainNotFoundError, apply_edits, extract_fields

SAMPLE = """<html><body>
<main id="main">
  <h1>Hello</h1>
  <p>World <a href="/x">link</a></p>
  <img alt="a photo" src="x.jpg">
</main>
</body></html>"""


def test_extract_fields_finds_text_and_attr_fields():
    fields = extract_fields(SAMPLE)
    kinds = [(f.kind, f.tag) for f in fields]
    assert ("text", "h1") in kinds
    assert ("text", "p") in kinds
    assert ("attr", "img") in kinds


def test_extract_fields_raises_without_main():
    with pytest.raises(MainNotFoundError):
        extract_fields("<html><body><p>no main here</p></body></html>")


def test_apply_edits_only_touches_targeted_field_preserving_rest():
    fields = extract_fields(SAMPLE)
    h1 = next(f for f in fields if f.tag == "h1")
    new_text = apply_edits(SAMPLE, {h1.index: "Hi there"})
    assert "<h1>Hi there</h1>" in new_text
    assert '<p>World <a href="/x">link</a></p>' in new_text
    assert 'alt="a photo"' in new_text


def test_apply_edits_escapes_attr_values():
    fields = extract_fields(SAMPLE)
    img = next(f for f in fields if f.kind == "attr")
    new_text = apply_edits(SAMPLE, {img.index: 'a "quoted" alt'})
    assert 'alt="a &quot;quoted&quot; alt"' in new_text


def test_apply_edits_rejects_unknown_index():
    fields = extract_fields(SAMPLE)
    bad_index = max(f.index for f in fields) + 5
    with pytest.raises(ValueError):
        apply_edits(SAMPLE, {bad_index: "x"})
