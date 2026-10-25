"""Reusable geometry checks. No CAD API calls, project IDs or automatic deletion."""
import collections
import math
from _dependencies import configure
configure()
from shapely.geometry import box
from shapely.ops import unary_union


def wire_points(row):
    return [tuple(int(c) for c in point.split(',')) for point in row['points'].split(';')]


def point_on_polyline(point, points):
    x, y = point
    return any(
        (x-x1)*(y2-y1) == (y-y1)*(x2-x1)
        and min(x1,x2) <= x <= max(x1,x2)
        and min(y1,y2) <= y <= max(y1,y2)
        for (x1,y1),(x2,y2) in zip(points,points[1:])
    )


def grid_points_on_wire(points, grid, origin):
    """Only exact integer points on the existing wire. Never moves its geometry."""
    if grid <= 0 or int(grid) != grid:
        raise ValueError('Grid must be a positive integer in native document units')
    result = set()
    for a, b in zip(points, points[1:]):
        if any(c % grid for c in (*a, *b)):
            raise ValueError('Wire endpoint is not on the requested frozen grid')
        dx, dy = b[0]-a[0], b[1]-a[1]
        count = math.gcd(abs(dx)//grid, abs(dy)//grid)
        if not count:
            result.add(a)
            continue
        sx, sy = dx//count, dy//count
        result.update((a[0]+k*sx, a[1]+k*sy) for k in range(count+1))
    return sorted(result, key=lambda p: ((p[0]-origin[0])**2+(p[1]-origin[1])**2, p))


def same_wire_alias_port_proof(alias, port, wire, retained_visible_name):
    """Return exact same-net/on-wire evidence; caller decides local usefulness."""
    if not (alias['page'] == port['page'] == wire['page']):
        return None
    if alias['name'] != port['name'] or alias['name'] != retained_visible_name:
        return None
    if alias['owner_wire_id'] != wire['id'] or port['wire_id'] != wire['id']:
        return None
    if not wire['net_id'] or wire['net_id'] != port['net_id']:
        return None
    if not (alias['owner_wire_net'] == wire['net_name'] == port['net_name']):
        return None
    points = wire_points(wire)
    location = (int(alias['loc_x']), int(alias['loc_y']))
    hot = (int(port['actual_hot_x']), int(port['actual_hot_y']))
    if not point_on_polyline(location, points) or not point_on_polyline(hot, points):
        return None
    return {'page': wire['page'], 'alias_id': alias['id'], 'alias_name': alias['name'],
            'kept_port_id': port['id'], 'native_net_id': wire['net_id'],
            'native_net_name': wire['net_name'], 'wire_id': wire['id'],
            'wire_points': points, 'alias_location': location, 'kept_port_hotspot': hot,
            'same_exact_name': True, 'same_native_net': True,
            'both_points_on_exact_ownerwire': True,
            'distance': math.dist(location, hot),
            'deletion_authorized': False,
            'remaining_checks': 'local visual usefulness, kept text readability, strict XML allowlist and native electrical equivalence'}


def connected_wire_path(wires, start_wire_id, target, page, net_id):
    """Endpoint-to-segment graph only; a mid/mid crossing does not make an edge.

    Native compiled net IDs must agree before this geometric proof. Callers must
    also preserve junction/native connection-count evidence at each graph edge.
    """
    rows = {r['id']: r for r in wires if r['page'] == page and r['net_id'] == net_id}
    if start_wire_id not in rows:
        return None
    points = {i: wire_points(row) for i, row in rows.items()}
    todo = collections.deque([start_wire_id])
    previous = {start_wire_id: None}
    goal = None
    while todo:
        current = todo.popleft()
        if point_on_polyline(target, points[current]):
            goal = current
            break
        for other, pts in points.items():
            if other in previous:
                continue
            if any(point_on_polyline(p, pts) for p in (points[current][0], points[current][-1])) or any(
                point_on_polyline(p, points[current]) for p in (pts[0], pts[-1])
            ):
                previous[other] = current
                todo.append(other)
    if goal is None:
        return None
    path = []
    while goal is not None:
        path.append({'wire_id': goal, 'native_net_id': net_id, 'points': points[goal]})
        goal = previous[goal]
    return list(reversed(path))


def protected_geometry(scene, unknown_pin_offset=20):
    """Body envelopes and explicitly uncertain zero-length visible pin numbers.

    Normal visible pin text is already part of Scene.text. Hidden pin names or
    numbers do not create imaginary text obstacles. Pin strokes remain in
    Scene.geom even when their labels are hidden.
    """
    result = []
    bodies = collections.defaultdict(list)
    for item in scene.geom:
        if item['kind'] == 'body_stroke':
            bodies[(item['page'], item['owner_id'])].append(item['geometry'])
    for (page, owner), geometries in bodies.items():
        result.append({'page': page, 'id': owner+':bodyguard', 'owner_id': owner,
                       'kind': 'whole_body_guard',
                       'geometry': unary_union(geometries).convex_hull.buffer(.5)})
    for problem in scene.unresolved:
        if problem.get('reason') != 'ZERO_LENGTH_PIN_SIDE_REQUIRES_NATIVE_BOUNDARY':
            continue
        pin = scene.pins.get((problem['page'], problem['id']))
        if not pin or pin.get('visible') != '1':
            continue
        style = scene.styles.get((pin['page'], pin['part_id']), {})
        if style.get('pin_numbers_visible') == '0':
            continue
        font = dict(scene.defaultfonts.get('4', {}))
        font.pop('index', None)
        metric, _ = scene.metric(pin['pin_number'], font)
        width = max(metric['advance_width'], metric['ink_bounds'][2]-metric['ink_bounds'][0])
        height = metric['cell_height']
        x, y = float(pin['actual_hot_x']), float(pin['actual_hot_y'])
        result.append({'page': pin['page'], 'id': pin['pin_id']+':unknown-number',
                       'owner_id': pin['part_id'], 'kind': 'unknown_pin_number_guard',
                       'geometry': box(x-unknown_pin_offset-width, y-unknown_pin_offset-height,
                                       x+unknown_pin_offset+width, y+unknown_pin_offset+height)})
    return result
