# QA — Interim hair recolours DG-169 to DG-175 (2026-07-27)

Seven recolours registered, taking `hair_back` from 1 to 8 assets. **Interim**: colour varies, silhouette does not.

## Why

A 50-token random sample across a full 777 run showed **identical hair on every token**. With one registered hair asset, hair was the most repetitive element in the collection — more visible than the five cycling robe colours, because it sits at the top of the figure where the eye lands first.

## Method

`scripts/build_hair_recolour.py` remaps the registered DG-031 silver layer. Luminance is normalised across the source's measured opaque range — 78 to 185, not 0 to 255, so the midtones are not crushed — then remapped through a three-stop palette.

Every painted detail survives: strand separation, wave structure, and the upper-left key light are all carried by the luminance channel, so only hue and value shift. Alpha is copied through untouched, which is why all seven produce gate results identical to the source.

| Check | Result |
|---|---|
| Rig gate `--trait --max-width-ratio 1.35` | 8/8 pass |
| Alpha bbox vs source | identical on all seven |
| sRGB ICC profile | present, 588 bytes, inherited through the channel ops |

The profile inheritance was verified rather than assumed — `embed_srgb_profile.py` reported all eight already tagged, and a direct read confirmed each carries the same 588-byte profile as every other registered asset.

## Scope and limits

**Colour varies, silhouette does not.** All seven share DG-031's exact shape, so the collection now has seven hair colours and one hair cut. That is a real improvement over one colour and one cut, and it is not the same as having eight hairstyles.

This does **not** contradict the earlier no-recolouring finding. That finding — recorded under the hair-back family in the backlog — says the eight `HAIR` sheet cells are distinct cuts that must each be rendered natively, and it still stands. DG-029 to DG-036 remain `pending` and are not satisfied by these. Numbering starts at `hair_back_011` so 001–008 stay reserved for the painted cuts.

## Effect on the collection

```
combination space   4800 -> 38400
hair_back           1 -> 8 registered
```

Preflight passes. The remaining visible repetition is now the face: `eyes`, `eyebrows` and `mouths` are all at zero, so every token has an identical expression.
