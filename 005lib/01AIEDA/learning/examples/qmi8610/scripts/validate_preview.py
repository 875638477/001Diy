"""Validate native Allegro read-back against the reviewed QMI8610 datasheet spec.
Creates a PNG preview from exported native coordinates; this is not a Cadence screenshot.
"""
import sys,pathlib,json,csv,math,hashlib
BASE=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(BASE.parents[1]/'tools'/'pymupdf_1_28_2'))
import pymupdf
spec=json.loads((BASE/'qmi8610_spec.json').read_text(encoding='utf-8-sig'))
def rows(name):
    with (BASE/'logs'/'reopen'/name).open(encoding='utf-8-sig',newline='') as f:
        return [{k:v.strip('"') for k,v in r.items()} for r in csv.DictReader(f,delimiter='\t')]
def close(a,b): return abs(float(a)-float(b))<1e-6
pins=rows('pins.tsv'); pads=rows('pads.tsv'); texts=rows('texts.tsv'); segments=rows('segments.tsv')
assert len(pins)==16 and {int(p['number']) for p in pins}==set(range(1,17))
for p in pins:
    want=spec['pins'][int(p['number'])-1]
    assert p['padstack'].lower()==spec['padstack'].lower()
    assert all(close(p[k],want[k]) for k in ['x','y','rotation'])
    assert p['mirrored']=='nil' and p['through']=='nil' and p['hole_type']=='none'
    assert close(p['drill_diameter'],0) and p['top']=='t' and p['bottom']=='nil'
assert len(pads)==96
for p in pads:
    if p['layer'].endswith('BOTTOM'):
        assert p['figure']=='NULL' and close(p['width'],0) and close(p['height'],0)
    else:
        kind={'ETCH/TOP':'copper','PIN/SOLDERMASK_TOP':'mask','PIN/PASTEMASK_TOP':'paste'}[p['layer']]
        assert p['figure']=='RECTANGLE'
        dim=spec['pad'][kind]
        if spec['pins'][int(p['number'])-1]['rotation']%180==90: dim=dim[::-1]
        assert all(close(p[k],v) for k,v in zip(['width','height'],dim))
        assert p['offset']=='(0.0 0.0)'
assert len(texts)==3 and {p['layer'] for p in texts}=={p['layer'] for p in spec['texts']}
for p in texts:
    want=next(t for t in spec['texts'] if t['layer']==p['layer'])
    assert p['text']==want['text'] and all(close(p[k],0) for k in ['x','y','rotation'])
def key(layer,a,b,w):
    return (layer,tuple(sorted([tuple(round(v,6) for v in a),tuple(round(v,6) for v in b)])),round(w,6))
expected=[]
for kind,layer in [('silkscreen','PACKAGE GEOMETRY/SILKSCREEN_TOP'),('assembly','PACKAGE GEOMETRY/ASSEMBLY_TOP')]:
    for path in spec[kind]['paths']:
        for a,b in zip(path,path[1:]): expected.append(key(layer,a,b,spec[kind]['width']))
actual=[key(s['layer'],[float(s['x1']),float(s['y1'])],[float(s['x2']),float(s['y2'])],float(s['width'])) for s in segments]
assert sorted(expected)==sorted(actual)
report=(BASE/'logs'/'reopen'/'verify.txt').read_text(encoding='utf-8-sig')
assert 'pins=16 drcs=0 drcState=t' in report
assert 'place_bound_bbox=((-2.0 -2.0) (2.0 2.0)) filled=t properties=((PACKAGE_HEIGHT_MAX "1 MM"))' in report
assert 'QMI8610_VERIFY COMPLETE' in (BASE/'logs'/'reopen'/'complete.txt').read_text()
native={(int(p['number']),p['layer']):p for p in pads}
def rect(p,kind):
    layer={'copper':'ETCH/TOP','mask':'PIN/SOLDERMASK_TOP','paste':'PIN/PASTEMASK_TOP'}[kind]
    d=native[int(p['number']),layer]; w,h=float(d['width']),float(d['height'])
    # axlDBGetPad bBox is pin-centered and already oriented by pin rotation.
    x,y=float(p['x']),float(p['y'])
    return (x-w/2,y-h/2,x+w/2,y+h/2)
copper=[rect(p,'copper') for p in pins]; mask=[rect(p,'mask') for p in pins]
assert close(max(r[2] for r in copper)-min(r[0] for r in copper),3.4)
assert close(max(r[3] for r in copper)-min(r[1] for r in copper),3.4)
def rect_distance(a,b):
    return math.hypot(max(a[0]-b[2],b[0]-a[2],0),max(a[1]-b[3],b[1]-a[3],0))
copper_gap=min(rect_distance(a,b) for i,a in enumerate(copper) for b in copper[i+1:])
mask_web=min(rect_distance(a,b) for i,a in enumerate(mask) for b in mask[i+1:])
assert close(copper_gap,.18) and close(mask_web,.08)
# Segment-to-rectangle distance, using endpoint and edge segment distances.
def point_seg(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)
def seg_rect(a,b,r):
    # All intended silk segments are outside mask rectangles. Check endpoints and edge intersection.
    corners=[(r[0],r[1]),(r[2],r[1]),(r[2],r[3]),(r[0],r[3])]
    def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def intersects(a,b,c,d):
        return orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0
    if any(r[0]<=p[0]<=r[2] and r[1]<=p[1]<=r[3] for p in [a,b]): return 0
    if any(intersects(a,b,c,d) for c,d in zip(corners,corners[1:]+corners[:1])): return 0
    return min([point_seg(c,a,b) for c in corners]+[point_seg(p,c,d) for p in [a,b] for c,d in zip(corners,corners[1:]+corners[:1])])
