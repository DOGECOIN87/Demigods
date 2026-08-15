from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'docs/qa/hand_region_grids_2026-08-15'; OUT.mkdir(parents=True,exist_ok=True)
items=[('pose2','assets/base_bodies/base_pose_002_viewer_left_vertical_grip.png',(340,690,520,850)),('pose4','assets/base_bodies/base_pose_004_viewer_left_palm_up.png',(340,690,540,850))]
for name,path,box in items:
 im=Image.open(ROOT/path).convert('RGBA').crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3),Image.Resampling.NEAREST)
 d=ImageDraw.Draw(im)
 for x in range(0,im.width,30): d.line((x,0,x,im.height),fill=(255,0,0,140),width=1); d.text((x+2,2),str(box[0]+x//3),fill=(255,0,0,255))
 for y in range(0,im.height,30): d.line((0,y,im.width,y),fill=(255,0,0,140),width=1); d.text((2,y+2),str(box[1]+y//3),fill=(255,0,0,255))
 for ax,ay in [(404,772),(438,772),(438,748)]:
  x=(ax-box[0])*3; y=(ay-box[1])*3; d.ellipse((x-8,y-8,x+8,y+8),outline=(0,255,0,255),width=3); d.text((x+8,y),f'{ax},{ay}',fill=(0,255,0,255))
 im.convert('RGB').save(OUT/f'{name}.png')
 print(OUT/f'{name}.png')
