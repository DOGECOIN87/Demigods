from pathlib import Path
from PIL import Image
import hashlib, json, shutil
from refit_trait_layer import refit, visible_box
ROOT=Path(__file__).resolve().parent.parent
SPECS={
 'neck_accessory_001_black_choker.png':(0.45,555),
 'neck_accessory_002_gold_blue_drop_choker.png':(0.45,550),
 'neck_accessory_003_black_ribbon_bow.png':(0.45,550),
 'neck_accessory_004_silver_dark_round_pendant.png':(0.45,550),
 'neck_accessory_005_silver_navy_long_pendant.png':(0.35,545),
 'neck_accessory_006_silver_pale_circle_charm.png':(0.45,550),
 'neck_accessory_007_gold_teardrop_pendant.png':(0.45,550),
 'neck_accessory_008_violet_ribbon_bow.png':(0.45,550),
}
def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 import argparse
 ap=argparse.ArgumentParser(); ap.add_argument('--out-dir',required=True); ap.add_argument('--in-place',action='store_true'); args=ap.parse_args()
 out=ROOT/args.out_dir; out.mkdir(parents=True,exist_ok=True)
 prov=[]
 for name,(scale,top_y) in SPECS.items():
  src=ROOT/'assets/neck_accessories'/name
  dst=src if args.in_place else out/name
  im=Image.open(src).convert('RGBA'); result=refit(im,scale=scale,top_y=top_y); result.save(dst)
  b=visible_box(result)
  prov.append({'asset':str(src.relative_to(ROOT)),'source_sha256':sha(src),'output_sha256':sha(dst),'scale':scale,'top_y':top_y,'output_bounds':list(b),'operation':'reduction_only_refit'})
  print(name, 'scale',scale,'top_y',top_y,'bounds',b)
 (out/'provenance.json').write_text(json.dumps({'operation':'neck_accessory_batch_refit','items':prov},indent=2)+'\n')
if __name__=='__main__': main()
