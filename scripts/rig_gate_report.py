#!/usr/bin/env python3
"""Rig-gate diagnostic for Demigods base-pose / master candidates.

Unlike ``intake_approved_base.py`` (which enforces a binary accept/reject), this
tool *measures* a candidate's alpha silhouette against the locked master rig in
``config/collection.json`` and reports the exact per-anchor pixel deltas — the
same numbers the manual QA table records — plus the scale/offset that would be
needed to align it. It never writes, resizes, or registers a production asset;
it only reports, so it is safe to run on any candidate at any time.

Provable-from-alpha gates: top-of-head Y, foot-baseline Y, horizontal center X,
and the maximum character bounds. Face/hand/waist anchors remain manual overlay
gates (they cannot be derived from the silhouette alone) and are printed as
reference targets only.

Usage:
    python scripts/rig_gate_report.py <file-or-dir> [more ...] [--tolerance N]
                                      [--config config/collection.json] [--json-report out.json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: pip install -r requirements.txt") from exc

ROOT = Path(__file__).resolve().parent.parent


def load_rig(config_path: Path) -> dict:
    cfg = json.loads(config_path.read_text())
    return {"canvas": cfg["canvas"], "rig": cfg["master_rig"]}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inclusive_alpha_bounds(image: Image.Image) -> tuple[int, int, int, int] | None:
    """Return inclusive (left, top, right, bottom) of non-zero alpha, or None."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()  # exclusive right/bottom, or None if fully transparent
    if bbox is None:
        return None
    left, top, right, bottom = bbox
    return (left, top, right - 1, bottom - 1)  # inclusive


def band_center_x(image: Image.Image, y0: int, y1: int) -> float | None:
    """Inclusive horizontal center of visible alpha within the Y band [y0, y1)."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    band = image.getchannel("A").crop((0, y0, image.width, y1))
    bb = band.getbbox()
    if bb is None:
        return None
    return (bb[0] + bb[2] - 1) / 2


def base_metrics(base_path: Path) -> dict | None:
    """Width and crown Y of the base body, for proportion reporting."""
    try:
        with Image.open(base_path) as im:
            im = im.convert("RGBA")
            bbox = inclusive_alpha_bounds(im)
    except (OSError, ValueError):
        return None
    if bbox is None:
        return None
    left, top, right, _ = bbox
    return {"width": right - left + 1, "crown_y": top}


# Sampled from the registered base master's cheek. The mannequin's own garment
# sits ~27 units from this, which is why it vanishes at thumbnail size; a real
# outfit has to clear it by a wide margin.
SKIN_REFERENCE = (253, 199, 163)


def skin_contrast(image: Image.Image) -> float | None:
    """Mean RGB distance of the layer's opaque pixels from base skin tone."""
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    total = 0
    count = 0
    for r, g, b, a in image.getdata():
        if a > 200:
            total += (
                (r - SKIN_REFERENCE[0]) ** 2
                + (g - SKIN_REFERENCE[1]) ** 2
                + (b - SKIN_REFERENCE[2]) ** 2
            ) ** 0.5
            count += 1
    return total / count if count else None


