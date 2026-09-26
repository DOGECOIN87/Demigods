# Demigods — prompts for the missing 1-of-1s

Prepared 2026-09-26. Twenty-one prompts that complete the 1-of-1 set at 77 pieces, plus seven reserves.

## Where the 77 stand

| Nos. | Pieces | Status |
|---|---|---|
| 001–007 | 7 legendaries | registered in `assets/legendary/` |
| 008–056 | 49 one-of-ones | received, in `images/one_of_ones/` |
| 057–077 | 21 in this pack | to generate |

This count puts the seven legendaries inside the 77 (7 + 49 + 21). If the 77 is meant to be on top of the legendaries, 28 are missing: also generate the seven reserves at the end of this file, as 078–084.

The four nature variations in `images/variations/` are not counted. They are outfit variations of legendary 007, not new characters.

## How the 21 were chosen

They fill gaps instead of repeating the existing 56. That set leans on night scenes, purple and blue palettes, knights, and star, moon and void themes. These favor daylight and warm or green palettes, and add:

- elements the set lacks: wind, stone, rainbow, hearth
- crafts: sculptor, painter, toymaker, confectioner, glass
- mythic figures not yet present: kitsune, valkyrie, raven seer, cat temple guardian, feathered serpent, djinn, harvest, pomegranate, owl

Every concept differs from all 49 names in `images/one_of_ones/` and from the seven legendaries.

## Generating them

Each prompt is complete. Paste one prompt, get one image. The subject comes first and the constraints last, which is the order `prompts/23_legendary_chatgpt.md` found image models follow best. The name and number stay out of the prompt text so they cannot be painted into the picture.

- **Tool and size.** Use the same generator as the 49, which all came out as native 1254 × 1254 PNGs. If a tool returns another square size, keep it as delivered and note it. Do not upscale (`prompts/00_locked_master_specification.md`).
- **Optional style reference.** Attach one existing piece to hold the look together, and add this line to the prompt: *Use the attached image only as a style reference for rendering, proportions and finish; design a completely new character, costume and setting.* Good choices:
  - daylight: `images/one_of_ones/one_of_one_048_falconer.png`
  - warm interior: `images/one_of_ones/one_of_one_052_alchemist.png`
  - dusk or night: `images/one_of_ones/one_of_one_045_lantern_festival.png`
- **Check every result** before keeping it:
  - exactly one character, with head and boots inside the frame
  - the signature element listed with the prompt is clearly visible
  - no text, letters or watermark
  - not a near-copy of an existing piece

  Keep one approved image per number.
- **Filing.** Save each image under its "Save as" name, or upload it anywhere in `images/` and have it renamed. Then run:

  ```bash
  python scripts/validate_legendary.py --dir images/one_of_ones --expect <count>
  ```

  It checks decode, PNG format, 1254 × 1254, full opacity, and that no two pieces share a digest.

### Batch run with an agent

For an agent that can make many images in one run, attach this file and send:

```text
Attached is a prompt pack for the Demigods collection. Generate every prompt in the section "Missing 1-of-1s (057–077)", 21 images in total, one separate image per prompt, using each prompt's text exactly as written. Never combine images into a grid, sheet or collage, and never add a name, number or caption to an image.

Make each image a square PNG, 1254 x 1254 if your image tool supports that size; otherwise use its native square size and do not upscale. Save each image under the exact file name given in its "Save as" line and return all 21 files.

Before returning an image, check it: exactly one character; head and boots inside the frame; the listed signature element clearly visible; no text, letters or watermark. Regenerate any image that fails a check.
```

## Missing 1-of-1s (057–077)

### 057 — Kitsune Shrine Keeper

Save as `images/one_of_ones/one_of_one_057_kitsune_shrine_keeper.png` · Signature element: blue foxfire orb and three fox tails.

