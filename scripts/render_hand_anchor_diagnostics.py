from pathlib import Path
from PIL import Image, ImageDraw
import json, math
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs/qa/hand_anchor_diagnostics_2026-08-15'; OUT.mkdir(parents=True,exist_ok=True)
items=[
 ('hand_object_006','base_pose_002_viewer_left_vertical_grip.png',(404,772)),
 ('hand_object_007','base_pose_002_viewer_left_vertical_grip.png',(404,772)),
 ('hand_object_008','base_pose_002_viewer_left_vertical_grip.png',(404,772)),
 ('hand_object_009','base_pose_002_viewer_left_vertical_grip.png',(404,772)),
 ('hand_object_010','base_pose_002_viewer_left_vertical_grip.png',(404,772)),
 ('hand_object_011','base_pose_004_viewer_left_palm_up.png',(404,772)),
 ('hand_object_012','base_pose_004_viewer_left_palm_up.png',(404,772)),
]
paths={e['id']:ROOT/e['path'] for e in json.loads((ROOT/'assets/asset_manifest.json').read_text())['registered_production_assets'] if e['category']=='hand_objects'}
for obj,base_name,anchor in items:
 base=Image.open(ROOT/'assets/base_bodies'/base_name).convert('RGBA'); objim=Image.open(paths[obj]).convert('RGBA')
 c=Image.new('RGBA',(1254,1254),(255,255,255,255)); c.alpha_composite(base); c.alpha_composite(objim)
 d=ImageDraw.Draw(c); x,y=anchor; d.line((x-30,y,x+30,y),fill=(255,0,0,255),width=3); d.line((x,y-30,x,y+30),fill=(255,0,0,255),width=3); d.ellipse((x-7,y-7,x+7,y+7),outline=(255,0,0,255),width=3)
 out=OUT/f'{obj}_anchor.png'; c.convert('RGB').save(out)
 print(out)