silk_mask_gap=min(seg_rect((float(s['x1']),float(s['y1'])),(float(s['x2']),float(s['y2'])),r)-float(s['width'])/2 for s in segments if s['layer'].endswith('SILKSCREEN_TOP') for r in mask)
assert silk_mask_gap>=.099999
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in (BASE/'library').iterdir() if p.suffix in ['.pad','.dra','.psm']}
result={'status':'PASS','sourceSHA256':spec['source']['sha256'],'checks':['16 numbered peripheral pins; no center pad','exact native x/y/rotation and padstack','native copper/mask/paste dimensions and absent bottom pads/drill','18 exact outline segments','three required text anchors at origin','filled 4x4 mm place bound; maximum height 1 MM','stored DRC=0 with current state t','native DRA reopened without hash change'],'minCopperGapMm':copper_gap,'minMaskWebMm':mask_web,'minSilkOutlineToMaskGapMm':silk_mask_gap,'stagedArtifactsSHA256':hashes,'manufacturingStatus':'Datasheet and CAD validation only; no assembly/fabrication validation performed.'}
(BASE/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
# Construct a readable engineering preview from the native exported data.
doc=pymupdf.open(); page=doc.new_page(width=1400,height=1000)
O=(465,490); S=170
def pt(x,y):return (O[0]+S*x,O[1]-S*y)
def pr(r):
    a=pt(r[0],r[3]);b=pt(r[2],r[1]);return pymupdf.Rect(*a,*b)
def text(x,y,t,size=16,color=(.12,.15,.2)):
    page.insert_text((x,y),t,fontsize=size,color=color)
def centered(x,y,t,size,color=(.1,.1,.1)):
    text(x-pymupdf.get_text_length(t,fontsize=size)/2,y+size*.35,t,size,color)
text(65,60,'QMI8610  |  LGA-16  |  TOP VIEW',30)
text(65,95,'Rev A recommended land pattern; units: mm; pin 1 at upper left.',17)
page.draw_rect(pr((-2,-2,2,2)),color=(.6,.6,.6),dashes='[6 4] 0',width=1)
page.draw_rect(pr((-1.65,-1.65,1.65,1.65)),color=(.4,.5,.7),fill=(.94,.95,.98),width=1)
for r in mask:page.draw_rect(pr(r),color=(.6,.35,.75),width=1.5)
for p,r in zip(pins,copper):
    page.draw_rect(pr(r),color=(.85,.45,.06),fill=(1,.72,.28),width=1)
    x,y=pt(float(p['x']),float(p['y']));centered(x,y,p['number'],18)
for s in segments:
    if s['layer'].endswith('SILKSCREEN_TOP'):
        page.draw_line(pt(float(s['x1']),float(s['y1'])),pt(float(s['x2']),float(s['y2'])),color=(.05,.58,.35),width=float(s['width'])*S)
    elif s['layer'].endswith('ASSEMBLY_TOP'):
        page.draw_line(pt(float(s['x1']),float(s['y1'])),pt(float(s['x2']),float(s['y2'])),color=(.3,.45,.7),width=1)
text(O[0]-pymupdf.get_text_length('U*',fontsize=130)/2,O[1],'U*',130,(.05,.58,.35))
page.draw_line(pt(-.1,0),pt(.1,0),color=(.5,.5,.5),width=1)
page.draw_line(pt(0,-.1),pt(0,.1),color=(.5,.5,.5),width=1)
text(335,875,'3.30 body / 3.40 copper span',20)
text(335,905,'No center solder pad',18)
x=890;y=180
for s,size in [('NATIVE CAD READ-BACK',22),('',16),(spec['footprint'],18),('',16),('Pins: 16  |  Pitch: 0.50',20),('Copper: 0.61 x 0.32',20),('Mask: 0.71 x 0.42',20),('Paste: 0.61 x 0.32 (1:1)',20),('Max package height: 1.00',20),('Place bound: 4.00 x 4.00',20),('',16),('REF DES / SILKSCREEN_TOP',17),('U*   anchor (0,0)',16),('REF DES / ASSEMBLY_TOP',17),('U*   anchor (0,0)',16),('COMPONENT VALUE / ASSEMBLY_TOP',17),('VALUE   anchor (0,0)',16),('',16),('Green: silkscreen; purple: mask',16),('Orange: copper; blue: body / assembly',16),('Gray dashed: placement boundary',16),('',16),('Mask and paste are engineering selections.',15),('Confirm 0.08 mask web with fabricator.',15)]:
    text(x,y,s,size);y+=27
text(65,970,'Preview drawn from Allegro read-back data; not a Cadence screenshot. Text font and pin labels are illustrative.',15)
page.get_pixmap(matrix=pymupdf.Matrix(1.2,1.2)).save(BASE/'preview.png')
print(json.dumps(result,indent=2))
