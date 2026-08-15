from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent.parent
MANIFEST=ROOT/'assets/asset_manifest.json'
BACKUP=ROOT/'incoming/hand_objects/recalibration_originals_2026-08-15'
manifest=json.loads(MANIFEST.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads((ROOT/'incoming/hand_objects/recalibration_2026-08-15/provenance.json').read_text())['items']
by_path={r['asset']:r for r in rows}
updated=0
for e in manifest['registered_production_assets']:
    p=e.get('path')
    if p not in by_path: continue
    r=by_path[p]; current=ROOT/p; backup=ROOT/'incoming/hand_objects/recalibration_originals_2026-08-15'/Path(p).name
    old=sha(backup); new=sha(current)
    if e.get('sha256') != old: raise SystemExit(f'{p}: manifest hash does not match immutable hand-object backup')
    e['sha256']=new
    prov=e.setdefault('provenance',{})
    post=list(prov.get('postprocessing',[])); method='native_integer_translation_to_measured_hand_landmark_2026-08-15'
    if method not in post: post.append(method)
    prov['postprocessing']=post; prov['pre_hand_recalibration_sha256']=old; prov['post_hand_recalibration_sha256']=new; prov['hand_recalibration_dx']=r['dx']; prov['hand_recalibration_dy']=r['dy']; prov['hand_recalibration_script']='scripts/recalibrate_hand_objects.py'; e['qa_report']='docs/qa/hand_object_recalibration_findings_2026-08-15.md'; updated+=1
if updated != len(rows): raise SystemExit(f'updated {updated}, expected {len(rows)}')
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n'); print('updated',updated,'hand-object manifest entries')
