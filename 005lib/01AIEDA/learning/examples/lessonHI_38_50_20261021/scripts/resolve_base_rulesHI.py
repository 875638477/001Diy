from pathlib import Path
import csv,re,json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
# Use the audited parser without running its baseline writer.
s=(R/'scripts/parse_baseline_HI_v2.py').read_text();exec(s[:s.index('summaries={}')])
allrules={}
for key in ['4L','2L']:
 B=R/f'logs/baseline_{key}_02'
 cprops={}
 for line in (B/'constraint_summary.txt').read_text().splitlines():
  if line.startswith('CLASS\t'):
   a=line.split('\t');cprops[a[1]]=dict(sx(a[3]) or [])
 pc={(x['cset'],x['layer']):dict(sx(x['values'])) for x in csv.DictReader((B/'physical_csets.tsv').open(),delimiter='\t',quotechar='\0')}
 sc={(x['cset'],x['layer']):dict(sx(x['values'])) for x in csv.DictReader((B/'spacing_csets.tsv').open(),delimiter='\t',quotechar='\0')}
 resolved=[]
 for x in csv.DictReader((B/'net_rules.tsv').open(),delimiter='\t',quotechar='\0'):
  props=dict(sx(x['props']) or []);pclass=sx(x['physicalClass']);sclass=sx(x['spacingClass'])
  pset=props.get('PHYSICAL_CONSTRAINT_SET') or cprops.get(pclass,{}).get('PHYSICAL_CONSTRAINT_SET') or 'DEFAULT'
  sset=props.get('SPACING_CONSTRAINT_SET') or cprops.get(sclass,{}).get('SPACING_CONSTRAINT_SET') or 'DEFAULT'
  for layer in ['TOP','BOTTOM']:
   p=pc[pset,layer];sp=sc[sset,layer]
   resolved.append({'net':x['net'],'layer':layer,'physicalClass':pclass,'spacingClass':sclass,'physicalCSet':pset,'physicalAssignmentSource':'net' if 'PHYSICAL_CONSTRAINT_SET' in props else ('netclass' if pclass else 'designDefault'),'spacingCSet':sset,'spacingAssignmentSource':'net' if 'SPACING_CONSTRAINT_SET' in props else ('netclass' if sclass else 'designDefault'),'widthMinMM':p['width_min'],'neckWidthMinMM':p['neckwidth_min'],'neckLengthMaxMM':p['necklength_max'],'allowEtch':p['allow_etch'],'approvedVias':pc[pset,'TOP'].get('vias'),'spacingMM':{k:sp[k] for k in ['line_line','smdpin_line','thrupin_line','via_line','line_shape','smdpin_smdpin','via_via','hole_line','hole_via','hole_hole']},'allPhysicalKeys':p,'allSpacingKeys':sp,'netProps':props})
 data={'status':'NATIVE_BASE_CSET_MAPPING_RESOLVED','variant':key,'scope':'Base net/class/default CSet selection resolved from native dumps. NOT a coordinate-dependent effective DRC getter. Region-Class and class-class interactions, object property overrides, same-net and electrical constraints must also be evaluated for each actual route.','sourceDirectory':str(B),'rules':resolved,'classProps':cprops,'nativeClassTableRows':str(B/'class_table.tsv'),'nativeSpecificClassTableNames':str(B/'specific_proof.tsv'),'regionShapesSource':str(R.parent/'lessonG_30_37_20261020/scripts/local_loops05.il'),'units':'MM'}
 (R/f'inventory/base_net_rules_{key}.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 with (R/f'inventory/base_net_rules_{key}.tsv').open('w',newline='') as f:
  w=csv.writer(f,delimiter='\t');w.writerow(['net','layer','physicalClass','physicalCSet','spacingClass','spacingCSet','widthMinMM','neckWidthMinMM','neckLengthMaxMM','allowEtch','approvedVias','lineLineMM','smdpinLineMM','viaLineMM','lineShapeMM'])
  for r in resolved:w.writerow([*[r[k] for k in ['net','layer','physicalClass','physicalCSet','spacingClass','spacingCSet','widthMinMM','neckWidthMinMM','neckLengthMaxMM','allowEtch','approvedVias']],*[r['spacingMM'][k] for k in ['line_line','smdpin_line','via_line','line_shape']]])
 allrules[key]={'rows':len(resolved),'selectedPhysicalCSets':sorted({x['physicalCSet'] for x in resolved})}
print(json.dumps(allrules,indent=2))
