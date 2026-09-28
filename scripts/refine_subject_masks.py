#!/usr/bin/env python3
"""Conservatively protect faint foreground detail in the existing subject masks.

The original anime segmentation gives some capes, sleeves, robes and held
objects low gray values. Treating those values as background blurs the art.
This produces separate review masks; it never changes the committed originals.
"""
from __future__ import annotations

import argparse
import json
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter


def refine(mask: np.ndarray) -> np.ndarray:
    high = (mask >= 150).astype(np.uint8)
    count, labels, stats, _ = cv2.connectedComponentsWithStats(high)
    if count < 2:
        raise ValueError('Mask has no confident subject pixels')
    primary = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    core = labels == primary

    # Keep sizable separate accessories near the subject, while rejecting
    # background fragments such as architecture entering from a frame edge.
    distance = cv2.distanceTransform((~core).astype(np.uint8), cv2.DIST_L2, 5)
    height, width = mask.shape
    for label in range(1, count):
        if label == primary:
            continue
        x, y, w, h, area = stats[label]
        if area < 800 or x == 0 or y == 0 or x + w >= width or y + h >= height:
            continue
        component = labels == label
        if distance[component].min() < 100:
            core |= component

    distance = cv2.distanceTransform((~core).astype(np.uint8), cv2.DIST_L2, 5)
    plausible = (
        ((mask >= 10) & (distance <= 15))
        | ((mask >= 25) & (distance <= 40))
        | ((mask >= 70) & (distance <= 70))
    )
    merged = (core | plausible).astype(np.uint8)
    merged = cv2.morphologyEx(
        merged, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
    )
    merged = cv2.dilate(merged, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    return merged * 255


def add_held_effects(mask: Image.Image, shapes: list[dict]) -> Image.Image:
    """Protect disconnected foreground objects using local, feathered shapes."""
    for item in shapes:
        overlay = Image.new('L', mask.size, 0)
        draw = ImageDraw.Draw(overlay)
        if 'box' in item:
            box = item['box']
            if len(box) != 4 or not (0 <= box[0] < box[2] <= mask.width and
                                         0 <= box[1] < box[3] <= mask.height):
                raise ValueError(f'Invalid held-effect ellipse: {box}')
            draw.ellipse(box, fill=255)
        elif 'polygon' in item:
            points = item['polygon']
            if len(points) < 3 or any(len(p) != 2 or not (0 <= p[0] < mask.width and
                                                       0 <= p[1] < mask.height) for p in points):
                raise ValueError(f'Invalid foreground polygon: {points}')
            draw.polygon([tuple(p) for p in points], fill=255)
        else:
            raise ValueError(f'Unknown foreground shape: {item}')
        overlay = overlay.filter(ImageFilter.GaussianBlur(item.get('feather', 4)))
        mask = ImageChops.lighter(mask, overlay)
    return mask


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, default=Path('images/variations/subject_masks'))
    parser.add_argument('--output-dir', type=Path, default=Path('images/variations/subject_masks_refined_review'))
    parser.add_argument('--expected-count', type=int, default=72)
    parser.add_argument('--overrides', type=Path, default=Path('config/depth_mask_overrides.json'))
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    if args.input_dir.resolve() == args.output_dir.resolve():
        parser.error('Output directory must differ from input directory')
    paths = sorted(args.input_dir.glob('*.png'))
    if len(paths) != args.expected_count:
        parser.error(f'Expected {args.expected_count} masks; found {len(paths)}')
    overrides = json.loads(args.overrides.read_text(encoding='utf-8'))
    unknown = set(overrides) - {path.name for path in paths}
    if unknown:
        parser.error(f'Overrides have no input mask: {sorted(unknown)}')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for number, src in enumerate(paths, 1):
        dest = args.output_dir / src.name
        if dest.exists() and not args.overwrite:
            parser.error(f'Output exists: {dest}; use --overwrite')
        with Image.open(src) as image:
            if image.mode != 'L':
                parser.error(f'Mask must be grayscale: {src}')
            result = Image.fromarray(refine(np.array(image)), mode='L')
            result = add_held_effects(result, overrides.get(src.name, []))
        payload = BytesIO()
        result.save(payload, format='PNG')
        with Image.open(BytesIO(payload.getvalue())) as check:
            check.load()
            assert check.size == result.size and check.mode == 'L'
        temporary = dest.with_suffix('.png.tmp')
        temporary.write_bytes(payload.getvalue())
        temporary.replace(dest)
        print(f'{number}/{len(paths)} {src.name}', flush=True)


if __name__ == '__main__':
    main()
