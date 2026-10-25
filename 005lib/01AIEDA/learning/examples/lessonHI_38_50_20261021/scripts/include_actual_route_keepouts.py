import pathlib
p=pathlib.Path(__file__).parent/'routing_geometry.py';s=p.read_text(encoding='utf8')
s=s.replace('import pathlib,sys,json,math','import pathlib,sys,json,math,csv')
s=s.replace('from cadence_poly import plane_from_native','from cadence_poly import plane_from_native,polygon_from_vertices\nfrom native_sexpr_data import parse as parse_native_data')
old="  self.regions=[]"
new="""  self.regions=[]
  direct=pathlib.Path(snapshot['readbackDirectory'])/'direct_geometry.tsv'
  self.nativeKeepoutEvidence=str(direct)
  with direct.open(encoding='utf8',newline='') as source:
   for row in csv.DictReader(source,delimiter='\\t'):
    layer=row['layer'].strip('"')
    if row['role']!='KEEPOUT' or not layer.startswith('ROUTE KEEPOUT/'):continue
    geometry=polygon_from_vertices(parse_native_data(row['vertices']))
    for target in LAYERS:
     if layer.endswith('/ALL') or layer.endswith('/'+target):self.add(None,target,geometry,'keepout','nativeROUTE_KEEPOUT')
"""
assert old in s;s=s.replace(old,new)
s=s.replace("  a=self.rule(net,layer);b=self.rule(other,layer)","  if kind=='keepout':return 0.0\n  a=self.rule(net,layer);b=self.rule(other,layer)")
p.write_text(s,encoding='utf8')