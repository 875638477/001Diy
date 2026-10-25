"""Read-only validator for Allegro lesson05 TSV snapshots; Python stdlib only.

Usage: python validate_lesson05.py --base LESSON_DIR --report TEMP_REPORT.json
No EDA inputs are changed. The output path must be supplied explicitly.
"""
import argparse
import collections
import csv
import datetime
import hashlib
import json
import math
import pathlib
import re
import sys

EPS = 1e-7
checks = collections.Counter()
failures = []

def check(condition, group, detail):
    checks[group] += 1
    if not condition:
        failures.append({"group": group, "detail": detail})

def close(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= EPS
    return a == b

def sexpr(s):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', s)
    pos = 0
    def parse():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        if token == '(':
            result = []
            while pos < len(tokens) and tokens[pos] != ')':
                result.append(parse())
            if pos == len(tokens):
                raise ValueError('Unclosed SKILL list: ' + s)
            pos += 1
            return result
        if token == ')':
            raise ValueError('Unexpected SKILL closing parenthesis')
        if token == 'nil':
            return None
        if token == 't':
            return True
        if token.startswith('"'):
            return json.loads(token)
        try:
            return float(token)
        except ValueError:
            return token
    value = parse()
    if pos != len(tokens):
        raise ValueError('Trailing SKILL tokens: ' + s)
    return value

def f(row, key):
    return float(row[key])

def truth(row, key):
    return row[key] == 't'

def transform(point, center, angle, mirror=False):
    x, y = point
    if mirror:
        x = -x
    rad = math.radians(angle)
    return (center[0] + x * math.cos(rad) - y * math.sin(rad),
            center[1] + x * math.sin(rad) + y * math.cos(rad))

def bounds(points):
    return [[min(p[0] for p in points), min(p[1] for p in points)],
            [max(p[0] for p in points), max(p[1] for p in points)]]

def corners(box):
    return [(box[0][0], box[0][1]), (box[1][0], box[0][1]),
            (box[1][0], box[1][1]), (box[0][0], box[1][1])]

def points_equal(a, b):
    return len(a) == len(b) and all(close(x, y) for x, y in
        zip(sorted(a), sorted(b)))

def layer_for(layer, mirror):
    return layer.replace('_TOP', '_BOTTOM').replace('/TOP', '/BOTTOM') if mirror else layer

def angle_equal(actual, expected):
    return abs((actual - expected + 180) % 360 - 180) <= EPS

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return h.hexdigest().upper()

def read_table(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def signature(rows):
    return collections.Counter(tuple(sorted(row.items())) for row in rows)

def case_at(row, cases, initial=False, symbol=False):
    point = (f(row, 'x' if symbol else 'sx'), f(row, 'y' if symbol else 'sy'))
    matches = [c for c in cases if close(point, c['initial' if initial else 'final'])]
    if len(matches) != 1:
        raise ValueError('Cannot identify unique case at ' + repr(point))
    return matches[0]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True, type=pathlib.Path)
    parser.add_argument('--report', required=True, type=pathlib.Path)
    args = parser.parse_args()
    base = args.base.resolve()
    report_path = args.report.resolve()
    if base == report_path or base in report_path.parents:
        parser.error('Report must be outside the read-only lesson directory')
    spec_path = base / 'spec.json'
    spec = json.loads(spec_path.read_text(encoding='utf-8-sig'))
    source_path = pathlib.Path(spec['sourceSpec'])
    src = json.loads(source_path.read_text(encoding='utf-8-sig'))
    cases = spec['cases']
    pin_specs = {str(p['number']): p for p in src['pins']}
    stages = {'before': base / 'logs/create02/before',
              'after': base / 'logs/create02/after',
              'after_save': base / 'logs/create02/after_save',
              'reopen': base / 'logs/reopen'}
    inputs = [p for p in base.rglob('*') if p.is_file()] + [source_path]
    initial_hashes = {str(p): sha(p) for p in inputs}
    snapshots = {}
    stage_counts = {}
    for stage, directory in stages.items():
        initial = stage == 'before'
        tables = {name: read_table(directory / (name + '.tsv'))
                  for name in ['symbols', 'pins', 'children']}
        snapshots[stage] = tables
        counts = collections.Counter()
        for name, expected in [('symbols', 3), ('pins', 288), ('children', 33)]:
            check(len(tables[name]) == expected, 'row_counts', stage + '/' + name)
            counts[name + '_rows'] = len(tables[name])
        seen_symbols = set()
        for row in tables['symbols']:
            case = case_at(row, cases, initial, True)
            key = case['id']
            check(key not in seen_symbols, 'symbol_identity', stage + '/' + key)
            seen_symbols.add(key)
            angle = 0 if initial else case['rotation']
            mirror = False if initial else case['mirror']
            check(angle_equal(f(row, 'rotation'), angle), 'symbol_transform', stage + '/' + key + '/angle')
            check(truth(row, 'mirrored') == mirror, 'symbol_transform', stage + '/' + key + '/mirror')
            check(row['name'].lower() == src['footprint'].lower(), 'symbol_identity', stage + '/' + key + '/name')
            check(int(row['pins']) == 16 and int(row['children']) == 11, 'symbol_identity', stage + '/' + key + '/membership')
            check(row['refdes'] == 'nil', 'scope', stage + '/' + key + '/unassigned')
        seen_pin_layers = set()
        layer_sets = collections.defaultdict(set)
        for row in tables['pins']:
            case = case_at(row, cases, initial)
            cid = case['id']
            p = pin_specs[row['number']]
            center = case['initial' if initial else 'final']
            angle = 0 if initial else case['rotation']
            mirror = False if initial else case['mirror']
            label = '{}/{}/pin{}/{}'.format(stage, cid, row['number'], row['layer'])
            key = (cid, row['number'], row['layer'])
            check(key not in seen_pin_layers, 'pin_layer_identity', label)
            seen_pin_layers.add(key)
            layer_sets[(cid, row['number'])].add(row['layer'])
            expected_xy = transform((p['x'], p['y']), center, angle, mirror)
            check(close((f(row, 'x'), f(row, 'y')), expected_xy), 'pin_xy', label)
            check(close((f(row, 'relx'), f(row, 'rely')), (p['x'], p['y'])), 'pin_relative_xy', label)
            expected_angle = angle + (-p['rotation'] if mirror else p['rotation'])
            check(angle_equal(f(row, 'rotation'), expected_angle), 'pin_rotation', label)
            check(angle_equal(f(row, 'relrotation'), p['rotation']), 'pin_relative_rotation', label)
            check(truth(row, 'mirrored') == mirror, 'pin_mirror', label)
            side = 'BOTTOM' if mirror else 'TOP'
            active = row['layer'].endswith(side)
            counts['active_pad_rows' if active else 'null_pad_rows'] += 1
            check(row['figure'] == ('RECTANGLE' if active else 'NULL'), 'pad_side_and_type', label)
            check(truth(row, 'on_layer') == active, 'copper_side_presence', label)
            kind = 'mask' if 'SOLDERMASK' in row['layer'] else 'paste' if 'PASTEMASK' in row['layer'] else 'copper'
            width, height = src['pad'][kind]
            local_corners = corners([[-width / 2, -height / 2], [width / 2, height / 2]])
            rotated_local = [transform(q, (0, 0), expected_angle) for q in local_corners]
            expected_box = bounds(rotated_local) if active else [[0, 0], [0, 0]]
            check(close(sexpr(row['bbox']), expected_box), 'pad_bbox', label)
            poly_box = sexpr(row['poly_bbox'])
            poly_vertices = sexpr(row['poly_vertices'])
            if kind == 'copper' and active:
                counts['copper_polygons'] += 1
                global_corners = [transform(q, expected_xy, expected_angle) for q in local_corners]
                check(close(poly_box, bounds(global_corners)), 'polygon_bbox', label)
                check(isinstance(poly_vertices, list) and len(poly_vertices) in (4, 5), 'polygon_vertex_count', label)
                if isinstance(poly_vertices, list):
                    vertices = [tuple(v[0]) for v in poly_vertices]
                    if len(vertices) == 5 and close(vertices[0], vertices[-1]):
                        vertices.pop()
                    counts['copper_polygon_vertices'] += len(vertices)
                    check(all(close(v[1], 0) for v in poly_vertices), 'polygon_straight_edges', label)
                    check(points_equal(vertices, global_corners), 'polygon_vertices', label)
                    check(close(bounds(vertices), poly_box), 'polygon_bbox_vs_vertices', label)
                    area = abs(sum(vertices[i][0] * vertices[(i+1) % len(vertices)][1]
                        - vertices[(i+1) % len(vertices)][0] * vertices[i][1]
                        for i in range(len(vertices)))) / 2
                    check(close(area, width * height), 'polygon_area', label)
            else:
                check(poly_box is None and poly_vertices is None, 'polygon_absence', label)
        expected_layers = {'ETCH/TOP', 'ETCH/BOTTOM', 'PIN/SOLDERMASK_TOP', 'PIN/SOLDERMASK_BOTTOM', 'PIN/PASTEMASK_TOP', 'PIN/PASTEMASK_BOTTOM'}
        check(len(layer_sets) == 48, 'physical_pin_count', stage)
        for key, layers in layer_sets.items():
            check(layers == expected_layers, 'six_layers_per_pin', stage + '/' + repr(key))
        seen_text = set()
        seen_pb = set()
        paths = collections.defaultdict(list)
        for row in tables['children']:
            case = case_at(row, cases, initial)
            cid = case['id']
            center = case['initial' if initial else 'final']
            angle = 0 if initial else case['rotation']
            mirror = False if initial else case['mirror']
            label = stage + '/' + cid + '/' + row['type'] + '/' + row['layer']
            counts['child_' + row['type']] += 1
            if row['type'] == 'text':
                matching = [t for t in src['texts'] if layer_for(t['layer'], mirror) == row['layer'] and t['text'] == row['text']]
                check(len(matching) == 1, 'text_identity', label)
                key = (cid, row['layer'], row['text'])
                check(key not in seen_text, 'text_identity', label + '/unique')
                seen_text.add(key)
                if matching:
                    t = matching[0]
                    check(close((f(row, 'x'), f(row, 'y')), transform((t['x'], t['y']), center, angle, mirror)), 'text_anchor', label)
                check(angle_equal(f(row, 'rotation'), angle), 'text_angle', label)
                check(truth(row, 'mirrored') == mirror, 'text_mirror', label)
                if not initial:
                    original = [b for b in snapshots['before']['children'] if case_at(b, cases, True)['id'] == cid and b['type'] == 'text' and layer_for(b['layer'], mirror) == row['layer'] and b['text'] == row['text']]
                    if len(original) == 1:
                        bb = sexpr(original[0]['bbox'])
                        initial_center = case['initial']
                        rel = [(x-initial_center[0], y-initial_center[1]) for x, y in corners(bb)]
                        check(close(sexpr(row['bbox']), bounds([transform(q, center, angle, mirror) for q in rel])), 'text_bbox_transform', label)
            elif row['type'] == 'shape':
                check(cid not in seen_pb, 'placebound_identity', label + '/unique')
                seen_pb.add(cid)
                check(row['layer'] == layer_for('PACKAGE GEOMETRY/PLACE_BOUND_TOP', mirror), 'placebound_layer', label)
                pb = src['placeBound']
                expected_box = bounds([transform(q, center, angle, mirror) for q in corners([pb['min'], pb['max']])])
                check(close(sexpr(row['bbox']), expected_box), 'placebound_bbox', label)
                check(truth(row, 'filled') == pb['filled'], 'placebound_filled', label)
                props = dict(sexpr(row['props']) or [])
                check(props.get('PACKAGE_HEIGHT_MAX') == spec['height'] == pb['PACKAGE_HEIGHT_MAX'], 'placebound_height', label)
            elif row['type'] == 'path':
                paths[(cid, row['layer'])].append(sexpr(row['bbox']))
            else:
                check(False, 'child_type', label)
        check(len(seen_text) == 9 and len(seen_pb) == 3, 'child_counts', stage)
        for case in cases:
            cid = case['id']
            center = case['initial' if initial else 'final']
            angle = 0 if initial else case['rotation']
            mirror = False if initial else case['mirror']
            for kind, layer in [('assembly', 'PACKAGE GEOMETRY/ASSEMBLY_TOP'), ('silkscreen', 'PACKAGE GEOMETRY/SILKSCREEN_TOP')]:
                actual = paths[(cid, layer_for(layer, mirror))]
                expected = []
                half_width = src[kind]['width'] / 2
                for path in src[kind]['paths']:
                    bb = bounds([transform(q, center, angle, mirror) for q in path])
                    expected.append([[bb[0][0]-half_width, bb[0][1]-half_width], [bb[1][0]+half_width, bb[1][1]+half_width]])
                check(len(actual) == len(expected), 'path_counts', stage + '/' + cid + '/' + kind)
                check(close(sorted(actual), sorted(expected)), 'path_bbox_transform', stage + '/' + cid + '/' + kind)
        stage_counts[stage] = dict(counts)
    persistence = {}
    for left, right in [('after', 'after_save'), ('after_save', 'reopen')]:
        for table in ['symbols', 'pins', 'children']:
            a, b = snapshots[left][table], snapshots[right][table]
            same = signature(a) == signature(b)
            byte_same = (stages[left] / (table + '.tsv')).read_bytes() == (stages[right] / (table + '.tsv')).read_bytes()
            persistence[left + '->' + right + '/' + table] = {'semantic_equal': same, 'byte_equal': byte_same, 'rows': len(a)}
            check(same, 'persistence', left + '->' + right + '/' + table)
    operations = (base / 'logs/create02/operations.txt').read_text(encoding='utf-8-sig')
    summary = (base / 'logs/reopen/summary.txt').read_text(encoding='utf-8-sig')
    check('LESSON05 COMPLETE' in operations, 'native_completion', 'create02')
    check('LESSON05_READ COMPLETE' in summary and 'units=("millimeters" 3)' in summary and 'symbols=3 drcs=0 drcState=t' in summary, 'native_completion', 'reopen')
    evidence = {'single_object_return_initial_car_error': 'car: argument #1 should be a list' in (base / 'logs/create/stdout.txt').read_text(encoding='utf-8-sig'),
                'old_dbid_type_predicate_true_after_save': 'old_symbol_dbid_is_type_after_save=t' in operations,
                'qt_thread_assertion_in_create02_stderr': 'ASSERT failure' in (base / 'logs/create02/stderr.txt').read_text(encoding='utf-8-sig')}
    final_hashes = {str(p): sha(p) for p in inputs}
    check(initial_hashes == final_hashes, 'read_only_input_hashes', 'all inspected lesson inputs and source spec unchanged during validation')
    report = {'validator': 'lesson05 independent standard-library validation',
        'base': str(base), 'time_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'numeric_tolerance_mm': EPS, 'pass': not failures,
        'checks': dict(checks), 'total_checks': sum(checks.values()), 'failures': failures,
        'stage_counts': stage_counts, 'persistence': persistence, 'evidence': evidence,
        'input_sha256': initial_hashes,
        'limitations': [
            'This board contains three unassigned PACKAGE symbol instances (refdes nil), not three Capture-netlisted components; networks and electrical connectivity are not tested.',
            'Mask/paste pad dimensions and side mapping are verified from axlDBGetPad fields. on_layer was exported using axlPadOnLayer on the copper side, so it is not an independent mask/paste presence query.',
            'Only copper polygons were exported. Mask/paste actual polygon vertices, path segments/width and text rendering are not present in these TSVs; path bounding boxes and text bounding-box transformations are checked instead.',
            'This mm/3 exercise does not explain the earlier mil/0 polygon bbox versus vertices discrepancy.',
            'Qt thread assertion remains present in create02 stderr although completion and independent persisted readback pass; clean exit cannot be inferred from stderr alone.',
            'DRC zero is not datasheet, assembly-process, net connectivity, SI, PI or EMI acceptance.',
            'axlIsDBIDType true after save confirms the value type only. The export script reacquires symbols and does not dereference the old dbid.'
        ]}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pass': report['pass'], 'total_checks': report['total_checks'],
        'failures': failures, 'reopen_counts': stage_counts['reopen'],
        'persistence': persistence, 'evidence': evidence,
        'report': str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if report['pass'] else 1

if __name__ == '__main__':
    sys.exit(main())
