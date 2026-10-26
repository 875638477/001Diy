import importlib.util,json,pathlib,shutil,sys
P=pathlib.Path(r'D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration')
spec=importlib.util.spec_from_file_location('base_audit',P/'run_pc_native_audit.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
R=pathlib.Path(r'D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/native_audits/final13_4layer');R.mkdir(parents=True,exist_ok=False)
for n in ['output','units']: (R/n).mkdir()
e=b.envfor(R)
final=json.loads((P/'FINAL_REF_MAPPING.json').read_text(encoding='utf-8-sig'))
assets={r['target']:r for r in json.loads((P/'PUBLIC_NEW_ASSETS.json').read_text(encoding='utf-8-sig'))}
names=sorted({r['target'] for r in final['ref_mapping']},key=str.casefold)
protected={}
for d,extensions in [(b.PUBLIC/'01Psm_lib',{'.psm','.ssm','.fsm','.osm','.bsm'}),(b.PUBLIC/'01Pad_lib',{'.pad'})]:
 for p in d.iterdir():
  if p.is_file() and p.suffix.lower() in extensions:protected[str(p)]=b.sha(p)
rows=[]
for name in names:
 p=b.PUBLIC/'01Psm_lib'/(name+'.psm');assert p.is_file(),p
 row=dict(mode='final_public',source_name=assets[name]['source_name'] if name in assets else name,stem=name,path=str(p),source_path=str(p),source_sha256=b.sha(p),alias_sha256=b.sha(p),audit_output=str(R/'output'/f'{len(rows):04}.sexp'))
 b.metadata(row,R,e,len(rows));rows.append(row)
blank=R/'blank.brd';shutil.copyfile(pathlib.Path(r'D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/fixture4/EMPTY4.brd'),blank)
jobs=[]
for row in rows:
 box=row['original_extents'];lit='(('+ ' '.join(box[0])+') ('+' '.join(box[1])+'))'
 jobs.append('('+b.q(row['stem'])+' '+b.q(row['audit_output'])+' '+b.q(row['original_units'])+' '+str(row['original_accuracy'])+' '+lit+')')
(R/'jobs.il').write_text('psmNativeBatch('+b.q(blank)+" '("+'\n'.join(jobs)+') '+b.q(R/'status.tsv')+' '+b.q(b.PUBLIC/'01Psm_lib')+' '+b.q(b.PUBLIC/'01Pad_lib')+')\n',encoding='ascii')
(R/'run.scr').write_text('set NOCONFIRM\nskill errset(load('+b.q(b.B/'psm_native_units.il')+') t)\nskill errset(load('+b.q(R/'jobs.il')+') t)\nquit\nfillin "yes"\n',encoding='ascii')
b.dump(R/'manifest.json',rows);print(json.dumps({'stage':'final_public81_begin','expected':len(rows)}),flush=True)
rec=b.launch([b.CAD/'tools/bin/allegro.exe','-product','Allegro_performance','-safe','-nographic','-s',R/'run.scr','-p',R,blank],R,e,1200,'allegro')
status=(R/'status.tsv').read_text(encoding='utf-8',errors='replace');assert status.rstrip().endswith('COMPLETE')
assert all(b.sha(p)==h for p,h in protected.items())
result=dict(status='RAW_PUBLIC_ONLY_FINAL_DEFINITIONS_EXPORTED_REQUIRES_GEOMETRY_REVIEW',expected=len(rows),outputs=sum(pathlib.Path(r['audit_output']).is_file() for r in rows),complete=True,source_files_unchanged=True,protected=protected,psmpath=str(b.PUBLIC/'01Psm_lib'),padpath=str(b.PUBLIC/'01Pad_lib'),launch=rec)
b.dump(R/'report.json',result);print(json.dumps({k:v for k,v in result.items() if k!='protected'}),flush=True)