"""Generate ASCII R/C display-value candidates from explicit JSON fields only.

Never reads or writes DSN/OLB. Missing/conflicting evidence produces REVIEW_NEEDED
with candidate_value=null. Original record fields are retained under metadata.
Explicit not-populated evidence is retained in the NC_ display prefix; package,
MPN and unrelated metadata are never searched for assembly-state substrings.
"""
from __future__ import annotations
import argparse
import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

NUMBER = r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?'
UNKNOWN = {'', '?', '-', 'n/a', 'na', 'unknown', 'tbd', 'unspecified'}
R_SCALE = {'': Decimal(1), 'R': Decimal(1), 'r': Decimal(1),
           'k': Decimal('1e3'), 'K': Decimal('1e3'), 'M': Decimal('1e6'),
           'm': Decimal('1e-3'), 'u': Decimal('1e-6'), 'G': Decimal('1e9')}
C_SCALE = {'': Decimal(1), 'p': Decimal('1e-12'), 'n': Decimal('1e-9'),
           'u': Decimal('1e-6'), 'm': Decimal('1e-3')}
ASSEMBLY_DNP = {'NI', 'DNP', 'DNI', 'NOT_INSTALLED', 'NOT_FITTED',
                'DO_NOT_POPULATE', 'DO_NOT_INSTALL', '\u7a7a\u8d34', '\u4e0d\u88c5', '\u4e0d\u8d34'}
ASSEMBLY_POPULATED = {'POPULATED', 'FITTED', 'INSTALLED', 'ASSEMBLED'}
RAW_ASSEMBLY_MARKERS = {'NI', 'DNP', 'DNI'}


def missing(value):
    return value is None or isinstance(value, str) and value.strip().casefold() in UNKNOWN


def numeric(value):
    if isinstance(value, bool):
        raise ValueError('Boolean is not a measurement')
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError('Invalid decimal number')
    if not result.is_finite() or len(result.as_tuple().digits) > 24 or abs(result.adjusted()) > 24:
        raise ValueError('Nonfinite or excessive numeric precision/range requires review')
    return result


def decimal_text(value):
    if value == 0:
        return '0'
    return format(value.normalize(), 'f')


def clean_units(value):
    if not isinstance(value, str) or len(value) > 256:
        raise ValueError('raw_value must be a short explicit string with units')
    value = unicodedata.normalize('NFKC', value).replace('\u00b5', 'u').replace('\u03bc', 'u')
    return re.sub(r'\s+', '', value.strip())


def resistance(value):
    s = clean_units(value).replace('\u03a9', 'R').replace('\u2126', 'R')
    s = re.sub(r'(?i:ohms?)$', 'R', s)
    embedded = re.fullmatch(r'([0-9]+)([RrKkM])([0-9]+)(?:R)?', s)
    if embedded:
        amount = numeric(embedded[1] + '.' + embedded[3]) * R_SCALE[embedded[2]]
    else:
        match = re.fullmatch('(' + NUMBER + r')([mkKMuG]?)[Rr]', s)
        if match:
            amount = numeric(match[1]) * R_SCALE[match[2]]
        else:
            match = re.fullmatch('(' + NUMBER + r')([kKMG])', s)
            if not match:
                if re.fullmatch('(' + NUMBER + ')m', s):
                    raise ValueError('Ambiguous m: use mR/mohm for milliohm or M for megaohm')
                raise ValueError('Unrecognized resistance/unit; bare numbers are not assumed to be ohms')
            amount = numeric(match[1]) * R_SCALE[match[2]]
    if amount < 0:
        raise ValueError('Negative resistance requires review')
    if amount == 0:
        return '0R'
    scale, unit = (Decimal('1e6'), 'M') if amount >= Decimal('1e6') else (
        (Decimal('1e3'), 'K') if amount >= Decimal('1e3') else (
            (Decimal(1), 'R') if amount >= 1 else (Decimal('1e-3'), 'mR')))
    return decimal_text(amount / scale) + unit


def capacitance(value):
    s = clean_units(value)
    embedded = re.fullmatch(r'([0-9]+)([pPnNuU])([0-9]+)[fF]?', s)
    if embedded:
        amount = numeric(embedded[1] + '.' + embedded[3]) * C_SCALE[embedded[2].lower()]
    else:
        match = re.fullmatch('(' + NUMBER + r')([pPnNuUmM]?)[fF]', s)
        if not match:
            raise ValueError('Unrecognized capacitance/unit; numeric codes are not decoded')
        if match[2] == 'M':
            raise ValueError('Ambiguous MF: explicitly use uF or mF, not legacy MF')
        amount = numeric(match[1]) * C_SCALE[match[2].lower()]
    if amount <= 0:
        raise ValueError('Capacitance must be positive')
    scale, unit = (Decimal('1e-6'), 'uF') if amount >= Decimal('1e-6') else (
        (Decimal('1e-9'), 'nF') if amount >= Decimal('1e-9') else (Decimal('1e-12'), 'pF'))
    return decimal_text(amount / scale) + unit


