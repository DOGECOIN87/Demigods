# Head Accessories DG-123–DG-127 — Source QA Rejection

**Date:** 2026-08-15
**Category:** Head accessories
**Backlog rows:** DG-123–DG-127
**Decision:** Reject all five generated sources for this batch; register none.

The batch was generated as isolated head-accessory concepts using the locked frontal anime-chibi fantasy direction and the DG-123 crown as the style reference for the subsequent four assets. The immutable generator-source files are retained under `images/trait_candidates/head_accessories/`, including the generator-created original RGB companions where present.

| Backlog ID | Asset | QA result | Rejection reason |
|---|---|---|---|
| DG-123 | Gold pointed crown | Rejected | The first source contained edge-touching alpha noise and failed the reduction-only normalizer's safe-isolation check. A final retry was also rejected because the output had no genuinely transparent pixels and a low-opacity rendered backdrop across the full canvas. |
| DG-124 | Large gold halo ring | Rejected | Both generated attempts retained a rendered dark backdrop / low-opacity matte across the full canvas; the alpha channel had no fully transparent field. |
| DG-125 | Green laurel wreath | Rejected | The retry contained only a handful of fully transparent pixels and retained a low-opacity rendered backdrop, making it unsuitable for the locked transform route. |
| DG-126 | Black curved horns | Rejected | The retry contained only a handful of fully transparent pixels and retained a low-opacity rendered backdrop, making it unsuitable for the locked transform route. |
| DG-127 | Silver winged circlet | Rejected | Both generated attempts retained a rendered dark backdrop / low-opacity matte across the full canvas; the alpha channel had no fully transparent field. |

No generic background-removal shortcut, repaint, crop, or manual alpha reconstruction was used. No normalized candidate passed intake, no review composite was approved, no compatibility rule was changed, and no manifest, backlog, or production ledger registration was performed.

The batch should be regenerated only when capacity is available and the generation route can produce a clean isolated source with genuine transparent alpha, a generous transparent margin, and no edge contact. The next attempt must not reuse these rejected files as production inputs.
