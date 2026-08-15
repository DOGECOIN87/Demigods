from pathlib import Path
from PIL import Image
import json

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / 'config' / 'collection.json').read_text())
RIG = CFG['master_rig']
BASE_DIR = ROOT / 'assets' / 'base_bodies'

def bounds(im):
    bb = im.getchannel('A').getbbox()
    return (bb[0], bb[1], bb[2]-1, bb[3]-1) if bb else None

def center_band(im, y0, y1):
    bb = im.getchannel('A').crop((0, y0, im.width, y1)).getbbox()
    return None if bb is None else (bb[0] + bb[2] - 1) / 2

for path in sorted(BASE_DIR.glob('*.png')):
    with Image.open(path) as src:
        im = src.convert('RGBA')
        b = bounds(im)
        full = (b[0] + b[2]) / 2
        head = center_band(im, RIG['top_of_head_y'], RIG['shoulder_line_y'] - 60)
        legs = center_band(im, RIG['waist_center'][1] + 130, RIG['foot_baseline_y'] + 1)
        body = None if head is None or legs is None else (head + legs) / 2
        print(path.name)
        print('  bounds=', b, 'full_center=', round(full, 2))
        print('  head_center=', None if head is None else round(head, 2), 'leg_center=', None if legs is None else round(legs, 2), 'body_center=', None if body is None else round(body, 2), 'delta=', None if body is None else round(body - RIG['canvas_center_x'], 2))
        print('  alpha=', im.getchannel('A').getextrema(), 'mode=', src.mode, 'size=', src.size)
