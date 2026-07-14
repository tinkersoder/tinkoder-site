"""
Content extraction & in-place patching for Tinkoder's hand-written static HTML.

This site has no templating system: each .html file is the final, deployed
artifact. To edit "content" without risking the rest of the page (nav,
footer, SVG illustrations, inline scripts, exact whitespace) we do NOT
parse-and-reserialize the DOM. Reserialization with any HTML library
normalizes quoting, self-closing slashes, and whitespace in ways that would
produce a huge, noisy diff and risk subtly breaking hand-tuned markup.

Instead we use the stdlib `html.parser.HTMLParser` purely to *locate* the
byte offsets of editable regions in the original text, and patch the file
by slicing the original string. Everything outside an edited field's span
is preserved byte-for-byte.

Two kinds of editable "fields" are extracted, both scoped to the contents
of the single `<main id="main">...</main>` element (the per-page content
block — the shared header/nav/footer shell is intentionally out of scope,
matching how `_dev/content_pages.py` already separates shell from content):

- text fields: the inner HTML of leaf-ish, human-text-bearing elements
  (h1-h6, p, li, span, a, blockquote, figcaption, dt, dd, button, label,
  legend, option). Nested allowed tags (e.g. an <a> inside a <p>) are NOT
  captured separately -- they stay embedded in the parent's inner HTML so
  inline links/emphasis survive untouched unless the editor deliberately
  edits that HTML.
- attribute fields: `placeholder`, `alt`, `data-success`, `data-error` --
  user-facing strings that live in attributes rather than text nodes
  (form hints, image alt text, async status messages).

Fields are returned in document order. That order is the basis for pairing
a Finnish field with its English counterpart by position (see sync.py) --
the two files are hand-maintained mirrors of each other, verified to have
identical tag-structure counts.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser

# Leaf-ish tags whose inner HTML is treated as one editable text field.
ALLOWED_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "li", "span", "a", "blockquote", "figcaption",
    "dt", "dd", "button", "label", "legend", "option",
}

# HTML5 void elements: no closing tag appears in the source, so they must
# never be pushed onto the ancestor stack (there will be no matching
# handle_endtag to pop them).
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Attributes worth exposing as their own editable fields.
ATTR_FIELDS = ("placeholder", "alt", "data-success", "data-error")


@dataclass
class Field:
    index: int
    kind: str  # "text" | "attr"
    tag: str
    attr: str | None  # set when kind == "attr"
    start: int
    end: int
    raw: str  # exact original substring, text[start:end]
    group: str  # nearest ancestor id, for grouping fields in the UI
    preview: str = field(default="")

    def __post_init__(self):
        text_only = re.sub(r"<[^>]+>", " ", self.raw)
        text_only = html.unescape(text_only)
        text_only = " ".join(text_only.split())
        self.preview = (text_only[:80] + "…") if len(text_only) > 80 else text_only


class _StackEntry:
    __slots__ = ("tag", "attrs", "field_root")

    def __init__(self, tag: str, attrs: dict, field_root: bool):
        self.tag = tag
        self.attrs = attrs
        self.field_root = field_root


class MainNotFoundError(ValueError):
    """Raised when a page has no <main id="main"> element to scope extraction to."""


class _FieldExtractor(HTMLParser):
    def __init__(self, raw_text: str):
        super().__init__(convert_charrefs=False)
        self.raw_text = raw_text
        self._line_offsets = self._compute_line_offsets(raw_text)
        self.stack: list[_StackEntry] = []
        self.in_main = False
        self.saw_main = False
        self.active_field_depth: int | None = None
        self._active_field_tag: str | None = None
        self._active_field_start: int | None = None
        self.fields: list[Field] = []

    @staticmethod
    def _compute_line_offsets(text: str) -> list[int]:
        offsets = [0]
        for m in re.finditer("\n", text):
            offsets.append(m.end())
        return offsets

    def _abs_offset(self) -> int:
        line, col = self.getpos()
        return self._line_offsets[line - 1] + col

    def _nearest_group(self) -> str:
        for entry in reversed(self.stack):
            gid = entry.attrs.get("id")
            if gid:
                return gid
        return "content"

    def _record_attr_fields(self, tag: str, starttag_abs_start: int, raw_starttag: str):
        for attr_name in ATTR_FIELDS:
            m = re.search(rf'\b{re.escape(attr_name)}="([^"]*)"', raw_starttag)
            if not m:
                continue
            val_start = starttag_abs_start + m.start(1)
            val_end = starttag_abs_start + m.end(1)
            raw_val = self.raw_text[val_start:val_end]
            self.fields.append(Field(
                index=-1, kind="attr", tag=tag, attr=attr_name,
                start=val_start, end=val_end, raw=raw_val,
                group=self._nearest_group(),
            ))

    def handle_starttag(self, tag, attrs):
        self._handle_open(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._handle_open(tag, attrs, self_closing=True)

    def _handle_open(self, tag, attrs, self_closing: bool):
        abs_start = self._abs_offset()
        raw_starttag = self.get_starttag_text() or ""
        attrs_dict = {k: (v or "") for k, v in attrs}

        if tag == "main" and attrs_dict.get("id") == "main":
            self.saw_main = True

        if self.in_main or (tag == "main" and attrs_dict.get("id") == "main"):
            self._record_attr_fields(tag, abs_start, raw_starttag)

        is_void = tag in VOID_ELEMENTS or self_closing
        content_start = abs_start + len(raw_starttag)

        opens_field = (
            self.in_main
            and tag in ALLOWED_TAGS
            and self.active_field_depth is None
            and not is_void
        )

        if not is_void:
            self.stack.append(_StackEntry(tag, attrs_dict, field_root=opens_field))
            if tag == "main" and attrs_dict.get("id") == "main":
                self.in_main = True
            if opens_field:
                self.active_field_depth = len(self.stack)
                self._active_field_tag = tag
                self._active_field_start = content_start

    def handle_endtag(self, tag):
        if not self.stack:
            return
        # Find matching open tag from the top (handles minor malformed nesting
        # gracefully by popping down to the first matching tag name).
        for depth in range(len(self.stack), 0, -1):
            if self.stack[depth - 1].tag == tag:
                popped_depth = depth
                break
        else:
            return  # stray end tag with no opener; ignore

        abs_start = self._abs_offset()

        if self.active_field_depth is not None and popped_depth == self.active_field_depth:
            start = self._active_field_start
            end = abs_start
            raw = self.raw_text[start:end]
            group = "content"
            for entry in self.stack[:popped_depth - 1][::-1]:
                if entry.attrs.get("id"):
                    group = entry.attrs["id"]
                    break
            self.fields.append(Field(
                index=-1, kind="text", tag=self._active_field_tag, attr=None,
                start=start, end=end, raw=raw, group=group,
            ))
            self.active_field_depth = None
            self._active_field_tag = None
            self._active_field_start = None

        del self.stack[popped_depth - 1:]

        if not any(e.tag == "main" for e in self.stack):
            self.in_main = False


def extract_fields(html_text: str) -> list[Field]:
    """Extract editable fields (text + attribute) from a page's <main id="main">.

    Raises MainNotFoundError if the page has no such element.
    """
    parser = _FieldExtractor(html_text)
    parser.feed(html_text)
    parser.close()
    if not parser.saw_main:
        raise MainNotFoundError('no <main id="main"> element found')
    fields = sorted(parser.fields, key=lambda f: f.start)
    for i, f in enumerate(fields):
        f.index = i
    return fields


def apply_edits(html_text: str, edits: dict[int, str]) -> str:
    """Apply {field_index: new_raw_value} edits to html_text.

    Re-extracts fields from html_text itself so offsets are always fresh;
    callers should pass edits keyed by the index produced by the most
    recent extract_fields(html_text) call on this exact text. Raises
    ValueError if an index is out of range.
    """
    fields = extract_fields(html_text)
    by_index = {f.index: f for f in fields}
    for idx in edits:
        if idx not in by_index:
            raise ValueError(f"field index {idx} not found (page may have changed on disk)")

    # Apply from the end of the file backwards so earlier offsets stay valid.
    ordered = sorted(edits.items(), key=lambda kv: by_index[kv[0]].start, reverse=True)
    text = html_text
    for idx, new_value in ordered:
        f = by_index[idx]
        if f.kind == "attr":
            new_value = html.escape(new_value, quote=True)
        text = text[:f.start] + new_value + text[f.end:]
    return text
