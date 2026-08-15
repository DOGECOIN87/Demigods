# Demigods Collection — Continuation Handover Prompt

You are continuing production oversight of the **Demigods** 777-token NFT collection in `DOGECOIN87/Demigods`. Work from the current `main` branch. Do not redesign the collection, weaken the locked modular-production contract, or perform minting, metadata publication, release, registration, or on-chain actions without explicit user authorization.

## Authoritative repository checkpoint

The repository is clean and synchronized with `origin/main` at commit **`3ccd8bd356dc98823ea4d7d7b48dde9d12636fc1`** (`QA hand object candidates 001 through 005`). The collection remains **770 generative tokens plus 7 reserved legendary one-of-ones**.

| Checkpoint item | Current state |
|---|---|
| Branch | `main...origin/main`, clean and synchronized |
| Production-QA checkpoint | `3ccd8bd356dc98823ea4d7d7b48dde9d12636fc1` (`QA hand object candidates 001 through 005`) |
| Backlog rows | 160 total |
| Ledger report | 76 registered production assets across categories; the backlog tally records 84 pending, 0 candidate, 0 QA-failed, 0 approved, and 77 registered rows |
| Complete categories | 9 of 16 |
| Head accessories | 0 / 10 registered; DG-123–DG-132 have QA-passed unregistered candidates |
| Hand objects | 0 / 12 registered; DG-133–DG-137 have QA-passed unregistered candidates |
| Latest QA result | DG-133–DG-137 passed binary intake, trait-rig, provenance, and pose-specific visual review |
| On-chain actions in this continuation | None |

The generated ledger in `docs/production_status.md` and the rows in `docs/trait-production-backlog.md` are authoritative. Older historical narrative elsewhere in the status document can describe superseded checkpoints.

## Work completed in the latest continuation

The first five hand-object backlog rows were produced as immutable generator-source evidence, normalized by the approved reduction-only workflow, and reviewed without registration. All five final review candidates are genuine 1254 × 1254 RGBA PNGs with `alpha_min=0`, valid source provenance, and a passing `--trait --max-width-ratio 1.30` gate. Unlike a generic partial trait, each hand object was also inspected in the approved pose-specific composite that governs its hand contact.

| Backlog ID | Asset | Approved pose | Result |
|---|---|---|---|
| DG-133 | Gnarled wood staff with blue flame/crystal | `base_pose_002_viewer_left_vertical_grip.png` | Automated QA pass; pose-context visual pass |
| DG-134 | Purple crystal orb | `base_pose_004_viewer_left_palm_up.png` | Automated QA pass; pose-context visual pass |
| DG-135 | Slender dark wand | `base_pose_002_viewer_left_vertical_grip.png` | Automated QA pass; pose-context visual pass |
| DG-136 | Silver straight sword | `base_pose_002_viewer_left_vertical_grip.png` | Automated QA pass; pose-context visual pass |
| DG-137 | Dark spellbook with gold star emblem | `base_pose_004_viewer_left_palm_up.png` | Automated QA pass; pose-context visual pass |

The generated source evidence is preserved under `images/trait_candidates/hand_objects/`. The normalized candidates and provenance reports are in `incoming/hand_objects/`. No generator source evidence was edited in place. The candidates remain unregistered; no assets were copied into `assets/hand_objects/`.

## Evidence files

The principal evidence is:

- `docs/qa/hand_objects_001-005_regen_review.md`
- `docs/qa/hand_objects_001-005_intake.json`
- `docs/qa/hand_objects_001-005_pose_review_sheet.png`
- `docs/qa/composites/hand_object_001_over_pose_002.png` through `hand_object_005_over_pose_004.png`
- `incoming/hand_objects/hand_object_001_arcane_staff_pose_002_left.provenance.json` through `hand_object_005_star_spellbook_pose_004_left.provenance.json`
- `scripts/render_hand_object_pose_context.py`

The pose-context renderer is deterministic evidence tooling: it composites each review candidate above the matching approved base pose in canonical layer order, then renders a review sheet. It does not change the manifest, backlog, ledger, or registered asset directories.

## Immediate next production priority

If registration is not explicitly authorized, produce the second hand-object representative batch **DG-138–DG-142**. These five assets all use the approved viewer-left vertical-grip pose, `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png`, with the contact/grip anchor at **X=404, Y=772**.

