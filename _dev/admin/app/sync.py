"""FI/EN sync validation -- the hard rule that both languages must never drift.

This does not (and cannot) verify that a translation is *correct*; it
verifies structural and completeness parity: the two pages must expose the
same number of editable fields (same shape), and no field may be left
empty on one side while its counterpart carries real content. Publishing
is blocked whenever this check fails.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass

from .content import Field, MainNotFoundError, extract_fields


@dataclass
class SyncResult:
    ok: bool
    issues: list[str]
    fi_fields: list[Field]
    en_fields: list[Field]


def _is_blank(raw: str) -> bool:
    text_only = re.sub(r"<[^>]+>", "", raw)
    text_only = html.unescape(text_only)
    return not text_only.strip()


def check_sync(fi_html: str, en_html: str) -> SyncResult:
    issues: list[str] = []
    try:
        fi_fields = extract_fields(fi_html)
    except MainNotFoundError:
        return SyncResult(False, ['Finnish page is missing <main id="main">'], [], [])
    try:
        en_fields = extract_fields(en_html)
    except MainNotFoundError:
        return SyncResult(False, ['English page is missing <main id="main">'], fi_fields, [])

    if len(fi_fields) != len(en_fields):
        issues.append(
            f"Structural mismatch: Finnish page has {len(fi_fields)} editable fields, "
            f"English page has {len(en_fields)}. The two pages must mirror each other's "
            f"structure -- fix by hand before publishing."
        )
        # Still compare the overlapping prefix so partial feedback is useful.

    for i in range(min(len(fi_fields), len(en_fields))):
        fi_f, en_f = fi_fields[i], en_fields[i]
        fi_blank, en_blank = _is_blank(fi_f.raw), _is_blank(en_f.raw)
        if fi_blank and not en_blank:
            issues.append(
                f"Field {i} ({fi_f.tag}, group '{fi_f.group}') is empty in Finnish "
                f"but has content in English: \"{en_f.preview}\""
            )
        elif en_blank and not fi_blank:
            issues.append(
                f"Field {i} ({en_f.tag}, group '{en_f.group}') is empty in English "
                f"but has content in Finnish: \"{fi_f.preview}\""
            )

    return SyncResult(ok=not issues, issues=issues, fi_fields=fi_fields, en_fields=en_fields)
