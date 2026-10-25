from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'SPI_external_2L_engineered_v6.json').read_text());p['batchId']='SPI_external_2L_engineered_v7';p['operations']=[]
def via(i,n,xy):p['operations'].append(dict(type='via',id=i,net=n,xy=xy,padstack='L28_VIA030_C060',purpose='Explicit signal/ground layer transition; verify native filled ground attachment'))
def route(i,n,l,pts,w=.2,purpose='Manual source-ordered SPI route'):
 p['operations'].append(dict(type='route',id=i,net=n,layer=l,points=pts,width=w,purpose=purpose))
for i,pts in enumerate([[[29.8,30.95],[28.4,32.35]],[[28.4,32.35],[22,32.35]],[[22,32.35],[22,37]]]):p['operations'].append(dict(type='deleteSegment',id='SPI_RIP_PREFILTER_'+str(i),net='V3V3',layer='TOP',points=pts,width=.6,purpose='Move low-current prefilter row +0.20mm to permit grounded guard return, no long BOTTOM power bridge'))
route('SPI_PREFILTER_ROW_SHIFT','V3V3','TOP',[[29.8,30.95],[28.2,32.55],[22,32.55],[22,37]],.6,'Low-current pre-10ohm feed only, retains local VDDA filter and ADC topology')
for n,a,b,topa,bot,topb in [
 ('SPI_SCK',[30.65,29.9],[21.85,29.95],[[32.0252,31],[31.75,31],[30.65,29.9]],[[30.65,29.9],[30.6,29.95],[21.85,29.95]],[[21.85,29.95],[21.65,30.15],[16.2,30.15],[14.59,28.54],[7,28.54]]),
 ('SPI_MOSI',[31.65,27.8],[14,29.3],[[32.0252,27],[32.0252,27.4248],[31.65,27.8]],[[31.65,27.8],[31.15,28.3],[26.6,28.3],[26.4,28.5],[14.8,28.5],[14,29.3]],[[14,29.3],[12.22,31.08],[7,31.08]]),
 ('SPI_MISO',[31.5,29.85],[21.75,30.8],[[32.0252,29],[32.0252,29.3248],[31.5,29.85]],[[31.5,29.85],[31.1,30.25],[31.1,30.35],[30.65,30.8],[21.75,30.8]],[[21.75,30.8],[18.93,33.62],[7,33.62]]),
 ('SPI_NSS',[29.8,32.3],[20.85,32.3],[[31.2236,33.02],[30.52,33.02],[29.8,32.3]],[[29.8,32.3],[20.85,32.3]],[[20.85,32.3],[16.99,36.16],[7,36.16]])]:
 via(n+'_EAST',n,a);via(n+'_WEST',n,b);route(n+'_EAST_TOP',n,'TOP',topa);route(n+'_BOTTOM_BRIDGE',n,'BOTTOM',bot);route(n+'_WEST_TOP',n,'TOP',topb)
for i,xy in [('SCK_E',[30.9,28.9]),('SCK_W',[20.5,29.32]),('MOSI_E',[32.8,25.3]),('MOSI_W',[14,30.6]),('MISO_E',[32.85,28.1]),('MISO_W',[22.5,31.7]),('GUARD_E',[27.1,31.55]),('GUARD_W',[21,31.55]),('NSS_E',[29,33.2]),('NSS_W',[20.8,33.75])]:via('SPI_RETURN_'+i,'GND',xy)
route('SPI_GUARD_CLOCK_MOSI','GND','BOTTOM',[[28.6,29],[28.85,29.25],[20.57,29.25],[20.5,29.32]],.6,'Connect existing C9 GND via to guard; same-layer ground beside SCK across missing TOP LDO reference')
route('SPI_GUARD_MISO_NSS','GND','BOTTOM',[[27.1,31.55],[21,31.55]],.6,'Explicit continuous GND guard across C8 positive pad reference gap and below prefilter')
p['assumptions']=['SPI teaching initially <=1MHz, lowest adequate GPIO speed, receiver waveform verification before increasing rate; edge rate rather than clock alone determines reflection risk','TOP power pads beneath local BOTTOM bridges preclude continuous opposite reference. Grounded coplanar rails and actual plane attachment are deliberate return paths, not impedance or EMI certification','0.2mm signals, 0.6mm guard copper; original VDDA prefilter TOP row moved +0.20mm, original08 not used']
(R/'SPI_external_2L_engineered_v7.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
# use same conservative actual copper checker and preserve v6 failure report
s=(R/'scripts/precheck_SPI_external_2L_v6.py').read_text().replace('engineered_v6.json','engineered_v7.json').replace('v6_precheck.json','v7_precheck.json')
# apply native copper deletes in-memory, exact unique matching
s=s.replace("items=[]", """for o in p['operations']:
 if o['type']=='deleteSegment':
  hits=[r for r in b['routes'] if r['net']==o['net'] and r['layer']=='ETCH/'+o['layer'] and r['startEnd'] in [o['points'],o['points'][::-1]] and abs(r['width']-o['width'])<1e-6]
  assert len(hits)==1,(o['id'],len(hits))
  b['routes'].remove(hits[0])
items=[]""")
(R/'scripts/precheck_SPI_external_2L_v7.py').write_text(s,encoding='utf-8')