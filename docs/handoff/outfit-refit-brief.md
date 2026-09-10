# Handoff: refit the eight remaining outfits to the base body

You are picking up the Demigods collection (`DOGECOIN87/Demigods`, 777 pieces:
770 generative + 7 legendary, locked 1254×1254 canvas). Work on branch
`claude/collection-assets-alignment-fdxdzw`, which is at `1534d8d`.

## The one rule that matters

**Passing tests are not evidence.** Every real defect in this collection was
found by rendering an asset over its bound base body and enlarging it; the
tests were written afterwards, to stop each one recurring. Before you claim
anything is fixed, composite it and look at it at 2× or more. Before you ship a
change, look at what it did to the parts you did not intend to touch. Six
separate repairs were reverted in this project because they measured clean and
looked wrong.

## What is already done

| Commit | What |
|---|---|
| `fb1a4a7` | Neck accessories withdrawn; six outfits given an inner garment at the neckline; `outfit_010`'s collar opened |
| `734eccd` | Head accessories 10 → 6; sleeves widened on `outfit_009` and `outfit_010` |
| `1534d8d` | `outfit_002` and `outfit_003` fitted to the body; rear auras 18 → 8; back accessories 8 → 7 |

Read these before starting. Each records the approaches that failed and why:

- `docs/qa/sleeve_widening_2026-09-10.md` — six failed sleeve repairs
- `docs/qa/outfit_body_fit_2026-09-10.md` — the torso fit and the eight it refuses to touch
- `docs/qa/outfit_necklines_2026-09-10.md` — three failed neckline repairs
- `docs/qa/effect_trait_count_2026-09-10.md`, `docs/qa/head_accessory_count_2026-09-10.md`

## The remaining defect

The base bodies wear a cream tank and shorts so they read as dressed on their
own. Eight of the ten outfits are drawn narrower than that body, so the
undergarment shows beside the garment: a strip at the waist and hip, and a
crescent of bare shoulder where a sleeved garment does not reach the deltoid.

The numbers below locate the defect. They do not define done — see
**Definition of done** at the end. Measure it yourself rather than trusting
them:

```
PYTHONPATH=scripts python3 -c "
import json, sys; sys.path.insert(0,'scripts')
import numpy as np; from PIL import Image; from pathlib import Path
import fit_outfit_torso as F
req = {r['trait']: r['requires'] for r in json.load(open('config/compatibility.json'))['requires']}
for n in sorted(p.name for p in Path('assets/outfits').glob('*.png')):
    g = np.asarray(Image.open(f'assets/outfits/{n}').convert('RGBA'))
    b = np.asarray(Image.open(f'assets/base_bodies/{req[n]}').convert('RGBA'))
    ends, holes = F.shortfalls(g, b, F.DEFAULT_MAX_PX)
    print(n, sum(x[-1] for x in ends) + sum(bb-a+1 for _,a,bb in holes))
"
```

As of `1534d8d`, torso and leg shortfall, with the worst bands:

| Outfit | Total | Worst bands |
|---|---|---|
| `outfit_010_celestial_robe_white_gold` | 5023 px | y619–805: 23 px |
| `outfit_009_navy_high_collar_coat` | 4789 px | y646–833: 21 px |
| `outfit_005_sun_temple_pose_005` | 4514 px | y824–886: 19 px; y704–791: 16 px |
| `outfit_007_brown_leather_long_coat` | 2567 px | y641–798: 18 px |
| `outfit_001_celestial_scholar_pose_001` | 2205 px | y818–880: 15 px |
| `outfit_004_lunar_oracle_pose_004` | 2032 px | y556–572: 36 px; y614–759: 19 px |
| `outfit_003_verdant_alchemist_pose_003` | 1190 px | y852–882: 19 px |
| `outfit_006_black_layered_hooded_robe` | 848 px | y685–793: 6 px |
| `outfit_002_storm_guardian_pose_002` | 449 px | y609–634: 12 px |
| `outfit_008_olive_ragged_cloak` | 40 px | negligible |

