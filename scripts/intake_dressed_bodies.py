#!/usr/bin/env python3
"""Normalize, review and register a batch of dressed-body outfit renders.

A dressed body is an outfit painted with the body intact (see
``scripts/normalize_dressed_body.py``). A batch is described by a sources file
kept beside the immutable renders, e.g.
``images/trait_candidates/outfits_dressed/sources.json``: one entry per render
naming its outfit family, its pose and the canonical output file, plus the
human review decision once there is one.

    # 1. normalize every render and draw the review sheets
    python scripts/intake_dressed_bodies.py images/trait_candidates/outfits_dressed/sources.json

    # 2. look at the sheets, record "review": {"decision": "approved", ...} per
    #    render in the sources file, then register the approved ones
    python scripts/intake_dressed_bodies.py images/trait_candidates/outfits_dressed/sources.json \\
        --register --qa-note docs/qa/dressed_bodies_2026-09-25.md

Registration copies the exact normalized bytes into ``assets/outfits/``, binds each
file to its base pose (``requires``), keeps that base out of the render (``hides``),
writes any ``excludes`` the review recorded, appends a manifest entry with the
full transform provenance, adds or flips the backlog row, and regenerates the
ledger. A render that fails the automated gates is never registered, whatever
its review says.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

try:
    from scripts import normalize_dressed_body as normalizer
    from scripts import validate_assets
except ImportError:  # Direct execution from scripts/.
    import normalize_dressed_body as normalizer  # type: ignore[no-redef]
    import validate_assets  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "asset_manifest.json"
BACKLOG = ROOT / "docs" / "trait-production-backlog.md"
COMPATIBILITY = ROOT / "config" / "compatibility.json"
PROMPT_PACK = "prompts/dressed_body_pose_pack_2026-09-25.md"

BASES = {
    "001": "base_body_001_neutral_master.png",
    "002": "base_pose_002_viewer_left_vertical_grip.png",
    "003": "base_pose_003_viewer_right_vertical_grip.png",
    "004": "base_pose_004_viewer_left_palm_up.png",
    "005": "base_pose_005_centered_two_hand_grip.png",
}
POSE_NAMES = {
    "001": "neutral, both hands open",
    "002": "viewer-left vertical grip",
    "003": "viewer-right vertical grip",
    "004": "viewer-left palm up",
    "005": "centered two-hand grip",
}
FACE_CATEGORIES = ("eyes", "eyebrows", "mouths", "expression_marks")
# Worst case for the face sheet: the widest blush, the lowest mouth, the highest brow.
FACE_SHEET_TRAITS = (
    "eyes/eyes_005_deep_blue.png",
    "eyebrows/eyebrows_012_bold_raised.png",
    "mouths/mouth_004_wide_open_smile.png",
    "expression_marks/expression_mark_001_pink_blush_strokes.png",
)
# Pixels where the union of every shared face trait would sit off the head or on
# its outline. These describe the accepted art rather than define it: the first
# twenty accepted renders measure 226-450 and 174-520, the registered base bodies
# themselves 90-252 off the head, and a black-robe render fitted with one uniform
# reduction - mouth on the chin, eye patches on the ears - 570-2530 and 467-1560.
FACE_OFF_HEAD_CEILING = 600
FACE_ON_OUTLINE_CEILING = 600
TRAIT_COVER = 32
OUTLINE_LUMINANCE = 150


# ---------------------------------------------------------------------------
# Measurements
# ---------------------------------------------------------------------------

def face_trait_union(assets: Path = ROOT / "assets") -> np.ndarray:
    """Where any registered eye, brow, mouth or expression mark puts paint."""
    union = np.zeros((normalizer.CANVAS, normalizer.CANVAS), np.uint8)
    for category in FACE_CATEGORIES:
        for path in sorted((assets / category).glob("*.png")):
            with Image.open(path) as image:
                union = np.maximum(union, np.asarray(image.convert("RGBA"))[..., 3])
    return union > TRAIT_COVER


def face_clearance(figure: np.ndarray, union: np.ndarray) -> dict[str, int]:
    """Face-trait pixels that would land off the head, or on its drawn outline."""
    alpha = figure[..., 3].astype(np.int32)
    luminance = 0.299 * figure[..., 0] + 0.587 * figure[..., 1] + 0.114 * figure[..., 2]
    off_head = union & (alpha < 250)
    on_outline = union & (alpha >= 250) & (luminance < OUTLINE_LUMINANCE)
    return {"off_head": int(off_head.sum()), "on_outline": int(on_outline.sum())}


def gates(path: Path, union: np.ndarray) -> tuple[bool, list[str], dict[str, int]]:
    """Automated gates a dressed body must pass before a human decision counts."""
    failures: list[str] = []
    result = validate_assets.validate_file(path, normalizer.CANVAS, normalizer.CANVAS,
                                           category="outfits")
    failures.extend(f"asset QA: {error}" for error in result.errors)
    with Image.open(path) as image:
        figure = np.asarray(image.convert("RGBA"))
    bbox = Image.fromarray(figure[..., 3]).getbbox()
    if bbox is None or bbox[1] != normalizer.TOP_OF_HEAD_Y or bbox[3] - 1 != normalizer.FOOT_BASELINE_Y:
        failures.append(f"crown and soles must sit on Y{normalizer.TOP_OF_HEAD_Y}-"
                        f"Y{normalizer.FOOT_BASELINE_Y}; bbox is {bbox}")
    clearance = face_clearance(figure, union)
    if clearance["off_head"] > FACE_OFF_HEAD_CEILING:
        failures.append(f"{clearance['off_head']} face-trait px would sit off the head "
                        f"(ceiling {FACE_OFF_HEAD_CEILING})")
    if clearance["on_outline"] > FACE_ON_OUTLINE_CEILING:
        failures.append(f"{clearance['on_outline']} face-trait px would cover the head's outline "
                        f"(ceiling {FACE_ON_OUTLINE_CEILING})")
    return not failures, failures, clearance


# ---------------------------------------------------------------------------
# Review sheets
# ---------------------------------------------------------------------------

def _grid_position(render: dict[str, Any], outfits: list[str]) -> tuple[int, int]:
    return outfits.index(render["outfit"]), int(render["pose"]) - 1


def render_sheets(renders: list[dict[str, Any]], out_dir: Path, sheet_dir: Path) -> list[Path]:
    """Two sheets: each figure with its base's silhouette in red, and each face
    wearing the worst-case shared traits."""
    sheet_dir.mkdir(parents=True, exist_ok=True)
    outfits = sorted({r["outfit"] for r in renders})
    faces = [Image.open(ROOT / "assets" / name).convert("RGBA") for name in FACE_SHEET_TRAITS]

    body_crop, body_w = (360, 120, 894, 1150), 300
    body_h = round(body_w * (body_crop[3] - body_crop[1]) / (body_crop[2] - body_crop[0]))
    face_crop = (440, 270, 814, 500)
    face_w, face_h = face_crop[2] - face_crop[0], face_crop[3] - face_crop[1]
    label = 16
    bodies = Image.new("RGB", (body_w * 5, (body_h + label) * len(outfits)), (28, 28, 30))
    face_sheet = Image.new("RGB", (face_w * 5, (face_h + label) * len(outfits)), (28, 28, 30))
    draw_b, draw_f = ImageDraw.Draw(bodies), ImageDraw.Draw(face_sheet)

    for render in renders:
        row, column = _grid_position(render, outfits)
        figure = Image.open(out_dir / render["target"]).convert("RGBA")
        with Image.open(ROOT / "assets" / "base_bodies" / BASES[render["pose"]]) as base:
            solid = np.asarray(base.convert("RGBA"))[..., 3] > 128
        edge = solid & ~ndi.binary_erosion(solid, iterations=2)
        tile = Image.new("RGBA", figure.size, (150, 150, 152, 255))
        tile.alpha_composite(figure)
        pixels = np.asarray(tile).copy()
        pixels[edge] = (255, 0, 0, 255)
        tile = Image.fromarray(pixels).convert("RGB").crop(body_crop).resize((body_w, body_h), Image.LANCZOS)
        bodies.paste(tile, (column * body_w, row * (body_h + label) + label))
        draw_b.text((column * body_w + 3, row * (body_h + label) + 2), render["target"][:-4], fill=(255, 255, 255))

        face = Image.new("RGBA", figure.size, (226, 226, 234, 255))
        face.alpha_composite(figure)
        for layer in faces:
            face.alpha_composite(layer)
        face_sheet.paste(face.crop(face_crop).convert("RGB"),
                         (column * face_w, row * (face_h + label) + label))
        draw_f.text((column * face_w + 3, row * (face_h + label) + 2), render["target"][:-4],
                    fill=(255, 255, 255))

    written = [sheet_dir / "figures_over_base_silhouette.png", sheet_dir / "faces_worst_case_traits.png"]
    bodies.save(written[0], optimize=True)
    face_sheet.save(written[1], optimize=True)
    return written


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def next_backlog_id(text: str) -> int:
    return max(int(n) for n in re.findall(r"^\| DG-(\d{3}) \|", text, re.MULTILINE)) + 1


def backlog_row(backlog_id: str, render: dict[str, Any], path: str) -> str:
    return (
        f"| {backlog_id} | outfit | {render['outfit_label']}, painted with the body intact, "
        f"Pose {render['pose']} ({POSE_NAMES[render['pose']]}) | `{render['source']}` | "
        f"Bound to `{BASES[render['pose']]}`, which it hides in the render | `{path}` | "
        f"`{PROMPT_PACK}` | registered |"
    )


def insert_outfit_row(text: str, row: str) -> str:
    """Append a row to the end of the Outfits table."""
    start = text.index("### Outfits")
    end = text.index("\n### ", start + 1)
    section = text[start:end]
    last = max(m.end() for m in re.finditer(r"^\| DG-\d{3} \|.*$", section, re.MULTILINE))
    return text[: start + last] + "\n" + row + text[start + last:]


def register(renders: list[dict[str, Any]], out_dir: Path, qa_note: str, sheets: list[Path]) -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    backlog = BACKLOG.read_text(encoding="utf-8")
    compatibility = json.loads(COMPATIBILITY.read_text(encoding="utf-8"))
    registered_paths = {e["path"] for e in manifest["registered_production_assets"]}
    today = date.today().isoformat()
    copies: list[tuple[Path, Path]] = []
    done: list[str] = []

    for render in renders:
        target = render["target"]
        path = f"assets/outfits/{target}"
        if path in registered_paths:
            print(f"skip {target}: already registered")
            continue
        candidate = out_dir / target
        provenance = json.loads(candidate.with_suffix(".provenance.json").read_text(encoding="utf-8"))
        sha = normalizer.sha256_file(candidate)
        if sha != provenance["output_sha256"]:
            print(f"error: {candidate} no longer matches its provenance hash", file=sys.stderr)
            return 1
        base = BASES[render["pose"]]

        existing = re.search(rf"^\| (DG-\d{{3}}) \|[^\n]*`{re.escape(path)}`[^\n]*$", backlog, re.MULTILINE)
        if existing:
            backlog_id = existing.group(1)
            line = existing.group(0)
            flipped = re.sub(r"\| (pending|candidate|approved|QA-failed) \|$", "| registered |", line)
            if flipped == line:
                print(f"error: backlog row {backlog_id} is not in a registerable state", file=sys.stderr)
                return 1
            backlog = backlog.replace(line, flipped)
        else:
            backlog_id = f"DG-{next_backlog_id(backlog):03d}"
            backlog = insert_outfit_row(backlog, backlog_row(backlog_id, render, path))

        manifest["registered_production_assets"].append({
            "id": f"outfit_{render['outfit']}_pose_{render['pose']}",
            "category": "outfits",
            "path": path,
            "status": "production_ready",
            "sha256": sha,
            "dimensions": [normalizer.CANVAS, normalizer.CANVAS],
            "format": "PNG",
            "mode": "RGBA",
            "backlog_id": backlog_id,
            "qa_composite": sheets[0].relative_to(ROOT).as_posix(),
            "provenance": {
                **{k: v for k, v in provenance.items() if k != "output_sha256"},
                "binds_pose": f"assets/base_bodies/{base}",
                "hides": ["base_bodies"],
                "review": render.get("review", {}).get("note", ""),
            },
            "approved_on": today,
            "qa_report": qa_note,
        })

        requires = compatibility.setdefault("requires", [])
        if not any(r.get("trait") == target and r.get("requires") == base for r in requires):
            requires.append({
                "trait": target,
                "requires": base,
                "reason": f"Painted with the body intact in Pose {render['pose']} "
                          f"({POSE_NAMES[render['pose']]}); the base binds the pose and the hand objects.",
            })
        hides = compatibility.setdefault("hides", [])
        if not any(h.get("trait") == target for h in hides):
            hides.append({
                "trait": target,
                "hides": "base_bodies",
                "reason": "Painted with the body intact; a bare copy of the base under it would show "
                          "wherever the two silhouettes differ, so the base is selected but not drawn.",
            })
        excluded = render.get("review", {}).get("excludes")
        if excluded:
            excludes = compatibility.setdefault("excludes", [])
            if not any(x.get("trait") == target for x in excludes):
                excludes.append({"trait": target, "excludes": sorted(excluded),
                                 "reason": render["review"]["excludes_reason"]})
        copies.append((candidate, ROOT / path))
        done.append(f"{backlog_id} {target}")

    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    BACKLOG.write_text(backlog, encoding="utf-8")
    COMPATIBILITY.write_text(json.dumps(compatibility, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for line in done:
        print(f"registered {line}")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "report_production_status.py"), "--write"],
                   check=True, cwd=ROOT)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sources", type=Path, help="sources JSON beside the immutable renders")
    parser.add_argument("--out-dir", type=Path, help="normalized candidates (default incoming/dressed_bodies_<received>)")
    parser.add_argument("--sheet-dir", type=Path, help="review sheets (default docs/qa/dressed_bodies_<received>)")
    parser.add_argument("--register", action="store_true", help="register every approved render that passes")
    parser.add_argument("--qa-note", help="repository path of the batch QA note; required with --register")
    args = parser.parse_args(argv)

    sources = json.loads(args.sources.read_text(encoding="utf-8"))
    received = sources["received"]
    out_dir = (args.out_dir or ROOT / "incoming" / f"dressed_bodies_{received}").resolve()
    sheet_dir = (args.sheet_dir or ROOT / "docs" / "qa" / f"dressed_bodies_{received}").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    renders = sources["renders"]
    union = face_trait_union()

    passing: list[dict[str, Any]] = []
    for render in renders:
        figure, report = normalizer.normalize(ROOT / render["source"])
        if report["source_sha256"] != render["sha256"]:
            print(f"error: {render['source']} does not match its recorded sha256", file=sys.stderr)
            return 1
        candidate = out_dir / render["target"]
        figure.save(candidate)
        report["output_sha256"] = normalizer.sha256_file(candidate)
        candidate.with_suffix(".provenance.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        passed, failures, clearance = gates(candidate, union)
        fit = report["fit"]
        decision = render.get("review", {}).get("decision", "unreviewed")
        print(f"{'PASS' if passed else 'FAIL'} {render['target']:52s} head {fit['head_scale']:.4f} "
              f"body {fit['body_scale']:.4f} face off/outline {clearance['off_head']}/"
              f"{clearance['on_outline']}  review: {decision}")
        for failure in failures:
            print(f"      - {failure}")
        if passed and decision == "approved":
            passing.append(render)

    sheets = render_sheets(renders, out_dir, sheet_dir)
    for sheet in sheets:
        print(f"sheet: {sheet.relative_to(ROOT)}")

    if not args.register:
        return 0
    if not args.qa_note:
        parser.error("--register needs --qa-note")
    return register(passing, out_dir, args.qa_note, sheets)


if __name__ == "__main__":
    raise SystemExit(main())
