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
| `outfit_002` | **17.2%** | **25.8%** |
| `outfit_003` | **16.1%** | **23.3%** |
| `outfit_004` | 39.1% | 39.1% |
| `outfit_005` | 19.8% | 19.8% |

### Four approaches that failed, and why the fifth works

Rejected: a feathered geometric hole (mushy edges, residue survived), a crisp
geometric cut (chewed fragments at the collar corners), a colour region-grow
(consumed the collar rim along with the interior — both are dark, so colour
cannot separate them — and left a hard bounding-box edge), and a fixed-column
alpha subtract (hard vertical edges where the column clipped).

Every one of them **invented its own boundary**. The working approach uses the
boundary already present in the artwork: the collar rim lies *outside* the neck's
silhouette and the painted interior lies *inside* it, so the base body's neck
alpha separates them exactly.

```
new_outfit_alpha = outfit_alpha * (1 - neck_mask)
```

Because that alpha is anti-aliased, the resulting edge is too — no feathering
needed and nothing invented. Two shaping terms make it read as a garment: the
opening narrows from 33px to 9px half-width into a V following the collar's own
front line (this is what removed the hard vertical edges), and removal fades out
over the lower span so the garment closes over the chest rather than ending on a
horizontal cut. Implemented in `scripts/open_collar.py`.

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
