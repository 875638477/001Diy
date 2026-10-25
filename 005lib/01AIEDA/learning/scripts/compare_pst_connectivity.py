"""Compare physical pin partitions of two Allegro PST exports (including NC)."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

def load(path):
    content = path.read_text(encoding='utf-8-sig', errors='strict')
    pins, duplicates, groups = {}, [], []
    for match in re.finditer(r"(?ms)^NET_NAME[ \t]*\r?\n'([^']*)'\r?\n(.*?)(?=^NET_NAME[ \t]*\r?$|^END\.)", content):
        name, body = match.groups()
        keys = [tuple(x.upper() for x in m) for m in re.findall(
            r'(?m)^NODE_NAME[ \t]+(\S+)[ \t]+(\S+)[ \t]*\r?$', body)]
        sets = [[key] for key in keys] if name == 'NC' else [keys]
        for keys in sets:
            if not keys:
                continue
            signature = tuple(sorted(keys))
            groups.append(signature)
            for key in keys:
                if key in pins:
                    duplicates.append(key)
                pins[key] = (signature, name)
    return pins, duplicates, groups

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--candidate', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r, rd, rg = load(a.reference)
    c, cd, cg = load(a.candidate)
    missing, extra = sorted(r.keys()-c.keys()), sorted(c.keys()-r.keys())
    common = r.keys() & c.keys()
    changed = sorted(k for k in common if r[k][0] != c[k][0])
    renamed = [{'pin': k, 'reference': r[k][1], 'candidate': c[k][1]}
               for k in sorted(common) if r[k][1] != c[k][1]]
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest().upper()
    result = {'status': 'PASS' if r and not (rd or cd or missing or extra or changed) else 'FAIL',
              'reference': str(a.reference), 'candidate': str(a.candidate),
              'reference_sha256': sha(a.reference), 'candidate_sha256': sha(a.candidate),
              'reference_pin_count': len(r), 'candidate_pin_count': len(c),
              'reference_partition_count': len(rg), 'candidate_partition_count': len(cg),
              'reference_duplicate_pins': rd, 'candidate_duplicate_pins': cd,
              'missing_pins': missing, 'extra_pins': extra, 'changed_partition_pins': changed,
              'renamed_pin_net_names': renamed,
              'scope': 'Complete physical refdes.pin connectivity, NC treated as separate pins. Net renames reported separately.'}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}))
    print(json.dumps({k: len(v) for k, v in result.items() if isinstance(v, list)}))
    if result['status'] != 'PASS':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
