from __future__ import annotations

from app.sync import check_sync

FI_OK = """<main id="main"><h1>Otsikko</h1><p>Teksti</p></main>"""
EN_OK = """<main id="main"><h1>Title</h1><p>Text</p></main>"""


def test_check_sync_passes_when_structurally_identical():
    result = check_sync(FI_OK, EN_OK)
    assert result.ok
    assert result.issues == []


def test_check_sync_flags_field_count_mismatch():
    en_extra = """<main id="main"><h1>Title</h1><p>Text</p><p>Extra</p></main>"""
    result = check_sync(FI_OK, en_extra)
    assert not result.ok
    assert any("Structural mismatch" in i for i in result.issues)


def test_check_sync_flags_blank_in_finnish():
    fi_blank = """<main id="main"><h1>Otsikko</h1><p></p></main>"""
    en_has_content = """<main id="main"><h1>Title</h1><p>Has content</p></main>"""
    result = check_sync(fi_blank, en_has_content)
    assert not result.ok
    assert any("empty in Finnish" in i for i in result.issues)


def test_check_sync_flags_blank_in_english():
    fi_has_content = """<main id="main"><h1>Otsikko</h1><p>Sisältöä</p></main>"""
    en_blank = """<main id="main"><h1>Title</h1><p></p></main>"""
    result = check_sync(fi_has_content, en_blank)
    assert not result.ok
    assert any("empty in English" in i for i in result.issues)


def test_check_sync_missing_main_element():
    result = check_sync("<div>no main</div>", EN_OK)
    assert not result.ok
    assert "main" in result.issues[0].lower()


def test_check_sync_both_blank_is_not_flagged():
    # Both sides empty is a (structural) parity, not a drift -- not this
    # check's job to demand content exist, only that it isn't asymmetric.
    fi = """<main id="main"><h1>Otsikko</h1><p></p></main>"""
    en = """<main id="main"><h1>Title</h1><p></p></main>"""
    result = check_sync(fi, en)
    assert result.ok
