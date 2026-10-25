"""Independent raw native fresh text/height review and current-identity CSV export. No native invocation.
Usage: python -B j55_validate_corrected.py --inputs audits/j55_fresh_inputs.json
Inputs: {"2L":{"board":"...","log":"..."},"4L":...}. Logs use original HI raw TSV schemas.
"""
from pathlib import Path
import sys,json,csv,hashlib,math,collections,argparse
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';H=R/'learning/examples/lessonHI_38_50_20261021'
ns={};src=(J/'scripts/j55_57_build.py').read_text(encoding='utf-8-sig');exec(src[:src.index("req=['REF DES")],ns);srows=ns['srows'];dump=ns['dump'];csvout=ns['csvout'];load=ns['load'];sha=ns['sha']
a=argparse.ArgumentParser();a.add_argument('--inputs',required=True);a.add_argument('--variant',choices=['2L','4L']);a=a.parse_args();inputs=load(a.inputs);spec=load(R/'learning/examples/de_15_26_20261019/integrated_circuit.json');values={c['ref']:c['value'] for c in spec['components']};allChecks=[];prior=J/'audits/j55_corrected_independent_summary.json';result=load(prior).get('variants',{}) if prior.exists() else {}
def pt(a,b):return math.dist(a,b)<.00011
for v in ([a.variant] if a.variant else ['2L','4L']):
 source=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';old=load(source/'normalized.json');P={p['ref']:p for p in old['placements']};L=Path(inputs[v]['log']);B=Path(inputs[v]['board']);assert B.resolve().is_relative_to(J.resolve());assert L.resolve().is_relative_to(J.resolve());assert B.exists()
 out=J/'assembly'/f'JK55_{v}_corrected_TRAINING';out.mkdir(exist_ok=True);raw=srows(L/'board_instance_texts.tsv');geo=srows(L/'g_actual_geometry.tsv');sym=[]
 if (L/'g_actual_symbols.tsv').exists():sym=srows(L/'g_actual_symbols.tsv')
 else:
  for line in (L/'jk55_instance_properties.tsv').read_text(encoding='utf-8').splitlines():
   if line.startswith('SYMBOL'+chr(9)):
    fields=line.split(chr(9));sym.append(dict(zip(['refdes','package','xy','rotation','mirrored'],[ns['sx'](z) for z in fields[1:]])))
 current={s['refdes']:s for s in sym if s['refdes']};check=[]
 def ck(label,passed,detail=None):check.append(dict(label=label,passed=bool(passed),detail=detail))
 ck('80 actual components',set(current)==set(P));ck('247 exact instance text count',len(raw)==247);ck('zero obsolete VALUEsilk',not any(t['layer']=='COMPONENT VALUE/SILKSCREEN_TOP' for t in raw));ck('7 PACKAGE silk text unchanged',len([t for t in raw if t['layer']=='PACKAGE GEOMETRY/SILKSCREEN_TOP'])==7)
 textRows=[];heightRows=[];defaults=0;explicit=0
 for ref,p in P.items():
  s=current[ref];ck(ref+' native placement unchanged',pt(s['xy'],p['xy']) and s['rotation']==p['rotation'] and bool(s['mirrored'])==bool(p['mirrored']) and s['package']==p['package'])
  for layer in ['REF DES/SILKSCREEN_TOP','REF DES/ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP']:
   actual=[t for t in raw if t['refdes']==ref and t['layer']==layer];ck(ref+' '+layer+' unique',len(actual)==1)
   if len(actual)!=1:continue
   t=actual[0];expected=values[ref] if layer.startswith('COMPONENT VALUE/') else ref
   template=next((z for z in p['texts'] if z['layer']==layer),None)
   if template is None and layer.startswith('COMPONENT VALUE/'):template=next((z for z in p['texts'] if z['layer']=='COMPONENT VALUE/SILKSCREEN_TOP'),None)
   if template is None:template=next(z for z in p['texts'] if z['layer']=='REF DES/ASSEMBLY_TOP')
   ok=t['text']==expected and pt(t['xy'],s['xy']) and t['rotation']==s['rotation'] and bool(t['mirrored'])==bool(s['mirrored']) and t['textBlock']==template['textBlock'] and t['justify'].upper()==template['justify'].upper()
   ck(ref+' '+layer+' actual origin/value/orientation/style',ok);textRows.append(dict(Variant=v,Reference=ref,Layer=layer,Text=t['text'],X_mm=t['xy'][0],Y_mm=t['xy'][1],Rotation=t['rotation'],Mirrored=bool(t['mirrored']),Justify=t['justify'],TextBlock=t['textBlock'],Result='PASS' if ok else 'FAIL'))
  oldShapes=[g for g in p['geometry'] if g['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP' and g['type']=='shape'];newShapes=[g for g in geo if g['refdes']==ref and g['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP' and g['type']=='shape'];ck(ref+' shape count',len(oldShapes)==len(newShapes)==1)
  if len(oldShapes)==len(newShapes)==1:
   q,n=oldShapes[0],newShapes[0];op=dict(q['props'] or []);np=dict(n['props'] or []);ck(ref+' shape geometry preserved',q['bbox']==n['bbox'] and q['vertices']==n['vertices']);default='PACKAGE_HEIGHT_MAX' not in op
   desired=dict(op)
   if default:desired['PACKAGE_HEIGHT_MAX']='1 MM';defaults+=1
   else:explicit+=1
   ck(ref+' all height properties correct',np==desired,dict(before=op,after=np,desired=desired));heightRows.append(dict(Variant=v,Reference=ref,ActualMax=np.get('PACKAGE_HEIGHT_MAX',''),HeightStatus='USER_DEFAULT_NOT_PHYSICAL_CERTIFICATION' if default else 'EXPLICIT_CAD_PRESERVED',AllProps=json.dumps(np,ensure_ascii=False)))
  for o in [g for g in p['geometry'] if g['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP' and g['type']=='path']:
   found=[g for g in geo if g['refdes']==ref and g['type']=='path' and g['layer']==o['layer'] and g['bbox']==o['bbox'] and g['props']==o['props']];ck(ref+' legacy bound path preserved',len(found)==1)
 ck('72 default and8 explicit shapeMAX',defaults==72 and explicit==8)
 for ref,p in P.items():
  for o in [t for t in p['texts'] if t['layer']=='PACKAGE GEOMETRY/SILKSCREEN_TOP']:
   found=[t for t in raw if t['refdes']==ref and all(t[k]==o[k] for k in ['layer','text','xy','rotation','mirrored','justify','textBlock','bbox'])];ck(ref+' PACKAGE silk literal preserved',len(found)==1)
 # Same electrical/mechanical definition identity; no component value inferred solely from old normalized metadata.
 oldcomp=ns['rawrows'](Path(old['readbackDirectory'])/'components.tsv');newcomp=ns['rawrows'](L/'components.tsv');ck('native80 component primitive/package identities unchanged',sorted(oldcomp,key=lambda x:x['refdes'])==sorted(newcomp,key=lambda x:x['refdes']))
 for f in ['stackup_full.tsv','cross_section.tsv','films_full.tsv','placed_pins.tsv','physical_pad_layers.tsv']:
  aa=srows(Path(old['readbackDirectory'])/f);bb=srows(L/f)
  # These canonical exports have no transient DBIDs. List order is not semantic.
  canon=lambda rr:sorted(json.dumps(z,sort_keys=True) for z in rr)
  ck(f+' canonical embedded definitions unchanged',canon(aa)==canon(bb))
 csvout(J/f'audits/j55_{v}_corrected_three_texts.csv',textRows);csvout(J/f'audits/j55_{v}_corrected_heights.csv',heightRows)
 bad=[c for c in check if not c['passed']];dump(J/f'audits/j55_{v}_fresh_independent_review.json',dict(status='PASS_INSTANCE_CORRECTION_ONLY' if not bad else 'FAIL',sourceBoard=str(B),sourceSHA256=sha(B),rawLog=str(L),checks=len(check),failed=len(bad),details=check,scope='Independent raw text/height/positions/native definition review. WholeboardDRC, routedCopper/reference, CAM and hardware release require separate native guard and audits.'))
 if bad:raise RuntimeError(v+' actual correction validation failures: '+json.dumps(bad[:8]))
 # All source poses remain exact; retag copies to actual new board, update actual height properties, never overwrite b019 training baseline.
 actualHeight={x['Reference']:x for x in heightRows}
 for prefix in ['BOM_80','BOM_grouped','coordinates_all80','SMT_candidates','non_SMT_and_DNP']:
  base=J/f'assembly/{prefix}_{v}_b019_TRAINING.csv';rows=list(csv.DictReader(base.open(encoding='utf-8-sig',newline='')))
  for row in rows:
   if 'Source_BRD_SHA256' in row:row['Source_BRD_SHA256']=sha(B)
   if 'CAD_Height_Max' in row:
    h=actualHeight[row['Reference']];row['CAD_Height_Max']=h['ActualMax'];row['Height_Status']=h['HeightStatus']
  csvout(out/(prefix+'_TRAINING_NOT_FOR_ASSEMBLY.csv'),rows)
 dump(out/'source_identity.json',dict(status='TRAINING_NOT_FOR_ASSEMBLY',board=str(B),sha256=sha(B),rawReadback=str(L),inputTrainingBaselineSHA256=sha(H/f'native_candidates/HI_{v}_padentry_normalized_b019_DRC_PENDING.brd'),placementAndElectricalIdentitiesPreserved=True,physicalHeightCertification=False,factoryCentroidRotationMapping=False,variantStack='LEGACY_4L_L3_GND' if v=='4L' else 'TOP_BOTTOM',wholeboardDRC='PENDING_NOT_APPROVED'))
 result[v]=dict(board=str(B),sha256=sha(B),checks=len(check),failed=0,requiredTexts=240,allInstanceTexts=247,userDefaultHeightShapes=72,preservedExplicitHeightShapes=8,preservedLegacyBoundPaths=4,assemblyDirectory=str(out));allChecks+=check
dump(J/'audits/j55_corrected_independent_summary.json',dict(status='PASS_INSTANCE_SPECIFICATION_TRAINING_ONLY',variants=result,bothVariantsReviewed=set(result)=={'2L','4L'},checks=sum(x['checks'] for x in result.values()),failed=0));print(json.dumps(result,indent=2))
