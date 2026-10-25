from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/adapt_power03bHI.py').read_text().replace('power_star_03b.json','power_star_03c.json').replace("b003b.json","b003c.json")
(R/'scripts/adapt_power03cHI.py').write_text(s,encoding='ascii')
s=(R/'scripts/compile_batchHI_v3.py').read_text()
s=s.replace("import json,hashlib,argparse","import json,hashlib,argparse,shutil")
old="h='set NOCONFIRM\\n'+''.join('skill errset(load('+q(p.as_posix())+') t)\\n' for p in loads)"
new="""snapshot=R/'source/batch_snapshots'/tag
snapshot.mkdir(parents=True,exist_ok=False)
input_records=[]
snaploads=[]
for i,orig in enumerate(loads):
 dest=snapshot/(f'{i:02d}_'+orig.name);shutil.copyfile(orig,dest);snaploads.append(dest)
 input_records.append({'source':str(orig),'snapshot':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest().upper()})
(snapshot/'inputs_manifest.json').write_text(json.dumps(input_records,indent=2),encoding='utf8')
h='set NOCONFIRM\\n'+''.join('skill errset(load('+q(p.as_posix())+') t)\\n' for p in snaploads)"""
assert old in s
s=s.replace(old,new)
s=s.replace("'endpointDefinitions':node_defs}","'endpointDefinitions':node_defs,'helperSnapshots':input_records}")
(R/'scripts/compile_batchHI_v4.py').write_text(s,encoding='ascii')
print('03c adapter and immutable per-batch compiler prepared')
