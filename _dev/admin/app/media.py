"""Local image optimization for uploaded media.

Uploaded images are downscaled (capped at MAX_DIMENSION on the long edge,
existing camera-orientation EXIF applied then dropped) and saved twice:
an optimized copy in a broadly-supported format (JPEG for photos, PNG kept
as PNG) plus a WebP variant, so a page's <img>/<picture> markup can pick
whichever it wants. Both land directly in the site's assets/uploads/
directory -- there is no separate cache or "original" store, matching the
rest of the tool's philosophy that a draft is just a file on disk, not a
row in some database.
"""
from __future__ import annotations

import io
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps

MAX_DIMENSION = 1920
JPEG_QUALITY = 82
WEBP_QUALITY = 80

# Content-Type -> output extension for the "primary" (non-WebP) copy.
ALLOWED_CONTENT_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}


class UnsupportedImageError(ValueError):
    """Raised for content types Pillow can't/shouldn't be asked to decode,
    or bytes that fail to decode as an image at all."""


@dataclass
class SavedImage:
    slug: str
    primary_path: Path  # absolute path to the optimized primary copy
    webp_path: Path     # absolute path to the WebP variant
    width: int
    height: int


def slugify_filename(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r"[^a-zA-Z0-9-]+", "-", stem).strip("-").lower()
    return stem or "image"


def _unique_slug(dest_dir: Path, slug: str, ext: str) -> str:
    """Find a slug that collides with neither the primary nor the webp file."""
    candidate = slug
    n = 2
    while (dest_dir / f"{candidate}.{ext}").exists() or (dest_dir / f"{candidate}.webp").exists():
        candidate = f"{slug}-{n}"
        n += 1
    return candidate


def optimize_and_save(
    data: bytes,
    original_filename: str,
    content_type: str,
    dest_dir: Path,
) -> SavedImage:
    """Resize `data` and write an optimized primary copy + a .webp copy into dest_dir.

    Raises UnsupportedImageError for anything that isn't a recognized image
    content type, or that Pillow can't decode.
    """
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise UnsupportedImageError(
            f"unsupported content type: {content_type!r} "
            f"(allowed: {', '.join(sorted(ALLOWED_CONTENT_TYPES))})"
        )

    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except Exception as exc:  # Pillow raises several distinct exception types
        raise UnsupportedImageError(f"could not decode image: {exc}") from exc

    img = ImageOps.exif_transpose(img) or img
    img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

    ext = ALLOWED_CONTENT_TYPES[content_type]
    dest_dir.mkdir(parents=True, exist_ok=True)
    slug = _unique_slug(dest_dir, slugify_filename(original_filename), ext)

    primary_path = dest_dir / f"{slug}.{ext}"
    if ext == "jpg":
        primary_img = img.convert("RGB") if img.mode in ("RGBA", "P") else img
        primary_img.save(primary_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
    elif ext == "png":
        img.save(primary_path, "PNG", optimize=True)
    else:  # webp requested as the primary format too
        img.save(primary_path, "WEBP", quality=WEBP_QUALITY)

    webp_path = dest_dir / f"{slug}.webp"
    if ext != "webp":
        webp_img = img.convert("RGBA") if img.mode == "P" else img
        webp_img.save(webp_path, "WEBP", quality=WEBP_QUALITY)

    return SavedImage(
        slug=slug,
        primary_path=primary_path,
        webp_path=webp_path,
        width=img.width,
        height=img.height,
    )