def analyze(path: Path, rig: dict, canvas: dict, tolerance: int, pose_variant: bool = False,
            trait: bool = False, floor_aura: bool = False, base: dict | None = None,
            max_width_ratio: float | None = None, min_skin_contrast: float | None = None) -> dict:
    result: dict = {"file": str(path), "sha256": sha256(path), "checks": [], "passed": False}
    head_cx = leg_cx = None
    alpha_min = None
    with Image.open(path) as im:
        im.load()
        w, h = im.size
        result["dimensions"] = [w, h]
        cw, ch = canvas["width"], canvas["height"]
        canvas_ok = (w == cw and h == ch)
        result["checks"].append(("canvas", canvas_ok, f"{w}x{h}", f"{cw}x{ch}", 0))
        has_alpha = ("A" in im.getbands())
        bounds = inclusive_alpha_bounds(im) if has_alpha else None
        if has_alpha:
            alpha_min = (im.convert("RGBA").getchannel("A").getextrema())[0]
        if has_alpha and bounds is not None and not trait:
            # Arm-free bands: head+neck (above the shoulders) and lower legs/feet.
            head_cx = band_center_x(im, rig["top_of_head_y"], rig["shoulder_line_y"] - 60)
            leg_cx = band_center_x(im, rig["waist_center"][1] + 130, rig["foot_baseline_y"] + 1)

    if not has_alpha:
        result["checks"].append(("alpha", False, "no alpha channel", "RGBA w/ transparency", 0))
        return result
    if bounds is None:
        result["checks"].append(("alpha", False, "fully transparent", "visible silhouette", 0))
        return result

    left, top, right, bottom = bounds
    result["inclusive_bounds"] = [left, top, right, bottom]
    center_x = (left + right) / 2
    mb = rig["maximum_character_bounds"]  # inclusive [x_min, y_min, x_max, y_max]

    def ok(delta): return abs(delta) <= tolerance

    if trait or floor_aura:
        # Partial layers (hair, eyes, crown, single wing) occupy only their own
        # region, so full-figure top-of-head / foot-baseline / center checks do
        # not apply. Verify a genuinely transparent background and staying in
        # bounds; confirm placement with a composite over the base body.
        result["checks"].append(("transparent_bg", alpha_min == 0, f"alpha_min={alpha_min}", "0", 0))
        result["trait_center_x"] = round(center_x, 1)
    else:
        head_delta = top - rig["top_of_head_y"]       # + => too low, - => too high
        foot_delta = bottom - rig["foot_baseline_y"]  # + => below baseline, - => above
        result["checks"].append(("top_of_head_y", ok(head_delta), top, rig["top_of_head_y"], head_delta))
        result["checks"].append(("foot_baseline_y", ok(foot_delta), bottom, rig["foot_baseline_y"], foot_delta))

        # Center check. Symmetric masters use the full-silhouette center; asymmetric
        # poses (a raised arm) skew it, so --pose-variant judges the arm-free body
        # center (head + leg bands) instead.
        if pose_variant and head_cx is not None and leg_cx is not None:
            body_center = (head_cx + leg_cx) / 2
            center_delta = body_center - rig["canvas_center_x"]
            result["body_center_x"] = {"head": round(head_cx, 1), "legs": round(leg_cx, 1), "mean": round(body_center, 1)}
            result["checks"].append(("body_center_x", ok(center_delta), round(body_center, 1), rig["canvas_center_x"], round(center_delta, 1)))
            result["silhouette_center_x"] = round(center_x, 1)
        else:
            center_delta = center_x - rig["canvas_center_x"]
            result["checks"].append(("center_x", ok(center_delta), round(center_x, 1), rig["canvas_center_x"], round(center_delta, 1)))

    # A ground-plane aura is not the character: to read as a ring the character
    # stands inside, its near arc must fall below the foot baseline. Keep the X
    # bounds and the top, but let the bottom run past the baseline. It still may
    # not touch the final canvas row, since that means the glow is clipped.
    bottom_limit = (canvas["height"] - 2) if floor_aura else mb[3]
    within = (left >= mb[0] and top >= mb[1] and right <= mb[2] and bottom <= bottom_limit)
    overflow = [
        f"L{mb[0]-left}" if left < mb[0] else "",
        f"T{mb[1]-top}" if top < mb[1] else "",
        f"R{right-mb[2]}" if right > mb[2] else "",
        f"B{bottom-bottom_limit}" if bottom > bottom_limit else "",
    ]
    result["checks"].append(("max_bounds", within, f"[{left},{top},{right},{bottom}]",
                             f"[{mb[0]},{mb[1]},{mb[2]},{bottom_limit}]",
                             " ".join(x for x in overflow if x) or "0"))

    # Proportion against the base body. hair_back_003 passed every silhouette
    # gate at 1.46x the body width because canvas, transparency and bounds do not
    # measure proportion; in composite it read as wings rather than hair.
    if base is not None and (trait or floor_aura):
        layer_width = right - left + 1
        ratio = layer_width / base["width"]
        result["width_ratio"] = round(ratio, 2)
        result["crown_offset"] = base["crown_y"] - top  # + => layer sits above the crown
        ratio_ok = max_width_ratio is None or ratio <= max_width_ratio
        result["checks"].append((
            "width_ratio", ratio_ok, f"{ratio:.2f}x",
            f"<={max_width_ratio:.2f}x" if max_width_ratio else "report-only",
            round(ratio - max_width_ratio, 2) if max_width_ratio else 0,
        ))

    # Garment/skin separation. The base mannequin wears a skin-toned tank top and
    # shorts, so an outfit that does not clear the skin tone leaves the character
    # reading as unclothed at thumbnail size.
    if min_skin_contrast is not None and (trait or floor_aura):
        contrast = skin_contrast(im)
        if contrast is not None:
            result["skin_contrast"] = round(contrast, 1)
            result["checks"].append((
                "skin_contrast", contrast >= min_skin_contrast, round(contrast, 1),
                f">={min_skin_contrast:.0f}", round(contrast - min_skin_contrast, 1),
            ))

    # Corrective guidance for the next NATIVE render (not applied here).
    height = bottom - top + 1
    target_height = rig["foot_baseline_y"] - rig["top_of_head_y"] + 1
    result["guidance"] = {
        "silhouette_height": height,
        "target_height": target_height,
        "scale_to_target": round(target_height / height, 4),
        "shift_center_x_by": round(rig["canvas_center_x"] - center_x, 1),
        "shift_head_top_by": rig["top_of_head_y"] - top,
    }

    # Single scalar for ranking a batch of candidates by closeness to the rig.
    overflow_px = (max(0, mb[0] - left) + max(0, mb[1] - top)
                   + max(0, right - mb[2]) + max(0, bottom - bottom_limit))
    if trait or floor_aura:
        result["deviation"] = round(abs(center_x - rig["canvas_center_x"]) + overflow_px, 1)
    else:
        result["deviation"] = round(abs(head_delta) + abs(foot_delta) + abs(center_delta) + overflow_px, 1)

    result["passed"] = canvas_ok and all(c[1] for c in result["checks"])
    return result


