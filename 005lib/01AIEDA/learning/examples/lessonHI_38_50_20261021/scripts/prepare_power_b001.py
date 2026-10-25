from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'engineering_power/power_critical_paths_01.json';d=json.loads(p.read_text())
d['batchId']='power_4L_b001';d['variant']='4L';d['sourceExpectedSHA256']='2D4A146A61F92AE6459C9E855AB086ED47B42360409608D8A12E30BB7EA21526'
d['constraintOperations']=[]
for rule in d['rules']:
 name=rule['id']+'_P'
 d['constraintOperations'] += [{'type':'csetCopy','domain':'physical','name':name,'copyFrom':rule['copyFrom'],'values':{'necklength_max':str(rule['changes']['necklength_max']['new'])+' MM'}},{'type':'region','id':rule['id'],'layer':'TOP','polygon':rule['polygon'],'assignments':[{'domain':'physical','netClass':'NC_SWITCHING_P','cset':name}]}]
(R/'batches').mkdir(exist_ok=True);(R/'batches/power_4L_b001.json').write_text(json.dumps(d,indent=2),encoding='utf8')
