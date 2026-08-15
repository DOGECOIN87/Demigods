from pathlib import Path
from PIL import Image, ImageDraw
import json, math

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT/'assets/asset_manifest.json').read_text())
OUT = ROOT/'docs/qa/registered_trait_sheets_2026-08-15'
OUT.mkdir(parents=True, exist_ok=True)
ORDER = ['backgrounds','rear_auras','back_accessories','hair_back','base_bodies','outfits','neck_accessories','eyes','eyebrows','mouths','expression_marks','hair_front','head_accessories','hand_objects','front_auras','global_finish']
entries = MANIFEST['registered_production_assets']
base = Image.open(ROOT/'assets/base_bodies/base_body_001_neutral_master.png').convert('RGBA')
for category in ORDER:
    group = [e for e in entries if e['category']==category]
    if not group: continue
    cols = 4
    tile = 300
    label_h = 28
    rows = math.ceil(len(group)/cols)
    sheet = Image.new('RGB',(cols*tile,rows*(tile+label_h)),(28,28,42))
    draw = ImageDraw.Draw(sheet)
    for i,e in enumerate(group):
        tile_im = Image.new('RGBA',(1254,1254),(0,0,0,0))
        # Full background is intentionally omitted; neutral gray lets canvas bounds and alpha read clearly.
        if category != 'base_bodies':
            tile_im.alpha_composite(base)
        src = Image.open(ROOT/e['path']).convert('RGBA')
        tile_im.alpha_composite(src)
        thumb = tile_im.resize((tile,tile),Image.Resampling.LANCZOS)
        x=(i%cols)*tile; y=(i//cols)*(tile+label_h)
        sheet.paste(thumb.convert('RGB'),(x,y))
        draw.rectangle((x,y+tile,x+tile,y+tile+label_h),fill=(28,28,42))
        draw.text((x+6,y+tile+7),e['id'],fill=(235,235,245))
    out=OUT/f'{category}.png'
    sheet.save(out,compress_level=3)
    print(out, len(group))
