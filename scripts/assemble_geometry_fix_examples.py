from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent.parent/'docs/qa/geometry_fix_examples_2026-08-15'
files=['staff_pose_002.png','lantern_pose_002.png','tome_pose_004.png','neck_pendant.png']
cell=420; label=32
sheet=Image.new('RGB',(cell*2, (cell+label)*2),(24,24,28)); d=ImageDraw.Draw(sheet)
for i,name in enumerate(files):
 im=Image.open(root/name).convert('RGB'); im.thumbnail((cell,cell)); x=(i%2)*cell; y=(i//2)*(cell+label); sheet.paste(im,(x+(cell-im.width)//2,y)); d.text((x+8,y+cell+8),name,fill='white')
sheet.save(root/'review_sheet.png')
print(root/'review_sheet.png')
