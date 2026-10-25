from pathlib import Path
import json,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
G=R.parent/'lessonG_30_37_20261020'
for name in ['inputs','source','scripts','library','logs','inventory','native','current','exports','review']:(R/name).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
manifest=[]
for key in ['4L','2L']:
 p=G/f'current/G_{key}_LAYOUT_v1.brd';q=R/f'inputs/HI_{key}_INPUT.brd'
 assert not q.exists();shutil.copyfile(p,q);assert sha(p)==sha(q)
 manifest.append({'variant':key,'source':str(p),'snapshot':str(q),'sha256':sha(p),'size':p.stat().st_size})
(R/'inputs/source_boards_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
copies=[]
for p in (G/'library').rglob('*'):
 if p.is_file():
  q=R/'library'/p.relative_to(G/'library');q.parent.mkdir(exist_ok=True,parents=True);assert not q.exists();shutil.copyfile(p,q)
  copies.append({'source':str(p),'copy':str(q),'sha256':sha(q)})
(R/'inputs/library_snapshot_manifest.json').write_text(json.dumps(copies,indent=2),encoding='utf8')
helpers=['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il']
for name in helpers:shutil.copyfile(G/'source'/name,R/'source'/name)
for name in ['inventoryG.il','placementG.il','local_copperG_v2.il']:shutil.copyfile(G/'scripts'/name,R/'source'/name)
shutil.copyfile(G/'scripts/launchG.py',R/'scripts/launchHI.py')
shutil.copyfile(G/'scripts/normalize_actual.py',R/'scripts/normalize_HI_actual.py')
p=R/'scripts/normalize_HI_actual.py';p.write_text(p.read_text().replace('lessonG_30_37_20261020','lessonHI_38_50_20261021'),encoding='ascii')
for key in ['4L','2L']:
 loads=[R/'source'/x for x in helpers+['inventoryG.il','placementG.il','local_copperG_v2.il']]+[R/'scripts/network_inventoryHI.il']
 h='set NOCONFIRM\n'+''.join('skill errset(load("'+x.as_posix()+'") t)\n' for x in loads)
 out=(R/f'logs/baseline_{key}_01').as_posix()
 h+='skill errset(axlDRCUpdate(t) t)\n'
 h+=f'skill errset(gSnapshot("{out}" "{(R/"library").as_posix()}") t)\n'
 h+=f'skill errset(hiNetworkInventory("{out}") t)\nquit\nfillin "yes"\n'
 (R/f'scripts/baseline_{key}_01.scr').write_text(h,encoding='ascii')
print(json.dumps({'inputs':manifest,'libraryFiles':len(copies),'root':str(R)},indent=2))
