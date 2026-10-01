#!/usr/bin/env python3
"""Build review evidence from current assets; never modify production artwork.

Includes every registered modular trait, all current flattened variations,
source/mask pairs, outfit/pose coverage and compatible hand-object composites.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    from scripts.generate_777 import render_order, violates_rules
    from scripts.hidden_layers import hidden_categories, in_hand_objects
    from scripts.intake_dressed_bodies import face_trait_union, gates
    from scripts import fit_outfit_torso
except ImportError:
    # Legacy intake helpers import their siblings by module name. Support both
    # direct CLI execution and importing this review builder from the repo root.
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from generate_777 import render_order, violates_rules
    from hidden_layers import hidden_categories, in_hand_objects
    from intake_dressed_bodies import face_trait_union, gates
    import fit_outfit_torso


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sheet(records: list[tuple[str, Image.Image]], path: Path, columns: int = 4,
          side: int = 300) -> None:
    gap, label = 10, 46
    rows = (len(records) + columns - 1) // columns
    canvas = Image.new('RGB', (columns * (side + gap) + gap,
                              rows * (side + gap + label) + gap), '#171c2d')
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 14)
    except OSError:
        font = ImageFont.load_default()
    for i, (title, im) in enumerate(records):
        x, y = gap + (i % columns) * (side + gap), gap + (i // columns) * (side + gap + label)
        preview = im.copy().convert('RGB')
        preview.thumbnail((side, side), Image.Resampling.LANCZOS)
        canvas.paste(preview, (x + (side - preview.width) // 2, y))
        title = title.replace('_', ' ')
        lines = ['']
        for word in title.split():
            candidate = (lines[-1] + ' ' + word).strip()
            if draw.textlength(candidate, font=font) > side and lines[-1]:
                lines.append(word)
            else:
                lines[-1] = candidate
        lines = lines[:2]
        draw.multiline_text((x, y + side + 3), '\n'.join(lines), fill='#e7edf9', font=font)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = BytesIO()
    canvas.save(payload, 'PNG', optimize=True)
    with Image.open(BytesIO(payload.getvalue())) as check:
        check.load()
    temporary = path.with_suffix('.png.tmp')
    temporary.write_bytes(payload.getvalue())
    with Image.open(temporary) as check:
        check.load()
    temporary.replace(path)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=Path('docs/qa/review_2026-10-01'))
    p.add_argument('--masks', type=Path, default=Path('images/variations/subject_masks_refined_review'))
    p.add_argument('--treated', type=Path, default=Path('images/variations/depth_treated_review_2026-10-01'))
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(Path('assets/asset_manifest.json').read_text())
    rules = json.loads(Path('config/compatibility.json').read_text())
    entries = manifest['registered_production_assets']
    by_id = {v['id']: Path(v['path']) for v in entries}
    bases = sorted(Path('assets/base_bodies').glob('*.png'))
    outfits = sorted(Path('assets/outfits').glob('*.png'))
    by_name = {p.name: p for p in by_id.values()}
    requires = {r['trait']: r['requires'] for r in rules['requires']}
    default = {
        'backgrounds': by_id['background_001'], 'base_bodies': bases[0],
        'outfits': by_id['outfit_001'], 'hair_back': by_id['hair_back_001'],
        'hair_front': by_id['hair_front_001'], 'eyes': by_id['eyes_005'],
        'eyebrows': by_id['eyebrows_001'], 'mouths': by_id['mouth_001'],
    }
    cache: dict[Path, Image.Image] = {}
    def load(path: Path) -> Image.Image:
        if path not in cache:
            with Image.open(path) as im:
                im.load()
                cache[path] = im.convert('RGBA')
        return cache[path]

    def composite(selection: dict[str, Path]) -> Image.Image:
        names = {p.name for p in selection.values()}
        hidden = hidden_categories(names, rules)
        hand = bool(names & in_hand_objects(rules))
        im = Image.new('RGBA', (1254, 1254))
        for category in render_order(hand):
            if category in selection and category not in hidden:
                im = Image.alpha_composite(im, load(selection[category]))
        return im.convert('RGB')

    def thumbnail(im: Image.Image, size: int = 420) -> Image.Image:
        result = im.copy()
        result.thumbnail((size, size), Image.Resampling.LANCZOS)
        return result

    checks = []
    union = face_trait_union()
    for cat in manifest['production_directories']:
        records = []
        for entry in [v for v in entries if v['category'] == cat]:
            path = Path(entry['path'])
            selection = dict(default)
            selection[cat] = path
            if cat == 'base_bodies':
                selection.pop('outfits')
            if cat == 'outfits':
                selection['base_bodies'] = by_name[requires[path.name]]
            if cat in ('hair_back', 'hair_front'):
                suffix = re.search(r'_(\d{3})_', path.name).group(1)
                selection['hair_front' if cat == 'hair_back' else 'hair_back'] = by_id[
                    ('hair_front_' if cat == 'hair_back' else 'hair_back_') + suffix]
            if cat == 'hand_objects':
                selection['base_bodies'] = by_name[requires[path.name]]
                selection.pop('outfits')
            im = composite(selection)
            if cat in ('eyes', 'eyebrows', 'mouths', 'expression_marks', 'hair_front', 'hair_back'):
                im = im.crop((350, 105, 910, 540))
            records.append((path.stem, thumbnail(im)))
            alpha = np.asarray(load(path).getchannel('A'))
            checks.append({'id': entry['id'], 'category': cat, 'path': str(path),
                           'dimensions': list(load(path).size), 'sha256_match': sha(path) == entry['sha256'],
                           'alpha_min': int(alpha.min()), 'alpha_max': int(alpha.max())})
        if records:
            if cat == 'outfits':
                for i in range(0, len(records), 15):
                    sheet(records[i:i + 15], a.output / f'traits_{cat}_{i // 15 + 1:02}.png', 5)
            else:
                sheet(records, a.output / f'traits_{cat}.png', min(5, len(records)))
    coverage = {}
    dressed_gates = []
    garment_shortfalls = []
    for path in outfits:
        family = re.search(r'outfit_(\d{3})_', path.name).group(1)
        base = requires.get(path.name)
        pose = '001' if base == 'base_body_001_neutral_master.png' else re.search(r'base_pose_(\d{3})_', base).group(1)
        coverage.setdefault(family, []).append(pose)
        if 'base_bodies' in hidden_categories({path.name}, rules):
            passed, failures, clearance = gates(path, union)
            dressed_gates.append({'path': str(path), 'passed': passed, 'failures': failures, 'face_clearance': clearance})
        else:
            pixels = fit_outfit_torso.shortfall(np.asarray(load(path)),
                                               np.asarray(load(by_name[base])),
                                               fit_outfit_torso.DEFAULT_MAX_PX)
            garment_shortfalls.append({'path': str(path), 'torso_leg_shortfall_pixels': pixels})

    hand_composites = []
    hand_records = []
    hand_face_overlap = []
    for path in sorted(Path('assets/hand_objects').glob('*.png')):
        base = by_name[requires[path.name]]
        alpha = np.asarray(load(path).getchannel('A'))
        # Exact fixed eye windows used by tests/test_face_occlusion.py.
        eye_counts = [int((alpha[y1:y2 + 1, x1:x2 + 1] > 128).sum())
                      for x1,y1,x2,y2 in ((505,334,584,403),(669,334,748,403))]
        hand_face_overlap.append({'path': str(path), 'opaque_pixels_in_eye_windows': eye_counts})
        for outfit in outfits:
            if requires.get(outfit.name) != base.name:
                continue
            selection = dict(default, base_bodies=base, outfits=outfit, hand_objects=path)
            if violates_rules(selection, rules):
                continue
            im = composite(selection)
            hand_records.append((path.stem[:15] + ' / ' + outfit.stem, thumbnail(im.crop((300, 300, 740, 980)))))
            hand_composites.append({'object': str(path), 'outfit': str(outfit), 'base': str(base)})
    for i in range(0, len(hand_records), 20):
        sheet(hand_records[i:i + 20], a.output / f'hand_composites_{i // 20 + 1:02}.png', 5)

    sources = sorted(Path('images/variations/complete_72').glob('*.png'))
    pairs, source_records, verification = [], [], []
    for i, path in enumerate(sources):
        with Image.open(path) as im:
            im.load(); original = im.convert('RGBA')
        with Image.open(a.masks / path.name) as im:
            im.load(); mask = im.convert('L')
        source_records.append((path.stem, thumbnail(original)))
        pairs.extend([(path.stem + ' source', thumbnail(original)), (path.stem + ' protection mask', thumbnail(mask))])
        row = {'file': path.name, 'source_sha256': sha(path), 'dimensions': list(original.size),
               'white_pixels': int((np.asarray(mask) == 255).sum()), 'mask_sha256': sha(a.masks / path.name)}
        treated = a.treated / path.name
        if treated.exists():
            with Image.open(treated) as im:
                im.load(); output = np.asarray(im.convert('RGBA'))
            keep = np.asarray(mask) == 255
            row['changed_protected_pixels'] = int(np.any(output != np.asarray(original), axis=-1)[keep].sum())
            row['output_sha256'] = sha(treated)
        verification.append(row)
        if (i + 1) % 6 == 0:
            sheet(pairs, a.output / f'masks_{(i + 1) // 6:02}.png', 4)
            pairs.clear()
    sheet(source_records, a.output / 'variations_72_sources.png', 8, 200)
    # Exact left-to-right, top-to-bottom order of the owner's marked 5x10 sheet.
    marked_order = [36,25,5,66,40,22,31,4,50,57,1,29,18,68,30,3,37,2,41,45,
                    10,60,65,55,32,19,64,47,56,42,12,43,17,23,49,
                    26,44,61,70,34,71,59,51,58,69,38,54,15,33,6]
    by_number = {int(p.name.split('_')[1]): p for p in sources}
    marked_records = []
    for number in marked_order:
        source = by_number[number]
        with Image.open(a.treated / source.name) as im:
            im.load()
            marked_records.append((source.stem.removeprefix('Demigods_'), thumbnail(im)))
    sheet(marked_records, a.output / 'random_50_corrected.png', 5, 180)
    archive = []
    for folder in ['images/variations/nature', 'images/variations/references', 'images/one_of_ones']:
        for path in sorted(Path(folder).iterdir()):
            if path.suffix.lower() not in ('.png', '.jpg', '.webp', '.jpeg'):
                continue
            with Image.open(path) as im:
                im.load()
                archive.append({'path': str(path), 'dimensions': list(im.size), 'format': im.format, 'sha256': sha(path)})
    sheet([(Path(v['path']).stem, thumbnail(load(Path(v['path'])))) for v in archive],
          a.output / 'historical_variations.png', 3)
    legend = [(v['id'], thumbnail(load(Path(v['path'])))) for v in manifest['legendary_one_of_ones']]
    sheet(legend, a.output / 'legendary_7.png', 4)
    report = {'registered_count': len(entries), 'category_counts': dict(Counter(v['category'] for v in entries)),
              'registered_assets': checks, 'outfit_pose_coverage': {k: sorted(v) for k,v in coverage.items()},
              'dressed_body_gates': dressed_gates, 'garment_shortfalls': garment_shortfalls,
              'hand_face_overlap': hand_face_overlap, 'compatible_hand_composites': hand_composites,
              'variation_count': len(sources), 'variation_pixel_checks': verification,
              'marked_sheet_order': marked_order, 'historical_images': archive}
    (a.output / 'collection_review.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Reviewed {len(entries)} registered assets, {len(sources)} current variations, '
          f'{len(archive)} historical images and {len(hand_composites)} hand/outfit combinations.')


if __name__ == '__main__':
    main()
