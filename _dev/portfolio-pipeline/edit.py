"""
Auto-edit a candidate photo into web-ready and Instagram-ready exports:
color/exposure correction, platform crop, subtle logo watermark.

Usage:
  uv run edit.py IMG20260616082145.jpg --instagram --website
  uv run edit.py IMG20260616082145.jpg --instagram --website --all-candidates
"""
import argparse
from pathlib import Path

from PIL import Image, ImageOps, ImageEnhance

from common import (
    ensure_dirs, load_state, save_state,
    PORTFOLIO_DIR, REJECTED_DIR, STAGED_IG_DIR, STAGED_WEB_DIR,
)

LOGO_PATH = Path(__file__).parent / "logo" / "tinkoder-logo-transparent.png"

IG_SIZE = (1080, 1350)      # 4:5, Instagram portrait
WEB_SIZE = (1600, 1067)     # 3:2, sits well in a wide card


def auto_correct(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Color(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    return img


def cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize+crop to exactly fill target aspect ratio, centered."""
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_h = src_h
        new_w = int(src_h * target_ratio)
    else:
        new_w = src_w
        new_h = int(src_w / target_ratio)
    left = (src_w - new_w) // 2
    top = (src_h - new_h) // 2
    img = img.crop((left, top, left + new_w, top + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def watermark(img: Image.Image, margin_frac=0.03, width_frac=0.12, opacity=0.55) -> Image.Image:
    if not LOGO_PATH.exists():
        return img
    img = img.convert("RGBA")
    logo = Image.open(LOGO_PATH).convert("RGBA")
    target_w = int(img.width * width_frac)
    scale = target_w / logo.width
    logo = logo.resize((target_w, int(logo.height * scale)), Image.LANCZOS)

    alpha = logo.split()[3].point(lambda a: int(a * opacity))
    logo.putalpha(alpha)

    margin = int(img.width * margin_frac)
    pos = (img.width - logo.width - margin, img.height - logo.height - margin)
    img.alpha_composite(logo, pos)
    return img.convert("RGB")


def process_one(path: Path, do_ig: bool, do_web: bool, state: dict):
    img = Image.open(path)
    corrected = auto_correct(img)

    if do_ig:
        out = cover_crop(corrected, *IG_SIZE)
        out = watermark(out)
        dest = STAGED_IG_DIR / f"{path.stem}.jpg"
        out.save(dest, quality=90)
        print(f"  instagram -> {dest}")

    if do_web:
        out = cover_crop(corrected, *WEB_SIZE)
        out = watermark(out)
        dest = STAGED_WEB_DIR / f"{path.stem}.jpg"
        out.save(dest, quality=88, optimize=True)
        print(f"  website   -> {dest}")

    state[path.name]["status"] = "staged"
    state[path.name]["staged_platforms"] = [
        p for p, on in (("instagram", do_ig), ("website", do_web)) if on
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filenames", nargs="*", help="candidate filenames in the portfolio root")
    ap.add_argument("--instagram", action="store_true")
    ap.add_argument("--website", action="store_true")
    ap.add_argument("--all-candidates", action="store_true",
                     help="process every file currently marked 'candidate' in state")
    args = ap.parse_args()

    if not args.instagram and not args.website:
        ap.error("pass --instagram and/or --website")

    ensure_dirs()
    state = load_state()

    targets = list(args.filenames)
    if args.all_candidates:
        targets += [n for n, v in state.items() if v.get("status") == "candidate"]
    targets = sorted(set(targets))

    if not targets:
        print("Nothing to process. Pass filenames or --all-candidates.")
        return

    for name in targets:
        path = PORTFOLIO_DIR / name
        if not path.exists():
            print(f"skip {name}: not found in {PORTFOLIO_DIR}")
            continue
        if name not in state or state[name].get("status") != "candidate":
            print(f"skip {name}: not marked 'candidate' (run curate_prefilter.py first)")
            continue
        print(f"{name}:")
        process_one(path, args.instagram, args.website, state)

    save_state(state)


if __name__ == "__main__":
    main()
