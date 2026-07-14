from __future__ import annotations

import io

import pytest
from PIL import Image

from app.media import UnsupportedImageError, optimize_and_save


def _png_bytes(w: int = 400, h: int = 300, color=(200, 50, 50)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (w, h), color).save(buf, "PNG")
    return buf.getvalue()


def test_optimize_and_save_creates_primary_and_webp(tmp_path):
    saved = optimize_and_save(_png_bytes(), "My Photo.PNG", "image/png", tmp_path)
    assert saved.primary_path.exists()
    assert saved.webp_path.exists()
    assert saved.primary_path.suffix == ".png"
    assert saved.webp_path.suffix == ".webp"


def test_optimize_and_save_downscales_to_max_dimension(tmp_path):
    saved = optimize_and_save(_png_bytes(3000, 1000), "wide.png", "image/png", tmp_path)
    assert max(saved.width, saved.height) <= 1920
    # aspect ratio preserved (3:1)
    assert abs(saved.width / saved.height - 3.0) < 0.05


def test_optimize_and_save_leaves_small_images_unscaled(tmp_path):
    saved = optimize_and_save(_png_bytes(200, 150), "small.png", "image/png", tmp_path)
    assert (saved.width, saved.height) == (200, 150)


def test_optimize_and_save_slugifies_filename(tmp_path):
    saved = optimize_and_save(_png_bytes(200, 200), "Some Weird Name!! v2.png", "image/png", tmp_path)
    assert saved.slug == "some-weird-name-v2"


def test_optimize_and_save_dedupes_colliding_names(tmp_path):
    a = optimize_and_save(_png_bytes(), "dup.png", "image/png", tmp_path)
    b = optimize_and_save(_png_bytes(), "dup.png", "image/png", tmp_path)
    assert a.slug != b.slug
    assert a.primary_path.exists() and b.primary_path.exists()
    assert a.primary_path != b.primary_path


def test_optimize_and_save_rejects_unsupported_content_type(tmp_path):
    with pytest.raises(UnsupportedImageError):
        optimize_and_save(_png_bytes(), "x.gif", "image/gif", tmp_path)


def test_optimize_and_save_rejects_undecodable_bytes(tmp_path):
    with pytest.raises(UnsupportedImageError):
        optimize_and_save(b"garbage-not-a-real-image", "x.png", "image/png", tmp_path)
