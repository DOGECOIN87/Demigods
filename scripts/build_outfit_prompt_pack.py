#!/usr/bin/env python3
"""Write the 2026-10-11 outfit prompt pack: 12 outfit families x 5 poses.

Every prompt attaches ONE image, the base pose being dressed, and describes the
outfit in words. The prompts encode what the intake and the generator need
(docs/workflows/dressed_body_intake.md, docs/pose_anatomy_2026-10-11.md):

- the figure stays on the rig: crown Y 140, chin Y 461, soles Y 1140;
- the head comes back bald and faceless (face, hair and headwear are layers);
- hands stay bare skin, because held items are painted over the hand in skin;
- in Pose 004 the held-item layers repaint the viewer-left forearm from the
  elbow down, so that sleeve ends at the elbow;
- dark outfits need a transparent background (black keying fails on them).

    python scripts/build_outfit_prompt_pack.py          # write the pack
    python scripts/build_outfit_prompt_pack.py --check  # fail if it is stale
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACK = ROOT / "prompts" / "outfit_prompt_pack_2026-10-11.md"

POSES = {
    "001": {
        "label": "neutral, both hands open",
        "file": "base_body_001_neutral_master.png",
        "arms": (
            "Both arms hang down and slightly away from the body. Both hands are open with the "
            "palms facing the viewer, beside the thighs (around X 404 and X 850, Y 772)."
        ),
        "fit": [
            "Both sleeves run the full length of each arm, follow its angle and end in a cuff at "
            "the wrist. Each whole hand stays bare and visible.",
            "Keep the open background gap between each arm and the body. Do not fill it with "
            "fabric.",
        ],
    },
    "002": {
        "label": "viewer-left vertical grip",
        "file": "base_pose_002_viewer_left_vertical_grip.png",
        "arms": (
            "The hand on the LEFT SIDE OF THE IMAGE is a closed fist with a vertical grip, held "
            "low at the side (around X 415-470, Y 735-800). The hand on the RIGHT SIDE OF THE "
            "IMAGE is open, palm facing the viewer."
        ),
        "fit": [
            "Staffs, swords and lanterns are added later as layers that repaint this fist and "
            "its wrist in bare skin. So the sleeve on the image-left arm ends in a slim, close "
            "cuff ABOVE the wrist (no lower than about Y 720). No ruffle, flare or trim may reach "
            "the fist or pass through it.",
            "The image-right sleeve runs to the wrist as usual. Its hand stays bare.",
            "Keep the fist exactly where it is in the attached image. A fist moved even 20 px "
            "leaves every held item floating beside the hand.",
            "Keep the open background gap between each arm and the body.",
        ],
    },
    "003": {
        "label": "viewer-right vertical grip",
        "file": "base_pose_003_viewer_right_vertical_grip.png",
        "arms": (
            "The hand on the RIGHT SIDE OF THE IMAGE is a closed fist with a vertical grip, held "
            "low at the side (around X 790-850, Y 735-800). The hand on the LEFT SIDE OF THE "
            "IMAGE is open, palm facing the viewer."
        ),
        "fit": [
            "The sleeve on the image-right arm ends in a slim, close cuff ABOVE the wrist (no "
            "lower than about Y 720). No ruffle, flare or trim may reach the fist or pass "
            "through it.",
            "The image-left sleeve runs to the wrist as usual. Its hand stays bare.",
            "Keep the fist exactly where it is. Do not mirror the outfit. Its viewer-left and "
            "viewer-right details stay on the same sides as in every other pose.",
            "Keep the open background gap between each arm and the body.",
        ],
    },
    "004": {
        "label": "viewer-left palm up",
        "file": "base_pose_004_viewer_left_palm_up.png",
        "arms": (
            "On the LEFT SIDE OF THE IMAGE, the forearm is bent forward at the elbow and the hand "
            "is held open with the PALM FACING UP at hip height (around X 400-500, Y 720-780), "
            "as if presenting something. The hand on the RIGHT SIDE OF THE IMAGE hangs open, "
            "palm facing the viewer."
        ),
        "fit": [
            "Orbs, books and flames are added later as layers that repaint this whole forearm, "
            "from the elbow to the fingertips, in bare skin. So on the image-left arm the "
            "sleeve is PUSHED UP and gathered just ABOVE THE ELBOW (ending no lower than about "
            "Y 665). The forearm, wrist and hand are bare skin with no bracer, cuff or bangle.",
            "The image-right sleeve runs to the wrist as usual. Its hand stays bare.",
            "The upturned palm stays empty, flat and fully visible.",
            "Keep the open background gap between each arm and the body.",
        ],
    },
    "005": {
        "label": "centred two-hand grip",
        "file": "base_pose_005_centered_two_hand_grip.png",
        "arms": (
            "Both arms come forward and inward. Both fists are stacked one above the other on "
            "the centre line at crotch height (around X 627, Y 830-900), as if resting on a "
            "planted sword hilt."
        ),
        "fit": [
            "Both sleeves follow the arms inward and end in cuffs at the wrists, just above the "
            "stacked fists. The fists stay bare and fully visible. Nothing passes in front of "
            "them.",
            "The forearms lie IN FRONT of the garment. The coat front, belt buckle and sash "
            "behind the hands are hidden, so keep the outfit's main ornament on the chest, "
            "collar and hem.",
            "The hem and anything hanging at the waist stay behind the fists.",
        ],
    },
}

# dark=True: black keying cannot separate this palette, so transparency is required.
OUTFITS = [
    {
        "number": "011", "slug": "celestial_regent", "name": "Celestial Regent", "dark": True,
        "spec": [
            "Under-layer: white high-collar shirt with a soft lace jabot at the throat. The "
            "collar stops below the chin.",
            "Main garment: navy-blue velvet long coat, fitted at the chest and flaring from the "
            "waist to mid-shin. It is open below the belt to show the white shirt and navy "
            "trousers. Long sleeves with deep folded cuffs embroidered in gold.",
            "Trim: gold star-and-constellation embroidery along the lapels, front edges, cuffs "
            "and hem. Small gold star buttons down the chest.",
            "Over-layer: short navy capelet over both shoulders, reaching mid-upper-arm and lined "
            "in pale gold satin. It closes at the collarbone with a gold eight-pointed star clasp "
            "set with a sapphire.",
            "Belt: wide dark-brown leather belt with an ornate gold buckle.",
            "Legs and feet: navy trousers tucked into black knee boots with gold toe caps and "
            "gold star studs on the boot cuffs.",
            "Signature: a gold crescent moon embroidered on the viewer-left breast.",
        ],
    },
    {
        "number": "012", "slug": "frost_marshal", "name": "Frost Marshal", "dark": False,
        "spec": [
            "Under-layer: pale-blue double-breasted waistcoat with silver buttons.",
            "Main garment: white military greatcoat to the shins, with ice-blue satin lining "
            "showing at the open front and hem. Long sleeves with ice-blue cuffs edged in silver "
            "braid.",
            "Over-layer: white fur collar draped across both shoulders, and silver fringed "
            "epaulettes on both shoulders.",
            "Sash: royal-blue sash from the viewer-right shoulder to the viewer-left hip, pinned "
            "with a silver snowflake medal on the chest.",
            "Trim: silver snowflake embroidery along the hem and front edges.",
            "Belt: black leather belt with a silver buckle.",
            "Legs and feet: white breeches and glossy black knee boots with silver buckles.",
        ],
    },
    {
        "number": "013", "slug": "ember_smith", "name": "Ember Smith", "dark": True,
        "spec": [
            "Under-layer: crimson wool tunic with a round neck and long sleeves. The cuffs are "
            "bound with dark leather straps.",
            "Main garment: dark-brown leather blacksmith apron from the chest to the knees, with "
            "bronze rivets along every edge and an engraved bronze rune plate at the centre of "
            "the chest.",
            "Over-layer: one bronze pauldron engraved with flame patterns on the viewer-right "
            "shoulder, held by a leather strap across the chest.",
            "Belts: two crossed leather belts at the hips with small pouches and a hanging bronze "
            "ring. No tools.",
            "Legs and feet: crimson trousers tucked into heavy brown riveted boots with bronze "
            "toe caps.",
        ],
    },
    {
        "number": "014", "slug": "verdant_druid", "name": "Verdant Druid", "dark": True,
        "spec": [
            "Under-layer: dark moss-green long-sleeved tunic.",
            "Main garment: knee-length robe of overlapping oak leaves in moss, olive and "
            "gold-green. The leaf points form a jagged hem that flares outward.",
            "Over-layer: leafy mantle over both shoulders, set with small acorns and amber "
            "beads.",
            "Arms: bark-textured bracers over the sleeves, ending at the wrist.",
            "Belt: braided vine belt with a polished amber clasp.",
            "Legs and feet: olive trousers under wrapped leaf greaves, and boots of woven root "
            "and bark.",
            "Signature: a polished amber oak-leaf brooch at the centre of the chest.",
        ],
    },
    {
        "number": "015", "slug": "lantern_kimono", "name": "Lantern Kimono", "dark": True,
        "spec": [
            "Layers: a white inner collar, then a red middle layer, then an outer deep-indigo "
            "silk kimono reaching the ankles. The wearer's left panel crosses over the right, "
            "forming a 'y' at the chest.",
            "Pattern: scattered gold butterflies and small paper lanterns embroidered on the "
            "indigo silk.",
            "Sleeves: wide kimono sleeves whose openings end AT THE WRISTS. The sleeve drapes "
            "hang below the forearms no lower than the hip and never cover the hands.",
            "Obi: wide red obi with gold floral brocade, tied with a gold cord with two red "
            "tassels.",
            "Hem: a flash of red lining and a thin gold edge.",
            "Feet: white tabi socks and black lacquered geta sandals.",
        ],
    },
    {
        "number": "016", "slug": "void_oracle", "name": "Void Oracle", "dark": True,
        "spec": [
            "Under-layer: black fitted tunic with a high collar and small silver buttons.",
            "Main garment: long robe in black and deep violet, ending just above the boot toes "
            "in layered tattered strips.",
            "Sleeves: fitted, ending at the wrist in short tattered violet points that do not "
            "touch the hands.",
            "Trim: fine silver filigree along every edge. Violet rune symbols embroidered (not "
            "glowing) along the hem.",
            "Over-layer: short black shoulder cape with jagged edges, closed by a silver crescent "
            "clasp set with an amethyst.",
            "Belt: thin silver chain belt with a small amethyst pendant.",
            "Feet: black pointed boots with silver toe tips.",
        ],
    },
    {
        "number": "017", "slug": "dawn_paladin", "name": "Dawn Paladin", "dark": False,
        "spec": [
            "Armour: polished white-and-gold plate breastplate with a sun emblem in the centre, "
            "and layered rounded pauldrons on both shoulders.",
            "Arms: white-gold arm plates over chainmail sleeves, ending at the wrist. No "
            "gauntlets.",
            "Under-layer: chainmail visible at the armpits and below the breastplate.",
            "Tabard: white tabard hanging at the front from the waist to the knees, with gold "
            "trim and a small sun motif.",
            "Skirt: chainmail skirt to mid-thigh at the sides.",
            "Legs and feet: white-gold armoured greaves and sabatons.",
        ],
    },
    {
        "number": "018", "slug": "clockwork_artisan", "name": "Clockwork Artisan", "dark": True,
        "spec": [
            "Under-layer: cream linen shirt with a soft folded collar.",
            "Waistcoat: brown leather waistcoat with brass buttons. A small cluster of brass "
            "gears sits on the viewer-left chest, and a gold pocket-watch chain crosses the "
            "front.",
            "Main garment: copper-brown tailcoat, open at the front, with tails to the back of "
            "the knees and brass-gear embroidery on the cuffs and lapels.",
            "Belt: leather belt with small brass-capped pouches.",
            "Legs and feet: brown-and-cream pinstripe trousers and brown boots with brass "
            "buckles.",
        ],
    },
    {
        "number": "019", "slug": "tide_captain", "name": "Tide Captain", "dark": True,
        "spec": [
            "Under-layer: white ruffled shirt. The ruffle sits below the chin.",
            "Main garment: deep-teal naval frock coat to the knees, with gold braid on the cuffs "
            "and front edges and gold anchor buttons.",
            "Over-layer: gold fringed epaulettes on both shoulders.",
            "Sash: wide crimson silk sash at the waist, knotted on the viewer-right hip with the "
            "ends hanging to mid-thigh.",
            "Legs and feet: cream breeches and tall cuffed brown boots with gold buckles.",
            "No scabbard, sword or pistol.",
        ],
    },
    {
        "number": "020", "slug": "desert_wanderer", "name": "Desert Wanderer", "dark": False,
        "spec": [
            "Under-layer: sand-beige linen under-robe to the ankles.",
            "Main garment: terracotta sleeveless over-robe, open at the front and reaching the "
            "shins, with bronze geometric trim.",
            "Over-layer: cream shawl draped across both shoulders and pinned on the chest with a "
            "bronze sun-disc brooch. The shawl stays below the chin. No hood.",
            "Arms: long linen sleeves bound at the forearm with tan cloth wraps, ending at the "
            "wrist.",
            "Sash: wide terracotta sash with a row of small bronze coins.",
            "Legs and feet: loose sand trousers wrapped at the shin, and leather sandals with "
            "ankle straps.",
        ],
    },
    {
        "number": "021", "slug": "rose_diplomat", "name": "Rose Diplomat", "dark": True,
        "spec": [
            "Under-layer: cream silk waistcoat with gold buttons, and a white lace cravat at the "
            "throat pinned with a ruby.",
            "Main garment: burgundy brocade frock coat to the knees, patterned with embroidered "
            "roses. Wide gold-trimmed lapels and large turned-back cuffs.",
            "Signature: a gold rose brooch on the viewer-left lapel.",
            "Legs and feet: white breeches and polished brown knee boots with folded cuffs.",
        ],
    },
    {
        "number": "022", "slug": "shadow_locksmith", "name": "Shadow Locksmith", "dark": True,
        "spec": [
            "Under-layer: dark grey fitted shirt with a high collar.",
            "Main garment: charcoal-black fitted long coat to the knees, with bronze trim along "
            "the edges and several crossing buckled leather straps across the chest.",
            "Arms: long sleeves with buckled strap cuffs ending at the wrist.",
            "Belt: wide belt with a ring of silver keys hanging at the viewer-right hip.",
            "Legs and feet: dark trousers and black boots with bronze buckles.",
        ],
    },
]

STYLE = (
    "Premium chibi fantasy character art matching the Demigods 1-of-1 collection. Highly "
    "detailed and ornate: at least three visible garment layers, fine embroidery, gold or "
    "silver filigree trim, small gems and buckles, and soft realistic fabric folds with "
    "texture. Painterly semi-realistic rendering with clean outlines. Soft key light from the "
    "upper-left, form shadows toward the lower-right, and a subtle cool rim light on the "
    "right edge. Front-facing, orthographic, one figure."
)

AVOID = (
    "eyes, eyebrows, nose, mouth, hair, hats, hoods, crowns, necklaces or chokers, earrings, "
    "gloves, gauntlets, rings, held items, weapons, scabbards, staffs, wings, auras, glows, "
    "particles, a ground shadow, floors, scenery, text, labels, borders, a painted "
    "checkerboard, a second figure, a changed camera angle, a mirrored pose, moved hands, a "
    "stretched or shortened body, a bigger or smaller head, fabric filling the gaps between "
    "the arms and the body, and anything cropped at the canvas edge"
)


def background(outfit: dict) -> str:
    if outfit["dark"]:
        return (
            "TRANSPARENT background (PNG with alpha). REQUIRED for this dark outfit: a black "
            "background cannot be separated from it. No gradient, floor or shadow."
        )
    return (
        "TRANSPARENT background (PNG with alpha). If transparency is impossible, use a flat pure "
        "black #000000 background and nothing else: no gradient, vignette, floor or shadow."
    )


def target(outfit: dict, pose: str) -> str:
    return f"outfit_{outfit['number']}_{outfit['slug']}_pose_{pose}.png"


def prompt(outfit: dict, pose_id: str) -> str:
    pose = POSES[pose_id]
    lines = [
        f"TASK",
        f"Edit the attached image. It is the Demigods base figure in Pose {pose_id} "
        f"({pose['label']}), and it is the ONLY reference. Dress this exact figure in the "
        f"{outfit['name']} outfit described below. Everything that is not clothing stays "
        f"exactly as it is. Output one image.",
        "",
        "ATTACHED IMAGE",
        f"{pose['file']} (repository: assets/base_bodies/{pose['file']})",
        "",
        "LOCKED: DO NOT CHANGE",
        "- Canvas 1254 x 1254 with the same framing. The figure keeps exactly its position and "
        "size.",
        "- Head: same size, shape and place (crown at Y 140, centred on X 627, about 353 px "
        "across the ears, chin at Y 461). Keep the ears.",
        f"- Arms and hands: {pose['arms']} Keep every arm angle, hand position and finger "
        "shape exactly.",
        "- Legs and stance: unchanged. The soles stay on Y 1140. Footwear must not raise the "
        "figure, lengthen the legs or widen the stance.",
        "- Proportions: no longer legs or torso, and no bigger or smaller head.",
        "",
        "HEAD AND FACE",
        "Return the head bald and FACELESS: smooth skin and ears only. Paint over the eyes, "
        "eyebrows, nose and mouth in the attached image with plain skin. Eyes, brows, mouth, "
        "hair and headwear are separate layers added later.",
        "",
        "HANDS",
        "All hands stay bare skin: no gloves, gauntlets, rings, wraps or bracers on the hands. "
        "Held items are added later as layers painted with a bare hand.",
        "",
        f"HOW THE CLOTHING MEETS THE ARMS IN POSE {pose_id} (overrides the outfit text if they "
        "conflict)",
        *[f"- {line}" for line in pose["fit"]],
        "",
        f"OUTFIT: {outfit['name'].upper()}",
        *[f"- {line}" for line in outfit["spec"]],
        "- Coverage: the beige tank top and shorts are completely hidden at the neckline, "
        "armholes, sides, waist and thighs. The neck may show above the collar.",
        "- Silhouette: hems and capes may flare outward but stay inside X 233-1021 and above "
        "Y 1140. The boots stay visible.",
        "- 'Viewer-left' and 'viewer-right' mean the left and right sides of the image.",
        "",
        "STYLE",
        STYLE,
        "",
        "BACKGROUND",
        background(outfit),
        "",
        "AVOID",
        AVOID + ".",
        "",
        "OUTPUT",
        f"Exactly one 1254 x 1254 PNG named: {target(outfit, pose_id)}",
    ]
    return "\n".join(lines)


def build() -> str:
    out = [
        "# Demigods outfit prompt pack (2026-10-11)",
        "",
        "Generated by `python scripts/build_outfit_prompt_pack.py`. Do not edit by hand: change "
        "the script and rerun it. Background and pose notes are in "
        "`docs/pose_anatomy_2026-10-11.md`.",
        "",
        "## How to use",
        "",
        "1. **Attach one image only**: the base pose named in the prompt, from "
        "`assets/base_bodies/`. It is the sole reference.",
        "2. Paste the whole prompt. Generate **Pose 001 first** for a family and review it. "
        "Then run Poses 002-005 with the same outfit text so the design stays identical.",
        "3. Keep the original PNG unedited. Save it to `images/trait_candidates/outfits_dressed/` "
        "and add a `sources.json` entry whose `target` is the output name in the prompt.",
        "4. Run `python scripts/intake_dressed_bodies.py "
        "images/trait_candidates/outfits_dressed/sources.json` and review the sheets "
        "(`docs/workflows/dressed_body_intake.md`).",
        "",
        "Checklist before accepting a render:",
        "",
        "- the head is bald and faceless, and the same size and place as the base;",
        "- the hands are bare skin and unmoved, and the Pose 002/003 fist is clear of fabric;",
        "- in Pose 004 the image-left forearm is bare from the elbow down;",
        "- no tank top or shorts show anywhere;",
        "- the background is transparent (or flat black for the outfits that allow it).",
        "",
        "## Outfits",
        "",
        "| # | Outfit | Background |",
        "|---|---|---|",
        *[
            f"| {o['number']} | {o['name']} | {'transparent required' if o['dark'] else 'transparent, or flat black'} |"
            for o in OUTFITS
        ],
        "",
    ]
    for outfit in OUTFITS:
        out += [f"## {outfit['number']} {outfit['name']}", ""]
        for pose_id, pose in POSES.items():
            out += [
                f"### {outfit['name']} - Pose {pose_id} ({pose['label']})",
                "",
                f"Attach: `assets/base_bodies/{pose['file']}`",
                "",
                "```text",
                prompt(outfit, pose_id),
                "```",
                "",
            ]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if the pack is out of date")
    args = parser.parse_args(argv)
    text = build()
    if args.check:
        if not PACK.exists() or PACK.read_text(encoding="utf-8") != text:
            print(f"stale: run python scripts/build_outfit_prompt_pack.py", file=sys.stderr)
            return 1
        print("PASS outfit prompt pack")
        return 0
    PACK.write_text(text, encoding="utf-8")
    print(f"wrote {PACK.relative_to(ROOT)}: {len(OUTFITS)} outfits x {len(POSES)} poses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
