# QA — green key spill on outfits 002–005, and the collar that needs a re-render

Date: 2026-07-29

## Defect

Four of the five registered outfits carried green-screen residue on their edges:

| Outfit | alpha-edge px fringed | peak G excess | total green px |
|---|---|---|---|
| `outfit_001` | 0.0% | 0 | 0 |
| `outfit_002` | 33.4% | 157 | 1259 |
| `outfit_003` | 33.9% | 196 | 926 |
| `outfit_004` | 49.2% | 202 | 1021 |
| `outfit_005` | 16.2% | 179 | 299 |

Outfits are a mandatory category, so this was visible on every token.

## Root cause

Every affected outfit already recorded `alpha_edge_contract_1` in its
postprocessing, so the contract was not missing — it was **ordered wrong**:

```
chroma_key_to_alpha -> alpha_edge_contract_1 -> rig_refit_scale_… (resample)
```

The contract removed the contaminated outer pixel, and then the refit's LANCZOS
resample blended the *still-contaminated* neighbours into a brand-new soft edge,
reintroducing the fringe. `outfit_001` is clean for exactly one reason: it has no
refit step, so nothing resampled its edge afterwards.

**An edge contract must run after any resample, not before.**

## Fix applied

`scripts/clean_chroma_key.py`, two passes:

1. `alpha_edge_contract_1_post_refit` — erode alpha by 1px, this time last.
2. `chroma_despill_edge_band_3` — clamp G to `max(R, B)`, restricted to a 3px
   band around the alpha edge.

| Outfit | green before | after | artwork px shifted >20 levels |
|---|---|---|---|
| `outfit_002` | 1259 | 455 | 54 |
| `outfit_003` | 926 | 24 | 38 |
| `outfit_004` | 1021 | 0 | 16 |
| `outfit_005` | 299 | 4 | 12 |

All four still pass `--trait --max-width-ratio 1.15`.

### Why the despill is band-limited

An unrestricted despill is not safe on this collection. Run across the whole
layer it desaturated the **green potion bottles** on `outfit_003`'s bandolier —
173 pixels shifted by more than 20 levels, visibly dulling real artwork. The
operation cannot distinguish key spill from a green object, so it is confined to
the band where spill actually occurs. The same outfit loses 38 pixels under the
3px band, and the potions are untouched.

## The sealed collars — fixed

`outfit_002` and `outfit_003` were both painted with **sealed collars**: the
opening is opaque (`a=255`), so the base body's fully-rendered neck never showed
and the head read as sitting on a tube.

| Outfit | neck visible before | after |
|---|---|---|
| `outfit_001` | 23.8% | 23.8% |
| `outfit_002` | **17.2%** | **26.3%** |
| `outfit_003` | **16.1%** | **30.3%** |
| `outfit_004` | 39.1% | 39.1% |
| `outfit_005` | 19.8% | 19.8% |

The two collars are sealed in different ways. `outfit_002`'s opening is filled
with the collar's own dark interior. `outfit_003` has a *duller neck painted into
the garment* — measured at `(194,141,114)` against the base body's brighter skin —
so the character wore a flat, lifeless neck.

### Five approaches, and what separated the last one

Rejected, in order: a feathered geometric hole (mushy edges, residue survived), a
crisp geometric cut (chewed fragments at the collar corners), a colour
region-grow (consumed the rim along with the interior — both are dark, so colour
cannot separate them — and clipped to a visible bounding box), a fixed-column
alpha subtract (hard vertical edges where the column crossed the widening
silhouette), and a **V-taper with a soft bottom fade**.

That fifth one is worth recording because it passed every measurement and still
looked wrong. It cross-faded removal out over ~18 rows, and skin blending into
dark teal produced a muddy translucent smear — the collar's top rim read as a
torn edge and there was no neckline at all. **A garment edge is a hard line; a
gradient does not read as fabric.**

The version that works combines two things:

*The boundary comes from the artwork, not from invented geometry.* The rim lies
outside the neck's silhouette and the interior inside it, so the base body's own
anti-aliased neck alpha separates them exactly, and the horizontal edge inherits
that anti-aliasing:

```
new_outfit_alpha = outfit_alpha * (1 - neck_mask)
```

*The bottom edge is crisp and lands on the collar's own front rim.* The rim was
traced from each image — the row where the interior gives way to the garment's
front face — and fitted as a shallow arc, with a fractional final row for
sub-pixel accuracy. Per-garment because collars differ:

| Outfit | rim centre | rim rise | half-width | transition traced |
|---|---|---|---|---|
| `outfit_002` | 502 | 12 | 32 | dark interior → teal placket |
| `outfit_003` | 520 | 27 | 30 | painted neck → white shirt |

Implemented in `scripts/open_collar.py`; a test asserts the alpha transition
completes within two rows, so the fade cannot come back.

### Residual spill on outfit_002

Opening the collar also solved its spill problem. The remaining 442 green pixels
sat on the collar interior and internal seams; with the interior gone, a
full-layer despill clears them to **0**.

A full despill is safe on `outfit_002` specifically, and that was verified rather
than assumed: every green run in the layer measures 1–5px horizontally, which is
edge spill. A green *object* — `outfit_003`'s potion bottles — produces runs an
order of magnitude longer. `outfit_003` therefore keeps the 3px-band despill.

## Head position

Lowering the head was prototyped (smooth displacement: head translates down N,
neck band absorbs it, nothing at or below the shoulder line moves) and works
cleanly at both 18px and 30px. It is **deliberately not applied**, because
lowering the head reduces visible neck — and too little visible neck is the
defect being fixed. Head height should be judged against a corrected collar, not
against this one.
