# Prompts — Facial Traits

## Eyes

```text
[INSERT LOCKED MASTER SPECIFICATION]

Create one matched eye-set trait: [COLOR / PUPIL / STYLE].
- both eyes aligned to Y 367 using identical approved spacing and scale
- include eye lines, lashes, sclera, irises, pupils, internal highlights, and shading
- use shared upper-left catchlight logic
- exclude eyebrows, nose, mouth, face, skin, blush, hair, and expression marks

OUTPUT: one transparent eye-pair PNG.
FILENAME: eyes_[NUMBER]_[COLOR]_[STYLE].png

[INSERT UNIVERSAL AVOID BLOCK]
```

## Eyebrows

```text
[INSERT LOCKED MASTER SPECIFICATION]

Create one matched eyebrow-pair trait expressing [MOOD].
- use the approved eyebrow anchor positions and line weight
- remain compatible with all approved eye sets
- exclude eyes, face, forehead, hair, nose, mouth, and blush

OUTPUT: one transparent eyebrow-pair PNG.
FILENAME: eyebrows_[NUMBER]_[MOOD].png

[INSERT UNIVERSAL AVOID BLOCK]
```

## Mouth

```text
[INSERT LOCKED MASTER SPECIFICATION]

Create one isolated mouth trait expressing [EXPRESSION].
- center at X 627, Y 441
- preserve approved width and vertical range
- include only the mouth line and any required stylized interior, tongue, lips, or small teeth
- exclude face, nose, chin, blush, eyes, eyebrows, hair, and expression marks

OUTPUT: one transparent mouth PNG.
FILENAME: mouth_[NUMBER]_[EXPRESSION].png

[INSERT UNIVERSAL AVOID BLOCK]
```
