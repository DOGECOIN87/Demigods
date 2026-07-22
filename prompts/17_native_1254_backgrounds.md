# Prompt — Native 1254 Background Production

Create exactly one Demigods background per request. Attach only the corresponding file from the eight-item set in `images/background_candidates/` as the visual reference.

## Shared output contract

```text
Create exactly one full-bleed Demigods background using the attached image only as the visual-direction and composition reference.

OUTPUT:
- render natively at exactly 1254 × 1254 pixels
- PNG in sRGB, RGB or fully opaque RGBA
- fill every canvas pixel; no transparent pixels or empty border
- exactly one background scene only
- no character, creature, silhouette, foreground avatar, UI, frame, caption, watermark, signature, or contact-sheet layout
- no readable letters, words, numbers, runes, pseudo-writing, or typographic symbols
- preserve a clear central staging region for the front-facing Demigods avatar within X 233–1021 and Y 129–1139
- harmonize the dominant scene lighting with an upper-left key direction and lower-right form shadows
- premium anime-fantasy game-art finish, crisp detail, controlled depth, coherent perspective, and clean edges

REFERENCE HANDLING:
- preserve the reference's recognizable environment, palette, architectural rhythm, mood, and central composition
- rebuild natively; do not resize, upscale, trace, tile, extend, or patch the 1024 × 1024 JPEG
- replace any letters or rune-like markings with nonlinguistic ornamental geometry
- do not add unrelated objects or merge elements from other background references

Return one PNG only with no explanatory text.
```

## Background 001 — Celestial throne hall

- Reference: `background_001_celestial_throne_hall_reference.jpg`
- Preserve: symmetrical white-marble columns, deep navy drapery, gold celestial ornament, distant central throne, blue carpet, grand palace depth.
- Remove: compass letters and all readable glyphs.
- Production filename: `background_001_celestial_throne_hall.png`

## Background 002 — Violet gothic sanctum

- Reference: `background_002_violet_gothic_sanctum_reference.jpg`
- Preserve: towering gothic nave, violet stained glass, dark stone, candlelit central altar, solemn symmetrical composition.
- Remove: religious text, letters, and readable symbols; retain only generic fantasy ornament.
- Production filename: `background_002_violet_gothic_sanctum.png`

## Background 003 — Arcane library

- Reference: `background_003_arcane_library_reference.jpg`
- Preserve: towering bookcases, cool moonlit arched window, suspended cyan magic lights, layered books and desks, luminous floor-circle composition.
- Replace: readable runes or pseudo-writing with abstract concentric geometry.
- Production filename: `background_003_arcane_library.png`

## Background 004 — Crescent-star dreamscape

- Reference: `background_004_crescent_star_dreamscape_reference.jpg`
- Preserve: navy-violet sky, soft layered clouds, luminous crescent, hanging gold stars, central floating celestial platform, whimsical premium fantasy mood.
- Avoid: text, readable symbols, characters, faces, or added scenery.
- Production filename: `background_004_crescent_star_dreamscape.png`

## Background 005 — Solar sky temple

- Reference: `background_005_solar_sky_temple_reference.jpg`
- Preserve: white-and-gold open-air temple arches, bright blue sky, soft clouds, central radiant compass-star motif, luminous ceremonial platform, clean celestial atmosphere.
- Replace: any readable markings with abstract nonlinguistic ornament.
- Production filename: `background_005_solar_sky_temple.png`

## Background 006 — Moonlit marble balcony

- Reference: `background_006_moonlit_marble_balcony_reference.jpg`
- Preserve: symmetrical pale-marble arches and columns, moonlit mountain horizon, starry deep-blue sky, balustrade, cool floor shadows, quiet nocturnal atmosphere.
- Avoid: characters, furniture, text, extra celestial bodies, or foreground props.
- Production filename: `background_006_moonlit_marble_balcony.png`

## Background 007 — Golden celestial gateway

- Reference: `background_007_golden_celestial_gateway_reference.jpg`
- Preserve: layered white-stone arches, radiant gold portal light, central star emblem, shallow ceremonial stairs, flanking dark-green plants, warm sacred fantasy mood.
- Replace: rune-like markings with abstract ornamental geometry.
- Production filename: `background_007_golden_celestial_gateway.png`

## Background 008 — Violet void portal

- Reference: `background_008_violet_void_portal_reference.jpg`
- Preserve: circular violet energy portal, dark floating stone platform, levitating black rock fragments, purple crystals, smoky void atmosphere, centered dramatic composition.
- Replace: ring glyphs and pseudo-writing with nonlinguistic geometric filigree.
- Production filename: `background_008_violet_void_portal.png`

## Acceptance gate

Run each result through `scripts/validate_assets.py` under `assets/backgrounds/` only after manual review. A file is production-ready only when it is natively 1254 × 1254, fully opaque, visually approved, correctly named, and registered with its exact SHA-256. Produce and approve backgrounds sequentially from 001 through 008.