Separately, bare shoulder cap (rows 496–545) on garments that *do* have a
sleeve below the shoulder, so the gap is not a design choice:

| Outfit | Bare px at the shoulder |
|---|---|
| `outfit_005_sun_temple` | 3747 |
| `outfit_009_navy_high_collar_coat` | 3152 |
| `outfit_010_celestial_robe_white_gold` | 2878 |
| `outfit_007_brown_leather_long_coat` | 1813 |
| `outfit_008_olive_ragged_cloak` | 894 |
| `outfit_003_verdant_alchemist` | 882 |
| `outfit_006_black_layered_hooded_robe` | 397 |

`outfit_006` is the clearest read: peach crescents on a black hooded robe.
`outfit_001`, `002`, `004` are sleeveless, so their bare shoulders are design.

## What will not work

Do not spend the session rediscovering these. Each was built, run, rendered
and reverted.

1. **Warping the garment edge outward on a structured coat.** This is what
   `scripts/fit_outfit_torso.py` does, and it is why only `outfit_002` and
   `outfit_003` are in its `FITTED` map. Moving an edge stretches the fabric
   behind it. On `outfit_009` it tore the coat front and broke the belt trim;
   on `outfit_010` it moved and narrowed the sash; on `outfit_005` it destroyed
   the hem trim; on `outfit_006` it slimmed the skirt and left pale seams.
2. **Flat-filling the strip.** The garment's own contour line ends up inside
   the filled area, as a dark line in the middle of the fabric.
3. **Repeating or averaging the edge pixel.** Horizontal banding, then a grey
   smear, because the pixel it repeats is the contour, not the fabric.
4. **A plainness heuristic as the only guard.** `PLAIN_LIMIT` in
   `fit_outfit_torso.py` catches most structured edges but not reliably enough
   to stand between a coat and a torn lapel. Keep it; do not trust it alone.
5. **Widening the shoulder cap.** Every outfit, including two with no seam
   anywhere else, sits 30–40 px inside the silhouette across rows 510–535. The
   base body's shoulder is wider than any garment drawn for it. Pushing fabric
   out to meet it flattens the shoulder line.

## What to do instead

The garments need to be **redrawn at the body's width**, not warped. Two routes,
in order of preference:

**Route A — regenerate the eight outfits against a measured body width.**
The generation prompts are under `prompts/`. Derive the base body's per-row
half-width from `assets/base_bodies/*.png` and state it in the prompt as an
explicit constraint, then re-run intake through the existing pipeline
(`scripts/bulk_intake.py`, the rig gates, `scripts/validate_manifest_consistency.py`).
Treat each regenerated outfit as a candidate: render it over its bound base,
compare against the current asset, and only register it if it is better on
every axis, not just the strip.

**Route B — narrow the base bodies' undergarment instead.**
The tank and shorts exist only so a base reads as decent on its own; every
token has an outfit over them. Repainting them in the body's own skin tone
would stop the strip reading as underwear on all eight at once, without
touching a single garment. This changes the master rig, so it needs the owner's
sign-off first — put it to them before building it. It does not fix the
shoulder crescent on `outfit_006`, which still needs the robe redrawn.

Do not mix the routes. If Route A lands, Route B is unnecessary.

## Rig facts you must not break

- Canvas 1254×1254. Centre X 627. Top of head Y 141. Foot baseline Y 1139.
  Max bounds `[233, 129, 1021, 1139]`.
- Four-base consensus anatomy: eye line 370.3, chin 476.5, shoulder junction
  496.3.
- Layer stack, bottom to top: background, rear_aura, back_accessory, hair_back,
  base_body, outfit, neck_accessory, eyes, eyebrows, mouth, expression_marks,
  hair_front, head_accessory, hand_object, front_aura, global_finish. Render
  order differs: hand_objects composite before base_bodies.
- Outfits 001–005 are bound to a specific pose in `config/compatibility.json`.
  006–010 require `base_body_001`. Do not break a binding.
- Semi-transparent fabric is still fabric. Use an alpha threshold near 16, not
  128, when deciding what is covered. Reading a translucent drape as bare body
  is what warped the sun temple tunic into hard-edged blocks.

