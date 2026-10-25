from pathlib import Path
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019')
p=B/'scripts'/'validate28.py';s=p.read_text()
marker="eq('2L source mask default Dk explicitly unqualified'"
at=s.index(marker)
extra="""for n in (2,4):
 mech=B/'logs'/('mech%d_01'%n);mBase=B/'logs'/'mechbase01'
 eq('%dL all explicit design-outline/keepin/keepout shapes preserved'%n,norm(rows(mech/'mechanical_direct.tsv')),norm(rows(mBase/'mechanical_direct.tsv')))
 rtext=(mech/'mechanical_roots.txt').read_text()
 for key in ['designOutline','keepinPlace','keepinRoute']:
  ck('%dL actual root %s exists'%(n,key),key+'=t' in rtext)
 outline=[r for r in rows(mech/'mechanical_direct.tsv') if q(r['layer'])=='BOARD GEOMETRY/DESIGN_OUTLINE']
 eq('%dL exactly one real design outline'%n,len(outline),1)
 eq('%dL real outline 80x60 bbox'%n,outline[0]['bbox'],'((0.0 0.0) (80.0 60.0))')
"""
s=s[:at]+extra+s[at:]
marker="spec['sources']="
at=s.index(marker)
extra="""sources.append(('https://www.ti.com/lit/pdf/SCAA082A','TI_SCAA082A.pdf','Rev A 2017, pages9-10 reference-return path and stackup design principles'))
sources.append(('https://gct.co/connector/usb4105','gct_usb4105_20261019.html','Shell stake length options are measured from component mounting datum; PCB thickness/process compatibility remains unverified'))
spec['manufacturingRelease']={'released':False,'twoLayer':{'usbMaskBridge_mm':0.100,'publicOshMinimumMaskWeb_mm':0.1016,'difference_mm':-0.0016,'action':'Revise mask or obtain process acceptance; no entire-board production claim'},'fourLayer':{'impedance90OhmGeometryConfirmed':False,'individualDielectricToleranceQualified':False,'stackupToleranceFieldsZeroMean':'Not supplied, not zero manufacturing tolerance'},'bothTargets':['USB4105 default shell stake S=0.95+/-0.15mm is measured from the component mounting datum, not PCB bottom. Compatibility and soldering on nominal1.6mm PCB are unverified.','Remaining 79 logical components are unplaced; reference planes not poured; no complete board manufacture release.']}
spec['explicitMechanicalReadback']='logs/mechbase01, logs/mech2_01, logs/mech4_01; root designOutline/keepinPlace/keepinRoute plus direct axlDBGetShapes geometry'
"""
s=s[:at]+extra+s[at:]
p.write_text(s,encoding='utf-8')
print('Validator extended for direct mechanical evidence and manufacturing differences')
