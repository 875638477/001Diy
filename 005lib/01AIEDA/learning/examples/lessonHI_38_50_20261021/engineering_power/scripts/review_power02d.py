from pathlib import Path
import json,math,csv,hashlib,sys,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');H=R.parent
sys.path.insert(0,str(H/'tooling/packages'))
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union
C=[];E=[]
def check(i,v,d=None):C.append(dict(id=i,passed=bool(v),detail=d))
def record(p):
 E.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
profile=json.loads((R/'rules_profile_2L_69nets.json').read_text());record(R/'rules_profile_2L_69nets.json')
expected={n:g for g in profile['groups'] for n in g['nets']}
plans=[json.loads((R/f).read_text()) for f in ['power_critical_paths_01.json','power_paths_02d.json']]
for variant in ['2L','4L']:
 cp=H/'inventory/checkpoints'/('power_'+variant+'_b002d')
 # Use frozen checkpoint where available, otherwise fixed native readback normalized snapshot copied here.
 live=cp/'normalized.json'
 a=json.loads(live.read_text())
 rb=Path(a['readbackDirectory'])
 assert rb.name=='reopen_power_'+variant+'_b002d',rb
 snap=R/'source'/('native_power02d_'+variant+'.json')
 shutil.copyfile(live,snap);record(snap)
 for n in ['native_summary.txt','hi_component_terminals.tsv','hi_net_connectivity.tsv','hi_reopen_endpoint_proofs.txt','hi_network_summary.txt','stackup_full.tsv','films_full.tsv','mechanical_roots.txt']:
  record(rb/n)
 nw=json.loads((cp/'networks.json').read_text(encoding='utf-8'));bp=Path(nw['board']);record(cp/'networks.json');record(bp)
 check(variant+'.immutableBRDHashMatchesReadback',hashlib.sha256(bp.read_bytes()).hexdigest().upper()==nw['sha256'].upper(),dict(board=str(bp),expected=nw['sha256']))
 original=json.loads((R/'source'/('normalized_actual_'+variant+'.json')).read_text(encoding='utf-8'))
 def identities(x):return {(c['ref'],p['number']):(p['net'] or None) for c in x['placements'] for p in c['pins'] if p['number'] and not p['mechanical']}
 check(variant+'.all272PinNetsPreservedFromG',identities(a)==identities(original))
 check(variant+'.all80ComponentModelsPreserved', {(c['ref'],c['package'],c['model'],c['value']) for c in a['placements']}=={(c['ref'],c['package'],c['model'],c['value']) for c in original['placements']})
 summary=(rb/'native_summary.txt').read_text()
 check(variant+'.native0DRC','drcs=0' in summary and'drcState=t' in summary,summary)
 check(variant+'.identity80comp69net','components=80' in summary and'nets=69' in summary)
 check(variant+'.logical272pins',sum(sum(bool(p['number']) and not p['mechanical'] for p in c['pins']) for c in a['placements'])==272)
 proof=(rb/'hi_reopen_endpoint_proofs.txt').read_text()
 check(variant+'.24freshEndpointProofs',proof.count('HI_ENDPOINT_PROOF ')==24 and'actual=nil' not in proof)
 ns=(rb/'hi_network_summary.txt').read_text()
 check(variant+'.142remaining','NATIVE_REMAINING_CONNECTIONS=142' in ns and'ACTUAL_NETTED_PHYSICAL_TERMINALS=266' in ns)
 bynet={}
 for t in csv.DictReader((rb/'hi_component_terminals.tsv').read_text().splitlines(),delimiter='\t'):
  bynet[t['terminal']]=(t['net'],t['component'])
 check(variant+'.CINlocalGNDsameNativeComponent',bynet.get('C3.2')==bynet.get('U2.1'),[bynet.get('C3.2'),bynet.get('U2.1')])
 check(variant+'.LDOinputGNDsameNativeComponent',bynet.get('C8.2')==bynet.get('U3.2'),[bynet.get('C8.2'),bynet.get('U3.2')])
 check(variant+'.LDOoutputGNDsameNativeComponent',bynet.get('C9.2')==bynet.get('U3.2'))
 check(variant+'.VINandFBnotshorted',bynet.get('U2.3')[0]=='VIN_PROT' and bynet.get('U2.4')[0]=='BUCK_FB')
 actual={}
 for x in a['routes']:
  if x['kind']=='line' and x['net']:
   actual.setdefault((x['net'],x['layer'].split('/')[-1]),[]).append((x['width'],LineString(x['startEnd'])))
 for pl in plans:
  for op in pl['operations']:
   if op['type']=='route':
    for j,(u,v) in enumerate(zip(op['points'],op['points'][1:])):
     w=op['widths'][j] if'widths' in op else op['width']
     lines=[g for ww,g in actual.get((op['net'],op['layer']),[]) if abs(ww-w)<1e-5]
     ok=bool(lines) and unary_union([g.buffer(.0002) for g in lines]).covers(LineString([u,v]))
     check(variant+'.actualGeometry.'+op['id']+'.'+str(j),ok,dict(width=w,start=u,end=v))
   elif op['type']=='via':
    vv=[v for v in a['vias'] if v['net']==op['net'] and math.dist(v['xy'],op['xy'])<.0002]
    check(variant+'.via.'+op['id'],len(vv)==1 and abs(vv[0]['drill']-.3)<1e-6)
    if vv:check(variant+'.viaAllCopper.'+op['id'],{p['layer'].split('/')[-1] for p in vv[0]['pads'] if p['figure'] and p['figure']!='NULL'}==({'TOP','BOTTOM'} if variant=='2L' else {'TOP','L2','L3','BOTTOM'}))
 # Official radius convention used; old full-holeAABB overestimated L-shapedsensevoid and false-rejected localcopper.
 target='ETCH/BOTTOM' if variant=='2L' else'ETCH/L2'
 ps=[p for p in a['planes'] if p['layer']==target and p['net']=='GND' and p['filled']]
 check(variant+'.actualReferencePlane',len(ps)==1)
 if ps:
  p=ps[0]
  def cadpoly(vs):
   out=[]
   for i,(end,rr) in enumerate(vs):
    start=vs[i-1][0]
    if not rr:
     out.append(end);continue
    r=abs(rr);dx=end[0]-start[0];dy=end[1]-start[1];d=math.hypot(dx,dy)
    assert d<=2*r+.001,(d,r)
    h=math.sqrt(max(0,r*r-d*d/4));mx=(start[0]+end[0])/2;my=(start[1]+end[1])/2
    options=[]
    for sign in [-1,1]:
     cx=mx+sign*(-dy/d)*h;cy=my+sign*(dx/d)*h
     a0=math.atan2(start[1]-cy,start[0]-cx);a1=math.atan2(end[1]-cy,end[0]-cx)
     delta=(a1-a0+math.pi)%(2*math.pi)-math.pi
     xx=math.cos(a0+delta/2)
     if (rr>0 and xx<0) or(rr<0 and xx>0):options.append((cx,cy,a0,delta))
    assert len(options)==1,(start,end,rr,options)
    cx,cy,a0,delta=options[0]
    assert abs(delta)<=math.pi/2+.003,delta
    steps=max(1,math.ceil(abs(delta)/math.radians(.5)))
    out.extend([[cx+r*math.cos(a0+delta*j/steps),cy+r*math.sin(a0+delta*j/steps)] for j in range(1,steps+1)])
   q=Polygon(out);assert q.is_valid
   return q
  outer=cadpoly(p['vertices']);holes=[cadpoly(h) for h in p['holes']]
  plane=outer.difference(unary_union(holes))
  check(variant+'.sampledArcAreaMatchesNative',abs(plane.area-p['area'])<.01,dict(sampled=plane.area,native=p['area'],bound=.01,arcStep_deg=.5))
  free=outer.buffer(-.0001).difference(unary_union(holes).buffer(.0001))
  corridor=LineString([[23.2,18],[23.7,22.55]]).buffer(.3)
  check(variant+'.CIN_U2planeReturnStrip0p6mm',free.covers(corridor),dict(layer=target,width=.6,points=[[23.2,18],[23.7,22.55]],h_mm=1.524 if variant=='2L' else .2104,method='OfficialaxlPolyFromDB radius applies previous->current vertex, positivearc leftofYaxis/negative right, quadrantlimited. Sample.5deg, nativearea agreement<.01mm2, outwardvoidbuffer.0001mm conservative. No field/current simulation.'))
  for pl in plans:
   for op in pl['operations']:
    if op['type']=='via' and op['net']=='GND':
     check(variant+'.solidReferenceViaDisk.'+op['id'],free.covers(Point(op['xy']).buffer(.3)),op['xy'])
  check(variant+'.generatedThermalSpokeWidth',all(x['width']>=.6-1e-5 for x in a['routes'] if x['net']=='GND' and x['layer']==target),dict(scope='All exported generatedGNDlines on reference>=.6. Offpadpower vias have whole.6disk in plane; no narrow single thermalspoke at tested vias.'))
 if variant=='4L':
  check(variant+'.bothActualGNDReferences',{p['layer'] for p in a['planes'] if p['filled'] and p['net']=='GND'}=={'ETCH/L2','ETCH/L3'})
 else:
  rp=cp/'base_net_rules.json';raw=json.loads(rp.read_text());record(rp)
  rules=raw['rules']
  check('2L.all69nets2layers',len(rules)==138 and{n['net'] for n in rules}==set(expected))
  for row in rules:
   g=expected[row['net']];prefix='2L.effectiveBase.'+row['net']+'.'+row['layer']+'.'
   for native,key in [('widthMinMM','width_min_mm'),('neckWidthMinMM','neckwidth_min_mm'),('neckLengthMaxMM','necklength_max_mm')]:check(prefix+native,abs(row[native]-g[key])<1e-5)
   check(prefix+'physicalCSet',row['physicalCSet']==g['physicalCSet'])
   check(prefix+'spacingCSet',row['spacingCSet']==g['spacingCSet'])
   check(prefix+'allowEtch',bool(row['allowEtch'])==(row['layer'] in g['allowed_layers']))
   check(prefix+'viaOnlyApproved',row['approvedVias'].strip(':')=='L28_VIA030_C060')
   for native,key in [('lineLineMM','line_line'),('smdpinLineMM','smdpin_line'),('viaLineMM','via_line'),('lineShapeMM','line_shape')]:check(prefix+native,abs(row['allSpacingKeys'][key]-g['spacingFields_mm'][key])<1e-5)
out=dict(status='PASS_INDEPENDENT_POWER02D_CHECKPOINT_REVIEW' if all(c['passed'] for c in C) else'FAIL_REVIEW',checks=len(C),failed=[c for c in C if not c['passed']],results=C,
 scope='Fixed02d checkpoints only, before03star/MCU/USB/ordinarysignals. Actual prescribed copper widths/routes/vias and localCINplane corridor plus69net2LbaseCSetprofile verified. No whole-board currentflow/groundneck/stability/EMI/manufacturing approval. Native topological samecomponent alone is insufficient; localplane strip independentlychecked.',
 necks_mm={'VIN_U2':.95,'U2_GND':.6,'SW_U2':1.15,'BOOT_U2':.6},
 phase='INPUT_BUCK_LDO_FEEDBACK_ONLY_NOT_FINAL_ROUTED_BOARD')
(R/'readouts/review_power02d.json').write_text(json.dumps(out,indent=2)+'\n')
(R/'readouts/evidence_power02d.json').write_text(json.dumps(dict(files=E),indent=2)+'\n')
print(json.dumps(dict(status=out['status'],checks=len(C),failed=out['failed'][:8])))