## Bookkeeping that must stay consistent

- `assets/asset_manifest.json` holds a SHA-256 per asset plus a provenance
  chain. Any script that edits an asset in place must refresh the hash and
  append its method to `provenance.postprocessing`.
- Backlog status vocabulary is fixed: `pending, candidate, QA-failed, approved,
  registered`. Nothing else validates.
- Match backlog rows by **asset path**, not by `DG-` id. Four rear auras carry
  no `backlog_id` in the manifest and were silently missed by an id-based
  update, leaving the ledger claiming they were still registered.
- After any registration change: `python3 scripts/validate_manifest_consistency.py`
  then `python3 scripts/report_production_status.py --write`.
- Retire, do not delete. Move withdrawn art to `incoming/<reason>_<date>/`,
  move its manifest entry to `blocked_assets` with the reason, the requirement
  for a replacement, and the SHA-256 it was retired at. Note that
  `incoming/.gitignore` excludes `*.png`, so the hash in the manifest is the
  only record that travels.
- If you retire an asset that another script names, update that script. The
  green-by-design exemption in `scripts/despeckle_chroma_residue.py` pointed at
  a retired aura and broke the chroma gate.

## Verification protocol

1. Composite the asset over its bound base on a white ground and on a dark one.
2. Crop the region you changed at 4× or more, and put before beside after.
3. Look at the whole figure at 1× as well — a fix that reads fine at 8× can
   change the silhouette.
4. Run `python3 -m unittest discover -s tests -q`. All 215 must pass.
5. Regenerate a sample sheet and look at it:
   `python3 scripts/generate_777.py --output <tmp> --supply 24 --seed <n>
   --allow-nonstandard-supply --overwrite`. It takes about three minutes.
6. Write the QA note *before* you commit, including the approaches that failed.

## Definition of done

No pixel budget. A budget is what let every earlier defect through: the gates
measured clean while the art was visibly wrong, and a number to hit is a number
to optimise instead of looking. The bar is the render.

**Done means: on every one of the ten outfits, composited over its bound base
body, no part of the base body's cream tank or shorts is visible anywhere, and
no bare skin is visible except where the garment is cut to show it.**

Where the garment is cut to show skin, per outfit, so you are not guessing:

| Outfit | Skin that is meant to show |
|---|---|
| `outfit_001_celestial_scholar` | both arms and one shoulder; it is sleeveless under a half-cape |
| `outfit_002_storm_guardian` | both arms and the left shoulder; sleeveless armour with one pauldron |
| `outfit_004_lunar_oracle` | both arms and both shoulders; a sleeveless wrap |
| `outfit_005_sun_temple` | both forearms below a short sleeve |
| `outfit_003`, `006`, `007`, `008`, `009`, `010` | hands and neck only |

Everything else showing is a defect, including the shoulder crescent on
`outfit_006`, `007`, `009` and `010`, which are sleeved garments that do not
reach the deltoid.

Also required:

- No garment silhouette, trim line, lapel, sash, belt end or hem changed shape.
  Put before beside after for each outfit and check the parts you did not
  intend to touch.
- `tests/test_outfit_body_fit.py` extended to every outfit rather than the two
  in `FITTED`. Set its threshold *after* the art is accepted, at whatever the
  accepted art measures plus a small margin, and say in the test docstring that
  the number describes the art rather than defining it. It exists to catch a
  regression later, not to decide whether you are finished now.
- QA note at `docs/qa/outfit_refit_<date>.md` with before/after crops and the
  approaches that failed.
- Ledger and manifest regenerated and consistent.

If some part cannot be fixed without redrawing more than you were asked to
change, say so plainly, name the outfit and the region, and leave it. Do not
ship a garment whose lapel moved in order to close a strip.

## Conventions

Develop on `claude/collection-assets-alignment-fdxdzw`. Do not push to another
branch without being asked. Do not open a pull request unless asked. End every
commit message with the attribution lines the session supplies, and keep model
identifiers out of anything committed.
