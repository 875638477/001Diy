from pathlib import Path
import shutil,json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text();i=s.index('procedure(hiPolygonMatches(');j=s.index('\nprocedure(',i+1);fn=s[i:j];assert 'let((poly vertices actual n ok found)' in fn;fn=fn.replace('let((poly vertices actual n ok found)','prog((poly vertices actual n ok found)').replace('  found))','  return(found)))');s=s[:i]+fn+s[j:];p.write_text(s,encoding='ascii')
old='HSE_replacement_rollback_4L_01';tag='HSE_replacement_rollback_4L_02';src=R/f'scripts/{old}.il';new=R/f'scripts/{tag}.il';new.write_text(src.read_text().replace(old,tag),encoding='ascii');snap=R/'source/readback_snapshots'/tag;snap.mkdir(parents=True,exist_ok=False);h='set NOCONFIRM\n';m=[]
loads=[R/'source/placementG.il',R/'source/local_copperG_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',new]
for k,p in enumerate(loads):
 dst=snap/(str(k).zfill(2)+'_'+p.name);shutil.copyfile(p,dst);h+='skill errset(load('+json.dumps(dst.as_posix())+') t)\n';m.append({'source':str(p),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiHSEReplacePilot() t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(m,indent=2))