```text
A chibi fox-spirit shrine keeper with soft white hair, tall white fox ears tipped in vermilion, three fluffy white fox tails fanned out behind, and amber-gold eyes, standing in the middle of a long tunnel of vermilion torii gates on a hillside shrine at golden hour. White and vermilion layered shrine robes with wide sleeves, gold flame-and-fox embroidery, a gold-tasseled red cord belt and lacquered black-and-gold boots. One hand holds a slender vermilion staff hung with white paper streamers; the other palm is raised with a floating orb of blue-teal foxfire. Stone fox guardian statues flank the path, red maple leaves drift through warm sunset light, and small foxfire wisps float between the gates. Palette: vermilion, white and gold with teal-blue foxfire accents.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 058 — Honey Warden

Save as `images/one_of_ones/one_of_one_058_honey_warden.png` · Signature element: honey-dipper scepter and orbiting golden bees.

```text
A chibi beekeeper-sage with tousled black hair tipped in honey gold, a delicate gold circlet of hexagons and honey-brown eyes, standing on a hexagon-tiled amber floor inside a sunlit honeycomb palace. A cream and honey-gold layered coat with hexagonal honeycomb quilting, a translucent iridescent bee-wing capelet, a black-and-gold striped sash, gold hexagon brooches set with amber, and honey-brown boots. One hand holds a golden honey-dipper scepter dripping glowing honey, while a few round, friendly golden bees circle in a gentle spiral. Towering walls of glowing honeycomb, slow drips of honey, a wildflower meadow seen through tall arched windows, warm afternoon sunbeams and floating pollen sparkles. Palette: honey amber, cream and gold with soft black accents.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 059 — Windcaller

Save as `images/one_of_ones/one_of_one_059_windcaller.png` · Signature element: crystal pinwheel staff and spiraling wind ribbons.

```text
A chibi wind sorcerer with wind-swept mint-green hair and bright sky-blue eyes, standing on a white stone terrace at the edge of a floating island high above the clouds. Flowing white and sky-blue layered robes with long ribbon sashes streaming sideways in the wind, gold spiral-and-feather embroidery, a short aqua capelet, a gold circlet with small wing ornaments, and light boots with gold wing clasps. One hand holds a tall pale-gold staff topped with a spinning pinwheel of crystal blades; visible ribbons of wind spiral around the figure, carrying leaves and petals. Other floating islands with white windmills and waterfalls spilling into the clouds, and colorful kites in a clear blue midday sky. Palette: sky blue, white and mint with gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 060 — Marble Sculptor

Save as `images/one_of_ones/one_of_one_060_marble_sculptor.png` · Signature element: colossal half-carved marble horse and floating marble chips.

```text
A chibi master sculptor with short ash-brown hair tied back with a cloth band and hazel-green eyes, standing in a sunlit open-air marble atelier carved into a white quarry. A cream linen tunic with rolled sleeves under a terracotta leather apron embossed with gold acanthus leaves, a sage-green sash, a tool belt of small chisels and brushes, and dusty leather boots, with a faint dusting of marble powder on the sleeves. Holds a gold-inlaid mallet and chisel as glittering marble chips float in the air; behind the character a colossal half-carved marble horse rears out of raw quarry stone. Scaffolding, rope pulleys, carved capitals and busts on plinths, cypress trees under a deep Mediterranean-blue sky, warm afternoon light and sparkling dust motes. Palette: white marble, terracotta and sage green with gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 061 — Rainbow Herald

Save as `images/one_of_ones/one_of_one_061_rainbow_herald.png` · Signature element: rainbow pouring from a crystal pitcher.

```text
A chibi rainbow herald with long pastel-lavender hair that shimmers with a rainbow sheen and prismatic violet eyes, standing on a wet, mirror-like stone ledge beside a great waterfall just after a rain shower. Layered white chiffon robes whose hems shift through soft pastel rainbow gradients, a gold filigree bodice set with prism-cut crystals, a sheer iridescent shawl and gold sandal-boots. Holds a crystal pitcher tilted so the water pouring from it turns into a bright rainbow that arcs over the character's head. Cliffs of waterfalls, drifting mist, a double rainbow across a clearing sky, sunlight breaking through the clouds and sparkling droplets everywhere. Palette: white and pastel rainbow with gold under a fresh blue sky.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 062 — Hearthkeeper

Save as `images/one_of_ones/one_of_one_062_hearthkeeper.png` · Signature element: living flame in a bronze lantern.

```text
A chibi hearthkeeper with soft wavy auburn hair and warm copper eyes, standing on warm flagstones in front of a great stone hearth in a cozy timber-beamed hall. A cream knitted shawl over a russet-orange wool coat-dress with gold ember-pattern embroidery, a deep brown corset belt with copper buckles, small herb pouches and a copper ladle at the belt, and fur-lined brown boots. Holds a round bronze lantern cradling a gentle living flame, with sparks rising from it like tiny stars. A crackling fire with a copper kettle, hanging dried herbs and garlands, stacked firewood, knitted blankets, candlelight, and frosted windows with snow falling outside. Palette: russet orange, cream and deep brown with copper and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 063 — Harvest Sovereign

