import pathlib,shutil,json,hashlib,re
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022')
HI=R.parent/'lessonHI_38_50_20261021'
D=pathlib.Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS')
S=R/'source/j55_readback_helpers';S.mkdir(parents=True,exist_ok=True)
A=R/'source/j55_official';A.mkdir(parents=True,exist_ok=True)
manifest=[]
for name in ['axlDBCreateText','axlDBChangeText','axlChangeLayer','axlTransformObject','axlDBAddProp','axlDBGetProperties','axlDBGetAttachedText','axlSaveDesign','axlDBTransactionStart','axlDBTransactionCommit','axlDBTransactionRollback','axlKillDesign','axlDBRefreshId']:
 p=D/(name+'.txt');q=A/p.name;shutil.copy2(p,q);manifest.append({'source':str(p),'copy':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest().upper()})
for v in ['2L','4L']:
 out=S/v;out.mkdir(exist_ok=True)
 src=HI/'source/readback_snapshots'/('reopen_padentry_'+v+'_b019_stored')
 for p in sorted(src.glob('*.il')):
  if p.name.startswith('16_'):continue
  text=p.read_text(encoding='utf-8-sig')
  if p.name.startswith('09_'):
   text=text.replace('procedure(gSnapshot(out lib)','procedure(jkSnapshot(out lib)').replace('  gInventory(out lib)\n','')
  q=out/p.name;q.write_text(text,encoding='utf8');manifest.append({'source':str(p),'copy':str(q),'originalSHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper(),'copySHA256':hashlib.sha256(q.read_bytes()).hexdigest().upper(),'adaptation':'09 snapshot library loading removed; other definitions preserved'})
(R/'native/j55_source_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(len(manifest))
