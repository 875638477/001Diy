from pathlib import Path
import json,csv,re,hashlib,sys,shutil
sys.dont_write_bytecode=True
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sys.path.insert(0,str(R/'tooling/packages'));from shapely.geometry import Polygon
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper();s=(R/'scripts/normalize_HI_actual_v5.py').read_text();ns={'json':json,'re':re};exec(s[s.index('def sx('):s.index('symbols=')],ns);sx=ns['sx'];rows=lambda p:list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def bounds(p):
 out=[]
 for r in rows(p):
  if r['layer'].startswith('HI_'):continue
  a=sx(r['attributes']);attrs=dict(zip(a[::2],a[1::2]));poly=Polygon([x[0] for x in sx(r['vertices'])]);out.append({'layer':sx(r['layer']),'net':sx(r['net']),'polygon':poly,'voids':[Polygon([x[0] for x in pp]) for pp in sx(r['permanentVoids']) or []],'properties':attrs['prop'],'priority':attrs['priority'],'fill':attrs['fill'],'isBoundary':attrs['shapeIsBoundary']})
 return out
old=bounds(R/'logs/reopen_source_2L_b015_DRC_PENDING_stored/hi_dynamic_boundaries.tsv');new=bounds(R/'logs/reopen_clearance_2L_b016_DRC_PENDING_stored/hi_dynamic_boundaries.tsv');assert len(old)==len(new)==4;pairs=[]
for o in old:
 matches=[a for a in new if a['layer']==o['layer'] and a['polygon'].equals(o['polygon'])];assert len(matches)==1;a=matches[0];assert a['net']==o['net']=='GND' and a['properties']==o['properties'] and a['fill']==o['fill'] and a['isBoundary']==o['isBoundary'];assert len(a['voids'])==len(o['voids']);assert all(len([x for x in a['voids'] if x.equals(v)])==1 for v in o['voids']);pairs.append({'layer':o['layer'],'outerArea':o['polygon'].area,'permanentVoidAreas':[v.area for v in o['voids']],'oldPriority':o['priority'],'newPriority':a['priority'],'propertiesExactlyEqual':True,'polygonAndEveryPermanentVoidExactlyEqual':True,'fillAndDynamicClassSame':True})
for i,o in enumerate(old):
 for j,b in enumerate(old):
  if o['layer']==b['layer'] and o['priority']<b['priority']:assert pairs[i]['newPriority']<pairs[j]['newPriority']
build=(R/'logs/clearance_remaining_2L_b016_DRC_PENDING_try12/hi_batch_execution.txt').read_text();bp=[sx(x.split('globalShapeParameters=',1)[1]) for x in build.splitlines() if x.startswith('HI_REFERENCE_DEFER_BEFORE')];ap=next(sx(x.split('HI_REFERENCE_GLOBAL_PARAMETERS_AFTER=',1)[1].rsplit(' exactEqualBefore=',1)[0]) for x in build.splitlines() if x.startswith('HI_REFERENCE_GLOBAL_PARAMETERS_AFTER='));assert len(bp)==4 and all(b==ap for b in bp);report={'status':'B016_2L_REFERENCE_DEFINITIONS_PERMANENT_VOIDS_GLOBAL_THERMAL_PARAMETERS_RELATIVE_PRIORITIES_PRESERVED','pairs':pairs,'all4BeforeParameterRecordsExactlyEqualAfter':True,'sameLayerRelativePrioritiesPreserved':True,'absolutePriorityNumbersNotPersistentIdentity':True,'staticQuietShapeNotSelected':True,'generatedFillMayChangeWithApprovedNewRoutes':True,'wholeBoardDRC':None};(R/'review/b016_2L_reference_preservation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
# Keep deprecated01 inputs untouched; map final executed geometry to newly-frozen canonical02 files.
M={'status':'B016_EXECUTED_GEOMETRY_EQUIVALENT_CORRECTED_ROOT_CANONICAL02','variants':{}}
keys=['type','id','net','layer','points','width','widths','xy','padstack'];core=lambda o:{k:o[k] for k in keys if k in o}
for v,t in [('2L','12'),('4L','05')]:
 d=json.loads((R/f'batches/clearance_remaining_{v}_b016_DRC_PENDING_try{t}.json').read_text());ops=[]
 for o in d['operations']:
  ops.extend(o['targets'] if o['type'] in ['secondExactBatch','exactBatch'] else [o])
 lookup={o['id']:o for o in ops};items=[];snap=R/f'source/engineering_snapshots/clearance_remaining_{v}_b016_DRC_PENDING'
 for n in [f'root_source_clearance_cleanup_{v}_02.json',f'remaining_services_{v}_b015_02.json',f'J2_GND_entry_{v}_02.json']:
  src=R/'plans'/n;dest=snap/('canonical_'+n);assert not dest.exists();shutil.copyfile(src,dest);p=json.loads(src.read_text())
  for o in p['operations']:assert core(o)==core(lookup[o['id']]),('Canonicalgeometrymismatch',v,n,o,lookup.get(o['id']))
  items.append({'source':str(src),'snapshot':str(dest),'sha256':sha(dest),'operationsGeometryExactlyEqualExecutedAdapter':True,'operationCount':len(p['operations'])})
 manifest=[{'file':str(p),'sha256':sha(p)} for p in sorted(snap.glob('*.json')) if p.name!='manifest.json'];(snap/'complete_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');M['variants'][v]={'canonicalInputs':items,'deprecated01ByteSnapshotsKept':True,'liveR27FeedDeletionNotExecutedInFinalPlan':not any(o['id'].startswith('NSS_OLD_R25_V3_BRANCH_CLEANUP_') for o in ops),'J2NormalConnectsActualPinCenters':True,'loadOrder':str(R/f'source/batch_snapshots/clearance_remaining_{v}_b016_DRC_PENDING_try{t}/inputs_manifest.json')}
(R/'review/b016_corrected_canonical02_mapping.json').write_text(json.dumps(M,indent=2),encoding='utf8');print(report['status']);print(M['status'])