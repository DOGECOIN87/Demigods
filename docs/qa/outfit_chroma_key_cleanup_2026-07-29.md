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

## Not fixed: outfit_002's residual spill and closed collar

`outfit_002` is the one outfit the mechanical fix cannot finish, for two related
reasons.

**Residual spill (455 px).** Its green is not confined to the alpha edge; it is
scattered through the collar interior and along several internal seams. Widening
the despill band trades badly — at band 14 the green falls to 61 but artwork
damage rises to 475 shifted pixels, an order of magnitude worse than the fix
applied.

**The collar is a sealed cone.** Its opening is painted opaque (`a=255`, dark
teal), so the base body's fully-rendered neck never shows and the head reads as
sitting on a tube. Measured neck visibility across the family:

| Outfit | neck px visible |
|---|---|
| `outfit_004` | 37.6% |
| `outfit_001` | 23.8% |
| `outfit_005` | 18.5% |
| `outfit_002` | **16.3%** |
| `outfit_003` | **15.6%** |

Four approaches to opening it by pixel surgery were tried and all rejected:
geometric hole cut with a feather (mushy edges, green residue survived), crisp
geometric cut (chewed fragments at the collar corners), colour region-grow
(consumed the collar rim along with the interior, since both are dark, and left
a hard bounding-box edge), and wider-band despill (artwork damage).

They fail for a structural reason rather than a tuning one: **the inside face of
the collar rim was never painted.** Removing the interior surface does not
reveal a collar seen from within — it reveals nothing, because nothing was drawn
there. No alpha edit can add geometry the artwork does not contain.

`outfit_002` and `outfit_003` need a re-render with an open collar. That
requirement is now recorded in `prompts/08_outfits.md`.

## Head position

Lowering the head was prototyped (smooth displacement: head translates down N,
neck band absorbs it, nothing at or below the shoulder line moves) and works
cleanly at both 18px and 30px. It is **deliberately not applied**, because
lowering the head reduces visible neck — and too little visible neck is the
defect being fixed. Head height should be judged against a corrected collar, not
against this one.
