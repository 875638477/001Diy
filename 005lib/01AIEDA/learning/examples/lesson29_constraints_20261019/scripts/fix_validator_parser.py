from pathlib import Path
import shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
shutil.copy2(R/'scripts/validate29.py',R/'scripts/validate29_v1_parser_failed.py')
shutil.copy2(R/'validation.json',R/'validation_v1_parser_failed.json')
p=R/'scripts/validate29.py';s=p.read_text()
s=s.replace("csv.DictReader(p.open(encoding='utf8'),delimiter='\\t')","csv.DictReader(p.open(encoding='utf8'),delimiter='\\t',quotechar='\\0')")
s=s.replace("phys[name,'TOP']['vias']=='L28_VIA030_C060'","[x for x in phys[name,'TOP']['vias'].split(':') if x]==['L28_VIA030_C060']")
s=s.replace("ck('coupon2 fully connected nets',len(rows(C/'nets.tsv'))==2 and all(x['pins']=='2' for x in rows(C/'nets.tsv')))","""connection=(R/'logs/coupon_connections.tsv').read_text()
ck('coupon2 actual pins per net via official query', 'NET\\tCAL_P\\t2\\t0\\t0' in connection and 'NET\\tCAL_N\\t2\\t0\\t0' in connection)
for n in ['CAL_P','CAL_N']:
 pinxy=[]
 for line in connection.splitlines():
  if line.startswith('PIN\\t'):
   z=line.split('\\t')
   if sx(z[4])==n:pinxy.append(sx(z[3]))
 routepair=next(sx(x['startEnd']) for x in r if sx(x['net'])==n)
 ck(n+' actual pins coincide with full route endpoints',sorted(pinxy)==sorted(routepair))
""")
p.write_text(s,encoding='ascii')
