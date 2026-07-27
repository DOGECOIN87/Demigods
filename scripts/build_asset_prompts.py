#!/usr/bin/env python3
"""Emit one ready-to-run prompt per unregistered backlog asset.

There are well over a hundred assets still to produce. Hand-writing a prompt for
each would guarantee drift the moment a backlog row changes, so every prompt is
derived from `docs/trait-production-backlog.md`: the description, source cell,
production path and dependency all come from the row itself.

Rerun after editing the backlog. Output lands in `prompts/generated/`, one file
per category, and is safe to overwrite — nothing there is hand-maintained.

The shared contract carries the constraints each rejected candidate taught us:
native canvas, no background removal, bright partial alpha, no stray pixels, and
a per-category gate command with its proportion and contrast thresholds.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKLOG_ID = re.compile(r"^DG-\d{3}$")
ASSET_PATH = re.compile(r"^assets/(?P<category>[a-z_]+)/(?P<stem>[A-Za-z0-9_]+)\.png$")

# Layer number, human title, and the gate invocation for each category.
CATEGORIES: dict[str, tuple[int, str, str, str]] = {
    "backgrounds": (1, "full-bleed background", "n/a — backgrounds are opaque, not gated by the rig",
                    "full canvas, RGB or fully opaque RGBA, no transparency"),
    "rear_auras": (2, "rear aura / effect behind the character",
                   "--floor-aura for ground rings, --trait for body-centred glows",
                   "no width ceiling; auras vary by design"),
    "back_accessories": (3, "back accessory (wings / cape / cloak / mantle)", "--trait",
                         "no ceiling — wings and capes run 1.6-2.0x body width by design"),
    "hair_back": (4, "hair-back layer (rear hair only)", "--trait --max-width-ratio 1.35",
                  "target ~1.2x body width; top must reach Y 132 or above or a bald gap shows"),
    "outfits": (6, "outfit (clothing only)",
                "--trait --max-width-ratio 1.15 --min-skin-contrast 70",
                "a garment hugs the figure AND must clear skin tone (253,199,163) by 70+"),
    "neck_accessories": (7, "neck accessory", "--trait", "small layer; sits at the collar"),
    "eyes": (8, "eye set (matched pair)", "--trait", "align to eye line Y 367"),
    "eyebrows": (9, "eyebrow pair", "--trait", "sits above the eye line"),
    "mouths": (10, "mouth", "--trait", "align to mouth centre X 627, Y 441"),
    "expression_marks": (11, "expression mark overlay", "--trait", "small layer"),
    "hair_front": (12, "hair-front layer (bangs / face-framing strands only)",
                   "--trait --max-width-ratio 1.35",
                   "match the paired hair-back width; top must reach Y 132 or above"),
    "head_accessories": (13, "head accessory", "--trait --max-width-ratio 1.30",
                         "aligned to head centre X 627 Y 343 and top-of-head Y 141"),
    "hand_objects": (14, "hand-held object", "--trait", "aligned to the named hand anchor"),
    "front_auras": (15, "front aura / effect in front of the character", "--trait",
                    "no width ceiling; must not cover the eyes or mouth"),
}

# Markdown appended to a category file's header. Use for workflow and ordering
# that applies to the whole category rather than to one asset.
CATEGORY_NOTES: dict[str, str] = {
    "outfits": """
## Release-blocking category

`outfits` is listed in `generate_777.REQUIRED_CATEGORIES`, so `generate_777.py`
refuses to run while the category is empty. It is required because the base
bodies wear only a skin-toned mannequin garment — tank top `(252,218,182)` and
shorts `(247,211,174)` against cheek skin `(253,199,163)`. At full resolution
that garment reads fine; at marketplace thumbnail size the contrast disappears
and the chibi figures read as unclothed.

## The contrast gate

```bash
python scripts/rig_gate_report.py --trait <file> \\
  --max-width-ratio 1.15 --min-skin-contrast 70
```

`skin_contrast` is the **mean RGB distance between the layer's opaque pixels and
the reference skin colour `(253,199,163)`**. The mannequin garment measures about
**27**; a deep navy robe measures about **274**. Any candidate below **70** must
be rejected: pale, skin-adjacent garments make the character appear unclothed at
thumbnail size, which is the exact failure this category exists to prevent.

## Production order

Produce in this order rather than by ID:

1. **DG-045** — `outfit_009_navy_high_collar_coat` — category representative test
2. **DG-040** — `outfit_004_black_ragged_hooded_cloak`
3. **DG-042** — `outfit_006_black_layered_hooded_robe`

