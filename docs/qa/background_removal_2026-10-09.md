# Background removal — rare 1-of-1 set (2026-10-09)

The blur/depth-treated review outputs were removed. Every rare 1-of-1 illustration is
instead cut out to a transparent RGBA PNG at its native size in
`images/variations/cutouts_2026-10-09/`, one image at a time. Nothing is batch
processed: each image gets its own review, its own written notes and its own
hand-placed corrections in `images/variations/cutouts_2026-10-09/recipes/NAME.json`.

The 77 sources are the 72 PNGs in `images/variations/complete_72/`, the four
1024 × 1024 WebPs in `images/variations/nature/` and the JPEG in
`images/variations/references/`.

## What is kept and what is removed

**Keep**

- The character: body, hair, every worn item (crowns, hair ornaments, earrings,
  capes, ribbons, tassels, chains, boots), including parts that trail far from the body.
- Everything the character holds, and everything attached to a held item: staffs,
  weapons, books, lanterns, banners hanging from a staff, charms and tassels hanging
  from a brush or staff, chains of a pocket watch.
- Magic the character is actively producing or controlling: ribbons of light flowing
  from the hands, a crystal floating over the palm, a crystal ball between the hands.
- Foreground items: objects and plants that sit in front of the character's plane —
  lower in the frame than the feet, or overlapping the bottom frame edge, usually
  depth-blurred. Props (books, chests, lanterns, scrolls, tools, rope coils), plants
  and flowers, crystals, shells, pearls, coral, feathers lying in front of the feet.
  Keep their blur: use feathered edges that match how soft they are.

**Remove**

- Sky, clouds, sun, moon, stars, weather, lightning, ambient sparkles, glows and auras
  behind the character.
- Architecture, scenery, furniture and every prop at or behind the feet line.
- Ground and terrain everywhere, including in the foreground corners: floors, water,
  ripples, reflections, cast shadows, snow drifts, sand, rocks and stones.
- Effects that are not the character's own held magic (environmental lightning arcs,
  falling petals, floating bubbles, drifting leaves).
- Background visible through gaps: inside loops of a ribbon or ring, between tassels,
  between hair strands, between lace holes, between foreground leaves.

When an element is ambiguous, decide by the rule above, write the decision into the
recipe notes with its coordinates, and stay consistent with the decisions recorded in
earlier recipes.

## Per-image procedure

Set up the environment once per shell:

```bash
source "$SCRATCHPAD/env"   # sets CUTOUT_MODELS and CUTOUT_CACHE
```

1. **Look at the source** at full size. List every element: character, held items,
   attached items, foreground items, and the background elements to remove.
2. **Compare the two model mattes** — `python3 scripts/cutout_review.py compare NAME`
   shows source | isnet-anime | BiRefNet over magenta. BiRefNet is usually the cleaner
   start; isnet sometimes keeps thin attached items BiRefNet drops.
3. **Zoom everywhere it matters** with
   `python3 scripts/cutout_review.py grid NAME --crop X0 Y0 X1 Y1 [--step 10] [--matte birefnet|isnet|result]`:
   every held item end to end, weapon and staff tips, hanging charms and tassels, hair
   ends, cape tatters, the feet, and all four bottom/side edges for foreground items.
   Grid labels are source pixel coordinates.
4. **Write the recipe** `recipes/NAME.json`:

   ```json
   {
    "notes": {
     "keep": ["...every kept element, foreground items prefixed FOREGROUND: with coordinates"],
     "remove": ["...every removed background element"],
     "fixes": ["...each correction with its coordinates and why"]
    },
    "base": "birefnet",
    "ops": []
   }
   ```

   Keep `"source"` if the stub has one (the WebPs and the JPEG).
5. **Preview each fix** with `render NAME --preview --crop ...` and read the review sheet
   (source | over magenta | over dark grey). Iterate until each region is right.
6. **Final render** with `render NAME` (no `--preview`), then read the full review sheet
   and confirm: nothing of the character, held items or foreground items is missing,
   no background remains (check over both magenta and dark grey), edges are clean.

## Recipe operations

Polygons are lists of `[x, y]` source-pixel points; `polys` is a list of polygons.

| op | effect |
|---|---|
| `"base"` | starting matte: `birefnet`, `isnet`, `max` (union) or `min` (intersection) |
| `"levels": [lo, hi]` | contrast stretch of the base matte (default `[8, 247]`) |
| `use` | inside `polys`, take another matte (`model`: `isnet`, `birefnet` or `min`; optional `levels`; `"combine": "max"` to add without weakening) |
| `keep` | inside `polys`, force fully opaque; `"feather": σ` gives a soft edge for blurred foreground items |
| `remove` | inside `polys`, force fully transparent |
| `grabcut` | edge-snap inside `box` `[x0,y0,x1,y1]`: `fg` drawn shape (result never grows past it), optional `sure_fg`, `bg`, `feather`. Fails when the item and what is behind it share colours — then trace with `keep` instead |
| `drop_dark` | inside `polys`, fade out pixels darker than `ramp: [d0, d1]` mean luminance (sky through bright ribbons, floor around white feathers) |
| `drop_warm` | inside `polys`, fade out pixels whose red-minus-blue exceeds `ramp: [w0, w1]` (beige or wooden background around blue or white items); `"invert": true` drops cool pixels instead (water or sky around warm items) |
| `key_lum` | inside `polys`, add opacity from mean luminance `ramp: [k0, k1]` (bright metal or crystal on a dark sky); isolated stars are then dropped by `min_island` |
| `drop_pale` | inside `polys`, fade out pixels that are both bright (mean above `lum`, default 110) and neutral or greenish (G minus R above `g_r`, default -12): pale haze and sky glow around brown or gold items |
| `key_blur` | inside `polys`, add opacity where the image is depth-blurred: local sharpness below `ramp: [b0, b1]` (default `[10, 22]`) is kept. Separates blurred foreground plants and props from the sharp ground and water behind them |
| `drop_sharp` | inside `polys`, fade out in-focus pixels (same sharpness measure and `ramp` as `key_blur`): trims sharp background showing inside a hand-traced blurred foreground item |
| `key_rb` | inside `polys`, add opacity from red-minus-blue `ramp` (warm items on cool water/sky); `"invert": true` for cool-on-warm |
| `remove_color` | inside `polys` (optional), drop pixels within `tol` of `rgb` |
| `fill_holes` | close enclosed transparent holes up to `max_area` px |
| `"min_island"` | drop disconnected specks smaller than this (default 150) |

Ops run in order, so later ops win. A typical image needs zero to four ops.

## Recorded decisions

The notes in each recipe are the record of what was judged foreground, held, attached
or background for that image, and where each correction was placed.
