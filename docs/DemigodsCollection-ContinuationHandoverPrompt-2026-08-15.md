# Demigods Collection — Continuation Handover Prompt

You are continuing production oversight of the **Demigods** 777-token NFT collection in `DOGECOIN87/Demigods`. Work from the current `main` branch. Do not redesign the collection, weaken the locked modular-production contract, or perform minting, metadata publication, release, or on-chain actions without explicit user authorization.

## Authoritative repository checkpoint

The repository is clean and synchronized with `origin/main` at commit **`6cfc460`** (`Regenerate head accessory QA candidates`). The collection remains **770 generative tokens plus 7 reserved legendary one-of-ones**.

| Checkpoint item | Current state |
|---|---|
| Branch | `main...origin/main`, clean and synchronized |
| Latest commit | `6cfc46022573316ba7773e78c57328c625a07e51` |
| Backlog rows | 160 total |
| Authoritative ledger tally | 84 pending, 0 candidate, 0 QA-failed, 0 approved, 77 registered |
| Complete categories | 9 of 16 |
| Head accessories | 0 / 10 registered; DG-123–DG-127 have QA-passed unregistered candidates |
| Latest QA result | DG-123–DG-127 passed binary intake and trait rig gate |
| On-chain actions in this continuation | None |

The generated ledger in `docs/production_status.md` and the rows in `docs/trait-production-backlog.md` are authoritative. Older historical narrative elsewhere in the status document may describe superseded checkpoints.

## Work completed in this continuation

The first head-accessory generation attempt was rejected because of edge-touching alpha noise and rendered low-opacity backdrops. The generation parameters were then revised to use stricter central placement, wider transparent margins, explicit no-backdrop constraints, and a distinct transparent-background key. DG-124 was additionally regenerated individually without a style-reference image after the first revised batch retained excessive backdrop noise.

The regenerated source evidence is preserved under `images/trait_candidates/head_accessories/`. The normalized review candidates and provenance reports are under `incoming/head_accessories/`. No source evidence was edited in place.

| Backlog ID | Asset | Normalized bounds | Width ratio | Result |
|---|---|---:|---:|---|
| DG-123 | Gold pointed crown | `[367,129,886,488]` | 1.17× | Binary QA pass; rig-gate pass; visual review pass |
| DG-124 | Large gold halo ring | `[367,129,886,654]` | 1.17× | Binary QA pass; rig-gate pass; visual review pass |
| DG-125 | Green laurel wreath | `[367,129,886,570]` | 1.17× | Binary QA pass; rig-gate pass; visual review pass |
| DG-126 | Balanced black curved horn set | `[377,129,876,579]` | 1.13× | Binary QA pass; rig-gate pass; visual review pass |
| DG-127 | Silver winged circlet | `[367,129,886,406]` | 1.17× | Binary QA pass; rig-gate pass; visual review pass |

All five normalized candidates are genuine 1254 × 1254 RGBA PNGs with `alpha_min=0`, remain within the locked trait bounds, and pass the `--trait --max-width-ratio 1.35` gate. The review sheet and individual base composites show isolated modular layers without visible face, outfit, body, or background contamination.

## Evidence files

The principal evidence is:

- `docs/qa/head_accessories_001-005_review_sheet.png`
- `docs/qa/composites/head_accessory_001_over_base.png` through `head_accessory_005_over_base.png`
- `docs/qa/head_accessories_001-005_rig_gate.json`
- `docs/qa/head_accessories_001-005_intake.json`
- `docs/qa/head_accessories_001-005_regen_review.md`
- `incoming/head_accessories/head_accessory_001_gold_pointed_crown.provenance.json` through `head_accessory_005_silver_winged_circlet.provenance.json`
- `images/trait_candidates/head_accessories/` regenerated sources and immutable generator originals

## Immediate next step

The regenerated candidates are **not registered**. The user requested regeneration, QA, and a handover prompt; registration was intentionally left as a separate production action.

If the user explicitly authorizes registration, review the five candidates once more in context and then register them atomically with:

```bash
cd /home/ubuntu/Demigods
python3 scripts/bulk_intake.py /home/ubuntu/Demigods/incoming/head_accessories \
  --register-approved DG-123 DG-124 DG-125 DG-126 DG-127 \
  --report /home/ubuntu/Demigods/docs/qa/head_accessories_001-005_registration.json \
  --sheet /home/ubuntu/Demigods/docs/qa/head_accessories_001-005_registration_review_sheet.png
```

After registration, run the complete required validation checkpoint:

```bash
python3 scripts/validate_config.py
python3 scripts/validate_assets.py assets
python3 scripts/validate_manifest_consistency.py
python3 scripts/report_production_status.py --check
python3 scripts/generate_777.py --preflight-only
python3 -m unittest discover -s tests -v
```

Then verify `git status --short --branch`, commit the registration batch atomically, and push `main`. Do not mint, publish metadata, release, or conduct any on-chain action.

If registration is not authorized, the next production priority remains the second head-accessory representative batch **DG-128–DG-132**: silver ornate tiara, silver forehead circlet with central drop, translucent white veil, pale-blue spiked tiara, and gold low-profile circlet. Read `prompts/00_locked_master_specification.md`, `prompts/01_universal_avoid_block.md`, and `prompts/09_head_and_neck_accessories.md` before generating. Preserve the 1254 × 1254 RGBA canvas, shared rig coordinates, premium anime-chibi fantasy style, upper-left lighting, transparent modular-layer role, and reduction-only source-transform workflow.

## Non-negotiable safeguards

Every registered asset must be a genuine 1254 × 1254 RGBA PNG with true transparent alpha. Never register a checkerboard, matte, opaque, cropped, or presentation-background image. Preserve immutable generator-source evidence and use only `scripts/normalize_generator_source.py` for source normalization. Do not invent backlog rows. The seven legendary assets remain separate and reserved; they must not enter the generative manifest. Do not mint, publish metadata, release, or conduct on-chain actions without explicit user approval.

**Handover date:** 2026-08-15
**Repository:** `DOGECOIN87/Demigods`
**Branch:** `main`
**Commit:** `6cfc460`
**Working tree at handover:** clean