The remaining mid-tone designs may follow in any order. Leave the three pale
designs until last, because they carry the highest contrast risk and are the
likeliest to need several attempts:

- **DG-037** — `outfit_001_celestial_robe_white_silver`
- **DG-041** — `outfit_005_white_blue_armored_mantle`
- **DG-046** — `outfit_010_celestial_robe_white_gold`

DG-045 leads because deep navy gives the largest possible margin over skin tone,
so it clears the release blocker with the fewest rejected rounds. There is no
reason to gate the release behind the hardest cases in the set.

**Register three or four approved outfits before rendering the collection.** The
gate only needs one, but a single robe across all 777 tokens produces excessive
visual repetition — and fixing that later means re-rendering the whole set.

## Workflow for every outfit candidate

1. Upload the candidate to `images/trait_candidates/outfits/`.
2. Run the outfit gate with `--max-width-ratio 1.15` and `--min-skin-contrast 70`.
3. Composite it over `assets/base_bodies/base_body_001_neutral_master.png`.
4. Check the neck, head and hand openings, garment coverage, and whether any
   mannequin garment shows through.
5. Downscale the composite to **210 px** and confirm the character still clearly
   reads as clothed. This is the test the category exists to pass.
6. Obtain human approval.
7. Register the asset.
8. Run `python scripts/report_production_status.py --write`.
""",
}

# Extra contract text folded into every prompt for a category.
CATEGORY_CONTRACT: dict[str, str] = {
    "outfits": """

THUMBNAIL CONTRAST — the single most important requirement:
- the garment must be clearly distinguishable from skin tone (253,199,163) at
  THUMBNAIL size, not only at full resolution
- no cream, beige, tan, peach, or unsaturated flesh-adjacent fabric
- give the garment a defined outline and clear internal value structure so its
  silhouette reads at 210 px
- pale designs must carry cool shadow and a distinct contrasting trim colour,
  never a warm skin-adjacent midtone
- modest, opaque, floor-length ceremonial clothing only

FIT:
- neck opening at the collar, shoulders at Y 569, waist centre X 627 Y 808
- hem clear of foot baseline Y 1139; bare feet and ankles may show below it
- clean openings where head, neck and hands emerge, matching the base silhouette
- hidden overlap beneath the neck and hand openings so no seam shows
- capes, mantles and wings belong to the SEPARATE back-accessory layer

CONTENT: no nudity, lingerie, swimwear, exposed torso or hips, or emphasized
anatomical contours.""",
}

SHARED = """CANVAS — restated because generators drift to 1024:
- exactly 1254 x 1254 pixels, generated natively at that size
- never upscale, downscale, or resample anything to reach 1254 x 1254

DO NOT REMOVE A BACKGROUND:
- paint directly onto an empty transparent canvas
- do NOT render on black, white, or any backdrop and then key it to transparency
- background removal leaves the old backdrop in the colour channels and produces a
  gray matte fringe, which is an automatic rejection

ALPHA MUST STAY BRIGHT:
- every partial-alpha pixel keeps a bright colour value
- a pixel at alpha 30 must still read as its own colour, never as dark gray
- composited over pure WHITE the layer must not darken the background

STRAY PIXELS:
- every pixel outside the asset must be exactly alpha 0
- no alpha-1 dust, speckles, or haze anywhere else on the canvas

LOCKED RIG:
- canvas center X 627; head centre X 627 Y 343; eye line Y 367; mouth centre X 627 Y 441
- shoulder line Y 569; waist centre X 627 Y 808; foot baseline Y 1139
- viewer-left hand anchor X 404 Y 772; viewer-right hand anchor X 850 Y 772
- every visible pixel within X 233-1021 and Y 129-1139
- perfectly front-facing and orthographic, zero yaw/pitch/roll/perspective
- soft upper-left key light ~45 degrees, lower-right form shadows, subtle cool right rim
- clean silhouette, controlled cel shading, crisp anti-aliased edges, premium anime-chibi finish

ISOLATION:
- exactly the requested asset and nothing else
- no body, face, hair, clothing, accessory, object, aura, scenery, or contact shadow
  unless it IS the requested asset
