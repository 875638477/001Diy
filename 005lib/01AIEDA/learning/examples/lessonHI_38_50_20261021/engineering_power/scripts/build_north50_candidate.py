from pathlib import Path
import sys,json,math,copy,re,csv,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
import numpy as np,shapely
O=H/'engineering_power'
for v in ['2L','4L']:
 cp=H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING'
 if (cp/'normalized.json').exists():n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');actualStatus='ACTUAL_SAVED_B016_CHECKPOINT'
 else:n=load(H/'review/PROVISIONAL_UNSAVED_b016_2L_try11.json');w=load(O/f'N49_{v}_networks.json');r=load(O/f'N49_{v}_rules.json');actualStatus='ACTUAL_UNSAVED_TRY11_PENDING_FORMAL_REBASE'
 p=load(O/f'N49_{v}_policy.json');p['pendingOperations']=[];base=load(O/f'N49_base_{v}.json')['operations'];search=load(O/f'N49_{v}_search01.json');prefix=load(O/f'N49_{v}_policy.json')['pendingOperations'];assert not search['failures'];deletes=[]
 for op in base:
  coll=n['vias'] if op['type']=='deleteVia' else n['routes']
  ms=[a for a in coll if a['net']==op['net'] and ((math.dist(a['xy'],op['xy'])<1e-6) if op['type']=='deleteVia' else a['layer']=='ETCH/'+op['layer'] and abs(a['width']-op['width'])<1e-6 and a['startEnd'] in [op['points'],list(reversed(op['points']))])];assert len(ms)==1,(v,op,len(ms));coll.remove(ms[0]);deletes.append(dict(id=op['id'],matchedExactlyOne=True))
 s=CopperScene(n,w,r,p);ops=[];issues=[]
 for op in prefix+search['operations']:
  op=copy.deepcopy(op);op['id']='N50_'+v+'_'+op['id'];ops.append(op)
  if op['type']=='route' and not s.path_clear(op['net'],op['layer'],op['points'],op.get('width',.2)):issues.append(dict(id=op['id'],reason='exact continuous path_clear failed'))
  if op['type']=='via':
   for l in LAYERS:
    bad,inside=s.forbidden(op['net'],l,.2,True,.001)
    if bad.intersects(Point(op['xy'])) or not inside.covers(Point(op['xy'])):issues.append(dict(id=op['id'],reason='via exact geometry/keepout/drillpad failed',layer=l))
  s.add_operation(op)
 # Common-plane shapes are mapped to actual native GND component1; staticquiet never eligible.
 commonBBoxes={}
 for row in csv.DictReader((Path(n['readbackDirectory'])/'hi_graph_objects.tsv').open(encoding='utf8'),delimiter='\t'):
  if row['net'].strip(chr(34))!='GND' or row['component']!='1' or row['type'].strip(chr(34))!='shape':continue
  mt=re.search(r'\bbBox \(\(([-+\d.]+) ([-+\d.]+)\) \(([-+\d.]+) ([-+\d.]+)\)\)',row['attributes'])
  if mt:commonBBoxes.setdefault(row['layer'].strip(chr(34)),[]).append(tuple(float(z) for z in mt.groups()))
 comm={};coverageIdentities=[]
 for a in n['planes']:
  if a['net']!='GND' or not a.get('generated'):continue
  g=plane_from_native(dict(a,holes=a.get('holes') or []));layer=a['layer'].removeprefix('ETCH/')
  if any(max(abs(x-y) for x,y in zip(g.bounds,bb))<.001 for bb in commonBBoxes.get(a['layer'],[])):
   comm.setdefault(layer,[]).append(g);coverageIdentities.append(dict(layer=layer,area=g.area,bbox=g.bounds,nativeGroundComponent=1))
 comm={l:unary_union(gs) for l,gs in comm.items()};refLayers=['BOTTOM'] if v=='2L' else ['L2','L3'];assert all(l in comm for l in refLayers),(v,list(comm),commonBBoxes.keys())
 quiet=unary_union([Polygon(a['polygon']) for a in p.get('reservedAreas',[]) if any(x in a['id'].upper() for x in ['HSE','OSC','QUIET'])]);allOldGroundVias=[a['xy'] for a in n['vias'] if a['net']=='GND'];returns=[];newSignal=[a for a in ops if a['type']=='via'];newGround=[]
 for vi in newSignal:
  sx,sy=vi['xy'];already=[a for a in newGround if math.dist(a['xy'],vi['xy'])<=1.5]
  if already:returns.append(dict(signalId=vi['id'],signalXY=vi['xy'],returnId=already[0]['id'],returnXY=already[0]['xy'],distanceMM=math.dist(vi['xy'],already[0]['xy']),shared=True));continue
  bads=[s.forbidden('GND',l,.6,True,.006) for l in LAYERS];xs=np.arange(round((sx-3)*20)/20,round((sx+3)*20)/20+.025,.05);ys=np.arange(round((sy-3)*20)/20,round((sy+3)*20)/20+.025,.05);xx,yy=np.meshgrid(xs,ys);valid=np.ones_like(xx,dtype=bool)
  for bad,inside in bads:valid &= ~shapely.contains_xy(bad,xx,yy)&shapely.contains_xy(inside,xx,yy)
  dist=np.hypot(xx-sx,yy-sy);valid &= (dist>=.92)&(dist<=3)
  if not quiet.is_empty:valid &= ~shapely.contains_xy(quiet.buffer(.35),xx,yy)
  found=[]
  for iy,ix in zip(*np.where(valid)):
   xy=[round(float(xx[iy,ix]),5),round(float(yy[iy,ix]),5)]
   if any(math.dist(xy,z)<.61 for z in allOldGroundVias+[a['xy'] for a in newGround]):continue
   disk=Point(xy).buffer(.3002,quad_segs=24)
   if not all(comm[l].covers(disk) for l in refLayers):continue
   found.append((float(dist[iy,ix]),xy))
  found.sort()
  if not found:returns.append(dict(signalId=vi['id'],signalXY=vi['xy'],status='NO_ELIGIBLE_COMMON_RETURN_WITHIN3MM'));continue
  d,xy=found[0];go=dict(type='via',id='N50_'+v+'_RETURN_'+str(len(newGround)+1),net='GND',xy=xy,padstack='L28_VIA030_C060',purpose='Native common component1 historical diskcoverage; actual final fill/return proof required; not oscillatorlocal ground')
  ops.append(go);newGround.append(go);s.add_operation(go);returns.append(dict(signalId=vi['id'],signalXY=vi['xy'],returnId=go['id'],returnXY=xy,distanceMM=d,currentRefCopperDiskCovered=refLayers,new=True))
 proofs=copy.deepcopy(search['proofs'])
 for a in newGround:proofs.append(dict(id=a['id']+'_APP_COMMON',**{'from':'C1.2','toAlias':a['id'],'connected':True}))
 lengths={}
 for op in ops:
  if op['type']=='route':lengths[op['net']]=lengths.get(op['net'],0)+sum(math.dist(a,b) for a,b in zip(op['points'],op['points'][1:]))
 result=dict(status='COMPLETE_GEOMETRIC_CANDIDATE_NATIVE_AND_FULL_COMBINED_REVIEW_PENDING' if not issues else 'GEOMETRY_REBASE_ISSUES_PENDING',variant=v,batchId='GPIO_NORTH6_'+v+'_50',sourceStatus=actualStatus,sourceCheckpoint=str(cp),sourceNativeLog=n['readbackDirectory'],sourceExpectedSHA256=w.get('sourceSHA256',w.get('sha256')),operations=base+ops,proofs=proofs,sourceRipupCount=len(base),signals=6,newSignalVias=len(newSignal),newGroundVias=len(newGround),deletes=deletes,geometryIssues=issues,returns=returns,newRouteLengthsMM=lengths,nativeCommonPlaneIdentities=coverageIdentities,pinPolicy=dict(PC13_PC14_PC15=dict(maxOutputFrequencyMHz=2,maxLoadPF=30,backupPowerSwitchCurrentLimitMA=3,prohibitCurrentSourceLED=True,source='ST DS5319 Rev20 Pinouts footnote5 and5.3.13 https://www.st.com/resource/en/datasheet/stm32f103c8.pdf',externalHeaderCableLoad='UNVERIFIED_DO_NOT_CALL_ARBITRARY_HIGH_SPEED_GPIO'),generalGPIO=dict(initialEdgePolicy='lowest sufficient slew; actual firmware load/rise/fall remain unconfigured; no equal-length requirement for ordinaryGPIO')),requiredBeforeNative=['Joint actual south7 complete-copper check; no greedy partial freeze','Replace this sourceSHA with exact formal2Lb016 if sourceStatus unsaved','No replay SOURCEfix or LIVEV3 deletion; originalJ12north remains','HSE uniqueanchor negative, all existing endpoint proofs, actual new GND componentconnectivity, no signal orphan','Physical inner layers/complete Films unchanged; no new global/inneretch permission','Actual2L TOPGND/4LL2L3 width/neck/reference after allmanual and finalfill','Final fresh full whole-board DRC; intermediate0scoped is not fullDRC'],notClaimed='SI/PI/EMI/90ohm/delay/manufacturing certification')
 (O/f'GPIO_NORTH6_{v}_50.json').write_text(json.dumps(result,indent=2));print(v,actualStatus,len(base+ops),'issues',issues,'returns',returns)