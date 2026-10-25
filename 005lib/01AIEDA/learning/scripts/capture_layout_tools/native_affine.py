"""Bind Capture part geometry to read-only native affine samples.
No CAD calls. Missing data never silently falls back for rotated/mirrored parts.
"""
import csv, math, pathlib

COLUMNS={'page','id','rotation','mirror','ox','oy','frame_origin_x','frame_origin_y','a_xx','a_xy','a_yx','a_yy','offset_x','offset_y'}

def read_frames(path):
    if path is None:return {}
    path=pathlib.Path(path)
    with path.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream,delimiter='\t')
        if not COLUMNS <= set(reader.fieldnames or []):raise ValueError('Incomplete native part-frame schema')
        result={}
        for source in reader:
            row=dict(source)
            for name in COLUMNS-{'page','id'}:
                row[name]=float(row[name])
                if not math.isfinite(row[name]):raise ValueError('Nonfinite native frame value')
            key=(row['page'],row['id'])
            if key in result:raise ValueError('Duplicate native part-frame key: '+str(key))
            if row['frame_origin_x']!=row['ox']+row['offset_x'] or row['frame_origin_y']!=row['oy']+row['offset_y']:raise ValueError('Inconsistent native affine offset: '+str(key))
            a,b,c,d=[row[k] for k in ('a_xx','a_xy','a_yx','a_yy')]
            if a*d-b*c not in (-1,1) or any(x not in (-1,0,1) for x in (a,b,c,d)) or a*a+c*c!=1 or b*b+d*d!=1 or a*b+c*d!=0:raise ValueError('Unsupported native orientation matrix: '+str(key))
            result[key]=row
        return result

def bind_part(owner,page,frames):
    result=dict(owner);key=(page,str(owner['dbId']));row=frames.get(key)
    if row is None:
        if int(owner.get('rotation',0)) or int(owner.get('mirror',0)):
            raise ValueError('Nonzero PartInst pose requires same-save native GetOffsetGraphicPoint frame table: '+str(key))
        # Legacy zero-pose model is still independently checked against native pins.
        result['_part_frame_model']='ZERO_POSE_ONLY_REQUIRES_PIN_BINDING'
        return result
    for field,source in [('locX','ox'),('locY','oy'),('rotation','rotation'),('mirror','mirror')]:
        if float(owner.get(field,0))!=row[source]:raise ValueError('Stale XML/native PartInst frame: '+str(key)+' '+field)
    result['_native_affine']=[row['a_xx'],row['a_xy'],row['a_yx'],row['a_yy'],row['frame_origin_x'],row['frame_origin_y']]
    result['_part_frame_model']='NATIVE_GETOFFSETGRAPHICPOINT_BASIS'
    return result

def apply_frame(x,y,owner,legacy_transform):
    frame=owner.get('_native_affine')
    if frame is None:
        if owner.get('_part_frame_model') and (int(owner.get('rotation',0)) or int(owner.get('mirror',0))):raise ValueError('Missing required native affine frame')
        return legacy_transform(x,y,owner)
    a,b,c,d,tx,ty=frame
    return [a*x+b*y+tx,c*x+d*y+ty]
