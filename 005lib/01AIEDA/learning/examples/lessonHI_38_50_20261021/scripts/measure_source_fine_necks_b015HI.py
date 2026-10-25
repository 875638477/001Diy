from pathlib import Path
import json,math,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');out=[]
for v in ['2L','4L']:
 C=R/f'inventory/checkpoints/source_{v}_b015_DRC_PENDING';N=json.loads((C/'normalized.json').read_text());checks=[]
 for net,pin,limit in [('GPIO_PB1','19',2.8),('GPIO_PB10','21',2.6),('VBUS_PRESENT_N','18',1.4)]:
  lines=[r for r in N['routes'] if r['layer']=='ETCH/TOP' and r['net']==net and r.get('fixedManualCline') and abs(r['width']-.16)<1e-7];pinxy=next(p['xy'] for c in N['placements'] if c['ref']=='U1' for p in c['pins'] if p['number']==pin)
  near=lambda a,b:math.dist(a,b)<.00011
  selected={i for i,r in enumerate(lines) if any(near(p,pinxy) for p in r['startEnd'])};assert selected,(net,pinxy)
  changed=True
  while changed:
   changed=False
   for i,r in enumerate(lines):
    if i not in selected and any(near(a,b) for j in selected for a in lines[j]['startEnd'] for b in r['startEnd']):selected.add(i);changed=True
  lengths=[math.dist(*lines[i]['startEnd']) for i in sorted(selected)];length=sum(lengths);checks.append({'net':net,'sourcePin':'U1.'+pin,'sourceActualXY':pinxy,'widthMM':.16,'actualContinuousTOPSourceClineLengthMM':length,'maximumEngineeringContractMM':limit,'pass':length<=limit+1e-7,'segments':[lines[i]['startEnd'] for i in sorted(selected)],'individualLengthsMM':lengths,'method':'Sum each actual fixed .16 TOP segment in endpoint-connected component rooted at physical pin center, using native saved/fresh-read geometry; includes pad-internal copper. Separate from native DRC neck-rule result.'})
 out.append({'variant':v,'sourceSnapshot':str(C),'sourceNormalizedSHA256':hashlib.sha256((C/'normalized.json').read_bytes()).hexdigest().upper(),'checks':checks})
D={'status':'PASS_EXPLICIT_FINE_NECK_GEOMETRY_CONTRACTS' if all(c['pass'] for d in out for c in d['checks']) else 'FAILED_ENGINEERING_FINE_NECK_CONTRACT','nativeDRC':'UNRECOMPUTED_PENDING','variants':out};(R/'review/source_b015_fine_neck_contracts.json').write_text(json.dumps(D,indent=2),encoding='utf8');print(json.dumps({'status':D['status'],'lengths':[{d['variant']:[(c['net'],c['actualContinuousTOPSourceClineLengthMM'],c['pass']) for c in d['checks']]} for d in out]},indent=2))
