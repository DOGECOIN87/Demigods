from pathlib import Path
from PIL import Image,ImageDraw
root=Path('/home/ubuntu/Demigods'); src=root/'incoming/hand_objects/revision_2026-08-15/pose_aware'; out=root/'docs/qa/pose_aware_hand_object_candidates_2026-08-15'; out.mkdir(parents=True,exist_ok=True)
entries=[
 ('hand_object_006_gold_lantern_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_007_gold_blue_gem_staff_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_008_blue_crescent_staff_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_009_violet_blade_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_010_horned_skull_scepter_pose_002_left.png','base_pose_002_viewer_left_vertical_grip.png','outfit_002_storm_guardian_pose_002.png',(438,772)),
 ('hand_object_011_round_talisman_pose_004_left.png','base_pose_004_viewer_left_palm_up.png','outfit_004_lunar_oracle_pose_004.png',(438,748)),
 ('hand_object_012_brown_tome_pose_004_left.png','base_pose_004_viewer_left_palm_up.png','outfit_004_lunar_oracle_pose_004.png',(438,748)),]
def asset(folder,name): return Image.open(root/'assets'/folder/name).convert('RGBA')
imgs=[]
for obj,base,outfit,anchor in entries:
 c=Image.new('RGBA',(1254,1254),(255,255,255,255)); item_path=src/obj if (src/obj).exists() else root/'assets/hand_objects'/obj; c.alpha_composite(Image.open(item_path).convert('RGBA')); c.alpha_composite(asset('base_bodies',base)); c.alpha_composite(asset('outfits',outfit)); d=ImageDraw.Draw(c); x,y=anchor; d.line((x-30,y,x+30,y),fill='red',width=4); d.line((x,y-30,x,y+30),fill='red',width=4); p=out/(obj.replace('.png','')+'.png'); c.convert('RGB').save(p); imgs.append((p,obj))
cell=320; label=32; sheet=Image.new('RGB',(cell*4,(cell+label)*2),(20,20,25)); d=ImageDraw.Draw(sheet)
for i,(p,n) in enumerate(imgs):
 im=Image.open(p); im.thumbnail((cell,cell)); x=i%4*cell; y=i//4*(cell+label); sheet.paste(im,(x+(cell-im.width)//2,y)); d.text((x+3,y+cell+5),n.replace('hand_object_',''),fill='white')
sheet.save(out/'review_sheet.png'); print(out/'review_sheet.png')