def package_code(value, family):
    if not isinstance(value, str):
        raise ValueError('Package must be an explicit string; leading zeroes must be retained')
    s = value.strip()
    prefixed = re.fullmatch(r'([RrCc])([0-9]{4,5})', s)
    if prefixed:
        if prefixed[1].upper() != family:
            raise ValueError('R/C package prefix conflicts with declared family; provide an evidence-backed canonical package')
        s = prefixed[2]
    if not s.isascii() or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.+\-]*', s):
        raise ValueError('Package must be one explicit ASCII code without whitespace or /')
    return s


def voltage(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        amount = numeric(value)  # Numeric rated_voltage is explicitly defined as volts.
    else:
        s = clean_units(value)
        embedded = re.fullmatch(r'([0-9]+)[Vv]([0-9]+)', s)
        match = re.fullmatch('(' + NUMBER + r')([mkK]?)[Vv]', s)
        if embedded:
            amount = numeric(embedded[1] + '.' + embedded[2])
        elif match:
            amount = numeric(match[1]) * {'': Decimal(1), 'm': Decimal('1e-3'), 'k': Decimal('1e3'), 'K': Decimal('1e3')}[match[2]]
        else:
            raise ValueError('rated_voltage string must include V; numeric fields use volts')
    if amount <= 0:
        raise ValueError('Rated voltage must be positive')
    return decimal_text(amount) + 'V'


def tolerance(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        amount = numeric(value)  # Numeric tolerance is percentage points, never a ratio.
    else:
        s = clean_units(value).removeprefix('+/-').removeprefix('\u00b1')
        match = re.fullmatch('(' + NUMBER + ')%', s)
        if not match:
            raise ValueError('Tolerance string must be a symmetric percentage, e.g.1%; no letter-code inference')
        amount = numeric(match[1])
    if not 0 < amount <= 100:
        raise ValueError('Tolerance must be a positive percentage no greater than100')
    return decimal_text(amount) + '%'


def assembly_inputs(record, raw):
    """Return the value text, explicit assembly evidence and validation issues.

    Only declared assembly fields and exact raw-value marker syntax count as
    evidence. In particular, NI in a package, MPN or historical metadata is not
    a population decision. An absent state remains UNSPECIFIED, not POPULATED.
    """
    evidence, issues = [], []
    value = raw
    if isinstance(value, str):
        value = value.strip()
        prefix = re.match(r'(?i)^NC_', value)
        if prefix:
            evidence.append({'origin': 'raw_value.NC_prefix', 'marker': value[:3], 'state': 'DNP'})
            value = value[3:].strip()
        suffix = re.search(r'/\s*(NI|DNP|DNI)\s*$', value, re.IGNORECASE)
        if suffix:
            evidence.append({'origin': 'raw_value.assembly_suffix', 'marker': suffix[1], 'state': 'DNP'})
            value = value[:suffix.start()].strip()
        if value.upper() in RAW_ASSEMBLY_MARKERS:
            evidence.append({'origin': 'raw_value.marker_only', 'marker': value, 'state': 'DNP'})
            value = ''  # An assembly marker never supplies an electrical value.
    for name in ('assembly_state', 'population'):
        marker = record.get(name)
        if marker is None or isinstance(marker, str) and not marker.strip():
            continue
        if not isinstance(marker, str):
            issues.append((name, 'invalid_assembly_state', 'Use an explicit NI/DNP or populated state string'))
            continue
        token = re.sub(r'[\s-]+', '_', marker.strip().upper())
        state = 'DNP' if token in ASSEMBLY_DNP else 'POPULATED' if token in ASSEMBLY_POPULATED else None
        if state is None:
            issues.append((name, 'unrecognized_assembly_state', 'Unrecognized assembly state is not discarded or guessed'))
        else:
            evidence.append({'origin': name, 'marker': marker, 'state': state})
    if record.get('dnp') is not None:
        marker = record['dnp']
        if not isinstance(marker, bool):
            issues.append(('dnp', 'invalid_assembly_state', 'dnp must be an explicit JSON Boolean'))
        else:
            evidence.append({'origin': 'dnp', 'marker': marker, 'state': 'DNP' if marker else 'POPULATED'})
    states = {item['state'] for item in evidence}
    if len(states) > 1:
        issues.append(('assembly_state', 'conflicting_assembly_state', 'Explicit populated and not-populated evidence conflict'))
    state = next(iter(states)) if len(states) == 1 else 'UNSPECIFIED'
    return value, state, evidence, issues


def normalize_record(record, index=0):
    result = {'index': index, 'metadata': copy.deepcopy(record), 'normalized_fields': {},
              'assembly_evidence': [], 'candidate_value': None, 'status': 'REVIEW_NEEDED',
              'issues': [], 'missing_fields': []}
    if not isinstance(record, dict):
        result['issues'].append({'field': 'record', 'code': 'invalid_record', 'detail': 'Expected an object'})
        return result
    issues, fields = result['issues'], result['normalized_fields']
    def issue(field, code, detail):
        issues.append({'field': field, 'code': code, 'detail': detail})
        if code.startswith('missing_') and field not in result['missing_fields']:
            result['missing_fields'].append(field)
    ref = record.get('ref')
    if not isinstance(ref, str) or not ref.strip():
        issue('ref', 'missing_ref', 'Explicit physical reference is required')
    else:
        result['ref'] = ref.strip()
    family = {'R': 'R', 'RESISTOR': 'R', 'C': 'C', 'CAPACITOR': 'C'}.get(str(record.get('family', '')).strip().upper())
    if family is None:
        issue('family', 'missing_or_unsupported_family', 'Declare R or C; never inferred from reference/footprint')
        return result
    fields['family'] = family
    raw, assembly_state, evidence, assembly_issues = assembly_inputs(record, record.get('raw_value'))
    fields['assembly_state'] = assembly_state
    fields['display_prefix'] = 'NC_' if assembly_state == 'DNP' else ''
    result['assembly_evidence'] = evidence
    for problem in assembly_issues:
        issue(*problem)
    compound = {}
    if missing(raw):
        issue('raw_value', 'missing_raw_value', 'Electrical value is unknown')
    elif not isinstance(raw, str):
        issue('raw_value', 'value_unit_required', 'raw_value must be a string with explicit units')
    else:
        parts = [s.strip() for s in raw.replace('+/-', '\u00b1').split('/')]
        expected = 3 if family == 'R' else 4
        if len(parts) == expected:
            compound = dict(zip(['package', 'tolerance'] if family == 'R' else ['package', 'rated_voltage', 'tolerance'], parts[1:]))
        elif len(parts) != 1:
            issue('raw_value', 'mixed_or_ambiguous_format', 'Use a single electrical value or the exact family-specific slash format')
        try:
            fields['electrical_value'] = (resistance if family == 'R' else capacitance)(parts[0])
        except ValueError as error:
            issue('raw_value', 'invalid_or_mixed_electrical_value', str(error))
    required = ['package', 'tolerance'] if family == 'R' else ['package', 'rated_voltage', 'tolerance']
    for name in required:
        normalize = (lambda v: package_code(v, family)) if name == 'package' else voltage if name == 'rated_voltage' else tolerance
        supplied = []
        for origin, value in [('explicit', record.get(name)), ('compound_raw_value', compound.get(name))]:
            if missing(value):
                continue
            try:
                supplied.append((origin, normalize(value)))
            except ValueError as error:
                issue(name, 'invalid_' + name, origin + ': ' + str(error))
        if not supplied:
            issue(name, 'missing_' + name, 'No valid explicit value; no example/default is substituted')
        else:
            fields[name] = supplied[0][1]
            if len({v for _, v in supplied}) > 1:
                issue(name, 'conflicting_' + name, 'Explicit and compound values differ: ' + repr(supplied))
    if not issues:
        order = ['electrical_value', 'package'] + (['rated_voltage'] if family == 'C' else []) + ['tolerance']
        candidate = fields['display_prefix'] + '/'.join(fields[name] for name in order)
        assert candidate.isascii()
        result['candidate_value'] = candidate
        result['status'] = 'READY'
    return result


def normalize_document(data):
    records = data.get('records') if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise ValueError('Input must be a record list or an object with records list')
    results = [normalize_record(row, i) for i, row in enumerate(records)]
    references = {}
    for row in results:
        if row.get('ref'):
            references.setdefault(row['ref'].casefold(), []).append(row)
    for duplicates in references.values():
        if len(duplicates) > 1:
            for row in duplicates:
                row['issues'].append({'field': 'ref', 'code': 'duplicate_reference', 'detail': 'Multiple input records require an explicit resolution'})
                row['candidate_value'], row['status'] = None, 'REVIEW_NEEDED'
    ready = sum(r['status'] == 'READY' for r in results)
    return {'schema': 'RC_VALUE_FORMAT_CANDIDATES_V1', 'rules_version': 2,
            'status': 'READY' if ready == len(results) else 'REVIEW_NEEDED',
            'input_metadata': {k: copy.deepcopy(v) for k, v in data.items() if k != 'records'} if isinstance(data, dict) else {},
            'summary': {'records': len(results), 'ready': ready, 'review_needed': len(results) - ready},
            'records': results, 'scope': 'Offline candidates only; no DSN/OLB or original user library is opened or modified.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--fail-on-review', action='store_true')
    args = parser.parse_args()
    if args.input.suffix.lower() != '.json' or args.output.suffix.lower() != '.json':
        parser.error('Input and new candidate output must be .json files, never DSN/OLB')
    raw = args.input.read_bytes()
    def reject_constant(value):
        raise ValueError('Non-JSON numeric constant: ' + value)
    data = json.loads(raw.decode('utf-8-sig'), parse_constant=reject_constant)
    result = normalize_document(data)
    result['input_sha256'] = hashlib.sha256(raw).hexdigest().upper()
    if args.input.read_bytes() != raw:
        raise ValueError('Input changed while generating candidates')
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(result['summary']))
    return 2 if args.fail_on_review and result['summary']['review_needed'] else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
