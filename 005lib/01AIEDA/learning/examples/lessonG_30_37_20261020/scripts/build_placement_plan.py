import json,math,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
inv=read(ROOT/'inventory/inventory_4L.json')
comps={c['ref']:c for c in inv['components']}
plan={}
def add(ref,x,y,r=0,purpose=''):
    plan[ref]={'ref':ref,'x':x,'y':y,'rotation':r,'side':'TOP','purpose':purpose,'owner':'root'}
def atpin(ref,pin,xy,r=0,purpose=''):
    p=next(p for p in comps[ref]['logicalPins'] if p['number']==str(pin))
    a=math.radians(r);px,py=p['localXY']
    add(ref,xy[0]-(px*math.cos(a)-py*math.sin(a)),xy[1]-(px*math.sin(a)+py*math.cos(a)),r,purpose)
add('J2',40,3.675,0,'Preserve F27 USB mechanical datum; opening toward y=0')
add('J3',74,12,0,'CAN at right edge, keep mating/test access')
add('J4',74,25,0,'UART at right edge, 3.3 V only')
add('J5',74,39,0,'I2C at right edge, separate 100 kHz contract')
add('J6',7,26,90,'SPI left edge; fixed actual pin1 origin then 12.7 mm row north')
add('J9',51,20,0,'SWD local 1x6 row accessible south-east of MCU')
for ref,x in [('J11',18),('J12',40),('J13',62)]:
    add(ref,x,55,90,'GPIO top edge; rotated real centered vertical header, clear low-height zone')
for ref,xy,purpose in [
 ('R23',(33.3,32.8),'SPI NSS source-side region, preserve fanout order'),
 ('R21',(33.3,30.5),'SPI SCK source-side region, edge rather than frequency matters'),
 ('R24',(33.3,28.2),'SPI MISO zero-ohm routing option'),
 ('R22',(33.3,25.9),'SPI MOSI source-side region')]:
    atpin(ref,1,xy,180,purpose)
atpin('R25',2,(30.5,35.3),180,'SPI NSS pullup outside series/fanout channel')
atpin('R19',2,(56.5,35),0,'I2C SCL 2.2k pullup, actual baseline retained')
atpin('R20',2,(56.5,37),0,'I2C SDA 2.2k pullup, actual baseline retained')
rootitems=list(plan.values())
(ROOT/'plans/root_placement.json').write_text(json.dumps({'status':'PROPOSED_ENGINEERING_PLACEMENT','placements':rootitems},ensure_ascii=False,indent=2),encoding='utf-8')
for rel in ['engineering_mcu/placement_mcu.json','engineering_power/placement_power.json']:
    path=ROOT/rel
    if not path.exists():
        print('WAIT',rel);continue
    obj=read(path)
    items=obj if isinstance(obj,list) else obj.get('placements',obj.get('components',[]))
    if isinstance(items,dict):items=[dict(v,ref=k) for k,v in items.items()]
    for item in items:
        ref=item['ref'];xy=item.get('xy',item.get('position'))
        if xy is None:xy=[item['x'],item['y']]
        # Root owns external connector positions; engineer suggestions remain in their files.
        if ref in plan:continue
        add(ref,*xy,item.get('rotation',item.get('angle',0)),item.get('purpose',item.get('rationale','')))
        plan[ref]['owner']=rel
override=ROOT/'plans/root_overrides.json'
if override.exists():
    for item in read(override)['placements']:
        if 'pin' in item:atpin(item['ref'],item['pin'],item['pinXY'],item.get('rotation',0),item.get('purpose',''))
        else:add(item['ref'],item['x'],item['y'],item.get('rotation',0),item.get('purpose',''))
        plan[item['ref']]['owner']='root_global_review_override'
missing=sorted(set(comps)-set(plan))
extra=sorted(set(plan)-set(comps))
for ref,item in plan.items():
    item['x']=round(item['x'],4);item['y']=round(item['y'],4)
    c=comps[ref];a=math.radians(item['rotation']);ca,sa=math.cos(a),math.sin(a)
    def xf(xy):return [round(item['x']+xy[0]*ca-xy[1]*sa,4),round(item['y']+xy[0]*sa+xy[1]*ca,4)]
    b=c['bodyExtent'];corners=[xf([x,y]) for x in [b[0][0],b[1][0]] for y in [b[0][1],b[1][1]]]
    item['extent']=[[min(p[0] for p in corners),min(p[1] for p in corners)],[max(p[0] for p in corners),max(p[1] for p in corners)]]
    item['pins']={p['number']:{'xy':xf(p['localXY']),'net':p['net']} for p in c['logicalPins']}
clashes=[]
items=list(plan.values())
for n,a in enumerate(items):
    for b in items[n+1:]:
        aa,bb=a['extent'],b['extent']
        dx=min(aa[1][0],bb[1][0])-max(aa[0][0],bb[0][0]);dy=min(aa[1][1],bb[1][1])-max(aa[0][1],bb[0][1])
        if dx>0 and dy>0:clashes.append({'a':a['ref'],'b':b['ref'],'overlap':[round(dx,4),round(dy,4)]})
zone=[]
for i in items:
    b=i['extent']
    if min(b[1][0],30)>max(b[0][0],10) and min(b[1][1],52)>max(b[0][1],42):zone.append(i['ref'])
status='READY_FOR_NATIVE_PLACEMENT' if not missing and not extra and not clashes and not zone else 'DRAFT_REQUIRES_REVIEW'
result={'status':status,'units':'mm','scope':'Teaching placement, not manufacturing released or fully routed','placements':items,'missing':missing,'extra':extra,'boundingBoxClashes':clashes,'anyComponentInLowHeightZone':zone}
(ROOT/'plans/placement_plan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':status,'count':len(items),'missing':missing,'clashes':clashes,'zone':zone},ensure_ascii=False))