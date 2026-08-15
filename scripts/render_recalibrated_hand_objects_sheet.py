from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs/qa/recalibrated_hand_objects_2026-08-15'; OUT.mkdir(parents=True,exist_ok=True)
entries=[
 ('hand_object_006_gold_lantern_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_007_gold_blue_gem_staff_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_008_blue_crescent_staff_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_009_violet_blade_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_010_horned_skull_scepter_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_011_round_talisman_pose_004_left.png','base_pose_004_viewer_left_palm_up.png','outfit_004_lunar_oracle_pose_004.png',(438,748)),
 ('hand_object_012_brown_tome_pose_004_left.png','base_pose_004_viewer_left_palm_up.png','outfit_004_lunar_oracle_pose_004.png',(438,748)),
]
def load(path): return Image.open(ROOT/path).convert('RGBA')
outs=[]
for obj,base,outfit,anchor in entries:
 c=Image.new('RGBA',(1254,1254),(255,255,255,255)); c.alpha_composite(load('assets/hand_objects/'+obj)); c.alpha_composite(load('assets/base_bodies/'+base)); c.alpha_composite(load('assets/outfits/'+outfit))
 d=ImageDraw.Draw(c); x,y=anchor; d.line((x-28,y,x+28,y),fill=(255,0,0,255),width=4); d.line((x,y-28,x,y+28),fill=(255,0,0,255),width=4); d.ellipse((x-9,y-9,x+9,y+9),outline=(255,0,0,255),width=4)
 p=OUT/(obj.replace('.png','')+'.png'); c.convert('RGB').save(p); outs.append(p)
cell=320; label=30; sheet=Image.new('RGB',(cell*4,(cell+label)*2),(25,25,30)); d=ImageDraw.Draw(sheet)
for i,p in enumerate(outs):
 im=Image.open(p); im.thumbnail((cell,cell)); x=(i%4)*cell; y=(i//4)*(cell+label); sheet.paste(im,(x+(cell-im.width)//2,y)); d.text((x+4,y+cell+5),p.stem.replace('hand_object_',''),fill='white')
sheet.save(OUT/'review_sheet.png'); print(OUT/'review_sheet.png')
