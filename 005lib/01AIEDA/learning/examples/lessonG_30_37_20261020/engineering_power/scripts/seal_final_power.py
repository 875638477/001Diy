from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_power');G=R.parent;B=G.parents[2]
note=B/'learning/notes/lessonG_power_20261020.md'
s=note.read_text(encoding='utf-8')
add="\nU2\u9ad8\u5ea6\u8865\u8bc1\uff1aTPS54202DDCR\u5b98\u65b9p28 DDC0006A\u56fe\u5df2\u6e32\u67d3\u89c6\u89c9\u6838\u5bf9\uff0cmax1.1mm\uff1b\u89c1rendered/tps54202_revC_p28.png\u3002\u4e0d\u80fd\u5957\u7528U3/U4\u76841.45mm\u6216native\u9ed8\u8ba41mm\u3002\n"
if add not in s:note.write_text(s+add,encoding='utf-8')
d=json.loads((R/'readouts/final_native_power_review.json').read_text(encoding='utf-8'))
inputs=[G/'native/G_2L_PLACEMENT_v3.brd',G/'native/G_4L_PLACEMENT_v3.brd',B/'learning/examples/de_15_26_20261019/integrated_circuit.json',G/'inventory/inventory_4L.json']
for v in d['variants'].values():
 p=Path(v['readback']);inputs.extend(p/n for n in ['g_actual_symbols.tsv','g_actual_pins.tsv','native_summary.txt','nets.tsv','mechanical_direct.tsv','route_geometry.tsv','vias.tsv','g_copper_shapes.tsv'])
def entry(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper(),'bytes':p.stat().st_size}
(R/'evidence_manifest.json').write_text(json.dumps({'scope':'Inputs independently checked for final layout checkpoint, not subsequent separate decoupling demonstration','files':[entry(p) for p in inputs]},indent=2),encoding='utf-8')
files=[p for p in R.rglob('*') if p.is_file() and p.name!='artifact_manifest.json']+[note]
manifest={'status':d['status'],'checks':d['checks'],'note':str(note),'files':[entry(p) for p in sorted(files,key=str)]}
(R/'artifact_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'status':manifest['status'],'checks':d['checks'],'files':len(files),'manifestSHA256':hashlib.sha256((R/'artifact_manifest.json').read_bytes()).hexdigest().upper(),'noteSHA256':hashlib.sha256(note.read_bytes()).hexdigest().upper()}))
