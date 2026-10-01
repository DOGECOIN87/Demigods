# Compact horned scepter 010 — 2026-10-01

The previously registered skull and horned head covered 1,359 opaque pixels
in the fixed viewer-left eye window `(505,334)–(584,403)`. The owner asked for
the foreground traits to be reviewed after the depth batch. A new native
1254 × 1254 transparent in-hand candidate narrows the skull while keeping the
purple gem, curved horns, shaft and wristless gripping hand.

The source is preserved at
`images/trait_candidates/hand_objects/in_hand_2026-10-01-scepter/010_compact_skull_source.png`
(SHA-256 `de95cc9745b8baf783002a0270adfe40d16bd62274f9c88e3cb68f8c884c59f1`).
The last batch in `scripts/register_in_hand_objects.py` uses the existing
`clean_render` and `fit_round2` pipeline at scale 1 and offset `(0,0)`. It
drops low-alpha detached specks and retains the artist's item geometry.

| Check | Previous | Compact candidate |
|---|---:|---:|
| Opaque pixels in eye window | 1,359 | 0 |
| Exposed base-fist core pixels | 0 | 0 |
| Exposed base-fist pixels including fringe | 1 | 0 |
| Output bounds | `(340,317)–(549,1012)` | `(369,375)–(530,1015)` |

The [four-column composite](compact_scepter_2026-10-01.png) shows the item
over the bare pose 002 and all three compatible dressed outfits (007, 008,
009). The skull leaves the face clear and the hand remains wrapped around the
shaft. The black robe's inward pose-002 fist remains excluded from hand
objects by the existing compatibility rule.

This replacement changes only the registered hand-object PNG, its checksum
and provenance in the manifest, and the reproducible registration batch. It
does not restore withdrawn traits or alter the outfit rules.
