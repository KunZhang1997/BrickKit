#!/usr/bin/env python3
"""Batch-convert BrickKit 1440px lossless-alpha RGBA WebP assets to 32-bit transparent PNGs.

Usage:
  pip install Pillow
  python3 scripts/export_png.py                  # exports all 1,053 items to ./exported-png/<category>/
  python3 scripts/export_png.py --category ai-compute
"""
import argparse
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Export BrickKit assets as 32-bit RGBA PNG files.")
    parser.add_argument("--output", type=Path, default=ROOT / "exported-png", help="Output directory")
    parser.add_argument("--category", type=str, default="", help="Optional category folder slug (e.g. ai-compute)")
    args = parser.parse_args()

    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    count = 0
    for item in catalog["items"]:
        rel = Path(item["path"])
        cat_slug = rel.parts[1]
        if args.category and cat_slug != args.category:
            continue
        src = ROOT / rel
        dst = args.output / cat_slug / f"{item['id']}.png"
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as im:
            im.convert("RGBA").save(dst, "PNG")
        count += 1

    print(f"Exported {count} transparent PNG files to {args.output}")


if __name__ == "__main__":
    main()
