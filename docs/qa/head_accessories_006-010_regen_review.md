# Head Accessories DG-128–DG-132 — Candidate Review

**Date:** 2026-08-15

**Category:** Head accessories

**Backlog rows:** DG-128–DG-132

**Scope:** Unregistered review candidates only. No manifest, backlog, ledger, metadata, release, minting, or on-chain change has been performed.

## Source and transformation record

The first generation attempt for this batch produced source images with edge-touching presentation haze. Those immutable source files remain preserved as `*_source1.png` evidence and were not normalized or registered. A second, isolation-focused source batch was generated with a distinct temporary alpha key, no style-reference image, explicit empty margins, and direct-cutout constraints. The normalized candidate files were derived only from the `*_source2.png` sources through `scripts/normalize_generator_source.py` using reduction-only placement at the locked head-accessory rig anchor.

| Backlog ID | Candidate | Source accepted for normalization | Alpha threshold | Final bounds | Automated result | Initial visual result |
|---|---|---|---:|---|---|---|
| DG-128 | Silver ornate tiara | `head_accessory_006_silver_ornate_tiara_source2.png` | 64 | `[367,129,886,443]` | Pass | **Visual pass — symmetrical, cleanly isolated, and facial features remain readable** |
| DG-129 | Silver forehead circlet with central drop | `head_accessory_007_silver_drop_circlet_source2.png` | 64 | `[367,129,886,312]` | Pass | **Visual pass — drop is centered at the forehead with clear eye and face separation** |
| DG-130 | Translucent white veil | `head_accessory_008_translucent_white_veil_source3.png` | 32 | `[387,129,866,510]` | Pass | **Visual pass — corrected side drapes preserve a clear, readable face window** |
| DG-131 | Pale-blue spiked tiara | `head_accessory_009_pale_blue_spiked_tiara_source3.png` | 32 | `[367,129,886,338]` | Pass | **Visual pass — corrected high band and short points remain above the eye zone** |
| DG-132 | Gold low-profile circlet | `head_accessory_010_gold_low_circlet_source2.png` | 32 | `[367,129,886,278]` | Pass | **Visual pass — the narrow gold silhouette is centered and preserves full face readability** |

The first automated intake report was `docs/qa/head_accessories_001-010_intake.json`. The authoritative final automated report after the two targeted source3 corrections is `docs/qa/head_accessories_006-010_intake.json`, with `docs/qa/head_accessories_006-010_review_sheet.png` as its matching composite review sheet. It contains the five present DG-128–DG-132 candidates.

## Review criterion

The binary and trait-rig gates are necessary but not sufficient. A candidate must also remain an isolated modular layer that reads cleanly and does not visibly merge with or undermine the base character in the required composite. The final source3 corrections for DG-130 and DG-131 meet that art-direction condition: the veil frames rather than covers the face, and the tiara’s high band remains clear of the eyebrow and eye zone.

## Current provisional disposition

All five candidates, DG-128 through DG-132, are **automated-pass and visual-pass**. They remain unregistered review candidates. The prior rejected source1 and source2 artifacts remain preserved as immutable generation evidence; only the two corrected review candidates and their provenance sidecars were replaced through the source3 reduction-only transform.

No asset in this batch is registered. The candidates may be considered for a separate, explicitly authorized batch-registration action only after the user directs it.
