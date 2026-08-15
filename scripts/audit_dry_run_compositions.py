from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / 'docs/qa/final_dry_run_20_2026-08-15/tokens.json/metadata'
rows = [json.loads(p.read_text()) for p in sorted(META.glob('*.json'))]
ids = [r['token_id'] for r in rows]
assert len(rows) == 20 and len(set(ids)) == 20
usage = Counter()
missing = []
for r in rows:
    for attr in r['attributes']:
        usage[attr['trait_type']] += 1
        source = ROOT / 'assets' / attr['source_file']
        if not source.exists():
            missing.append((r['token_id'], attr['trait_type'], attr['source_file']))
print('tokens=', len(rows), 'unique=', len(set(ids)))
print('category_usage=')
for k in sorted(usage): print(' ', k, usage[k])
print('missing_sources=', missing)
