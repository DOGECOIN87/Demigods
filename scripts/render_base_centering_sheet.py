from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
paths = sorted((ROOT / 'assets' / 'base_bodies').glob('*.png'))
cell = 300
sheet = Image.new('RGB', (len(paths) * cell, cell + 46), (32, 32, 38))
for i, path in enumerate(paths):
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    bg = bg.convert('RGB')
    bg.thumbnail((cell - 20, cell - 20))
    x = i * cell + (cell - bg.width) // 2
    y = (cell - bg.height) // 2
    sheet.paste(bg, (x, y))
    # Draw a red guide at the scaled canvas-center x=627.
    sx = i * cell + 10 + round(627 / 1254 * (cell - 20))
    ImageDraw.Draw(sheet).line((sx, 0, sx, cell), fill=(210, 60, 60), width=2)
    ImageDraw.Draw(sheet).text((i * cell + 8, cell + 8), path.stem, fill=(238, 238, 238))
out = ROOT / 'docs' / 'qa' / 'base_centering_visual_comparison.png'
out.parent.mkdir(parents=True, exist_ok=True)
sheet.save(out)
print(out)
