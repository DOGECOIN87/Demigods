# Legendary 1-of-1 prompts — ChatGPT variant

Seven prompts rewritten for ChatGPT's image generation. Same seven pieces as
`prompts/22_legendary_one_of_one.md`; different construction, because the two
generators fail in different ways.

## Why a second variant exists

`prompts/batch_legendary.md` works on Grok and does not work here. Measured
against that file: the actual subject line appears at **line 52 of 63**, after
six prohibition bullets and forty lines of canvas and rig constraints. Grok reads
the whole thing and complies. ChatGPT does not:

* **It rewrites the prompt before generating.** A long structured brief gets
  compressed, and compression keeps the opening and discards the tail — which is
  exactly where the subject was.
* **It weights the opening heavily.** Leading with prohibitions makes the
  prohibitions the subject.
* **It handles negation poorly.** "No text, no border, no watermark" raises the
  odds of text, borders and watermarks rather than lowering them.
* **Coordinates and alpha language are inert.** "X 233-1021", "orthographic",
  "zero yaw/pitch/roll", "genuine transparent alpha" cannot be acted on by a
  chat image model; they only consume attention.

So these prompts lead with the subject, describe rather than constrain, keep the
1-of-1 element in the first third, and end with one short avoid line.

## Known limitation: canvas size

ChatGPT cannot emit 1254 × 1254. Its image models produce fixed sizes —
1024×1024, 1024×1536, 1536×1024 (DALL·E 3: 1024×1024, 1792×1024, 1024×1792).
None is 1254 square.

Ask for a **square** image and you will get 1024 × 1024. That is smaller than the
locked canvas, and `prompts/00` forbids upscaling to reach 1254. For a modular
trait layer this is disqualifying. For a legendary it is a judgement call the
collection has not made: a flattened illustration upscaled 1024 → 1254 loses
real detail, and it will sit beside tokens that were rendered natively.

If a piece must come from ChatGPT, record the upscale in the manifest's
`postprocessing` rather than hiding it. The seven currently registered pieces are
native 1254 and need no such note.

---

## Legendary 01 — Sovereign of the Solar Court

```
A chibi sun deity standing at the centre of an open-air white-and-gold sky temple at high noon.

He wears a layered ceremonial sun-temple robe with a high pleated mantle, gold geometric borders and a radiant pectoral disc at the chest. Golden hair, a crown of gold solar spikes, calm steady expression, arms open at his sides.

Behind him a full solar corona ring blazes outward. Thin rays of light cross in FRONT of his shoulders and over the robe, and warm bounce light spills onto the pale marble platform at his feet. Wide blue sky and a distant floor of clouds beyond the temple.

Palette: white marble, warm gold, sunlit cream, amber, one deep-orange accent.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, standing with both feet on the ground, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## Legendary 02 — Oracle of the Waning Crescent

```
A chibi moon oracle standing on a moonlit pale-marble balcony at night, one hand raised to touch a glowing crescent.

She wears an asymmetric wrapped lunar robe in deep violet with silver-edged trim, a trailing sash, and a crescent clasp at the shoulder. Long silver-white hair, a gold crescent headpiece with a soft veil, serene half-lidded expression.

A large luminous crescent hovers beside her raised hand, and its silver light wraps around her arm and across the front of the robe. Behind her, arches open onto night mountains and a low field of stars; candlelight pools on the wet marble floor.

Palette: deep violet, silver, pale lilac, cool white, muted indigo shadow.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, standing with both feet on the ground, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## Legendary 03 — Heir of the Celestial Throne

```
A chibi young monarch seated on a great throne in a symmetrical white-marble celestial hall.

He wears formal celestial court dress: a deep navy half-cape mapped with gold constellations, white fur trim at the shoulders, gold embroidery, and a high collar that leaves the neck visible. Golden hair, a tall gold star-crown, composed expression, one hand resting on a slender star-tipped sceptre.

The star-mapped cape spills over the arm of the throne and pools across the polished floor, catching the light. Navy drapery and gold ornament line the hall behind him; a soft glowing circle marks the floor at the throne's foot.

Palette: white marble, deep navy, polished gold, one sapphire accent.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## Legendary 04 — Keeper of the Arcane Index

```
A chibi young scholar standing in a moonlit arcane library, holding an open book that glows from within.

