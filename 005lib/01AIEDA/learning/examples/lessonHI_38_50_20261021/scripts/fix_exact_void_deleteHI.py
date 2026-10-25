from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text();old='unless(axlDeleteObject(target) error("Cannot delete exact old permanent void\\n"))';new='unless(axlShapeDeleteVoids(target) error("Cannot delete exact old permanent void\\n"))';assert old in s;p.write_text(s.replace(old,new),encoding='ascii')
old='HSE_replacement_rollback_4L_02';tag='HSE_replacement_rollback_4L_03';new=R/f'scripts/{tag}.il';new.write_text((R/f'scripts/{old}.il').read_text().replace(old,tag),encoding='ascii');snap=R/'source/readback_snapshots'/tag;snap.mkdir(parents=True,exist_ok=False);h='set NOCONFIRM\n';m=[]
for i,p in enumerate([R/'source/placementG.il',R/'source/local_copperG_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',new]):
 dst=snap/(str(i).zfill(2)+'_'+p.name);shutil.copyfile(p,dst);h+='skill errset(load('+json.dumps(dst.as_posix())+') t)\n';m.append({'source':str(p),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiHSEReplacePilot() t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(m,indent=2))
