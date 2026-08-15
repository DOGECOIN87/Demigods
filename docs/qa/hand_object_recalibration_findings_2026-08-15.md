# Hand-object recalibration findings — 2026-08-15

The native base-pose review confirms that the viewer-left vertical-grip pose has a closed hand on the viewer-left side, while the viewer-left palm-up pose has an open palm extended farther outward and lower. A single shared anchor `(404, 772)` is therefore insufficient for all objects.

The current hand-object composites were visually misleading because the object layers were positioned from generic canvas bounds rather than an object-specific grip/contact point. The recalibration must use a per-object contact coordinate: the staff, blade, and scepter should have their shaft/handle crossing the closed-hand center; the lantern should place its handle loop at the closed-hand center; the talisman should place its hanging loop at the palm center; and the tome should place its lower inner edge into the palm rather than its visual bounding-box center.

The next diagnostic will calculate these contact points from the source alpha geometry and render native-resolution composites with explicit crosshairs at the measured hand landmarks. No production bytes have been changed during this recalibration phase.

## Native source observations

The gold-blue staff has a long thin shaft with no explicit enlarged grip region; its contact should therefore be defined by the shaft center at the closed-hand landmark, not by the visible-object bounding-box center. The lantern has a distinct hanging loop at the top; the loop—not the lantern body—must coincide with the closed-hand landmark. The previous placement made the object read as a side prop because the visible body was aligned near the hand instead of the grip feature.

## Measured hand regions

The coordinate-grid crops show the nominal locked anchor `(404,772)` is left of the visible gripping center in both poses. In the vertical-grip pose, the closed fist occupies approximately `x=405–450, y=750–805`, with the shaft contact center around `(438,772)`. In the palm-up pose, the open hand occupies approximately `x=395–465, y=720–770`; the usable palm contact center is around `(438,748)`. The prior object placements at `x=404, y=772` therefore place the objects near the wrist/left edge rather than through the hand.

Recalibration targets: pose 002 contact `(438,772)`; pose 004 contact `(438,748)`. Object-specific feature points must be translated to these targets: shaft center for staffs/blade/scepter, hanging-loop center for the lantern, loop center for the talisman, and the tome’s inner lower grip edge for the book.

## Object-specific contact observations

The violet blade's usable grip is the wrapped handle below the gold guard, not the blade or guard. The brown tome should be seated into the palm with its lower-left interior edge crossing the palm center; aligning its bounding-box center makes it float beside the hand. These features will receive explicit per-object target coordinates in the next transform pass.

## First recalibrated result

The recalibrated native-resolution staff composite now shows the shaft passing directly through the closed fist at the viewer-left hand. The prior side-mounted appearance is corrected. The remaining lantern and palm-up objects require the same native-resolution confirmation before the hand-object batch is finalized.

## Additional recalibrated results

The lantern loop now seats directly into the closed fist and the body hangs naturally below it. The tome now overlaps the palm-up hand at the inner left edge rather than floating to the side. These two representative results confirm that per-object translation is correcting the visual contact failure more effectively than the prior shared-anchor placement.

## Seven-item native review

The complete recalibrated sheet shows each object crossing the measured red hand anchor: the lantern loop, staff shafts, blade handle, and scepter shaft intersect the closed fist; the talisman loop and tome edge intersect the palm-up hand. This is the first review pass in which all seven registered objects visually share the same measured hand contact model.

## User-requested pose and silhouette correction

The pose-2 hand is a closed viewer-left grip with the fingers wrapping around an object near the hand center; the current vertical staff/scepter treatment reads as an upright prop rather than a naturally held item. The pose-4 hand is an open, palm-up viewer-left hand with the fingers extending horizontally; a book should rest across the palm/fingers with its spine and lower edge aligned to the palm, not sit beside the hand. The user also identified the violet sword as too thick and the current book design as incorrect. Revisions must therefore change orientation and contact geometry, not only translate the existing assets.

## Native silhouette inspection

The violet sword source is a broad, heavy fantasy blade whose blade width dominates the handle; it needs a narrower blade and a more believable grip-to-blade proportion. The tome source is a small closed book shown nearly upright/diagonal with a front-cover emblem; for the pose-4 open palm it should instead read as a horizontally resting, slightly open spellbook with the spine/inner edge seated across the palm and the pages extending over the fingers.

## Revision candidates

A revised sword candidate was generated with a substantially narrower blade while retaining the original purple/gold identity. A revised book candidate was generated as a compact, slightly open spellbook intended to rest across the palm. Both image-generation outputs include a visible checkerboard preview background and 1920×1920 dimensions, so they must be normalized by removing only the checkerboard and fitting the subject to the locked 1254×1254 RGBA canvas before acceptance.

## Normalized candidate review

The normalized sword candidate is visibly narrower than the registered sword while retaining the purple faceted blade, gold guard, wrapped grip, and pommel. The normalized book candidate is now a compact, slightly open horizontal spellbook with visible pages and a defined spine, matching the requested palm-up holding concept. Both are clean 1254×1254 RGBA files and are ready for composite placement review; they have not yet replaced the registered production assets.

## Book candidate revision v2

The first pose-aware sheet confirmed that the book still read as a thin side wedge at character scale. A second focused edit produced a clearly open, broad spellbook with two leather covers, visible cream pages, a central spine, and a mostly horizontal three-quarter view. This v2 candidate is the one to normalize and test against the pose-4 open palm.

## Pose-aware candidate audit

The pose-aware staging batch passes the native audit for the five pose-2 objects and the revised pose-4 book: all are 1254×1254 RGBA, remain within the intended canvas bounds, and have alpha overlap in a 61×61 neighborhood around their measured hand anchors. The sword candidate now has a narrower silhouette, while the pose-2 held objects lean outward by 12 degrees around the closed-grip anchor. The v2 spellbook occupies the palm-up envelope from approximately `(300,683)` to `(609,815)`.

## Installed production review

The installed native-resolution sheet confirms the revised pose behavior: the staffs, sword, and scepter now lean with the closed-grip pose instead of standing perfectly straight; the lantern remains naturally vertical from its loop because it hangs by gravity. The sword is visibly slimmer. The v2 book now extends horizontally from the pose-4 palm with a clear cover/page silhouette and its inner edge crossing the measured palm anchor.

## Final 100-token pose-aware sample

The final 100-token dry run produced 100 unique tokens and passed all metadata, source, canvas, and compatibility checks. The review sheet shows the revised sword and angled pose-2 objects recurring without a visible systematic placement failure at sample-sheet scale; the pose-4 book appears as a horizontal palm-held object in its compatible combinations.
