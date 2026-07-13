"""
Technical prefilter for new photos in /mnt/ssdintenso/portfolio.

This only catches objectively broken shots (blurry, too dark/bright, too
small) -- it has no idea what the photo shows or whether it's a good
representation of the work. That judgement call is made separately (by
Claude, reading the "candidate" images) before anything gets edited.

Usage: uv run curate_prefilter.py
"""
import numpy as np
from PIL import Image

from common import ensure_dirs, load_state, new_source_files, REJECTED_DIR

MIN_LONG_EDGE = 1000       # px, below this it's unusable for web/IG
BLUR_VARIANCE_MIN = 60.0   # Laplacian variance below this = too soft
DARK_MEAN_MAX = 25         # 0-255 mean luma below this = too dark
BRIGHT_MEAN_MIN = 235      # 0-255 mean luma above this = blown out


def laplacian_variance(gray: np.ndarray) -> float:
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    kh, kw = kernel.shape
    padded = np.pad(gray, 1, mode="edge")
    out = np.zeros_like(gray, dtype=np.float32)
    for i in range(kh):
        for j in range(kw):
            if kernel[i, j] == 0:
                continue
            out += kernel[i, j] * padded[i:i + gray.shape[0], j:j + gray.shape[1]]
    return float(out.var())


def score(path):
    img = Image.open(path)
    img.load()
    w, h = img.size
    gray = np.asarray(img.convert("L"), dtype=np.float32)
    # Downscale for speed on big phone photos; variance is scale-sensitive
    # so keep it consistent by capping the long edge before scoring.
    if max(w, h) > 1600:
        scale = 1600 / max(w, h)
        gray_img = Image.fromarray(gray).resize(
            (int(w * scale), int(h * scale))
        )
        gray = np.asarray(gray_img, dtype=np.float32)

    return {
        "width": w,
        "height": h,
        "sharpness": round(laplacian_variance(gray), 1),
        "mean_brightness": round(float(gray.mean()), 1),
    }


def verdict(s: dict) -> tuple[str, str]:
    if min(s["width"], s["height"]) == 0:
        return "reject", "unreadable"
    if max(s["width"], s["height"]) < MIN_LONG_EDGE:
        return "reject", f"resolution too low ({s['width']}x{s['height']})"
    if s["sharpness"] < BLUR_VARIANCE_MIN:
        return "reject", f"too blurry (sharpness {s['sharpness']})"
    if s["mean_brightness"] < DARK_MEAN_MAX:
        return "reject", f"too dark (mean brightness {s['mean_brightness']})"
    if s["mean_brightness"] > BRIGHT_MEAN_MIN:
        return "reject", f"blown out (mean brightness {s['mean_brightness']})"
    return "candidate", "passed technical prefilter"


def main():
    ensure_dirs()
    state = load_state()
    files = new_source_files()
    if not files:
        print("No new photos.")
        return

    for path in files:
        s = score(path)
        v, reason = verdict(s)
        state[path.name] = {"status": v, "reason": reason, "metrics": s}
        print(f"{v:9s} {path.name:30s} {reason}")
        if v == "reject":
            path.rename(REJECTED_DIR / path.name)

    from common import save_state
    save_state(state)

    n_candidates = sum(1 for v in state.values() if v["status"] == "candidate")
    print(f"\n{n_candidates} candidate(s) left in {files[0].parent} for visual review.")


if __name__ == "__main__":
    main()
