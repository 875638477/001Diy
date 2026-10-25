from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
for fn in ['review_power02d.py','review_power03c.py']:
 p=R/'scripts'/fn;s=p.read_text()
 needle=" summary=(rb/'native_summary.txt').read_text()"
 pos=s.index(needle)
 extra=""" nw=json.loads((cp/'networks.json').read_text(encoding='utf-8'));bp=Path(nw['board']);record(cp/'networks.json');record(bp)
 check(variant+'.immutableBRDHashMatchesReadback',hashlib.sha256(bp.read_bytes()).hexdigest().upper()==nw['sha256'].upper(),dict(board=str(bp),expected=nw['sha256']))
 original=json.loads((R/'source'/('normalized_actual_'+variant+'.json')).read_text(encoding='utf-8'))
 def identities(x):return {(c['ref'],p['number']):(p['net'] or None) for c in x['placements'] for p in c['pins'] if p['number'] and not p['mechanical']}
 check(variant+'.all272PinNetsPreservedFromG',identities(a)==identities(original))
 check(variant+'.all80ComponentModelsPreserved', {(c['ref'],c['package'],c['model'],c['value']) for c in a['placements']}=={(c['ref'],c['package'],c['model'],c['value']) for c in original['placements']})
"""
 s=s[:pos]+extra+s[pos:]
 p.write_text(s)
print('patchedidentityandBRDhash')
