from pathlib import Path
import json,csv,hashlib,collections,math,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
outputs={}
for v in ['4L','2L']:
 log=R/f'logs/reopen_postcritical_{v}_b010';src=log/'hi_actual_reference_samples.tsv'
 rows=list(csv.DictReader(src.open(),delimiter='\t',quotechar='\0'));groups={}
 for row in rows:
  net=json.loads(row['net']);layer=json.loads(row['signalLayer']);ref=json.loads(row['referenceLayer']);key=net+'@'+layer
  g=groups.setdefault(key,{'net':net,'layer':layer,'referenceLayer':ref,'sampleCount':0,'uncoveredSamples':0,'applicationOnlySamples':0,'quietOnlySamples':0,'overlappingApplicationQuietSamples':0,'uncoveredXY':[]})
  a=int(row['applicationDynamicCount']);q=int(row['staticQuietCount']);g['sampleCount']+=1
  if not a and not q:g['uncoveredSamples']+=1;g['uncoveredXY'].append(row['xy'])
  elif a and q:g['overlappingApplicationQuietSamples']+=1
  elif a:g['applicationOnlySamples']+=1
  else:g['quietOnlySamples']+=1
 for g in groups.values():g['coveredSampleFraction']=(g['sampleCount']-g['uncoveredSamples'])/g['sampleCount']
 outputs[v]={'status':'GEOMETRIC_NATIVE_POINT_SAMPLING_NOT_RETURN_PATH_APPROVAL','boardIdentity':json.loads((R/f'inventory/current_{v}.json').read_text()),'input':str(src),'inputSHA256':hashlib.sha256(src.read_bytes()).hexdigest().upper(),'sampleCount':len(rows),'uncoveredSamples':sum(g['uncoveredSamples'] for g in groups.values()),'perNetLayer':sorted(groups.values(),key=lambda g:(-g['uncoveredSamples'],g['net'])),'limits':['Actual filled ETCH copper and actual voids queried by official axlGeoPointInShape(...,t).','Centerline samples max0.1mm; endpoints may sit at deliberate antipads/gaps and need contextual review. Samples double-count common line endpoints.','Geometric point coverage does not prove field width, continuous conducting return path, topology, adequate transition return or SI/EMI compliance.','Quiet-island-only coverage is acceptable only for explicitly approved HSE-related paths; all other use requires engineering review.','Boards remain partially routed. Global TOP application pour for2L and final stitch/reference review remain pending.']}
 print(v,'samples',len(rows),'uncovered',outputs[v]['uncoveredSamples'],'worst',[(g['net'],g['layer'],g['uncoveredSamples']) for g in outputs[v]['perNetLayer'][:8]])
(R/'review/native_reference_coverage_b010.json').write_text(json.dumps(outputs,indent=2),encoding='utf8')
p=R/'native/README.md';s=p.read_text();s=s.replace('Two-layer postcritical b010 is in progress as of this update.','Two-layer postcritical b010:62 remaining,58 vias,410 ETCH segments including generated thermals,7 actual GND polygons;68 batch endpoint proofs, fresh readonly zero DRC and stable SHA. The two-layer local TOP patches connect one additional ground terminal compared with four-layer.')
p.write_text(s,encoding='utf8')
