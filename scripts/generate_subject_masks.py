#!/usr/bin/env python3
"""Generate review-candidate anime subject masks for flattened Demigods PNGs.

Requires `pip install 'rembg[cpu]>=2.0.60'`. The first run downloads the
isnet-anime ONNX model. Inspect every mask before treating or approving art.
"""
from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFilter
from rembg import new_session, remove


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir', type=Path, default=Path('images/variations/complete_72'))
    p.add_argument('--output-dir', type=Path, default=Path('images/variations/subject_masks'))
    p.add_argument('--expand', type=int, default=5, help='Odd max-filter width; 1 disables expansion')
    p.add_argument('--overwrite', action='store_true')
    args = p.parse_args()
    if args.output_dir.resolve() == args.input_dir.resolve():
        p.error('Input and output directories must differ')
    if args.expand < 1 or args.expand % 2 != 1:
        p.error('--expand must be a positive odd integer')
    images = sorted(args.input_dir.glob('*.png'))
    if not images:
        p.error('No PNG sources found')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    session = new_session('isnet-anime')
    for number, source in enumerate(images, 1):
        dest = args.output_dir / source.name
        if dest.exists() and not args.overwrite:
            p.error(f'Output exists: {dest}; pass --overwrite to replace')
        with Image.open(source) as im:
            im.load()
            mask = remove(im.convert('RGB'), session=session, only_mask=True).convert('L')
            size = im.size
        if args.expand > 1:
            mask = mask.filter(ImageFilter.MaxFilter(args.expand))
        payload = BytesIO()
        mask.save(payload, format='PNG')
        with Image.open(BytesIO(payload.getvalue())) as check:
            check.load()
            assert check.size == size and check.mode == 'L'
        temporary = dest.with_suffix('.png.tmp')
        temporary.write_bytes(payload.getvalue())
        with Image.open(temporary) as check:
            check.load()
        temporary.replace(dest)
        print(f'{number}/{len(images)} {source.name}', flush=True)


if __name__ == '__main__':
    main()