He wears a layered scholar's robe in black and white with gold filigree and a high mantle collar. Dark tousled hair, bright teal eyes, absorbed concentration.

Several books orbit slowly around him in a ring — some passing BEHIND his body, others crossing in FRONT of the robe — their open pages lit from inside. Glowing sigil circles hang in the air around the ring. The nearest light falls on his face and hands. Tall bookcases recede on both sides, a single arched window behind, and a luminous circle marks the floor at his feet.

Palette: dark walnut, deep teal shadow, cyan and violet light, aged parchment, brass.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, standing with both feet on the ground, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## Legendary 05 — Warden of the Violet Void

```
A chibi void warden standing on a floating stone platform before a great circular violet void portal, holding a dark singularity above one open palm.

He wears a black layered void-mantle with a smooth high gorget at the shoulders, gold trim, and a ragged lower hem. Pale silver hair, a dark spiked crown, cold blue eyes, calm and unbothered.

A small violet singularity ringed with light hovers over his raised palm. Void flame rises from the platform, passing BEHIND his legs and in FRONT of the trailing hem, and the edges of his hem and hair dissolve into drifting embers. Broken rock fragments and slow smoke drift in the violet dark around him.

Palette: near-black violet, magenta, cold white core light, deep indigo.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, standing with both feet on the ground, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## Legendary 06 — Tempest Sovereign

```
A chibi storm sovereign standing on a high stone parapet in driving weather, lightning striking down into his raised open palm.

He wears bronze-plated storm armour over a teal underlayer, one heavy pauldron, and a short weather-worn cape. Pale silver hair, a slim circlet, bright blue eyes, braced and steady.

Forked lightning comes down out of the cloudbank into his upturned hand, and its branching arcs cross both BEHIND his body and in FRONT of the armour. The strike lights the stone at his feet and the underside of the cape. Dark storm clouds and a distant curtain of rain fill the sky behind him.

Palette: storm navy, teal, weathered bronze, pale electric blue, cold grey.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, standing with both feet on the ground, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## Legendary 07 — Verdant Archivist

```
A chibi plant archivist standing in an overgrown glass conservatory, holding an open book that glows green.

He wears an alchemist's layered robe in soft moss and cream with gold trim and a leaf-patterned mantle, a bandolier of glass vials across the chest, and sturdy boots. Green hair, a circlet of woven leaves, calm patient expression.

Living vines grow up from the floor and wind around one arm, passing BEHIND his torso and over the forearm. Two open vials release glowing spores that drift across the whole scene. Hanging planters and ivy trail from a glass roof, daylight filters green through the leaves, and a luminous circle marks the floor at his feet.

Palette: olive and moss green, warm brown leather, brass, cream, amber glass.

Style: premium anime chibi fantasy game art. Large head, small body, cute proportions. Front-facing and symmetrical, standing with both feet on the ground, the whole figure visible from crown to feet. Soft key light from the upper left, form shadows toward the lower right, a subtle cool rim on the right. Clean cel shading, crisp edges, rich painterly detail, readable at small size.

Square image that fills the entire frame. One character only. Clean artwork with no lettering anywhere.
```

## If a piece still comes back wrong

In order of what usually fixes it:

1. **Ask for one change at a time.** ChatGPT edits conversationally. "Keep everything, but make the lightning branch in front of the cape as well as behind it" works better than re-pasting a corrected prompt.
2. **Restate the 1-of-1 element on its own.** It is the paragraph that matters and the one most often dropped.
3. **Drop the palette line** if the colours are being followed at the cost of the subject.
4. **Never add "do not" lists.** If text keeps appearing, say "clean artwork, unlettered surfaces" rather than "no text".
