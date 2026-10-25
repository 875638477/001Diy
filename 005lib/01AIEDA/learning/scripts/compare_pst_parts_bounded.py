"""Review an explicit per-reference pin order/name normalization plan.

Run compare_pst_parts.py first and retain its exact result. This separate review
never waives physical pin numbers, electrical fields, body text or sections.
The plan must come from the selected library templates before PST export.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

from compare_pst_parts import load


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def split_definition(definition):
    match = re.fullmatch(r"(?s)  pin\n(.*?)  end_pin;\n(.*)", definition)
    if not match:
        raise ValueError('Unsupported primitive pin/body structure')
    region, body = match.groups()
    matches = list(re.finditer(r"(?ms)^    '([^']+)':\n(.*?)(?=^    '[^']+':\n|\Z)", region))
    if ''.join(m.group(0) for m in matches) != region:
        raise ValueError('Unparsed primitive pin text')
    pins = []
    for item in matches:
        name, payload = item.groups()
        numbers = re.findall(r"(?m)^\s*PIN_NUMBER='\(([^)]*)\)';\s*$", payload)
        if len(numbers) != 1 or not numbers[0] or ',' in numbers[0]:
            raise ValueError('Bounded normalization supports one physical number per declaration')
        pins.append({'name': name, 'number': numbers[0], 'payload': payload})
    if len({p['number'] for p in pins}) != len(pins):
        raise ValueError('Repeated physical pin number')
    return pins, body


def review_one(reference, candidate, plan):
    if reference['sections'] != candidate['sections']:
        raise ValueError('Section numbers changed')
    before, body_before = split_definition(reference['definition'])
    after, body_after = split_definition(candidate['definition'])
    if body_before != body_after:
        raise ValueError('Primitive body fields changed')
    # Ordered, explicit expectations prevent a fresh arbitrary reordering being
    # accepted just because the sets of physical numbers happen to match.
    for key, pins in [('before', before), ('after', after)]:
        actual = [{'number': p['number'], 'name': p['name']} for p in pins]
        if actual != plan[key]:
            raise ValueError(key+' pin order/name differs from the pre-export template plan')
    old = {p['number']: p for p in before}
    new = {p['number']: p for p in after}
    if old.keys() != new.keys():
        raise ValueError('Physical pins changed')
    for number in old:
        if old[number]['payload'] != new[number]['payload']:
            raise ValueError('Physical pin electrical/number fields changed: '+number)
    return {'physical_pins': len(old),
            'order_changed': [p['number'] for p in before] != [p['number'] for p in after],
            'name_changes': [{'number': n, 'before': old[n]['name'], 'after': new[n]['name']}
                             for n in old if old[n]['name'] != new[n]['name']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('reference', 'candidate', 'plan', 'output'):
        parser.add_argument('--'+key, required=True, type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding='utf-8-sig'))
    if plan.get('provenance') != 'SOURCE_AND_TARGET_LIBRARY_XML_BEFORE_PST_EXPORT':
        raise ValueError('Plan must be prepared independently from library XML before export')
    expected = plan['references']
    ref, nr = load(args.reference)
    cand, nc = load(args.candidate)
    missing, extra = sorted(ref.keys()-cand.keys()), sorted(cand.keys()-ref.keys())
    failures, accepted, exact = [], [], 0
    for name in sorted(ref.keys() & cand.keys()):
        before, after = ref[name], cand[name]
        if (before['definition'], before['sections']) == (after['definition'], after['sections']):
            exact += 1
            # A planned identity transformation must still fit its declared plan.
            if name in expected:
                try:
                    review_one(before, after, expected[name])
                except ValueError as error:
                    failures.append({'ref': name, 'error': str(error)})
            continue
        if name not in expected:
            failures.append({'ref': name, 'error': 'No prior template allowlist entry'})
            continue
        try:
            accepted.append({'ref': name, **review_one(before, after, expected[name])})
        except ValueError as error:
            failures.append({'ref': name, 'error': str(error)})
    unknown_plan_refs = sorted(expected.keys()-ref.keys())
    report = {'status': 'PASS_BOUNDED_TEMPLATE_PIN_NORMALIZATION' if not (missing or extra or failures or unknown_plan_refs) else 'FAIL',
              'reference_directory': str(args.reference), 'candidate_directory': str(args.candidate),
              'plan': str(args.plan), 'plan_sha256': sha(args.plan),
              'source_files_sha256': {n: sha(args.reference/n) for n in ('pstchip.dat', 'pstxprt.dat', 'pstxnet.dat')},
              'candidate_files_sha256': {n: sha(args.candidate/n) for n in ('pstchip.dat', 'pstxprt.dat', 'pstxnet.dat')},
              'reference_parts': len(ref), 'candidate_parts': len(cand),
              'reference_primitives': nr, 'candidate_primitives': nc,
              'exact_effective_parts': exact, 'accepted_explicit_normalizations': accepted,
              'missing_parts': missing, 'extra_parts': extra, 'failures': failures,
              'unknown_plan_references': unknown_plan_refs,
              'scope': 'Only ordered pin-name declarations explicitly predicted from source/target library XML. Complete physical-number/electrical payload, body fields and sections remain exact. Primitive identity/PART_NAME changes are separately covered by the original strict report. Connectivity needs a separate PST partition comparison.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if not isinstance(v, (list, dict))}))
    print(json.dumps({k: len(v) for k, v in report.items() if isinstance(v, list)}))
    if report['status'] == 'FAIL':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