| Backlog ID | Asset | Canonical future production path |
|---|---|---|
| DG-138 | Warm-gold hanging lantern | `assets/hand_objects/hand_object_006_gold_lantern_pose_002_left.png` |
| DG-139 | Gold staff with blue gem | `assets/hand_objects/hand_object_007_gold_blue_gem_staff_pose_002_left.png` |
| DG-140 | Blue crescent-moon staff | `assets/hand_objects/hand_object_008_blue_crescent_staff_pose_002_left.png` |
| DG-141 | Violet short blade/dagger | `assets/hand_objects/hand_object_009_violet_blade_pose_002_left.png` |
| DG-142 | Horned skull scepter | `assets/hand_objects/hand_object_010_horned_skull_scepter_pose_002_left.png` |

Before generating, read `prompts/00_locked_master_specification.md`, `prompts/01_universal_avoid_block.md`, and `prompts/10_hand_objects.md`. Review `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png` as the required invisible alignment guide. Preserve the 1254 × 1254 RGBA target canvas, premium anime-chibi fantasy style, perfectly front-facing orthographic appearance, upper-left lighting, transparent modular-layer role, and reduction-only source-transform workflow.

For DG-138, use a narrow lantern handle or loop that meets the vertical-grip anchor, then allow the warm-gold lantern body to hang below the hand without crossing the character’s torso, legs, or canvas bounds. For DG-139 and DG-140, place narrow vertical shafts through the viewer-left grip; their gold-blue gem and blue crescent heads should rise on the outer left side of the body without entering the face region. For DG-141, put the dagger grip at the anchor and direct the compact blade upward, keeping the blade outside the face and torso. For DG-142, use a narrow scepter shaft at the grip and place the horned skull head high enough to remain clear of the face but low enough to remain inside the locked bounds.

## Required candidate workflow

Every source must be preserved under `images/trait_candidates/hand_objects/` before any normalization. Use only `scripts/normalize_generator_source.py` to derive a normalized review candidate. It must be a reduction-only transformation with documented source SHA-256, output SHA-256, source dimensions/mode, alpha-cleanup threshold, scale less than 1, and final placement. Never edit generator sources in place or use a generic background-removal workflow.

Run non-registering intake QA for the completed batch with `scripts/bulk_intake.py`, writing a batch-specific report and neutral-base review sheet. Then generate pose-specific composites over `base_pose_002_viewer_left_vertical_grip.png` for all five assets, using `scripts/render_hand_object_pose_context.py` as the precedent. Extend its `ITEMS` mapping for DG-138–DG-142 or create a dedicated batch renderer, but write separate `hand_objects_006-010` evidence files rather than overwriting the DG-133–DG-137 evidence.

The following sequence is appropriate after each future five-asset batch. Do not add `--register-approved` unless the user has separately authorized registration.

```bash
cd /home/ubuntu/Demigods
python3 scripts/bulk_intake.py /home/ubuntu/Demigods/incoming/hand_objects \
  --report /home/ubuntu/Demigods/docs/qa/hand_objects_006-010_intake.json \
  --sheet /home/ubuntu/Demigods/docs/qa/hand_objects_006-010_neutral_review_sheet.png \
  --qa-note 'Unregistered QA review for DG-138–DG-142.'
python3 scripts/render_hand_object_pose_context.py
```

Before checkpointing, visually inspect the generated pose review sheet and relevant individual composites. A binary or rig-gate pass is not sufficient if the object merely floats beside the hand, visibly covers the hand incorrectly, invades the face or torso, contains a body/hand/background artifact, or does not read as the stated backlog asset.

## Registration safeguard

DG-123–DG-132 and DG-133–DG-137 are **not registered**. If the user explicitly authorizes a registration batch, perform a final context review of the exact nominated candidates first, then use `scripts/bulk_intake.py` with the exact `--register-approved` backlog IDs. After a registration action, run the complete validation checkpoint:

```bash
python3 scripts/validate_config.py
python3 scripts/validate_assets.py assets
python3 scripts/validate_manifest_consistency.py
python3 scripts/report_production_status.py --check
python3 scripts/generate_777.py --preflight-only
python3 -m unittest discover -s tests -v
```

Then verify `git status --short --branch`, commit the registration batch atomically, and push `main`. Do not mint, publish metadata, release, or conduct any on-chain action.

## Non-negotiable safeguards

Every registered asset must be a genuine 1254 × 1254 RGBA PNG with true transparent alpha. Never register a checkerboard, matte, opaque, cropped, or presentation-background image. Preserve immutable generator-source evidence and use only `scripts/normalize_generator_source.py` for source normalization. Do not invent backlog rows. The seven legendary assets remain separate and reserved; they must not enter the generative manifest. Do not mint, publish metadata, release, or conduct any on-chain action without explicit user approval.

**Handover date:** 2026-08-15

**Repository:** `DOGECOIN87/Demigods`

**Branch:** `main`

**Production-QA checkpoint:** `3ccd8bd`

**Working tree at handover:** clean