- no text, letters, runes, pseudo-writing, watermark, border, frame, or contact sheet
- no duplicate variation, alternate colour, or before/after view"""


def parse_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Strip markup wholesale: edge-stripping leaves backticks that sit mid-cell,
        # e.g. "`FACE`, eyes r1c1".
        cells = [c.replace("`", "").replace("**", "").strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 8 or not BACKLOG_ID.fullmatch(cells[0]):
            continue
        match = ASSET_PATH.fullmatch(cells[5])
        if match is None:
            continue
        rows.append({
            "id": cells[0], "description": cells[2], "source": cells[3],
            "dependency": cells[4], "path": cells[5], "status": cells[7],
            "category": match.group("category"), "stem": match.group("stem"),
        })
    return rows


def render_prompt(row: dict[str, str]) -> str:
    layer, title, gate, proportion = CATEGORIES[row["category"]]
    if row["category"] == "backgrounds":
        opening = (
            f"Create exactly one full-bleed Demigods {title}, rendered NATIVELY at exactly "
            "1254 x 1254 pixels.\n\nATTACH: the matching reference image."
        )
        extra = (
            "\n\nBACKGROUND CONTRACT:\n"
            "- fill every canvas pixel; no transparency and no empty border\n"
            "- preserve a clear central staging region within X 233-1021 and Y 129-1139\n"
            "- provide a believable floor surface at foot baseline Y 1139 that a character\n"
            "  can stand on and a floor-ring aura can sit on\n"
            "- generate FULLY SHARP and UNVIGNETTED; the collection depth and colour grade is\n"
            "  applied afterward by scripts/apply_background_depth.py, and requesting it here\n"
            "  double-treats the image irreversibly\n"
            "- rebuild natively from the reference; never upscale, trace, tile, or patch it"
        )
    else:
        opening = (
            f"Create exactly one isolated Demigods {title}, rendered NATIVELY at exactly "
            "1254 x 1254 pixels as a PNG in RGBA mode with genuine transparent alpha.\n\n"
            "ATTACH: assets/base_bodies/base_body_001_neutral_master.png "
            "(placement/scale/lighting reference) + docs/rig/rig_guide_1254.png"
        )
        extra = ""

    extra += CATEGORY_CONTRACT.get(row["category"], "")

    return (
        f"{opening}\n\n{SHARED}{extra}\n\n"
        f"SUBJECT: {row['description']}.\n"
        f"- source reference: {row['source']}\n"
        f"- render this design only; do not substitute or embellish beyond the reference\n\n"
        f"PROPORTION: {proportion}.\n\n"
        f"OUTPUT: one {'opaque' if row['category'] == 'backgrounds' else 'transparent'} "
        f"1254 x 1254 PNG named {row['stem']}.png. No text, no alternate versions."
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backlog", type=Path, default=ROOT / "docs" / "trait-production-backlog.md")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "prompts" / "generated")
    args = parser.parse_args(argv)

    rows = [r for r in parse_rows(args.backlog) if r["status"] != "registered"]
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["category"] in CATEGORIES:
            grouped[row["category"]].append(row)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for stale in args.out_dir.glob("*.md"):
        stale.unlink()

    index = ["# Generated per-asset prompts", "",
             f"Generated by `python scripts/build_asset_prompts.py` from "
             f"`docs/trait-production-backlog.md`. **Do not hand-edit** — rerun instead.", "",
             "One prompt per unregistered backlog asset. Category templates live in "
             "`prompts/ready_to_run_trait_prompts.md`; the specific designs live here.", "",
             "| Category | Assets | File |", "|---|---|---|"]

    total = 0
    for category in sorted(grouped, key=lambda c: CATEGORIES[c][0]):
        # Always emit in ID order. Production order is expressed in CATEGORY_NOTES,
        # so backlog row order never silently reshuffles a generated file.
        entries = sorted(grouped[category], key=lambda r: r["id"])
        layer, title, gate, _ = CATEGORIES[category]
        lines = [f"# {category} — {len(entries)} assets to produce", "",
                 f"Layer {layer:02d}. Generated from the backlog; do not hand-edit.", "",
                 f"**Gate every candidate:** `python scripts/rig_gate_report.py {gate} <file>`", "",
                 "Then composite over `assets/base_bodies/base_body_001_neutral_master.png` "
                 "and confirm placement before requesting approval.", ""]
        if category in CATEGORY_NOTES:
            lines.append(CATEGORY_NOTES[category])
        lines.extend(["---", ""])
        for row in entries:
            lines.append(f"## {row['id']} — {row['stem']}\n")
            lines.append(f"Dependency: {row['dependency']}  \nPath: `{row['path']}`\n")
            lines.append("```text\n" + render_prompt(row) + "\n```\n")
        destination = args.out_dir / f"{category}.md"
        destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
        index.append(f"| `{category}` | {len(entries)} | `prompts/generated/{category}.md` |")
        total += len(entries)
        print(f"  {category:20s} {len(entries):3d} prompts")

    index.extend(["", f"**{total} assets** still to produce."])
    (args.out_dir / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"\n{total} prompts across {len(grouped)} categories -> {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