def print_report(r: dict) -> None:
    print("=" * 78)
    print(Path(r["file"]).name)
    print(f"  sha256: {r['sha256']}")
    if "inclusive_bounds" in r:
        print(f"  inclusive visible bounds: {r['inclusive_bounds']}")
    if "skin_contrast" in r:
        print(f"  skin contrast: {r['skin_contrast']} RGB units from base skin tone")
    if "width_ratio" in r:
        print(f"  width vs base body: {r['width_ratio']}x; "
              f"crown offset {r['crown_offset']:+d} px (+ = above the head top)")
    print(f"  {'CHECK':<16}{'RESULT':<8}{'ACTUAL':<16}{'TARGET':<16}DELTA")
    for name, passed, actual, target, delta in r["checks"]:
        print(f"  {name:<16}{('PASS' if passed else 'FAIL'):<8}{str(actual):<16}{str(target):<16}{delta}")
    if "guidance" in r and not r["passed"]:
        g = r["guidance"]
        print(f"  guidance: scale x{g['scale_to_target']} (h {g['silhouette_height']}->{g['target_height']}), "
              f"shift head_top {g['shift_head_top_by']:+d} px, center_x {g['shift_center_x_by']:+} px")
    print(f"  >>> {'PASS — silhouette gates met' if r['passed'] else 'FAIL — do not register'}")


def gather(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.glob("*.png")))
        elif path.is_file():
            files.append(path)
        else:
            print(f"warning: not found: {p}", file=sys.stderr)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Rig-gate diagnostic for Demigods pose/master candidates.")
    ap.add_argument("paths", nargs="+", help="PNG file(s) or directory(ies)")
    ap.add_argument("--config", type=Path, default=ROOT / "config" / "collection.json")
    ap.add_argument("--tolerance", type=int, default=1, help="Allowed +/- pixel delta on each anchor (default 1).")
    ap.add_argument("--pose-variant", action="store_true",
                    help="Judge center by the arm-free body (head + leg bands) instead of the full "
                         "silhouette. Use for asymmetric poses (raised arm).")
    ap.add_argument("--trait", action="store_true",
                    help="Partial-layer mode (hair, eyes, crown, wings): checks canvas, genuine "
                         "transparency, and max bounds only; skips the full-figure head/foot/center "
                         "gates. Confirm placement with a composite over the base body.")
    ap.add_argument("--floor-aura", action="store_true",
                    help="Ground-plane aura mode: like --trait, but the visible bounds may extend "
                         "below foot baseline Y so the character reads as standing inside the "
                         "effect. X bounds and the top bound still apply.")
    ap.add_argument("--base", type=Path, default=ROOT / "assets" / "base_bodies" / "base_body_001_neutral_master.png",
                    help="base body used to report a partial layer's width ratio and crown offset")
    ap.add_argument("--max-width-ratio", type=float,
                    help="fail a partial layer wider than this multiple of the base body width "
                         "(hair sits near 1.2; wings and capes legitimately exceed it)")
    ap.add_argument("--min-skin-contrast", type=float,
                    help="fail a layer whose opaque pixels average closer than this RGB "
                         "distance to base skin tone (253,199,163). Use for outfits: the "
                         "mannequin's own garment measures about 27 and disappears at "
                         "thumbnail size. 70 is a sensible floor.")
    ap.add_argument("--json-report", type=Path)
    args = ap.parse_args()

    spec = load_rig(args.config)
    base_spec = base_metrics(args.base) if args.base else None
    files = gather(args.paths)
    if not files:
        print("No PNG candidates found.", file=sys.stderr)
        return 2

    reports = [analyze(f, spec["rig"], spec["canvas"], args.tolerance, args.pose_variant, args.trait, args.floor_aura,
                              base_spec, args.max_width_ratio, args.min_skin_contrast)
               for f in files]
    for r in reports:
        print_report(r)

    passed = sum(1 for r in reports if r["passed"])
    print("=" * 78)
    if len(reports) > 1:
        ranked = sorted(reports, key=lambda r: r.get("deviation", float("inf")))
        print("CLOSEST FIRST (total silhouette deviation in px; lower is better):")
        for r in ranked:
            dev = r.get("deviation")
            tag = "PASS" if r["passed"] else "FAIL"
            print(f"  {tag}  dev={('n/a' if dev is None else dev):<7} {Path(r['file']).name}")
        print("-" * 78)
    print(f"{passed}/{len(reports)} candidate(s) meet the silhouette rig gate "
          f"(tolerance +/-{args.tolerance}px). Face, hand, waist, clothing, anatomy, "
          f"lighting and identity remain manual overlay gates.")
    if args.json_report:
        args.json_report.write_text(json.dumps(reports, indent=2))
        print(f"JSON report written to {args.json_report}")
    return 0 if passed == len(reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
