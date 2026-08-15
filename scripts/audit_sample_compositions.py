from pathlib import Path
import argparse, json
from PIL import Image
try:
    from scripts.generate_777 import violates_rules, load_json
except ImportError:
    from generate_777 import violates_rules, load_json

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--sample', required=True)
args = parser.parse_args()
sample = ROOT / args.sample
meta_dir = sample / 'tokens.json' / 'metadata'
config = load_json(ROOT / 'config/compatibility.json')
rows = [json.loads(p.read_text()) for p in sorted(meta_dir.glob('*.json'))]
errors = []
trait_sigs = []
for row in rows:
    trait_sigs.append(row['trait_signature'])
    attrs = {a['trait_type']: a for a in row['attributes']}
    selection = {}
    for a in row['attributes']:
        path = ROOT / 'assets' / a['source_file']
        if not path.exists():
            errors.append((row['token_id'], 'missing_source', a['source_file']))
            continue
        selection[a['trait_type']] = path
        try:
            with Image.open(path) as im:
                if im.size != (1254, 1254): errors.append((row['token_id'], 'wrong_canvas', a['source_file'], im.size))
                if a['trait_type'] == 'backgrounds':
                    if im.mode not in ('RGB', 'RGBA'):
                        errors.append((row['token_id'], 'wrong_mode', a['source_file'], im.mode))
                elif im.mode not in ('RGBA', 'LA'):
                    errors.append((row['token_id'], 'wrong_mode', a['source_file'], im.mode))
                if a['trait_type'] not in ('backgrounds','global_finish') and im.getchannel('A').getbbox() is None:
                    errors.append((row['token_id'], 'empty_alpha', a['source_file']))
        except Exception as exc:
            errors.append((row['token_id'], 'decode_error', a['source_file'], str(exc)))
    if violates_rules(selection, config): errors.append((row['token_id'], 'compatibility_violation'))
    if 'backgrounds' not in attrs or 'base_bodies' not in attrs: errors.append((row['token_id'], 'missing_required_category'))
print('tokens=', len(rows))
print('unique_trait_signatures=', len(set(trait_sigs)))
print('errors=', len(errors))
for e in errors[:50]: print('ERROR', e)
if len(rows) != 100 or len(set(trait_sigs)) != 100 or errors:
    raise SystemExit(1)
print('PASS 100/100 token metadata, source, canvas, and compatibility checks')