Save as `images/one_of_ones/one_of_one_063_harvest_sovereign.png` · Signature element: gilded wheat-sheaf scepter and overflowing harvest horn.

```text
A chibi harvest sovereign with long wheat-blond braids and olive-green eyes, standing on a round golden stone threshing floor surrounded by rolling fields of ripe wheat at sunset. Layered robes of wheat gold and deep olive embroidered with grain stalks, a woven gold crown of wheat ears and small red poppies, amber gem clasps, a sash of autumn leaves, and sturdy tan leather boots. Holds a tall scepter made from a gilded sheaf of wheat; a woven horn-shaped basket overflowing with apples, grapes, pumpkins and bread rests beside the boots. Golden fields to the horizon, bound sheaves, a distant windmill, fruit-heavy orchard trees, a huge warm orange sun low in the sky, and drifting golden chaff sparkles. Palette: wheat gold, olive green and sunset orange with poppy-red accents.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 064 — Pomegranate Princess

Save as `images/one_of_ones/one_of_one_064_pomegranate_princess.png` · Signature element: split spring/underworld setting and glowing pomegranate.

```text
A chibi spring-and-underworld princess with long dark plum hair woven with pale pink blossoms and ruby-red eyes, standing exactly on the threshold where a blooming spring garden meets a candlelit underworld hall. An asymmetric gown split down the middle: one half soft blossom pink and spring green with embroidered flowers, the other half deep plum and black velvet with gold filigree and garnet gems; a flower crown whose blossoms turn to dark crystal on one side, and dainty gold boots. Holds an open, glowing pomegranate in both hands, its seeds shining like rubies. Behind one side, a sunlit meadow of spring blossoms and butterflies; behind the other, a dark hall of violet candles beside a gentle river of starlight; petals drift across the dividing line. Palette: plum, blossom pink, spring green and ruby with gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 065 — Valkyrie

Save as `images/one_of_ones/one_of_one_065_valkyrie.png` · Signature element: wings of golden light and knotwork sun shield.

```text
A chibi valkyrie with long platinum-blonde braids and steel-blue eyes, wearing a silver winged helmet, standing in a great golden longhall of carved wood. Burnished silver and bronze scale armor over layered crimson skirts, a white wolf-fur mantle, engraved knotwork and garnet studs, and fur-trimmed boots. Large wings of warm golden light unfold from the shoulders; one hand rests on a round bronze-rimmed shield painted with a gold knotwork sun, and the other is raised in salute. Carved dragon-prow pillars, rows of round painted shields along the walls, long tables, braziers and warm torchlight, with golden dust drifting in shafts of light from high windows. Palette: bronze, crimson and silver with warm gold and white.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 066 — Raven Seer

Save as `images/one_of_ones/one_of_one_066_raven_seer.png` · Signature element: two ravens and orbiting glowing knotwork stones.

```text
A chibi rune seer with shaggy teal-black hair with one silver streak and glowing pale-teal eyes, standing on a mossy stone circle among the colossal roots of an ancient world tree. A hooded charcoal cloak lined with deep forest green, silver knotwork clasps, a layered leather-and-wool tunic, silver amulets and wrapped boots. Holds a gnarled staff wound with silver wire; two sleek black ravens perch on the staff and on one shoulder, and smooth stones carved with glowing teal knotwork patterns orbit slowly around the figure. Enormous twisting roots rising into mist, a softly glowing spring at the base of the tree, hanging moss, drifting teal motes, and cool twilight pierced by pale shafts of light. Palette: charcoal, forest green and glowing teal with silver.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 067 — Cat Temple Guardian

