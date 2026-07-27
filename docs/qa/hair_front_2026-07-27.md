# QA — Front hair clears the bald-head defect (2026-07-27)

Eight procedural fringe layers registered as DG-229 to DG-236, plus the first
eight compatibility rules the collection has ever carried.

- Token sheet: `composites/hair_front_tokens_2026-07-27.png`
- Before, for comparison: `composites/face_tokens_thumbnail_2026-07-27.png`

## The defect

`hair_front` held nothing, which by itself would only mean a thinner collection.
Measurement showed it meant more than that:

| Scalp row | Head width | Covered by `hair_back` |
|---|---|---|
| Y 150 | 124 px | 0 px (0%) |
| Y 200 | 275 px | 0 px (0%) |
| Y 250 | 322 px | 0 px (0%) |
| Y 300 | 329 px | 0 px (0%) |
| Y 340 | 312 px | 1 px (0%) |

All eight registered `hair_back` assets are wisps either side of the skull —
their bounds start at Y 132 but none of it is over the head. The base master is
deliberately bald. So **every token in the collection rendered as a bald head**,
which is the same class of defect as the outfit blocker, and it had been sitting
in plain sight in every QA sheet.

## Build

`scripts/build_hair_front.py`. The cap is taken from the base body's **own
alpha**, dilated 4 px so the hair sits proud of the scalp rather than looking
painted onto it. Deriving it from the body rather than drawing an ellipse means
it cannot drift from the skull if the base is ever re-rendered.

The fringe is tapered capsules — signed distance to a segment minus a radius that
shrinks along it — evaluated at 3× supersampling inside the hair band only.
Supersampling the full canvas would be 14 million evaluations in pure Python; the
band is 400 × 345, about a hundredth of that, and runs in 8 seconds per palette.

Two numbers came from measurement rather than taste:

**The cap hands over along a curve, not a row.** Cropping the cap at a single Y
drew a hard horizontal line straight across the face — the first attempt did
exactly that and looked like a helmet brim. The handover now runs from Y 232 at
the centre to Y 322 at the temples on a cosine, so the cap keeps covering the
sides of the skull while the locks hang over the forehead.

**Locks tip at Y 285-306.** The recovered eyebrows occupy Y 292-343 and
`hair_front` composites at layer 12, above `eyebrows` at 09. A longer fringe
would hide a whole category behind another one. At this length the brows read
under the fringe, which is what the composite sheet confirms.

The locks also overlap laterally on purpose. A sparse set leaves scalp showing
between the tips and reads as a torn edge rather than a fringe.

## First compatibility rules

The random sheet immediately showed a gold fringe over red back-hair. Front and
back are independent categories, so nothing stopped it.

`config/compatibility.json` had held zero rules since it was written.
`generate_777.py` has always honoured `requires`; it had simply never been given
anything. Eight rules now pair each fringe with its matching back layer:

```json
{
  "trait": "hair_front_003_fringe_gold.png",
  "requires": "hair_back_011_recolour_gold.png",
  "reason": "front and back hair must share a colour"
}
```

Combination space is 43,130,880 with the rules applied.

## Known limits

**Colour varies, shape does not.** All eight share one fringe silhouette, so the
collection gains eight fringe *colours* and one fringe *cut*. They are simpler
than the painted hair — no strand separation, no wave structure, a single
three-stop ramp driven by distance from the key light at (548, 196).

The eight `HAIR` sheet lower-row cells are distinct cuts, so DG-115 to DG-122
stay pending and are not satisfied by these.

The requires rules mean a token with front hair must also take back hair. That is
correct today, since both categories are populated in matching colours, but a
future palette added to one side and not the other will silently shrink the
usable space rather than fail loudly.
