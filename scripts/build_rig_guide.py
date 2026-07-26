#!/usr/bin/env python3
"""Render the locked master rig as a transparent 1254x1254 overlay guide.

Reads the immutable anchors from ``config/collection.json`` and draws the
top-of-head line, foot baseline, center axis, maximum character bounds, and the
face/shoulder/waist/hand landmarks with labels. The result is a visual QA and
generation aid — NOT a production trait. It is written to ``docs/rig/`` so it
stays out of the production asset-discovery path.

Usage:
    python scripts/build_rig_guide.py [--config config/collection.json] [--out docs/rig/rig_guide_1254.png]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent

GUIDE = (0, 200, 255, 190)      # cyan lines
BOUNDS = (255, 90, 90, 220)     # red maximum-bounds box
AXIS = (255, 210, 0, 150)       # gold center axis
DOT = (120, 255, 120, 255)      # green hand anchors
LABEL = (255, 255, 255, 235)


def font(size: int):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", size)
    except Exception:
        return ImageFont.load_default()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=ROOT / "config" / "collection.json")
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "rig" / "rig_guide_1254.png")
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text())
    W, H = cfg["canvas"]["width"], cfg["canvas"]["height"]
    r = cfg["master_rig"]
    cx = r["canvas_center_x"]
    mb = r["maximum_character_bounds"]  # inclusive [x0,y0,x1,y1]

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(20)

    def hline(y, color, label, dashed=False):
        if dashed:
            for x in range(0, W, 24):
                d.line([(x, y), (min(x + 12, W), y)], fill=color, width=2)
        else:
            d.line([(0, y), (W, y)], fill=color, width=2)
        d.text((8, y + 4), label, fill=LABEL, font=f)

    # maximum character bounds box
    d.rectangle([mb[0], mb[1], mb[2], mb[3]], outline=BOUNDS, width=3)
    d.text((mb[0] + 6, mb[1] + 6), f"max bounds [{mb[0]},{mb[1]},{mb[2]},{mb[3]}]", fill=BOUNDS, font=f)

    # center axis
    d.line([(cx, 0), (cx, H)], fill=AXIS, width=2)
    d.text((cx + 6, 8), f"center X {cx}", fill=AXIS, font=f)

    # key horizontal anchors
    hline(r["top_of_head_y"], GUIDE, f"top of head  Y {r['top_of_head_y']}")
    hline(r["head_center"][1], GUIDE, f"head center  Y {r['head_center'][1]}", dashed=True)
    hline(r["eye_line_y"], GUIDE, f"eye line  Y {r['eye_line_y']}", dashed=True)
    hline(r["mouth_center"][1], GUIDE, f"mouth  Y {r['mouth_center'][1]}", dashed=True)
    hline(r["shoulder_line_y"], GUIDE, f"shoulder  Y {r['shoulder_line_y']}", dashed=True)
    hline(r["waist_center"][1], GUIDE, f"waist  Y {r['waist_center'][1]}", dashed=True)
    hline(r["foot_baseline_y"], GUIDE, f"foot baseline  Y {r['foot_baseline_y']}")

    # hand anchors
    for name, (hx, hy) in (("L-hand", r["viewer_left_hand_anchor"]),
                           ("R-hand", r["viewer_right_hand_anchor"])):
        d.ellipse([hx - 9, hy - 9, hx + 9, hy + 9], fill=DOT)
        d.text((hx + 12, hy - 10), f"{name} ({hx},{hy})", fill=LABEL, font=f)

    # head center crosshair
    hcx, hcy = r["head_center"]
    d.line([(hcx - 14, hcy), (hcx + 14, hcy)], fill=GUIDE, width=2)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    img.save(args.out)
    print(f"Wrote {args.out.relative_to(ROOT)}  ({W}x{H} RGBA)")
    print("Overlay a candidate on this guide for visual QA, or attach it to the "
          "image generator as the coordinate reference.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
