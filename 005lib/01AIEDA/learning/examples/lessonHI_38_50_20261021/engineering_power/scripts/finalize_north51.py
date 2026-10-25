from pathlib import Path
import sys,json,math,copy,hashlib
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power'
for v in ['2L','4L']:
 cp=H/f'inventory/checkpoints/clearance_{v}_b016_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');p=load(O/f'N49_{v}_policy.json');p['pendingOperations']=[];q=load(O/f'GPIO_NORTH6_{v}_50.json');old=next(a for a in q['operations'] if a['id']==f'N50_{v}_RETURN_1');newxy=[41.4,28.15];oldxy=old['xy'];old['xy']=newxy;old['purpose']='Local common GND return for genuine new PC14 source transition; replacing old-signalvia41,27.8 leaves historical antipad in frozen fills, so require actual regenerated commonproof rather than full frozen disk predicate.'
 for op in q['operations']:
  if op['type']=='deleteVia':coll=n['vias'];ms=[a for a in coll if a['net']==op['net'] and math.dist(a['xy'],op['xy'])<1e-6];assert len(ms)==1;coll.remove(ms[0])
  elif op['type']=='deleteSegment':coll=n['routes'];ms=[a for a in coll if a['net']==op['net'] and a['layer']=='ETCH/'+op['layer'] and abs(a['width']-op['width'])<1e-6 and a['startEnd'] in [op['points'],list(reversed(op['points']))]];assert len(ms)==1;coll.remove(ms[0])
 s=CopperScene(n,w,r,p)
 for op in q['operations']:
  if op['type'] in ['via','route']:s.add_operation(op)
 hits=[];margins=[]
 for l in LAYERS:
  disk=Point(newxy).buffer(.3,quad_segs=48)
  for a in s.obstacles:
   if a['layer']!=l or a['net']=='GND':continue
   gap=disk.distance(a['geometry']);need=s.space('GND',a['net'],l,a['kind'],True);margins.append(dict(layer=l,otherNet=a['net'],kind=a['kind'],source=a['source'],gapMM=gap,requiredMM=need,marginMM=gap-need))
   if gap<need-.0001:hits.append(margins[-1])
 commonCoverage=[]
 for a in n['planes']:
  l=a['layer'].removeprefix('ETCH/')
  if a['net']!='GND' or not a.get('generated') or l not in (['BOTTOM'] if v=='2L' else ['L2','L3']):continue
  g=plane_from_native(dict(a,holes=a.get('holes') or []));area=g.intersection(disk).area
  if area>1e-5:commonCoverage.append(dict(layer=l,planeAreaMM2=g.area,currentExistingCopperIntersectionMM2=area,currentFullDiskAreaMM2=disk.area,historicalOldSignalAntipadNotRecomputed=True))
 assert not hits,(v,hits)
 assert commonCoverage,(v,'newGND has no actual reference copper contact even before oldsignalantipad removal')
 ret=q['returns'][0];ret.update(returnXY=newxy,distanceMM=math.dist(ret['signalXY'],newxy),currentRefCopperDiskCovered=False,actualExistingCommonCopperContact=commonCoverage,reason='Do not add far2.28mm GND redundant to existing common vias merely to satisfy oldfullDisk predicate; actual nearGND has nonzero broadplane contact and final removal/refill expands oldsignalantipad. Not a claim oldpixel is finalHFreturn.')
 q['sourceCheckpointSHAEvidence']=dict(normalizedSHA256=hashlib.sha256((cp/'normalized.json').read_bytes()).hexdigest(),networksSHA256=hashlib.sha256((cp/'networks.json').read_bytes()).hexdigest(),rulesSHA256=hashlib.sha256((cp/'base_net_rules.json').read_bytes()).hexdigest());q['batchId']='GPIO_NORTH6_'+v+'_51';q['geometryIssues']=[];q['sourceReturnExactReview']=dict(oldFarXY=oldxy,newXY=newxy,distanceMM=ret['distanceMM'],nearest=sorted(margins,key=lambda a:a['marginMM'])[:8],coverage=commonCoverage,requiredNativeProof='NewGNDmust reach C1.2; do notaccept pad merely same net or countdistance. ExistingcommonGND/negative all preserved.')
 q['scope']='Complete6net normal0.2 traces,5newstock signalvias minus2oldPC14stockvias,4newstockGND. No new ruleexceptions/alllayerpermissions. Endpointsfrom realU1pins, no artificialsourceConnectivity declaration.'
 (O/f'GPIO_NORTH6_{v}_51.json').write_text(json.dumps(q,indent=2));print(v,'39op',ret['distanceMM'],'hits',hits,'coverage',commonCoverage,'nearest',sorted(margins,key=lambda a:a['marginMM'])[:2])