Save as `images/one_of_ones/one_of_one_067_cat_temple_guardian.png` · Signature element: black cat companion and lapis moon-disc staff.

```text
A chibi temple guardian with a sleek black bob, black cat ears and gold-rimmed green cat-like eyes, standing on a polished sandstone floor inside a sunlit riverside temple at golden hour. Crisp white pleated linen robes, a broad jeweled collar of gold, lapis lazuli and turquoise, gold arm cuffs, a lapis-blue sash and gold sandal-boots. Holds a slender gold staff topped with a lapis moon disc, while a sleek black cat with a gold collar sits at the character's feet looking up. Tall lotus-capital columns painted with lapis-and-gold lotus and wing patterns, rows of seated cat statues, palm trees, and a wide river glittering through the colonnade in warm low sun with floating gold dust. Palette: lapis blue, gold, linen white and turquoise.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 068 — Feathered Serpent Priest

Save as `images/one_of_ones/one_of_one_068_feathered_serpent_priest.png` · Signature element: luminous feathered serpent coiling around the staff.

```text
A chibi sky-serpent priest with long dark-brown hair in a high ponytail and dark golden-brown eyes, wearing a radiant headdress of long emerald and turquoise plumes, standing on the top platform of a jungle step pyramid in the morning mist. Layered garments of jade green and cream woven with gold geometric step patterns, a turquoise mosaic pectoral, jade bead necklaces and ear ornaments, gold wrist cuffs, a short feathered cape and sandal-boots with jade beads. Holds a gold staff around which a small luminous feathered serpent coils, its emerald-and-turquoise feathers and gold scales glowing. Other pyramids rise above a lush rainforest canopy with waterfalls and scarlet macaws, sun rays slant through the mist, and feather-light sparkles drift in the air. Palette: jade, turquoise and gold with terracotta and cream.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 069 — Djinn Lamp Keeper

Save as `images/one_of_ones/one_of_one_069_djinn_lamp_keeper.png` · Signature element: star-filled smoke rising from a golden lamp; hovering carpet.

```text
A chibi lamp keeper with wavy midnight-blue hair and bright gold eyes, standing on a richly patterned flying carpet that hovers just above a palace terrace at twilight. A turquoise and magenta silk coat with gold arabesque embroidery, a jeweled sash, billowing cream trousers, a small gold-trimmed turban with a large sapphire and a plume, and curled gold-tipped slippers. Holds a polished golden oil lamp from which a swirl of glowing blue smoke rises and spirals overhead, filled with tiny stars. Onion domes and slender towers, turquoise tiled arches, hanging lanterns, a garden of palms and fountains below, and a twilight sky shading from coral to violet with the first stars. Palette: turquoise, magenta and gold against twilight violet.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 070 — Chromatic Painter

Save as `images/one_of_ones/one_of_one_070_chromatic_painter.png` · Signature element: brushstroke of living color turning into flowers and birds.

```text
A chibi master painter with messy emerald-green hair flecked with bright paint and vivid turquoise eyes, standing on a paint-splashed wooden floor in a sun-flooded atelier with tall arched windows. A cream smock-coat splashed with color over a navy waistcoat with gold buttons, a floppy deep-red beret, a rainbow-striped scarf and paint-spattered boots. Holds a wooden palette of glowing paints in one hand and sweeps a giant brush with the other, leaving a floating ribbon of living color that turns into painted flowers and birds in mid-air. Easels and canvases of colorful landscapes, jars of brushes, pigment bottles, a skylight, and afternoon sunlight with floating paint droplets like colorful sparkles. Palette: cream and navy with vivid rainbow paint and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 071 — Wind-Up Toymaker

Save as `images/one_of_ones/one_of_one_071_wind_up_toymaker.png` · Signature element: golden carousel music box and fluttering wind-up birds.

