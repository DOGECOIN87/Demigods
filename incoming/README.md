# Candidate drop folder

Save generated trait PNGs here under the exact filename its prompt names, then
run the batch through QA in one pass.

```
python scripts/bulk_intake.py incoming/
```

That matches each file to its backlog row, runs binary QA and the category's rig
gate, composites it over the base master in correct layer order, and writes a
single review sheet to `docs/qa/batch_review_sheet.png`.

Look at the sheet, then register what you approve:

```
python scripts/bulk_intake.py incoming/ --register-approved DG-029 DG-030
```

Registration copies the exact approved bytes to `assets/<category>/`, writes the
manifest entry, binds any front-hair layer to its matching rear-hair layer in
`config/compatibility.json`, flips the backlog row to `registered`, and
regenerates the production ledger.

## Rules the gate will enforce for you

- native 1254 x 1254, never upscaled to reach it
- RGBA with genuine transparency; a fully opaque layer fails
- no baked transparency checkerboard — a rendered checker pattern is a hard
  reject, and it cannot be extracted afterwards
- no burned-in UI text, labels, or coordinate overlays
- the filename must match a backlog row's production path

Files here are gitignored. Nothing in this folder is part of the collection until
it is registered.
