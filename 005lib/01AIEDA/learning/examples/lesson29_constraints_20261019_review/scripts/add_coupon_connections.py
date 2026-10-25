from pathlib import Path
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019_review')
p=B/'scripts'/'review29.py';s=p.read_text()
insert=r'''
conn=[r for r in table(A/'logs'/'coupon_connections.tsv') if r['kind'] in ['NET','PIN']]
for net in ['CAL_P','CAL_N']:
 n=next(r for r in conn if r['kind']=='NET' and r['net_or_ref']==net)
 eq('Official pinsOfNet '+net+' count',int(n['count_or_pin']),2)
 eq('Official '+net+' unconnected',int(n['unconnected_or_xy']),0)
 eq('Official '+net+' unplaced',int(n['unplaced_or_net']),0)
 pins=[r for r in conn if r['kind']=='PIN' and q(r['unplaced_or_net'])==net]
 endpoints=[]
 for r in pins:
  numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',r['unconnected_or_xy'])]
  endpoints.append(tuple(numbers))
 line=next(r for r in cp if q(r['net'])==net)
 numbers=[float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',line['startEnd'])]
 eq('Coupon '+net+' actual endpoint pins coincide with route',sorted(endpoints),sorted([tuple(numbers[:2]),tuple(numbers[2:])]))
eq('Coupon four actual connected placed pins',len([r for r in conn if r['kind']=='PIN']),4)
eq('Coupon actual pin/net identities preserved across queries',
 sorted((r['net_or_ref'],r['count_or_pin'],q(r['unplaced_or_net'])) for r in conn if r['kind']=='PIN'),
 sorted((r['refdes'],r['pin'],r['net']) for r in table(A/'logs'/'read_coupon'/'component_pins.tsv')))
'''
s=s.replace('# Evidence identity snapshot, not a copy of implementation validator.',insert+'\n# Evidence identity snapshot, not a copy of implementation validator.')
s=s.replace("(R/'evidence_manifest.json').write_text", """for p in [A/'logs'/'coupon_connections.tsv',A/'logs'/'coupon_board02'/'stdout.txt',A/'logs'/'read_coupon'/'launch.json',A/'logs'/'read_coupon'/'native_summary.txt',A/'logs'/'read_coupon'/'component_pins.tsv',A/'logs'/'read_coupon'/'route_geometry.tsv',A/'exports'/'F29_RULES.tcf',A/'exports'/'export_result.json',A/'exports'/'techfile_run'/'compare_stdout.txt',A/'exports'/'techfile_run'/'compare_techfile.log']:
 evidence.append({'path':str(p),'SHA256':sha(p)})
(R/'evidence_manifest.json').write_text""")
p.write_text(s,encoding='utf-8')
print('Coupon actual pin connection crosscheck added')
