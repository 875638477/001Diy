import sys
sys.dont_write_bytecode=True
import pathlib,json,math,hashlib,copy,html
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');O=R/'review/b020_engineering';sys.path.insert(0,str(R/'scripts'))
from routing_geometry import CopperScene,load,Point,LineString,unary_union,plane_from_native

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def geometry_graph(sc,net):
 objects=[x for x in sc.obstacles if x['net']==net];parent=list(range(len(objects)))
 def root(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 def join(i,j):parent[root(i)]=root(j)
 for i,a in enumerate(objects):
  for j,b in enumerate(objects[:i]):
   if a['layer']==b['layer'] and a['geometry'].distance(b['geometry'])<1e-6:join(i,j)
   elif a['layer']!=b['layer'] and a['kind']==b['kind']:
    if a['kind']=='via' and a['geometry'].centroid.distance(b['geometry'].centroid)<1e-6:join(i,j)
    elif a['kind']=='thrupin' and a['source']==b['source']:join(i,j)
 terms={a['source']:root(i) for i,a in enumerate(objects) if a['kind'] in ('smdpin','thrupin')}
 return objects,root,terms

report={'status':'READ_ONLY_LOCAL_CANDIDATE_GEOMETRY_CHECKED_NOT_NATIVE_OR_SI_SIGNOFF','sourceStatus':'Saved b019 DRC_PENDING; USB solver/full-board checks still pending','variants':{},'changesRequireNativeReview':True,'nativeStarted':False}
for v in ('2L','4L'):
 s=load(O/f'PB10_NW_{v}_v46_snapshot.json');original=load(R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING'/'normalized.json');d=R/'inventory/checkpoints'/f'padentry_{v}_b019_DRC_PENDING';rules=load(d/'base_net_rules.json');sc=CopperScene(s,load(d/'networks.json'),rules,load(R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_policy.json'))
 audits=load(O/'PB10_NW_North4_repack_v46.json')[v]
 identitiesEqual=s['placements']==original['placements'];checks={}
 for net in ('GPIO_PA3','GPIO_PA2','GPIO_PA1','GPIO_PC15','GPIO_PC13','GPIO_PB10'):
  obj,find,terms=geometry_graph(sc,net);sets={};
  for key,cc in terms.items():sets.setdefault(str(cc),[]).append(key)
  checks[net]={'terminalComponents':list(sets.values()),'allActualPhysicalPinsConnected':len(sets)==1,'geometryOnlyNotNativeBFS':True}
  if net=='GPIO_PB10':
   c=terms['U1.21'];xy=Point(30,35.72);checks[net]['sourcePinToCandidateVia']=any(a['kind']=='via' and a['geometry'].covers(xy) and find(i)==c for i,a in enumerate(obj));checks[net]['fullJ12ExpectedDisconnected']=len(sets)==2
 # Full source-state inner via/pad drills remain unmodified other than explicit objects.
 refs=[]
 for o in audits['deltaOperations']:
  if o['type']!='route' or o['net']!='GPIO_PB10':continue
  reference='TOP' if v=='2L' and o['layer']=='BOTTOM' else ('BOTTOM' if v=='2L' else ('L3' if o['layer']=='BOTTOM' else 'L2'))
  ground=unary_union([plane_from_native(dict(p,holes=p.get('holes') or [])) for p in original['planes'] if p['net']=='GND' and p['filled'] and p['layer']=='ETCH/'+reference]);missing=LineString(o['points']).difference(ground)
  refs.append({'id':o['id'],'signalLayer':o['layer'],'referenceLayer':reference,'missingCurrentFillCenterlineWKT':missing.wkt,'missingLengthMM':missing.length,'comment':'Original fill only; old via holes/thermal voids are stale after this candidate. Refill and native return/common/HSE checks are mandatory.'})
 # Explicit current-fill status around each proposed new return pad; not a new native common connection proof.
 returnFootprints=[]
 for xy in ([29.2,35.35],)+(([36.9,27.8],) if v=='2L' else ()):
  for layer in ('TOP','BOTTOM'):
   ground=unary_union([plane_from_native(dict(p,holes=p.get('holes') or [])) for p in original['planes'] if p['net']=='GND' and p['filled'] and p['layer']=='ETCH/'+layer]);disk=Point(xy).buffer(.3,quad_segs=128)
   returnFootprints.append({'xy':xy,'layer':layer,'copperPadOverlapCurrentGNDMM2':disk.intersection(ground).area,'padAreaMM2':disk.area,'nativeCommonProof':'PENDING_NATIVE_REFILL'})
 report['variants'][v]={'boardSHA256':audits['actualSourceSHA256'],'placementAndEveryPhysicalPinStrictlyUnchanged':identitiesEqual,'outerAuditRecords':sum(1 for x in audits['audit'] if x['layer'] in ('TOP','BOTTOM')),'innerViaAuditRecords':sum(1 for x in audits['audit'] if x['layer'] in ('L2','L3')),'unresolvedBaseAndFiniteSpacingIssues':audits['unresolvedCount'],'physicalConnectivityGeometry':checks,'referenceGaps':refs,'proposedReturnCurrentFillOverlap':returnFootprints,'newReturnViaToPB10ViaMM':math.dist([29.2,35.35],[30,35.72]),'newPC13ViaToRetainedReturnMM':math.dist([29.25,40.05],[30.05,40.25]),'ruleChanges':[],'newViaPadstack':'L28_VIA030_C060 globally approved in existing profile','newNormalWidthsMM':.2,'inputHashes':{str(p.relative_to(R)):sha(p) for p in [d/'normalized.json',d/'networks.json',d/'base_net_rules.json',R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_delta.json',R/'engineering_mcu/plans'/f'GPIO_PB1_inward_{v}_80_policy.json']}}
 # Lightweight exported engineering diagram; data is actual old reference fill plus proposed manual line, never a future fill rendering.
 reference='TOP' if v=='2L' else 'L3';ground=unary_union([plane_from_native(dict(p,holes=p.get('holes') or [])) for p in original['planes'] if p['net']=='GND' and p['filled'] and p['layer']=='ETCH/'+reference])
 polys=[f'<path d="{ground.svg().split(chr(34))[1]}" />'] if False else []
 background=ground.svg(scale_factor=.08,fill_color='#b9d9c3',opacity=.7)
 lines=[]
 for op in audits['deltaOperations']:
  if op['type']=='route' and op['layer']=='BOTTOM':
   colour='#d33226' if op['net']=='GPIO_PB10' else '#4265af';width=op['width'];points=' '.join(f'{x},{y}' for x,y in op['points']);lines.append(f'<polyline points="{points}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
 for p in s['placements']:
  if p['ref']=='U1':
   for a in p['pins']:
    if not a['number']:continue
    x,y=a['xy'];lines.append(f'<circle cx="{x}" cy="{y}" r=".08" fill="#777"/>')
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="820" viewBox="0 0 1100 820"><rect width="1100" height="820" fill="white"/><text x="30" y="30" font-family="sans-serif" font-size="18">{v} PB10 local candidate v46; current {reference} GND projection (not repoured)</text><text x="30" y="55" font-family="sans-serif" font-size="14">Red = proposed PB10 BOTTOM; blue = repacked ordinary North tails; geometry only, no native run</text><svg x="30" y="80" width="1040" height="710" viewBox="26 -42 16 19"><g transform="scale(1,-1)">{background}{"".join(lines)}</g></svg></svg>'
 (O/f'PB10_{v}_v46_reference.svg').write_text(svg,encoding='utf8')
# Verify all previously sealed native evidence without changing it.
m=load(R/'review/b017_b019_native_artifact_manifest.json');fail=[]
for a in m['files']:
 p=R/a['path']
 if not p.is_file() or p.stat().st_size!=a['size'] or sha(p)!=a['sha256']:fail.append(a['path'])
report['priorSealedCollection']={'manifest':'review/b017_b019_native_artifact_manifest.json','manifestSHA256':sha(R/'review/b017_b019_native_artifact_manifest.json'),'count':len(m['files']),'failureCount':len(fail),'failures':fail,'all1545Unchanged':not fail}
(O/'PB10_v46_review_summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'variants':{v:{'unresolved':a['unresolvedBaseAndFiniteSpacingIssues'],'identitiesEqual':a['placementAndEveryPhysicalPinStrictlyUnchanged'],'connectivity':a['physicalConnectivityGeometry']} for v,a in report['variants'].items()},'sealed':report['priorSealedCollection']},indent=2))
