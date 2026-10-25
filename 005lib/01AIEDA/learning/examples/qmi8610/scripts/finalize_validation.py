"""Verify published files and native PSM transformations, preserving standalone evidence."""
import sys,pathlib,json,csv,hashlib,re
BASE=pathlib.Path(__file__).resolve().parent.parent
spec=json.loads((BASE/'qmi8610_spec.json').read_text(encoding='utf-8-sig'))
result=json.loads((BASE/'validation.json').read_text(encoding='utf-8-sig'))
assert result['status']=='PASS'
def near(a,b):return abs(float(a)-float(b))<1e-6
with (BASE/'logs/placement/placement_pins.tsv').open(encoding='utf-8-sig',newline='') as f:
    rows=[{k:v.strip('"') for k,v in r.items()} for r in csv.DictReader(f,delimiter='\t')]
counts={};seen=set()
for p in rows:
    n=int(p['number']);q=spec['pins'][n-1];x,y=q['x'],q['y'];case=p['case']
    assert (case,n) not in seen;seen.add((case,n))
    counts[case]=counts.get(case,0)+1
    if case=='TOP_0': want=(x-10,y,q['rotation'],'nil','t','nil')
    elif case=='TOP_90':want=(-y,x,(q['rotation']+90)%360,'nil','t','nil')
    elif case=='BOTTOM_0':want=(10-x,y,(-q['rotation'])%360,'t','nil','t')
    else:raise AssertionError('Unexpected case')
    assert all(near(p[k],v) for k,v in zip(['x','y','rotation'],want[:3]))
    assert (p['mirrored'],p['top'],p['bottom'])==want[3:]
    assert near(p['relx'],x) and near(p['rely'],y)
assert counts=={'TOP_0':16,'TOP_90':16,'BOTTOM_0':16}
assert 'QMI8610_PSM_LOAD COMPLETE' in (BASE/'logs/placement/placement.txt').read_text(encoding='utf-8-sig')
for file in ['pins.tsv','pads.tsv','segments.tsv','texts.tsv']:
    assert (BASE/'logs/reopen'/file).read_bytes()==(BASE/'logs/public_reopen'/file).read_bytes()
assert 'pins=16 drcs=0 drcState=t' in (BASE/'logs/public_reopen/verify.txt').read_text(encoding='utf-8-sig')
assert 'QMI8610_VERIFY COMPLETE' in (BASE/'logs/public_reopen/complete.txt').read_text()
public={}
for target in spec['public'].values():
    path=pathlib.Path(target);h=hashlib.sha256(path.read_bytes()).hexdigest().upper()
    assert h==result['stagedArtifactsSHA256'][path.name]
    public[str(path)]={'sha256':h,'bytes':path.stat().st_size}
# Native text bbox includes glyph/stroke extents. It is separate from its origin anchor.
with (BASE/'logs/public_reopen/text_boxes.tsv').open(encoding='utf-8-sig',newline='') as f:
    textboxes=list(csv.DictReader(f,delimiter='\t'))
silk=next(p for p in textboxes if p['layer'].strip('"')=='REF DES/SILKSCREEN_TOP')
bb=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',silk['bbox'])]
assert len(bb)==4
with (BASE/'logs/public_reopen/pads.tsv').open(encoding='utf-8-sig',newline='') as f:
    pads=[{k:v.strip('"') for k,v in r.items()} for r in csv.DictReader(f,delimiter='\t')]
mask=[]
for p in spec['pins']:
    m=next(m for m in pads if int(m['number'])==p['number'] and m['layer']=='PIN/SOLDERMASK_TOP')
    w,h=float(m['width']),float(m['height'])
    mask.append([p['x']-w/2,p['y']-h/2,p['x']+w/2,p['y']+h/2])
def distance(a,b):
    return (max(a[0]-b[2],b[0]-a[2],0)**2+max(a[1]-b[3],b[1]-a[3],0)**2)**.5
text_gap=min(distance(bb,m) for m in mask)
assert text_gap>=.1
result.update({'publicArtifacts':public,'publicReopen':'PASS, native TSV identical to staged readback; DRA hash unchanged','compiledPsmLoad':{'status':'PASS','cases':counts,'pinsChecked':len(rows),'board':str(BASE/'logs/placement/qmi8610_validation.brd'),'mirrorAtZeroRotation':'x flips about component origin; y is unchanged; TOP pads move to BOTTOM'},'nativeSilkTextBBoxMm':bb,'minSilkTextBBoxToMaskGapMm':text_gap})
(BASE/'final_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