```text
A chibi toymaker with fluffy ginger hair, round gold spectacles pushed up on the head and bright blue eyes, standing on the polished wooden floor of a cozy, magical toy workshop. A burgundy waistcoat with brass buttons over a cream shirt with rolled sleeves, a dark green work apron full of tiny tools, a patterned bow tie, striped stockings and buckled brown boots. Cradles an open golden music box with a tiny spinning carousel inside, while little wind-up tin birds flutter around the character. Shelves crowded with wooden soldiers, marionettes, rocking horses and spinning tops, a toy train circling the floor on its track, warm lamplight, a round window, and floating gears and sawdust sparkles. Palette: burgundy, forest green and cream with brass and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 072 — Confectioner

Save as `images/one_of_ones/one_of_one_072_confectioner.png` · Signature element: whisk-scepter spinning ribbons of spun sugar.

```text
A chibi royal confectioner with fluffy strawberry-pink hair and sweet mint-green eyes, standing on a glossy checkerboard floor of pink and cream marble inside a whimsical candy palace. A frilly cream and pastel-pink pastry-chef coat with ruffles like piped frosting, mint-green bows, macaron-shaped gold buttons, a lace apron, a small tilted chef's toque topped with a strawberry, and pink ribbon boots. Holds a golden whisk-scepter that swirls ribbons of glittering spun sugar, and balances a tiny tiered cake crowned with strawberries in the other hand. Towers of layered cakes, macaron staircases, lollipop trees, candy-cane columns, a chocolate fountain, and floating sprinkles and sugar-crystal sparkles in soft bright daylight. Palette: pastel pink, mint and cream with soft gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 073 — Hedge Witch

Save as `images/one_of_ones/one_of_one_073_hedge_witch.png` · Signature element: cauldron steam forming glowing leaves; floating broom.

```text
A chibi hedge witch with long wavy deep-violet hair and warm golden eyes, wearing a tall, crooked, wide-brimmed witch hat, standing on the flagstone floor of a cozy herb-filled cottage. A layered plum and moss-green coat-dress with patched pockets, a shawl embroidered with stars and leaves, dangling copper charms, and laced boots. Stirs a bubbling copper cauldron with a long wooden spoon; its green-gold steam curls into swirling glowing leaves, and a broom floats upright nearby. Bundles of dried herbs hanging from the beams, shelves of jars and candles, a round window onto a flower garden, a sleepy toad on a stool, and warm golden light. Palette: plum and moss green with copper and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 074 — Stained Glass Artisan

Save as `images/one_of_ones/one_of_one_074_stained_glass_artisan.png` · Signature element: rose-window medallion casting jewel-colored beams.

```text
A chibi stained-glass artisan with shoulder-length copper-red hair and luminous sapphire eyes, standing on a stone floor dappled with pools of colored light inside a soaring glass hall. A deep navy work coat trimmed with ruby, emerald and sapphire glass beads, a leather apron, gold filigree bracers, a gold collar set with colored glass, and fingerless gloves. Holds up a glowing circular stained-glass medallion in a rose-window pattern; beams of ruby, emerald and sapphire light shine through it onto the floor and across the character's face. Towering geometric and floral stained-glass windows, workbenches with sheets of colored glass and tools, a kiln glowing orange, colored light shafts and floating glass-dust sparkles. Palette: ruby, emerald and sapphire jewel tones on dark stone, with gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 075 — Autumn Stag Prince

Save as `images/one_of_ones/one_of_one_075_autumn_stag_prince.png` · Signature element: white stag companion and glowing amber maple leaf.

```text
A chibi forest prince with tousled chestnut hair, small elegant golden antlers and warm amber eyes, standing on a mossy stone path in a blazing autumn maple forest. A burnt-orange and cream layered hunting coat with gold oak-and-maple leaf embroidery, a crimson leaf-shaped mantle, brown leather belts with amber stones, a thin gold circlet woven through the antlers, and tall brown boots. A majestic white stag with gold-tipped antlers stands close behind, and the character rests one hand on its neck while the other holds a single glowing amber maple leaf. Towering maples in crimson, orange and gold, falling leaves swirling in sun shafts, a stream with stepping stones, ferns and mushrooms. Palette: burnt orange, crimson and cream with gold and forest brown.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 076 — Wandering Bard

Save as `images/one_of_ones/one_of_one_076_wandering_bard.png` · Signature element: gilded lute with ribbons of golden light.

```text
A chibi wandering bard with wavy sandy-brown hair under a jaunty feathered cap and bright green eyes, standing on the cobblestones of a lively old town square at dusk. A forest-green doublet with gold embroidery, a burgundy half-cape fastened with a gold lyre brooch, cream puffed sleeves and soft brown boots. Plays a gilded lute; ribbons of glowing golden light flow from its strings and swirl around the square. Half-timbered houses with flower boxes, strings of bunting and warm lanterns, a stone fountain, a peach-and-violet sunset sky and floating firefly sparkles. Palette: forest green, burgundy and cream with warm gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### 077 — Owl Sage

