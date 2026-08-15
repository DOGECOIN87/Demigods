from pathlib import Path
from PIL import Image

root = Path('/home/ubuntu/Demigods/images/trait_candidates/hand_objects')
for p in sorted(root.glob('DG-*_source*.png')):
    im = Image.open(p).convert('RGBA')
    alpha = im.getchannel('A')
    amin, amax = alpha.getextrema()
    hist = alpha.histogram()
    nonzero = sum(hist[1:])
    opaque = hist[255]
    bbox = alpha.getbbox()
    corner = im.getpixel((0, 0))
    bands = {f'{lo}-{hi}': sum(hist[lo:hi+1]) for lo, hi in [(0,31),(32,63),(64,127),(128,191),(192,254),(255,255)]}
    print(p.name, im.size, 'alpha_min_max', (amin, amax), 'nonzero', nonzero, 'opaque', opaque, 'bbox', bbox, 'corner', corner, 'bands', bands)
