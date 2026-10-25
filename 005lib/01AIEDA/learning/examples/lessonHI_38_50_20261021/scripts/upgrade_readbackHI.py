from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/prepare_readbackHI.py'
s=p.read_text()
s=s.replace("P.add_argument('--plan');","P.add_argument('--plan');P.add_argument('--compiled');")
s=s.replace("R/'scripts/batchHI.il',R/'scripts/extraReadHI.il'","R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/extraReadHI.il'")
s=s.replace(" for op in d.get('operations',[]):\n  if op['type']=='via':"," if a.compiled:\n  meta=json.loads(Path(a.compiled).read_text())\n  defs=meta['endpointDefinitions']\n  def pt(x):return 'list('+' '.join(str(float(v)) for v in x)+')'\n  il+='  hiNodeDefinitions=list('+' '.join('list('+json.dumps(k)+' '+json.dumps(v[0])+' '+json.dumps(v[1])+' '+pt(v[2])+' '+json.dumps(v[3])+')' for k,v in defs.items())+')\\n'\n for op in d.get('operations',[]):\n  if op['type']=='via':")
p=R/'scripts/prepare_readbackHI_v2.py';p.write_text(s,encoding='ascii')
print(p)