Save as `images/one_of_ones/one_of_one_077_owl_sage.png` · Signature element: silver owl perched on the raised forearm.

```text
A chibi wisdom sage with short silver-gray hair crowned with a laurel of olive leaves and sharp gray-blue eyes, standing on the sunlit marble terrace of a hilltop temple above an olive grove and the sea. Ivory and deep olive layered robes with a gold meander-pattern border, a bronze owl-feather mantle, bronze arm guards and laced sandal-boots. A wise silver-white owl with golden eyes perches on the character's raised forearm; the other hand holds a long olive-wood staff topped with a bronze owl-wing crest. White columns, olive trees, a view of a turquoise bay with distant islands, scrolls on a stone bench, bright clear morning light and floating olive leaves. Palette: ivory, olive and bronze with turquoise sea and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

## Reserves (R1–R7)

Use these as replacements if a concept above does not work out. Use all seven if the 77 is counted on top of the legendaries; they then take numbers 078–084, as their "Save as" lines show.

### R1 — Tea Master

Save as `images/one_of_ones/one_of_one_078_tea_master.png` · Signature element: steam rising from the teapot in the shape of a flying crane.

```text
A chibi tea master with long straight black hair held by a jade hairpin and calm celadon-green eyes, standing on the polished wooden deck of a mountainside tea pavilion at dawn. Layered robes in celadon green and cream with fine gold tea-leaf embroidery, a wide deep-brown sash, jade toggles and soft cloth boots. Holds a small celadon teapot in both hands; the rising steam curls into the shape of a flying crane. Terraced tea fields on misty mountain slopes, pine trees, paper lanterns, a low table set with tea bowls, and soft pink-gold sunrise light. Palette: celadon green, cream and wood brown with soft gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### R2 — Sky Balloon Aeronaut

Save as `images/one_of_ones/one_of_one_079_sky_balloon_aeronaut.png` · Signature element: compass projecting a golden path into the sky.

```text
A chibi aeronaut with short wind-tossed tangerine hair and teal eyes, standing on a wooden launch platform on a cliff at sunrise as patchwork hot-air balloons rise all around. A teal aviator coat with brass buttons and gold compass-rose embroidery, a long cream scarf streaming in the wind, leather gloves, a leather flight cap and sturdy boots. Holds a glowing brass compass whose needle projects a golden path of light into the sky. Dozens of colorful patchwork balloons, a valley of green fields and winding rivers far below, birds, and a peach-and-gold sunrise sky. Palette: teal and tangerine with cream and brass.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### R3 — Lighthouse Keeper

Save as `images/one_of_ones/one_of_one_080_lighthouse_keeper.png` · Signature element: lantern beam sweeping across the sea.

```text
A chibi lighthouse keeper with curly navy-black hair and sea-green eyes, standing on the railed gallery at the top of a lighthouse on a rocky coast at twilight. A navy peacoat with brass buttons over a cream cable-knit sweater, a mustard-yellow scarf, gold anchor-and-rope embroidery and sturdy boots. Holds up a large brass storm lantern whose beam sweeps out across the sea as a broad golden ray. Rolling waves breaking on the rocks below, gulls, a distant sailing ship, the great lighthouse lens glowing behind, and a purple-blue twilight sky with the first stars. Palette: navy and cream with brass yellow and sea green.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### R4 — Gem Delver

Save as `images/one_of_ones/one_of_one_081_gem_delver.png` · Signature element: freshly mined glowing gem.

