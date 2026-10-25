from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');tag='deleteVia_rollback_4L_02';snap=R/'source/readback_snapshots'/tag;snap.mkdir(parents=True,exist_ok=False);h='set NOCONFIRM\n';records=[]
for i,p in enumerate([R/'source/placementG.il',R/'source/local_copperG_v2.il',R/'scripts/batchHI_shapes_v3.il']):
 dst=snap/(str(i).zfill(2)+'_'+p.name);shutil.copyfile(p,dst);h+='skill errset(load('+json.dumps(dst.as_posix())+') t)\n';records.append({'source':str(p),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiDeleteViaRollbackPilot('+json.dumps((R/'logs'/tag).as_posix())+') t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(records,indent=2))
