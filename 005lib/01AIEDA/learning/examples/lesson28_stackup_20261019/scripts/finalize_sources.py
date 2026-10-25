from pathlib import Path
import re,json,hashlib
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
p=B/'scripts'/'validate28.py';s=p.read_text()
s=s.replace("sources.append(('https://gct.co/connector/usb4105'","sources.append(('https://gct.co/files/drawings/usb4105.pdf'")
mark="(B/'specification.json').write_text"
at=s.index(mark)
s=s[:at]+"""for record in spec['sources']:
 if record['file'].endswith('GCT_USB4105_RevB4_inherited.pdf'):
  record['retrievedDate']='2026-10-18 original download; reused 2026-10-19'
  record['inheritedFrom']='learning/examples/lesson10_connector_20261018/source/usb4105.pdf'
spec['webObservation']={'url':'https://gct.co/connector/usb4105','date':'2026-10-19','scope':'Web text verified shell stake lengths .60/.95/1.20mm; direct local HTML fetch received access challenge, not bypassed. Original drawing PDF is the archived source.'}
"""+s[at:]
p.write_text(s,encoding='utf-8')
p=B/'scripts'/'lesson28.il';s=p.read_text()
# Canonical replay source uses fully explicit validated Film parameter files.
s=s.replace('"/copper_films_2.il" else "/copper_films_4.il"','"/copper_films_2_exact.il" else "/copper_films_4_exact.il"')
p.write_text(s,encoding='ascii')
# Check saved UTF-8 note and every local relative link.
note=Path(r'D:\001DIY\005lib\01AIEDA\learning\notes\lesson28_stackup_20261019.md')
text=note.read_text(encoding='utf-8')
missing=[]
for target in re.findall(r'\]\(([^)]+)\)',text):
 if '://' in target or target.endswith('artifact_manifest.json'):continue
 if not (note.parent/target).resolve().exists():missing.append(target)
assert not missing,missing
print('Local learning note links verified')
