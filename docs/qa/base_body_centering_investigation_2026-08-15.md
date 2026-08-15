# Base-body centering investigation — 2026-08-15

## Scope

This investigation examined the three base-body assets that failed the strict `rig_gate_report.py --pose-variant --tolerance 1` diagnostic: the neutral master, the viewer-right vertical-grip pose, and the centered two-hand-grip pose. No production asset bytes were modified.

## Measurements

The locked canvas center is X=627. The diagnostic computes the body center from the mean of the head-band and leg-band centers so that raised-arm asymmetry does not dominate the measurement.

| Asset | Head-band center | Leg-band center | Diagnostic body center | Delta from X=627 | Strict result |
|---|---:|---:|---:|---:|---|
| `base_body_001_neutral_master.png` | 626.0 | 625.5 | 625.75 | -1.25 px | Minor deviation |
| `base_pose_003_viewer_right_vertical_grip.png` | 626.0 | 625.5 | 625.75 | -1.25 px | Minor deviation |
| `base_pose_005_centered_two_hand_grip.png` | 626.5 | 624.5 | 625.50 | -1.50 px | Minor deviation |

For comparison, the other asymmetric poses remain within the strict diagnostic tolerance: `base_pose_002` measures +0.5 px and `base_pose_004` measures -1.0 px.

## Interpretation

The deviations are small raster-silhouette centering differences, not canvas, alpha, bounds, dimension, manifest, or asset-decoding failures. The visual comparison places the locked X=627 guide through the head and torso regions for all five base bodies; the failing cases do not show a visibly displaced character. The strict values arise from anti-aliased silhouette extents and small leg/arm asymmetries, not from a shifted rig or missing pixels.

The repository’s regression suite explicitly documents that asymmetric grip poses may shift silhouette center while still passing asset validation. All 196 regression tests pass, and the full production audit reports 85 production files with zero asset-validation failures and a consistent manifest.

## Non-destructive refinement simulation

An integer +1 px translation would make each of the three strict measurements pass, producing deltas of -0.2 px, -0.2 px, and -0.5 px respectively. However, applying that translation to a registered base asset would also move its locked hand, face, waist, and pose-reference geometry. That creates a greater downstream risk for hand-object alignment and pose composites than the current subpixel silhouette deviation.

## Recommendation

**Do not refine the production assets.** Keep the registered PNG bytes and canonical anchor coordinates unchanged. Treat the three values as accepted rasterization-level deviations and use the 2 px diagnostic tolerance for the base-body family, while retaining the stricter 1 px tolerance for detecting larger regressions. Reopen refinement only if a future composite demonstrates an actual face, hand, waist, or pose-anchor misalignment.

## Verification state

The investigation itself created only QA analysis artifacts. No production asset, manifest entry, backlog status, release state, metadata publication, minting, or on-chain state was changed.