```text
A chibi gem delver with spiky slate-gray hair and bright ruby eyes, standing between mine-cart rails in a glittering underground mine. A rugged brown leather jerkin with brass rivets, a teal scarf, a small lantern clipped to a leather headband, heavy gloves, a tool belt with gem pouches, and sturdy boots. Rests a gold-inlaid pickaxe on one shoulder and holds up a freshly mined, glowing multicolored gem in the other palm. Timber-braced tunnels, walls veined with glowing rubies, sapphires and emeralds, a mine cart heaped with gems, hanging lanterns and sparkling dust. Palette: earthy brown and teal with jewel-tone gems and brass.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### R5 — White Tiger Guardian

Save as `images/one_of_ones/one_of_one_082_white_tiger_guardian.png` · Signature element: white tiger companion.

```text
A chibi guardian with short white hair streaked with black, small white tiger ears and icy jade eyes, standing at the top of stone stairs before a great mountain gate at dawn. White and jade layered armor-robes with black stripe patterns, gold cloud embroidery, a jade medallion and a white fur collar. A large, majestic white tiger with glowing jade eyes stands protectively at the character's side, one hand resting on its head. A stone guardian gate, pine trees clinging to cliffs, waterfalls, swirling mist and a soft pink dawn. Palette: white and jade with black and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### R6 — Tarot Seer

Save as `images/one_of_ones/one_of_one_083_tarot_seer.png` · Signature element: arc of floating gilded cards and a crystal ball.

```text
A chibi fortune seer with long straight black hair tipped in violet, a sheer veil pinned back from the face and mysterious golden eyes, standing on layered rugs inside an opulent candlelit fortune-teller's tent. Deep teal and gold draped robes, a coin-trimmed sash, layered gold jewelry and velvet slippers. Holds a glowing crystal ball in one hand while a fan of large gilded cards with abstract star, moon and sun patterns floats in an arc around the character. Silk drapes, hanging brass lanterns, curling incense smoke, and a starry night visible through the tent opening. Palette: deep teal, gold, burgundy and violet.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

### R7 — Steam Train Conductor

Save as `images/one_of_ones/one_of_one_084_steam_train_conductor.png` · Signature element: emerald signal lantern and an arriving steam train.

```text
A chibi train conductor with neat black hair and bright amber eyes, standing on the platform of a grand glass-roofed railway station as a magical steam train arrives. A deep maroon conductor's coat with gold braid and brass buttons, a peaked cap with a gold winged-wheel badge, white gloves and polished black boots. Raises a brass signal lantern glowing emerald green. An ornate steam locomotive with gold trim and billowing white steam, iron arches and a glass roof, hanging round lamps, and morning sunbeams slanting through the steam. Palette: maroon, black and cream with brass and gold.

Render it as a premium chibi fantasy-anime collectible illustration: a single character about two and a half heads tall, with a large head, a small compact body, big glossy jewel-toned eyes full of layered sparkling highlights, a small nose and a small calm mouth. The whole figure is centered and faces the viewer, from the top of the head near the top edge down to the boots near the bottom edge, with a soft reflection or shadow on the ground beneath. The costume is ornate and layered, with intricate gold filigree, fine embroidery, gems and tassels. The setting is rich and deep with storytelling detail, glowing particles, soft bokeh and luminous light. Crisp clean linework, vivid saturated color, painterly jewel-like lighting. Square 1:1 full-bleed illustration.

Avoid: text, letters, numbers, logos, watermarks, signatures, borders, extra people, a cropped head or feet.
```

## Progress

- [ ] 057 — Kitsune Shrine Keeper
- [ ] 058 — Honey Warden
- [ ] 059 — Windcaller
- [ ] 060 — Marble Sculptor
- [ ] 061 — Rainbow Herald
- [ ] 062 — Hearthkeeper
- [ ] 063 — Harvest Sovereign
- [ ] 064 — Pomegranate Princess
- [ ] 065 — Valkyrie
- [ ] 066 — Raven Seer
- [ ] 067 — Cat Temple Guardian
- [ ] 068 — Feathered Serpent Priest
- [ ] 069 — Djinn Lamp Keeper
- [ ] 070 — Chromatic Painter
- [ ] 071 — Wind-Up Toymaker
- [ ] 072 — Confectioner
- [ ] 073 — Hedge Witch
- [ ] 074 — Stained Glass Artisan
- [ ] 075 — Autumn Stag Prince
- [ ] 076 — Wandering Bard
- [ ] 077 — Owl Sage
