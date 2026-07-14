"""Registry of editable page pairs (Finnish original <-> English mirror).

Deliberately excludes 404.html: it is a single bilingual file (both
languages in one document) rather than a FI/EN pair, and is low-value to
expose in a content GUI built around side-by-side pairs. It can still be
edited by hand like today.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# _dev/admin/app/pages.py -> app -> admin -> _dev -> <site root>
SITE_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class PagePair:
    slug: str
    title: str
    fi_path: str  # relative to SITE_ROOT
    en_path: str  # relative to SITE_ROOT


PAGE_PAIRS: list[PagePair] = [
    PagePair("etusivu", "Etusivu / Home", "index.html", "en/index.html"),
    PagePair("palvelut", "Palvelut / Services", "palvelut.html", "en/services.html"),
    PagePair("portfolio", "Portfolio", "portfolio.html", "en/portfolio.html"),
    PagePair("tietoa", "Tietoa / About", "tietoa.html", "en/about.html"),
    PagePair("yhteys", "Yhteystiedot / Contact", "yhteys.html", "en/contact.html"),
    PagePair("tietosuoja", "Tietosuoja / Privacy", "tietosuoja.html", "en/privacy.html"),
]

def get_pair(slug: str) -> PagePair | None:
    # Scans PAGE_PAIRS live (rather than a dict built once at import time)
    # so tests can monkeypatch PAGE_PAIRS with a fixture registry and have
    # get_pair() honor it immediately.
    return next((p for p in PAGE_PAIRS if p.slug == slug), None)


def fi_abs(pair: PagePair) -> Path:
    return SITE_ROOT / pair.fi_path


def en_abs(pair: PagePair) -> Path:
    return SITE_ROOT / pair.en_path
