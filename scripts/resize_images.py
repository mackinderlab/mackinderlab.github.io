"""Shrink oversized images before the site builds.

Photos uploaded through Pages CMS often come straight off a phone (4000px wide,
several MB). This script runs in the GitHub Actions build (see
.github/workflows/pages.yml) and resizes them on the build machine only, so the
published site is fast while the originals stay untouched in the repo.

Limits (longest side): people photos 800px, the home page banner 2560px,
everything else 1600px. Large JPEGs are also re-compressed.
"""

from pathlib import Path

import yaml
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "assets" / "images"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}
JPEG_RECOMPRESS_BYTES = 400_000


def banner_path():
    try:
        home = yaml.safe_load((ROOT / "_data" / "home.yml").read_text(encoding="utf-8")) or {}
        return (ROOT / str(home.get("banner", "")).lstrip("/")).resolve()
    except Exception:
        return None


def limit_for(path, banner):
    if banner and path.resolve() == banner:
        return 2560
    if "people" in path.relative_to(IMAGES).parts:
        return 800
    return 1600


def main():
    banner = banner_path()
    changed = 0
    for path in sorted(IMAGES.rglob("*")):
        if path.suffix.lower() not in EXTS or not path.is_file():
            continue
        try:
            with Image.open(path) as im:
                im.load()
                fmt = im.format
                limit = limit_for(path, banner)
                too_big = max(im.size) > limit
                heavy_jpeg = fmt == "JPEG" and path.stat().st_size > JPEG_RECOMPRESS_BYTES
                if not (too_big or heavy_jpeg):
                    continue
                before = path.stat().st_size
                out = ImageOps.exif_transpose(im)
                if too_big:
                    out.thumbnail((limit, limit), Image.LANCZOS)
                if fmt == "JPEG":
                    out.convert("RGB").save(path, "JPEG", quality=82, optimize=True, progressive=True)
                elif fmt == "PNG":
                    out.save(path, "PNG", optimize=True)
                else:
                    out.save(path, fmt)
        except Exception as exc:  # an odd file should never stop the build
            print(f"warning: skipped {path.relative_to(ROOT)}: {exc}")
            continue
        changed += 1
        print(f"resized {path.relative_to(ROOT)}: {before // 1024} KB -> {path.stat().st_size // 1024} KB")
    print(f"{changed} image(s) resized")


if __name__ == "__main__":
    main()
