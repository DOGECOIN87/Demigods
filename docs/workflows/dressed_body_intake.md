# Dressed-Body Outfit Intake

A *dressed body* is an outfit painted with the body intact: the base pose and its garment as one bald, faceless figure. It exists because the other route - an isolated garment layer over the bare base - never met the body it was drawn for, and every repair that warped, filled or stretched a garment edge was reverted (`docs/handoff/outfit-refit-brief.md`). A dressed body has no seam to fit.

It is registered in the `outfits` category and bound to one base pose, like the pose-locked outfits before it, with one difference: the base is **selected but not drawn**. The base still binds the pose, the hand objects bind to the same base, and the metadata names the pose through it; a `hides` rule in `config/compatibility.json` keeps it out of the render so a bare copy of the figure cannot show wherever the two silhouettes differ by a pixel. Face, hair and head traits layer onto the dressed figure exactly as they do onto a base.

## Source requirements

- One 1254 × 1254 PNG per outfit and pose, front-facing, bald and faceless (skin and ears only - the shared face layers add eyes, brows and mouth, and cover only the features they draw).
- Transparent background preferred. A flat pure-black background is accepted for light and mid-tone outfits; a dark garment must be transparent, because keying separates figure from black by brightness.
- The figure on the base's proportions: crown near Y 140, head centred on X 627 at the base's size, soles near Y 1140, fist and palm where the base has them. Prompts: `prompts/dressed_body_pose_pack_2026-09-25.md`.

## Steps

1. **Freeze the source.** Put the untouched render in `images/trait_candidates/outfits_dressed/` and add an entry to `sources.json` there: `source`, `sha256`, `mode`, `dimensions`, `outfit`, `outfit_slug`, `outfit_label`, `pose`, `target` (`outfit_<NNN>_<slug>_pose_<PPP>.png`). The source is evidence and is never edited.
2. **Normalize and review.**

   ```bash
   python scripts/intake_dressed_bodies.py images/trait_candidates/outfits_dressed/sources.json
   ```

   Each render goes through `scripts/normalize_dressed_body.py` into `incoming/dressed_bodies_<date>/` with a provenance sidecar, then through the automated gates: binary asset QA, crown and soles exactly on Y 141 and Y 1139, and the face check - where the union of every shared eye, brow, mouth and expression-mark pixel would land off the head or on its outline. Two sheets go to `docs/qa/dressed_bodies_<date>/`: every figure with its base's silhouette in red, and every face wearing the worst-case traits.
3. **Look.** Passing the gates is not approval. Check each figure against the red silhouette (head, hands, feet), each face on the face sheet, and composite the hand objects over every Pose 002 and Pose 004 figure. A fist or palm that is not where the base's is gets an `excludes` for the hand objects rather than a warp.
4. **Record the decision** in the render's `sources.json` entry: `"review": {"decision": "approved", "reviewed_on": ..., "note": ...}`, plus `"excludes"` and `"excludes_reason"` when needed.
5. **Register.**

   ```bash
   python scripts/intake_dressed_bodies.py images/trait_candidates/outfits_dressed/sources.json \
       --register --qa-note docs/qa/<batch note>.md
   ```

   This copies the exact normalized bytes into `assets/outfits/`, writes the `requires`, `hides` and any `excludes` rules, appends the manifest entry with the full provenance, adds or flips the backlog row, and regenerates the ledger. A render that fails a gate is never registered, whatever its review says.
6. **Retire what it replaces.** When a dressed render arrives for a family and pose that still has an original garment layer (outfits 001-005 and 010), retire that layer the way `scripts/withdraw_superseded_traits.py` retired outfits 006-009: move it to `incoming/<reason>_<date>/`, record it in `blocked_assets` with its SHA-256, remove its `requires` rule, and mark its backlog row `withdrawn`. Two versions of one outfit in one pose would be a duplicate trait.
7. **Validate and commit**, as for any registration: `validate_config.py`, `validate_assets.py`, `validate_manifest_consistency.py`, `report_production_status.py --check`, `generate_777.py --preflight-only`, and the unit tests.

## What the fit does

`scripts/normalize_dressed_body.py` recovers alpha, isolates the figure and fits it to the rig without enlarging anything:

- **Alpha.** An RGBA source keeps its own matte, re-levelled so its interior (which generators leave near 252) is opaque and its low-alpha halo is cleared. An RGB source is keyed off black: near-black at least three pixels across is background - the gaps under the arms and between fingers are - and anything thinner is contour paint, which one pass had keyed into pinholes through the navy boots. The outer two pixels take partial alpha from their brightness against the art just inside them, and colour is un-premultiplied from black.
- **Fit.** The head is scaled so the chin lands on Y 461 and the body below it so the soles land on Y 1139, blended over 50 rows of neck. A render already on the rig's proportions gets one uniform reduction. A render drawn with long legs keeps its head at the rig's size: one uniform reduction of the black-robe renders shrank their heads by up to 7% and put the mouth on the chin.
