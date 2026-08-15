from pathlib import Path
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parent.parent/'docs/qa/hand_anchor_diagnostics_2026-08-15'
files=sorted(root.glob('hand_object_*_anchor.png'))
cell=314
sheet=Image.new('RGB',(cell*4,cell*2),(20,20,25))
d=ImageDraw.Draw(sheet)
for i,p in enumerate(files):
    im=Image.open(p).convert('RGB'); im.thumbnail((300,300))
    x=(i%4)*cell; y=(i//4)*cell
    sheet.paste(im,(x,y)); d.text((x+3,y+302),p.stem,fill='white')
sheet.save(root/'sheet.png')
print(root/'sheet.png')
