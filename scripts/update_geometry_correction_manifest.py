from pathlib import Path
import hashlib, json
ROOT=Path(__file__).resolve().parent.parent
MANIFEST=ROOT/'assets/asset_manifest.json'
manifest=json.loads(MANIFEST.read_text())
base_backup=ROOT/'incoming/base_bodies/refinement_originals_2026-08-15_coverage'
neck_backup=ROOT/'incoming/neck_accessories/refinement_originals_2026-08-15'
base_names={
 'base_body_001':'base_body_001_neutral_master.png',
 'base_pose_002':'base_pose_002_viewer_left_vertical_grip.png',
 'base_pose_003':'base_pose_003_viewer_right_vertical_grip.png',
 'base_pose_004':'base_pose_004_viewer_left_palm_up.png',
 'base_pose_005':'base_pose_005_centered_two_hand_grip.png',
}
neck_ids={f'neck_accessory_{i:03d}':f'neck_accessory_{i:03d}_{suffix}.png' for i,suffix in {
 1:'black_choker',2:'gold_blue_drop_choker',3:'black_ribbon_bow',4:'silver_dark_round_pendant',5:'silver_navy_long_pendant',6:'silver_pale_circle_charm',7:'gold_teardrop_pendant',8:'violet_ribbon_bow'}.items()}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
updates=0
for e in manifest['registered_production_assets']:
    eid=e.get('id')
    if eid in base_names:
        name=base_names[eid]; current=ROOT/'assets/base_bodies'/name; backup=base_backup/name; method='hide_undergarment_repaint_2026-08-15'
    elif eid in neck_ids:
        name=neck_ids[eid]; current=ROOT/'assets/neck_accessories'/name; backup=neck_backup/name; method='reduction_only_neck_refit_2026-08-15'
    else: continue
    if not backup.exists(): raise SystemExit(f'missing backup: {backup}')
    old=sha(backup); new=sha(current)
    if eid.startswith('base_') and e.get('sha256') not in (old, new):
        raise SystemExit(f'{eid}: manifest hash does not match backup or current')
    if eid.startswith('neck_') and e.get('sha256') != old:
        raise SystemExit(f'{eid}: manifest hash does not match immutable neck backup')
    e['sha256']=new
    prov=e.setdefault('provenance',{})
    prior=list(prov.get('postprocessing',[]))
    if method not in prior: prior.append(method)
    prov['postprocessing']=prior
    prov.setdefault('pre_geometry_correction_sha256',old)
    prov['post_geometry_correction_sha256']=new
    prov['geometry_correction_script']='scripts/update_geometry_correction_manifest.py'
    prov['geometry_correction_method']=method
    e['qa_report']='docs/qa/geometry_corrections_2026-08-15.md'
    updates+=1
if updates != len(base_names)+len(neck_ids): raise SystemExit(f'updated {updates}, expected {len(base_names)+len(neck_ids)}')
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('updated',updates,'manifest entries')
