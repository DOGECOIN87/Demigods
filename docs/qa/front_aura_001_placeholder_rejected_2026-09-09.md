# DG-145 front aura 001 — registered placeholder, deregistered 2026-09-09

**Asset:** `assets/front_auras/aura_front_001_orange_rising_flame.png`
**Backlog row:** DG-145, "Orange rising foreground flame"
**Decision:** QA-failed and deregistered. The registered file is removed; the immutable
candidate is retained at
`images/trait_candidates/front_auras/aura_front_001_orange_rising_flame_candidate.png`.

## What it actually was

A flat-shaded placeholder. Its 126,276 opaque pixels carry **three distinct colour buckets**:
hard-edged orange and gold triangles plus a few solid circles, with no internal value
structure, no falloff, and no soft edge anywhere. Alongside a category whose rear-aura
siblings are analytic distance-field renders with genuine luminous alpha, it is not the same
kind of object.

`docs/production_status.md` states that no prompt, placeholder, low-resolution preview,
damaged binary, or contact sheet may be counted as a completed production asset. This one was,
and nothing in the pipeline objected: it is a native 1254 × 1254 RGBA PNG with genuine
transparency, inside the locked bounds, and it passes the trait rig gate. Every gate the
repository had measures the container, not the picture.

## Why it mattered more than a rear aura would

Front auras are layer 15, above the character. A rear aura with the same flaw would sit behind
the body and read as background noise. This one covered the figure with opaque geometry on
every token it appeared on, at an 82% appearance rate before the category was reweighted — it
was the most visible thing in the collection.

It was caught by rendering a twelve-token sample sheet, not by any check.

## Effect on the ledger

`front_auras` returns to `pending_categories` at 1 of 2 registered. The remaining asset,
`aura_front_002_gold_light_pillars`, is a genuine soft light effect: 3,191 opaque pixels of
thin vertical pillars that read as light over the character rather than as shapes on top of it.
It stays registered.

## What replacing it needs

A rising flame is organic. `docs/qa/aura_ice_ring_procedural_rejected_2026-07-29.md` already
established that the procedural route fails for this class — a soft glow is fully described by
distance and falloff, but a flame's read comes from internal value structure that an outline
does not contain. DG-145 therefore needs an image generator driven by `prompts/12_auras.md`,
with the additional constraint that a foreground aura must stay legible as light: it composites
over the face.
