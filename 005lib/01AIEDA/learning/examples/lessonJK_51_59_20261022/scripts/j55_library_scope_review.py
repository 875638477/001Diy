from pathlib import Path
import json,collections,hashlib
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';H=R/'learning/examples/lessonHI_38_50_20261021';D=R/'learning/examples/de_15_26_20261019';ns={};src=(J/'scripts/j55_57_build.py').read_text(encoding='utf-8-sig');exec(src[:src.index("req=['REF DES")],ns);rows=ns['srows'];load=ns['load'];dump=ns['dump'];sha=ns['sha']
for v in ['2L','4L']:
 S=load(H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING/normalized.json');L=Path(S['readbackDirectory']);g=rows(L/'g_package_geometry.tsv');items=[]
 for package in sorted({p['package'] for p in S['placements']}):
  gg=[z for z in g if z['package']==package];refs=[p['ref'] for p in S['placements'] if p['package']==package];layers=collections.Counter(x['layer'] for x in gg if x['type']=='text');sh=[x for x in gg if x['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP']
  items.append(dict(package=package,instances=refs,embeddedDefinitionTextLayers=dict(layers),embeddedDefinitionMissingRequired=[l for l in ['REF DES/SILKSCREEN_TOP','REF DES/ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP'] if layers[l]==0],embeddedBounds=[dict(type=x['type'],props=x['props'],bbox=x['bbox']) for x in sh],correctionScope='Instance overrides only. Embedded/public package definitions remain historical and are not certified as fixed for future placements.'))
 dump(J/f'audits/j55_{v}_embedded_definition_vs_instance_scope_b019.json',dict(status='READ_ONLY_EMBEDDED_DEFINITION_SCOPE',source=str(L/'g_package_geometry.tsv'),sha256=sha(L/'g_package_geometry.tsv'),packageCount=len(items),packages=items,refreshCaution='Replacing/refreshing from unchanged source PSM may reintroduce inherited missing/offset text or height. Re-run instance audit after library refresh/ECO; do not treat this JK patch as public library update.'))
m=load(D/'dependency_copy_manifest.json');observations=[]
for x in m['files']:
 for kind in ['source','destination']:
  p=Path(x[kind]);observations.append(dict(kind=kind,path=str(p),exists=p.exists(),currentSHA256=sha(p) if p.exists() else None,historicalCopySHA256=x['sha256'].upper(),matchesHistoricalCopy=(sha(p)==x['sha256'].upper()) if p.exists() else False))
dump(J/'audits/j55_library_dependency_readonly_observation.json',dict(status='CURRENT_READ_ONLY_FILE_OBSERVATION_NOT_PROOF_OF_ALL_PAST_LIBRARY_HISTORY',source=str(D/'dependency_copy_manifest.json'),sourceSHA256=sha(D/'dependency_copy_manifest.json'),files=observations))
print('embedded definitions reviewed; source/destination library observations',len(observations),'historical matches',sum(x['matchesHistoricalCopy'] for x in observations),'missing',sum(not x['exists'] for x in observations))
