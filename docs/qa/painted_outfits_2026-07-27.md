# QA — Painted robes replace the procedural coats (2026-07-27)

Six painted robes supplied by the collection owner, registered as DG-199 to
DG-204. The five interim procedural coats (DG-164 to DG-168) are removed: files,
registrations and backlog rows. They existed only to clear the release blocker
and were flat and near-identical. `scripts/build_outfit.py` is kept.

- Fitted robes on a full character: `composites/painted_outfits_2026-07-27.png`
- Pose interaction: `composites/painted_outfit_poses_2026-07-27.png`

## What arrived, and what had to change

Each reference is a native 1254 × 1254 **RGB** file. The transparency checker
visible in a viewer is painted into the pixels — there is no alpha channel, and
the corners read `(253,253,253)`. They are also drawn at full humanoid
proportions, roughly 1100 px collar to hem, against a rig whose entire body below
the chin is 606 px.

`scripts/intake_painted_outfit.py` handles both.

**Backdrop.** Flood fill from the canvas border through near-white, near-neutral
pixels — not a brightness threshold, which would eat the white-and-gold robes
whose fabric is as bright as the backdrop. The fill stops at their grey shading
and gold linework. Tolerance has real headroom: 225 and 235 agree to within 1%,
while 242 leaks through the garment and claims the whole canvas.

Edge alpha comes from softening that mask, and edge colour is then
un-premultiplied against the backdrop white. Without the second step the layer
carries a pale rim — invisible on a light page, obvious against the dark
backgrounds these actually stand on.

**Fit.** Collar at Y 442, hem at Y 1108, scaled about the locked centre axis.
Rescaling during intake was **waived by the collection owner** for this batch and
is recorded in each manifest entry as `rig_refit_collar_y_442_hem_y_1108`.

Y 442 was found by measurement, not by eye. Seating the collar at Y 480 puts the
hem exactly where the procedural coats had it and looks right in isolation, but
leaves a rim of bare shoulder outside the pauldrons on **every robe and every
pose** — the deltoid sits below the pauldron edge. Sweeping scale and offset for
zero bare skin in the shoulder band, subject to keeping the hem at 1108, lands on
Y 442. Five of six robes then measure zero; the white-and-gold robe measures 564
px of 32,242 in the band (1.7%), from its open V-neck.

All six pass the rig gate and sit inside `maximum_character_bounds`.

## The finding worth reading: sleeves defeat the pose variants

An outfit composites *over* the base body, so its sleeves replace whatever the
arms were doing — and a garment is painted with one arm position baked in. The
five base poses differ from each other *only* in arms and hands.

Measured as the share of each pose's silhouette difference from the neutral
master that the garment covers:

| Base pose | Painted robe | Procedural coat (removed) |
|---|---|---|
| 001 neutral master | 0.0% | 0.0% |
| 004 viewer-left palm-up | 58.6% | 33.6% |
| 003 viewer-right vertical grip | 63.6% | 44.6% |
| 002 viewer-left vertical grip | 64.7% | 44.3% |
| 005 centered two-hand grip | 82.8% | 61.2% |

The wide bell sleeves make it worse. But the right-hand column is the point:
**this was already true and had not been measured.** Under any sleeved outfit the
five poses are close to interchangeable, and under a painted robe pose 005 loses
the two-hand grip that is its whole reason to exist.

Nothing looks broken — a robe covering the arms reads as a robe, and the hands
still emerge from the bell cuffs on poses 001–004. The cost is variety: four of
the five base-pose assets contribute far less than their count suggests, and the
combination space overstates the visible difference between tokens.

Three ways out, none taken yet:

1. **Compatibility exclusion.** Rule out pose 005 for wide-sleeve outfits.
   Cheapest, and `config/compatibility.json` currently holds zero rules so the
   machinery is unused. Costs combination space, and does nothing for 002–004.
2. **Per-pose sleeve variants.** Render each robe once per arm position. Five
   times the artwork, and the only option that actually preserves the poses.
3. **Accept it.** Treat the poses as near-cosmetic and stop counting them as
   variety. Honest, and free.

The measurement belongs in the record either way; the decision does not have to
be made now.

## Known limits

These six are distinct painted designs, not recolours, so the category gains six
*designs*. They do not correspond to any cell in the `OUTFIT` sheet, so DG-037 to
DG-046 stay pending.

The garments are drawn for a standing figure with arms down. Any future base pose
with raised arms will not work with them at all, rather than merely hiding
detail.
