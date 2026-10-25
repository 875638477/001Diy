"""Emit display-only candidate plans. Never imports XML or modifies a CAD design.

No automatic Alias deletion or wire extension. Those need a separately approved
exact proof and native electrical gate. Candidate property moves are bounded to
keep RefDes/Value associated with their part instead of chasing zero collisions.
"""
import argparse
import collections
import hashlib
import json
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _dependencies import configure, add_options
configure()
from capture_layout_scene import Scene, collisions, table, validate_bindings
from xml_support import save_json
from layout_geometry import grid_points_on_wire, wire_points, point_on_polyline, protected_geometry
from shapely.geometry import box
from shapely.affinity import translate
from shapely.strtree import STRtree


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for key in ['xml', 'native', 'text-native', 'output']:
        ap.add_argument('--'+key, required=True, type=pathlib.Path)
    ap.add_argument('--part-frames',type=pathlib.Path,help='Same-save native affine TSV; required for nonzero part poses')
    ap.add_argument('--grid', required=True, type=int)
    ap.add_argument('--max-property-displacement', type=int, default=40,
                    help='Maximum Manhattan translation from current local property position; document units')
    ap.add_argument('--text-clearance', type=float, default=.5)
    ap.add_argument('--unknown-pin-offset', type=int, default=20)
    ap.add_argument('--font-cache', type=pathlib.Path)
    ap.add_argument('--page-filter')
    add_options(ap)
    a = ap.parse_args()
    if a.grid <= 0 or a.max_property_displacement < 0 or a.text_clearance < 0:
        ap.error('Grid must be positive; displacement and clearance must be nonnegative')
    a.output.mkdir(parents=True, exist_ok=True)
    source_sha = hashlib.sha256(a.xml.read_bytes()).hexdigest()
    scene = Scene(a).build()
    binding = validate_bindings(scene)
    core = {'alias', 'port_name', 'power_name', 'part_display'}
    baseline = collisions(scene.text, scene.geom)
    affected = {(r['page'],r[k+'_id']) for r in baseline for k in ['a','b'] if r[k+'_kind'] in core}
    native_aliases = {(r['page'],r['id']):r for r in table(a.native/'aliases.tsv')}
    wires = {(r['page'],r['id']):r for r in table(a.native/'wires.tsv')}
    # Bind to the saved XML/native pair; stale IDs are unsafe after Save/reopen.
    for t in scene.text:
        if t['kind']=='alias':
            row=native_aliases.get((t['page'],t['id']))
            if not row or row['name']!=t['text'] or row['owner_wire_id']!=t['owner_id']:
                raise ValueError('Stale native Alias inventory')
    working=[dict(t) for t in scene.text]
    fixed=scene.geom+protected_geometry(scene,a.unknown_pin_offset)
    bypage=collections.defaultdict(list)
    for item in fixed:bypage[item['page']].append(item)
    indexes={p:STRtree([g['geometry'] for g in gs]) for p,gs in bypage.items()}
    plans=[];reviews=[]
    for t in working:
        if (t['page'],t['id']) not in affected:continue
        if t['rotation'] and t['kind']!='alias':
            reviews.append({'page':t['page'],'id':t['id'],'reason':'ROTATED_PROPERTY_REQUIRES_SEPARATE_REVIEW'})
            continue
        page=t['page'];others=[o for o in working if o['page']==page and o['id']!=t['id']]
        text_geometries=[o['geometry'].buffer(a.text_clearance) for o in others]
        ti=STRtree(text_geometries)
        points=[]
        if t['kind']=='alias':
            wire=wires[(page,t['owner_id'])];wp=wire_points(wire)
            if not point_on_polyline(tuple(t['anchor']),wp):
                reviews.append({'page':page,'id':t['id'],'reason':'SOURCE_ALIAS_NOT_ON_EXACT_OWNERWIRE'})
                continue
            try:points=grid_points_on_wire(wp,a.grid,t['anchor'])
            except ValueError as ex:
                reviews.append({'page':page,'id':t['id'],'reason':str(ex)})
                continue
        else:
            span=(a.max_property_displacement//a.grid)*a.grid
            offsets=[(dx,dy) for dx in range(-span,span+1,a.grid)
                     for dy in range(-span,span+1,a.grid)
                     if abs(dx)+abs(dy)<=a.max_property_displacement]
            offsets.sort(key=lambda p:(abs(p[0])+1.5*abs(p[1]),abs(p[1]),p))
            points=[(t['anchor'][0]+dx,t['anchor'][1]+dy) for dx,dy in offsets]
        accepted=None
        for point in points:
            dx,dy=point[0]-t['anchor'][0],point[1]-t['anchor'][1]
            if not dx and not dy:continue
            g=translate(t['geometry'],xoff=dx,yoff=dy);e=g.buffer(a.text_clearance)
            bounds=scene.page_bounds[page]
            if not box(bounds[0]+2,bounds[1]+2,bounds[2]-2,bounds[3]-2).covers(e):continue
            hit=False
            for j in indexes[page].query(e):
                other=bypage[page][int(j)]
                if t['kind']=='alias' and other['kind']=='wire' and other['id']==t['owner_id']:
                    if g.intersection(other['geometry']).area>.02:hit=True;break
                elif e.intersects(other['geometry']):hit=True;break
            if hit:continue
            if any(e.intersects(text_geometries[int(j)]) for j in ti.query(e)):continue
            accepted=(point,g,dx,dy);break
        if accepted is None:
            reviews.append({'page':page,'id':t['id'],'kind':t['kind'],'ref':t['ref'],'text':t['text'],
                            'reason':'NO_CLEAR_POSITION_WITHIN_ASSOCIATION_BOUND_OR_EXISTING_OWNERWIRE'})
            continue
        point,g,dx,dy=accepted
        row={'page':page,'id':t['id'],'owner_id':t['owner_id'],'kind':t['kind'],'ref':t['ref'],
             'property_name':t['property'],'actual_display_string':t['text'],
             'translation_dx':dx,'translation_dy':dy,'font_unchanged':True,
             'rotation_unchanged':True,'old_rotation':t['rotation'],
             'old_justification':t['justification'],'new_justification':t['justification'],
             'hotspot_pin_wire_glyph_unchanged':True,'GUI_verified':False,
             'status':'CANDIDATE_ONLY_REQUIRES_STRICT_XML_ALLOWLIST_NATIVE_REOPEN_AND_ELECTRICAL_GATE'}
        if t['kind']=='alias':
            row.update(action='ALIAS_SET_LOCATION',old_x=t['anchor'][0],old_y=t['anchor'][1],
                       new_x=point[0],new_y=point[1],owner_wire_id=t['owner_id'],target_on_original_wire=True)
        else:
            ox,oy=t['original_offset'];row.update(action='DP_SET_LAYOUT',old_local_x=ox,old_local_y=oy,
                                                new_local_x=ox+dx,new_local_y=oy+dy)
        plans.append(row);t['geometry']=g;t['anchor']=list(point);t['bbox']=list(g.bounds)
    post=collisions(working,scene.geom)
    postcore=[r for r in post if r['a_kind'] in core or r['b_kind'] in core]
    save_json(a.output/'candidate_plan.json',plans);save_json(a.output/'reviews.json',reviews)
    save_json(a.output/'summary.json',{'input_xml_sha256':source_sha,'source_unchanged':source_sha==hashlib.sha256(a.xml.read_bytes()).hexdigest(),
              'grid_document_units':a.grid,'native_binding':binding,'max_property_displacement':a.max_property_displacement,
              'plan_count':len(plans),'review_count':len(reviews),'post_core_ink_candidates':len(postcore),
              'automatic_alias_deletions':0,'wire_extensions':0,'CAD_started':False,'design_written':False,'GUI_verified':False})
    print(json.dumps({'plans':len(plans),'reviews':len(reviews),'remaining_core_candidates':len(postcore)}))


if __name__=='__main__':main()
