from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
E=R.parent.parent
items=[
(E/'lessonG_30_37_20261020/engineering_power/sources/tps54202_revC.pdf','tps54202_revC.pdf','https://www.ti.com/lit/ds/symlink/tps54202.pdf','TPS54202RevC layoutp20-21/packagep28'),
(E/'lessonG_30_37_20261020/engineering_power/sources/tlv755p_revD.pdf','tlv755p_revD.pdf','https://www.ti.com/lit/ds/symlink/tlv755p.pdf','TLV755PRevD layout/thermalp17,p21/packagep44'),
(E/'lessonG_30_37_20261020/engineering_power/sources/tcan332_revF.pdf','tcan332_revF.pdf','https://www.ti.com/lit/ds/symlink/tcan332.pdf','TCAN33xRevF 7.4/7.5 PDF29-30'),
(E/'de_15_26_20261019/power_interface_spec.json','power_interface_spec.json',None,'DEfinalsystemcontractandassemblyprofiles'),
(E/'de_15_26_20261019/mcu_spec.json','mcu_spec.json',None,'MCUpinsboot/debuganderrata')]
out=[]
for src,dst,url,pages in items:
 target=R/'source'/dst;shutil.copyfile(src,target)
 out.append(dict(source=str(src),copy=str(target),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),url=url,sections=pages))
(R/'source/engineering_sources_manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('sourcecopies',len(out))
