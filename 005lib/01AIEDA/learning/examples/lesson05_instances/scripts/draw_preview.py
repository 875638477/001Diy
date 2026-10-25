"""Draw a learning PNG from native lesson05 readback TSVs (no PDF file output)."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys

sys.path.insert(0, 'D:/001DIY/005lib/01AIEDA/learning/tools/pymupdf_1_28_2')
import pymupdf as fitz

def parse_skill(value):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', value)
    idx = 0
    def item():
        nonlocal idx
        token = tokens[idx]
        idx += 1
        if token == '(':
            out = []
            while tokens[idx] != ')':
                out.append(item())
            idx += 1
            return out
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
    result = item()
    if idx != len(tokens):
        raise ValueError(value)
    return result

def table(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def same_xy(row, origin):
    return abs(float(row['sx']) - origin[0]) < 1e-7 and abs(float(row['sy']) - origin[1]) < 1e-7

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', type=Path, default=Path('D:/001DIY/005lib/01AIEDA/learning/examples/lesson05_instances'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    base = args.base.resolve()
    output = args.output.resolve()
    if base in output.parents:
        parser.error('PNG must remain outside the read-only lesson directory')
    paths = [base/'spec.json'] + [base/'logs/reopen'/f'{name}.tsv' for name in ['symbols', 'pins', 'children']]
    before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    spec = json.loads(paths[0].read_text(encoding='utf-8-sig'))
    symbols, pins, children = [table(p) for p in paths[1:]]
    assert len(symbols) == 3 and len(pins) == 288 and len(children) == 33
    doc = fitz.open()
    page = doc.new_page(width=1536, height=980)
    page.insert_font(fontname='CN', fontfile='C:/Windows/Fonts/msyh.ttc')
    page.insert_font(fontname='CB', fontfile='C:/Windows/Fonts/msyhbd.ttc')
    navy = (0.10, 0.17, 0.24)
    muted = (0.36, 0.43, 0.49)
    light = (0.95, 0.97, 0.98)
    orange = (0.93, 0.52, 0.18)
    copper_edge = (0.66, 0.32, 0.09)
    mask_fill = (0.84, 0.94, 0.97)
    mask_edge = (0.23, 0.62, 0.72)
    green = (0.16, 0.52, 0.39)
    red = (0.79, 0.19, 0.20)
    blue = (0.13, 0.37, 0.65)

    def text(x, y, value, size=14, color=navy, bold=False):
        page.insert_text((x, y), value, fontsize=size, fontname='CB' if bold else 'CN', color=color)

    def line(a, b, color=muted, width=1, dashes=None):
        page.draw_line(a, b, color=color, width=width, dashes=dashes)

    def arrow(a, b, color, width=1.6):
        line(a, b, color, width)
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        ux, uy = dx/length, dy/length
        line(b, (b[0]-7*ux+3*uy, b[1]-7*uy-3*ux), color, width)
        line(b, (b[0]-7*ux-3*uy, b[1]-7*uy+3*ux), color, width)

    page.draw_rect(page.rect, color=None, fill=(1, 1, 1))
    text(36, 58, '第 5 课｜实例移动、旋转与换层镜像', 30, bold=True)
    text(37, 90, '按 Allegro 原生只读重开数据绘制 · 非 Cadence 截图 · 所有几何均来自 reopen TSV', 15, muted)
    page.draw_rect((38, 113, 58, 126), color=mask_edge, fill=mask_fill, width=1)
    text(68, 126, '阻焊开窗 mask', 13)
    page.draw_rect((226, 113, 246, 126), color=copper_edge, fill=orange, width=1)
    text(256, 126, '铜焊盘 copper', 13)
    line((417, 119), (448, 119), green, 1.5, '[5 3] 0')
    text(458, 126, 'PlaceBound / 高度', 13)
    line((654, 119), (674, 119), blue, 1.8)
    line((664, 109), (664, 129), blue, 1.8)
    text(684, 126, '三项文字共用的原点锚点', 13)
    page.draw_rect((966, 113, 986, 126), color=red, width=2)
    text(996, 126, 'Pin 1 教学标注', 13)

    titles = {'MOVE': '移动 MOVE', 'ROTATE': '旋转 ROTATE', 'MIRROR': '换层镜像 MIRROR'}
    summaries = []
    for i, case in enumerate(spec['cases']):
        left = 32 + i * 504
        right = left + 464
        page.draw_rect((left, 151, right, 892), color=(0.82, 0.87, 0.90), fill=light, width=1)
        origin = tuple(case['final'])
        sym = [s for s in symbols if abs(float(s['x'])-origin[0]) < 1e-7 and abs(float(s['y'])-origin[1]) < 1e-7][0]
        mirror = sym['mirrored'] == 't'
        side = 'BOTTOM' if mirror else 'TOP'
        actual_angle = float(sym['rotation'])
        text(left+22, 187, titles[case['id']], 22, bold=True)
        if case['id'] == 'MOVE':
            sub = 'Δ = (+1.877, +5.456) mm · TOP'
        elif case['id'] == 'ROTATE':
            sub = '+90° 逆时针 · 围绕自身原点 · TOP'
        else:
            sub = '镜像并转到 BOTTOM · 板全局 XY 顶视'
        text(left+22, 216, sub, 13, muted)
        center = (left+232, 410)
        scale = 72.0
        def project(xy):
            return fitz.Point(center[0]+(xy[0]-origin[0])*scale,
                              center[1]-(xy[1]-origin[1])*scale)
        def rect(box):
            a, b = project(box[0]), project(box[1])
            return fitz.Rect(min(a.x, b.x), min(a.y, b.y), max(a.x, b.x), max(a.y, b.y))
        rows = [p for p in pins if same_xy(p, origin)]
        child_rows = [c for c in children if same_xy(c, origin)]
        mask_rows = [p for p in rows if p['layer'] == 'PIN/SOLDERMASK_'+side]
        copper_rows = [p for p in rows if p['layer'] == 'ETCH/'+side]
        assert len(mask_rows) == len(copper_rows) == 16
        for row in mask_rows:
            bb = parse_skill(row['bbox'])
            xy = (float(row['x']), float(row['y']))
            box = [[xy[0]+bb[0][0], xy[1]+bb[0][1]], [xy[0]+bb[1][0], xy[1]+bb[1][1]]]
            page.draw_rect(rect(box), color=mask_edge, fill=mask_fill, width=0.9)
        for row in copper_rows:
            verts = parse_skill(row['poly_vertices'])
            assert row['figure'] == 'RECTANGLE' and verts is not None
            points = [project(v[0]) for v in verts]
            shape = page.new_shape()
            shape.draw_polyline(points+[points[0]])
            is_pin1 = row['number'] == '1'
            shape.finish(color=red if is_pin1 else copper_edge, fill=orange, width=2.3 if is_pin1 else 0.8, closePath=True)
            shape.commit()
            dx, dy = float(row['x'])-origin[0], float(row['y'])-origin[1]
            if abs(dx) > abs(dy):
                dx = math.copysign(0.96, dx)
            else:
                dy = math.copysign(0.96, dy)
            pp = project((origin[0]+dx, origin[1]+dy))
            # Center labels using an approximate glyph width; geometry remains native.
            text(pp.x - (4 if len(row['number']) == 1 else 7), pp.y+4,
                 row['number'], 12, red if is_pin1 else navy, is_pin1)
        pbs = [c for c in child_rows if c['type'] == 'shape' and 'PLACE_BOUND_' in c['layer']]
        assert len(pbs) == 1
        pb = pbs[0]
        pb_box = parse_skill(pb['bbox'])
        props = dict(parse_skill(pb['props']))
        page.draw_rect(rect(pb_box), color=green, width=1.5, dashes='[6 4] 0')
        pbr = rect(pb_box)
        text(pbr.x0, pbr.y0-9, 'PlaceBound '+side, 11, green, True)

        texts = [c for c in child_rows if c['type'] == 'text']
        assert len(texts) == 3
        for c in texts:
            assert abs(float(c['x'])-origin[0]) < 1e-7 and abs(float(c['y'])-origin[1]) < 1e-7
        anchor = project((float(texts[0]['x']), float(texts[0]['y'])))
        page.draw_circle(anchor, 7, color=blue, fill=(1, 1, 1), width=1.3)
        line((anchor.x-10, anchor.y), (anchor.x+10, anchor.y), blue, 1.8)
        line((anchor.x, anchor.y-10), (anchor.x, anchor.y+10), blue, 1.8)
        rad = math.radians(float(texts[0]['rotation']))
        end = (anchor.x+40*math.cos(rad), anchor.y-40*math.sin(rad))
        arrow((anchor.x, anchor.y), end, blue)
        text(anchor.x-43, anchor.y+26, '3 文字锚点重合', 10.5, blue)

        ax = left+26
        ay = 570
        arrow((ax, ay), (ax+28, ay), muted, 1)
        arrow((ax, ay), (ax, ay-28), muted, 1)
        text(ax+33, ay+4, '+X', 10, muted)
        text(ax-7, ay-35, '+Y', 10, muted)
        line((center[0]-36, 577), (center[0]+36, 577), navy, 1.2)
        line((center[0]-36, 573), (center[0]-36, 581), navy, 1.2)
        line((center[0]+36, 573), (center[0]+36, 581), navy, 1.2)
        text(center[0]-18, 595, '1 mm', 10, muted)

        pin1 = [p for p in copper_rows if p['number'] == '1'][0]
        text(left+22, 627, '原点 O = ({:.3f}, {:.3f}) mm'.format(*origin), 15, navy, True)
        text(left+22, 653, 'PIN 1 = ({:.3f}, {:.3f}) mm'.format(float(pin1['x']), float(pin1['y'])), 13, red, True)
        text(left+22, 680, '铜 16 个 / mask 16 个 · 实际 '+side+' 图层', 12.5, muted)
        line((left+22, 699), (right-22, 699), (0.80, 0.85, 0.88), 0.8)
        text(left+22, 723, '文字锚点（均等于 O）', 13, bold=True)
        sorted_texts = sorted(texts, key=lambda c: c['layer'])
        for j, c in enumerate(sorted_texts):
            layer = c['layer']
            label = 'Value / 装配' if layer.startswith('COMPONENT VALUE') else ('RefDes / 丝印' if 'SILKSCREEN' in layer else 'RefDes / 装配')
            data = '{}  {}°  {}'.format(side, int(float(c['rotation'])), '镜像' if c['mirrored'] == 't' else '无镜像')
            text(left+22, 750+j*25, label, 12)
            text(left+190, 750+j*25, data, 11.5, muted)
        width = pb_box[1][0]-pb_box[0][0]
        height = pb_box[1][1]-pb_box[0][1]
        text(left+22, 841, 'PB {:.3f} × {:.3f} mm · filled={}'.format(width, height, pb['filled']), 12, green, True)
        text(left+22, 865, 'PACKAGE_HEIGHT_MAX = '+props['PACKAGE_HEIGHT_MAX'], 12, green)
        summaries.append({'case': case['id'], 'origin': origin, 'side': side,
                          'copper_polygons': len(copper_rows), 'mask_rectangles': len(mask_rows),
                          'text_anchors': len(texts), 'placebound': pb_box,
                          'height': props['PACKAGE_HEIGHT_MAX'],
                          'pin1_xy': [float(pin1['x']), float(pin1['y'])]})

    text(37, 923, 'refdes = nil：三个未分配 PACKAGE 实例；不含网络，未绘布线。文字仅显示锚点/方向，不是字形渲染。', 13, muted)
    text(37, 950, 'BOTTOM 面板保留板全局 XY 顶视，不再次从底面翻图。数据源：logs/reopen/{symbols,pins,children}.tsv', 12, muted)
    output.parent.mkdir(parents=True, exist_ok=True)
    page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(output)
    after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before == after
    print(json.dumps({'png': str(output), 'pixels': [2304, 1470], 'drawn_from': [str(p) for p in paths[1:]],
        'input_files_unchanged': before == after, 'cases': summaries,
        'cadence_screenshot': False, 'pdf_written': False}, indent=2))

if __name__ == '__main__':
    main()
