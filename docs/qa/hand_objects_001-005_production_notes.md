# Hand Objects DG-133–DG-137 — Production Notes

**Date:** 2026-08-15

**Scope:** Unregistered source-candidate production only. No production asset, manifest, backlog, ledger, metadata, release, minting, or on-chain modification is authorized by this work.

## Approved pose references

The first hand-object batch contains two pose families. DG-133, DG-135, and DG-136 must be aligned to `assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png`: an upright object shaft must meet the viewer-left closed hand at the locked viewer-left hand anchor, without adding a second hand or any body pixels. DG-134 and DG-137 must be aligned to `assets/base_bodies/base_pose_004_viewer_left_palm_up.png`: their lower support/contact geometry must sit naturally above the viewer-left open palm, without adding a hand, arm, body, or background.

All five candidates must use the locked 1254 × 1254 RGBA review canvas after reduction-only transformation. The source prompt must request a single isolated object, genuine alpha, a clean transparent margin, front-facing orthographic view, and upper-left lighting. Object-only source art must not contain a body, hand, arm, grip illustration, outfit, face, character, label, background, or an opaque presentation matte.

## Batch composition

| Backlog ID | Asset | Pose family | Intended contact behavior |
|---|---|---|---|
| DG-133 | Gnarled wood staff with blue flame/crystal | Viewer-left vertical grip | Narrow vertical shaft intersects the closed-grip position at X=404, Y=772; shaft may extend upward but remains within the locked canvas |
| DG-134 | Purple crystal orb | Viewer-left palm-up | Compact orb rests just above the open palm at X=404, Y=772; no hand or arm pixels in the asset |
| DG-135 | Slender dark wand | Viewer-left vertical grip | Thin vertical or gently diagonal shaft meets the closed-grip position at X=404, Y=772 |
| DG-136 | Silver straight sword | Viewer-left vertical grip | Straight narrow sword grip meets the closed-grip position at X=404, Y=772; blade extends upward |
| DG-137 | Dark spellbook with gold star emblem | Viewer-left palm-up | Closed book is centered immediately above the open palm at X=404, Y=772; no body or hand pixels |
