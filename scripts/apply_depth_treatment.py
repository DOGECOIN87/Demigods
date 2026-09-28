#!/usr/bin/env python3
"""Batch background depth treatment for complete Demigods illustrations.

A grayscale subject mask per image is required: white protects the character,
black treats the background. A mask must match the source PNG dimensions.
No source file is modified. Outputs remain review candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir', type=Path, default=Path('images/variations/complete_72'))
    p.add_argument('--mask-dir', type=Path, required=True,
                   help='One grayscale PNG per image, with the same filename; white=untouched subject')
    p.add_argument('--output-dir', type=Path, default=Path('images/variations/depth_treated_review'))
    p.add_argument('--expected-count', type=int, default=0, help='0 accepts the current roster; use 77 when complete')
    p.add_argument('--limit', type=int, default=0, help='Preview the first N images')
    p.add_argument('--blur-radius', type=float, default=10.0)
    p.add_argument('--saturation', type=float, default=0.84)
    p.add_argument('--brightness', type=float, default=0.99)
    p.add_argument('--contrast', type=float, default=0.98)
    p.add_argument('--feather-radius', type=float, default=1.5,
                   help='Blur the mask edge in pixels; use 0 for strict protection')
    p.add_argument('--sheet-columns', type=int, default=8, help='Review sheet columns')
    p.add_argument('--sheet-thumb', type=int, default=180, help='Square thumbnail side in pixels')
    p.add_argument('--overwrite', action='store_true')
    return p


def make_contact_sheet(paths: list[Path], destination: Path, columns: int, thumb: int) -> None:
    """Create a labeled grid from the actual processed PNGs."""
    padding, label_height = 12, 28
    cell_width, cell_height = thumb + padding, thumb + label_height + padding
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new('RGB', (columns * cell_width + padding,
                              rows * cell_height + padding), (24, 27, 42))
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(paths):
        x = padding + (index % columns) * cell_width
        y = padding + (index // columns) * cell_height
        with Image.open(path) as im:
            preview = im.convert('RGB')
            preview.thumbnail((thumb, thumb), Image.Resampling.LANCZOS)
        sheet.paste(preview, (x + (thumb - preview.width) // 2, y))
        draw.text((x, y + thumb + 4), path.stem[:26], fill=(238, 240, 246))
    sheet.save(destination, format='PNG', optimize=True)


def main(argv: list[str] | None = None) -> int:
    a = parser().parse_args(argv)
    if a.input_dir.resolve() == a.output_dir.resolve() or a.output_dir.resolve() == a.mask_dir.resolve():
        raise SystemExit('Output directory must differ from the source and mask directories')
    if min(a.blur_radius, a.feather_radius, a.saturation, a.brightness, a.contrast) < 0:
        raise SystemExit('Treatment parameters must be nonnegative')
    if a.sheet_columns < 1 or a.sheet_thumb < 32:
        raise SystemExit('Sheet columns must be positive and thumbnails at least 32 px')
    if a.expected_count < 0 or a.limit < 0:
        raise SystemExit('Counts must be nonnegative')
    if not a.input_dir.is_dir() or not a.mask_dir.is_dir():
        raise SystemExit('Input and mask directories must exist')
    images = sorted(p for p in a.input_dir.iterdir() if p.is_file() and p.suffix.lower() == '.png')
    if a.expected_count and len(images) != a.expected_count:
        raise SystemExit(f'Expected {a.expected_count} PNGs; found {len(images)} in {a.input_dir}')
    if not images:
        raise SystemExit('No PNGs found')
    images = images[:a.limit] if a.limit else images
    manifest_path = a.output_dir / 'processing_manifest.json'
    sheet_path = a.output_dir / 'contact_sheet.png'
    if not a.overwrite:
        existing = [str(a.output_dir / p.name) for p in images if (a.output_dir / p.name).exists()]
        if existing or manifest_path.exists() or sheet_path.exists():
            raise SystemExit(f'Output exists; pass --overwrite to replace: {(existing or [str(manifest_path if manifest_path.exists() else sheet_path)])[0]}')
    # Validate every selected mask before writing any outputs.
    for src in images:
        mask_path = a.mask_dir / src.name
        if not mask_path.is_file():
            raise SystemExit(f'Missing subject mask: {mask_path}')
        with Image.open(src) as im, Image.open(mask_path) as mask:
            if im.size != mask.size:
                raise SystemExit(f'Mask size mismatch for {src.name}: {mask.size} vs {im.size}')
            if mask.mode not in ('L', '1'):
                raise SystemExit(f'Mask must be grayscale (L or 1): {mask_path}')

    a.output_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for src in images:
        mask_path = a.mask_dir / src.name
        with Image.open(src) as im, Image.open(mask_path) as raw_mask:
            original = ImageOps.exif_transpose(im).convert('RGBA')
            mask = raw_mask.convert('L')
            # Keep exactly opaque white pixels untouched. Feather only the exterior
            # of the subject mask so no soft blend changes the protected interior.
            if a.feather_radius:
                expanded = mask.filter(ImageFilter.MaxFilter(3))
                feathered = expanded.filter(ImageFilter.GaussianBlur(a.feather_radius))
                mask = ImageChops.lighter(mask, feathered)
            background = original.convert('RGB')
            background = ImageEnhance.Color(background).enhance(a.saturation)
            background = ImageEnhance.Brightness(background).enhance(a.brightness)
            background = ImageEnhance.Contrast(background).enhance(a.contrast)
            background = background.filter(ImageFilter.GaussianBlur(a.blur_radius)).convert('RGBA')
            result = Image.composite(original, background, mask)
            result.putalpha(original.getchannel('A'))
            destination = a.output_dir / src.name
            result.save(destination, format='PNG', optimize=True, icc_profile=im.info.get('icc_profile'))
        entries.append({'source': str(src), 'source_sha256': digest(src),
                        'mask': str(mask_path), 'mask_sha256': digest(mask_path),
                        'output': str(destination), 'output_sha256': digest(destination),
                        'dimensions': list(result.size)})
        print(f'{src.name} -> {destination}')
    manifest = {'input_dir': str(a.input_dir), 'mask_dir': str(a.mask_dir),
                'output_dir': str(a.output_dir), 'processed_count': len(entries),
                'parameters': {k: getattr(a, k) for k in
                               ('blur_radius', 'saturation', 'brightness', 'contrast', 'feather_radius')},
                'files': entries}
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    make_contact_sheet([a.output_dir / p.name for p in images], sheet_path, a.sheet_columns, a.sheet_thumb)
    print(f'Processed {len(entries)} images; manifest: {manifest_path}; sheet: {sheet_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
