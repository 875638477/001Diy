from pathlib import Path
import json,sys,math,runpy,hashlib
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'));sys.path.insert(0,str(R/'scripts'))
from shapely.geometry import Point,box
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely.prepared import prep
from cadence_poly import conservative_plane
ctx=runpy.run_path(str(R/'scripts/precheck_SPI_external_4L_v5.py'));items=ctx['items'];req=ctx['req'];b=ctx['b'];p=ctx['p'];new=[];proof=[]
ps={l:unary_union([conservative_plane(dict(z,holes=z['holes'] or [])) for z in b['planes'] if z['net']=='GND' and z['layer']=='ETCH/'+l]) for l in ['L2','L3']}
ps={l:prep(q) for l,q in ps.items()}
tree=STRtree([a['g'] for a in items])
actualG=[dict(id='BASE_GND'+str(i),xy=v['xy']) for i,v in enumerate(b['vias']) if v['net']=='GND'];sig=[o for o in p['operations'] if o['type']=='via']
for o in sig:
 exist=sorted(actualG+new,key=lambda z:math.dist(z['xy'],o['xy']))
 if exist and math.dist(exist[0]['xy'],o['xy'])<=1.5:
  proof.append(dict(signal=o['id'],xy=o['xy'],ground=exist[0]['id'],groundXY=exist[0]['xy'],distance_mm=math.dist(exist[0]['xy'],o['xy']),newVia=False));continue
 options=[]
 for dx in range(-30,31):
  for dy in range(-30,31):
   if not .95<=math.hypot(dx,dy)*.05<=1.5:continue
   xy=[round(o['xy'][0]+dx*.05,4),round(o['xy'][1]+dy*.05,4)];pt=Point(xy);g=pt.buffer(.3,quad_segs=32)
   if not all(ps[l].covers(g) for l in ['L2','L3']):continue
   if any(math.dist(xy,z['xy'])<.6 for z in actualG+new):continue
   if any(math.dist(xy,z['xy'])<.92 for z in sig):continue
   margin=99;ok=True
   for ai in tree.query(g.buffer(.51)):
    a=items[int(ai)]
    v=dict(id='TEST',net='GND',g=g,layer=a['layer'],new=True,kind='via')
    if a['kind']=='pad' and pt.distance(a['g'])<.15:ok=False;break
    if a['net']=='GND':continue
    d=g.distance(a['g']);r=req(v,a);margin=min(margin,d-r)
    if d<r+1e-4:ok=False;break
   if not ok:continue
   bodyPenalty=sum(1 for c in b['placements'] if c.get('bodyExtent') and box(*c['bodyExtent'][0],*c['bodyExtent'][1]).intersects(pt.buffer(.15)))
   dist=math.dist(xy,o['xy']);options.append((bodyPenalty,dist- min(margin,.2)*.1,xy,margin))
 assert options,('NO_LEGAL_GND',o['id'])
 options.sort();_,_,xy,m=options[0];v=dict(type='via',id='SPI4_RETURN_'+str(len(new)+1),net='GND',xy=xy,padstack='L28_VIA030_C060',purpose='Chosen by actual all-layer copper/pad clearance and native existing L2/L3 GND annulus coverage, not guessed coordinate')
 new.append(v)
 for layer in ['TOP','BOTTOM']:items.append(dict(id=v['id'],net='GND',g=Point(xy).buffer(.3,quad_segs=32),layer=layer,new=True,kind='via'))
 proof.append(dict(signal=o['id'],xy=o['xy'],ground=v['id'],groundXY=xy,distance_mm=math.dist(xy,o['xy']),newVia=True,minimumExtraConservativeClearance_mm=m))
p['operations']+=new;p['batchId']='SPI_external_4L_engineered_v6';p['status']='FINAL_ENGINEERING_CANDIDATE_NEEDS_NATIVE_GLOBAL_INTEGRATION';p['sourceExpectedSHA256']='A9215927856EF4D3AD6D6CBAE3F227365EE09640821C8403336863C0A35F9437';p['groundReturnSelection']=proof;p['limitations']=['Native future signalvia antipads/ground thermal spokes require postfill proof','L2/L3 actual reference projection audited separately. Only TOP/BOTTOM signal copper permitted.','New via pad/mask/tent and exact MPN physical body remain manufacturing conditions.','J6 external cable single-ground pinout and actual edge rate must be controlled. No 90ohm/SI/EMI certification.']
(R/'SPI_external_4L_engineered_v6.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
s=(R/'scripts/precheck_SPI_external_4L_v5.py').read_text().replace("(H/'plans/SPI_external_4L_candidate_v5.json')", "(R/'SPI_external_4L_engineered_v6.json')").replace('4L_v5_precheck.json','4L_v6_precheck.json')
(R/'scripts/precheck_SPI_external_4L_v6.py').write_text(s,encoding='utf-8')
(R/'readouts/SPI4L_return_v6_selection.json').write_text(json.dumps(dict(status='ACTUAL_COPPER_AND_L2_L3_GND_SELECTION_NEEDS_NATIVE',signals=proof,newGroundVias=new,source='postcritical_4L_b010'),indent=2),encoding='utf-8')
print(json.dumps(dict(newViaCount=len(new),signals=proof),indent=2))