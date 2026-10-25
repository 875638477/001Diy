import json,pathlib,math,hashlib,datetime
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
plan=read(ROOT/'plans/placement_plan.json');desired={p['ref']:p for p in plan['placements']}
inv=read(ROOT/'inventory/inventory_4L.json');expected={c['ref']:c for c in inv['components']}
results={}
for variant in ['4L','2L']:
    p=ROOT/f'inventory/normalized_actual_{variant}.json'
    if not p.exists():results[variant]={'status':'AWAITING_NATIVE_READBACK'};continue
    d=read(p);items=d['placements'];actual={i['ref']:i for i in items};checks=[]
    def ck(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
    ck('80 exact logical references',len(items)==80 and len(actual)==80 and set(actual)==set(expected))
    count=0
    for ref,e in expected.items():
        if ref not in actual:continue
        a=actual[ref];want=desired[ref];xy=a['xy']
        ck(ref+' origin and rotation',abs(xy[0]-want['x'])<.00011 and abs(xy[1]-want['y'])<.00011 and abs((a['rotation']-want['rotation']+180)%360-180)<.0001)
        ck(ref+' package',a['package'].upper()==e['package'].upper())
        ep={pin['number']:pin for pin in e['logicalPins']};ap={pin['number']:pin for pin in a['pins'] if pin['number']}
        ck(ref+' logical pin set',set(ep)==set(ap),{'expected':len(ep),'actual':len(ap)})
        rad=math.radians(a['rotation']);ca,sa=math.cos(rad),math.sin(rad)
        for num,pp in ep.items():
            if num not in ap:continue
            aa=ap[num];count+=1;local=pp['localXY'];pos=[xy[0]+local[0]*ca-local[1]*sa,xy[1]+local[0]*sa+local[1]*ca]
            ck(ref+'.'+num+' net and absolute pad anchor',(aa['net'] or None)==(pp['net'] or None) and math.dist(pos,aa['xy'])<.0002)
        ck(ref+' actual body matches planned transformed native extent',max(abs(a['bodyExtent'][j][k]-want['extent'][j][k]) for j in (0,1) for k in (0,1))<.00021)
    collisions=[];zone=[];holeclash=[];outside=[]
    for n,a in enumerate(items):
        box=a['bodyExtent']
        if min(box[1][0],30)>max(box[0][0],10) and min(box[1][1],52)>max(box[0][1],42):zone.append(a['ref'])
        if a['ref']!='J2' and (box[0][0]<.8 or box[0][1]<.8 or box[1][0]>79.2 or box[1][1]>59.2):outside.append(a['ref'])
        for x,y in [(5,5),(75,5),(75,55),(5,55)]:
            dx=max(box[0][0]-x,0,x-box[1][0]);dy=max(box[0][1]-y,0,y-box[1][1])
            if math.hypot(dx,dy)<2.5-1e-4:holeclash.append([a['ref'],[x,y],math.hypot(dx,dy)])
        for b in items[n+1:]:
            bb=b['bodyExtent'];dx=min(box[1][0],bb[1][0])-max(box[0][0],bb[0][0]);dy=min(box[1][1],bb[1][1])-max(box[0][1],bb[0][1])
            if dx>1e-4 and dy>1e-4:collisions.append([a['ref'],b['ref'],dx,dy])
    ck('actual body extents do not overlap',not collisions,collisions)
    ck('all unknown-height parts kept outside restricted zone',not zone,zone)
    ck('actual body extents clear teaching 5mm hole envelopes',not holeclash,holeclash)
    ck('body inside board margin apart from recorded J2 edge exception',not outside,outside)
    failures=[c for c in checks if not c['pass']]
    results[variant]={'status':'PASS_PLACEMENT_GEOMETRY_LOGICAL_MAPPING' if not failures else 'REQUIRES_CORRECTION','readbackDirectory':d['readbackDirectory'],'checks':len(checks),'logicalPinsCompared':count,'failures':failures,'checksDetail':checks,'snapshotSHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'Native placement/pad mapping/bounds review; does not replace native DRC, conductive graph, reference-copper verification or manufacturing/hardware verification.'}
out=ROOT/'review';out.mkdir(exist_ok=True)
report={'date':datetime.datetime.now().astimezone().isoformat(),'scope':'Independent geometry and circuit-pin comparison against saved native snapshots','variants':results}
(out/'root_geometry_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for k,v in results.items():print(k,v['status'],v.get('checks'),v.get('logicalPinsCompared'),json.dumps(v.get('failures'),ensure_ascii=False)[:3000])