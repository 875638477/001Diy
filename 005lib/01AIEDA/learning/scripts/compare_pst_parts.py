"""Compare effective primitive electrical/footprint/value data by physical refdes.

Only primitive identity and body PART_NAME may change for a cache rename.
All other primitive text, pin order, and per-ref section numbers remain exact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

def load(directory):
    chip = (directory/'pstchip.dat').read_text(encoding='utf-8-sig')
    primitives = {}
    for m in re.finditer(r"(?ms)^primitive '([^']+)';\n(.*?)^end_primitive;", chip):
        name, body = m.groups()
        identity = re.findall(r"(?m)^\s*PART_NAME='([^']*)';\s*$", body)
        comparable = re.sub(r"(?m)^\s*PART_NAME='[^']*';\s*$", '', body)
        if name in primitives:
            raise ValueError('Duplicate primitive '+name)
        primitives[name] = (comparable, identity)
    text = (directory/'pstxprt.dat').read_text(encoding='utf-8-sig')
    parts = {}
    for m in re.finditer(r"(?ms)^PART_NAME[ \t]*\n[ \t]+(\S+) '([^']+)':;(.*?)(?=^PART_NAME[ \t]*\n|\Z)", text):
        ref, primitive, body = m.groups()
        if ref.upper() in parts:
            raise ValueError('Duplicate physical reference '+ref)
        if primitive not in primitives:
            raise ValueError('Undefined primitive '+primitive)
        parts[ref.upper()] = {'primitive': primitive, 'definition': primitives[primitive][0],
            'part_name': primitives[primitive][1],
            'sections': re.findall(r'(?m)^SECTION_NUMBER[ \t]+(\S+)', body)}
    if not parts or not primitives:
        raise ValueError('Empty PST input')
    return parts, len(primitives)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--reference', type=Path, required=True)
    p.add_argument('--candidate', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    r, rp = load(a.reference)
    c, cp = load(a.candidate)
    missing, extra = sorted(r.keys()-c.keys()), sorted(c.keys()-r.keys())
    changed, identity = [], []
    for ref in sorted(r.keys() & c.keys()):
        if (r[ref]['definition'], r[ref]['sections']) != (c[ref]['definition'], c[ref]['sections']):
            changed.append({'ref': ref, 'reference': r[ref], 'candidate': c[ref]})
        if (r[ref]['primitive'], r[ref]['part_name']) != (c[ref]['primitive'], c[ref]['part_name']):
            identity.append({'ref': ref, 'reference_primitive': r[ref]['primitive'],
                             'candidate_primitive': c[ref]['primitive'],
                             'reference_part_name': r[ref]['part_name'], 'candidate_part_name': c[ref]['part_name']})
    result = {'status': 'PASS' if not (missing or extra or changed) else 'FAIL',
        'reference': str(a.reference), 'candidate': str(a.candidate),
        'reference_part_count': len(r), 'candidate_part_count': len(c),
        'reference_primitive_count': rp, 'candidate_primitive_count': cp,
        'missing_parts': missing, 'extra_parts': extra, 'changed_effective_definitions': changed,
        'documented_identity_changes': identity,
        'scope': 'By physical refdes: exact ordered primitive pin mappings/electrical attributes, footprint, VALUE and all other body fields plus section numbers. Only primitive identity/body PART_NAME excluded and separately recorded.'}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, list)}))
    print(json.dumps({k: len(v) for k, v in result.items() if isinstance(v, list)}))
    if result['status'] != 'PASS':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
