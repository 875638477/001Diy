from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
p={'status':'DRAFT_ENGINEERING_CANDIDATE_NOT_NATIVE','batchId':'SPI_external_2L_engineered_v6','variant':'2L','sourceExpectedSHA256':'76ED85DA3999A7DAFBDF9EB99EEC425B480A5EAEB49843BF970F8664707DE0AF','operations':[],'assumptions':['SPI initial teaching <=1MHz; GPIO lowest adequate output speed, verify receiver waveform before increasing speed','0.20mm signals, normal 0.60mm grounded guard rails; no controlled impedance claim','No prefilter08 executed. Bottom LDO crossing deliberately uses same-layer GND guard, not fictitious TOP plane under power pads.']}
def via(i,n,xy,purpose):p['operations'].append(dict(type='via',id=i,net=n,xy=xy,padstack='L28_VIA030_C060',purpose=purpose))
def route(i,n,l,pts,w=.2,purpose='Manual topology preserving source resistor ordering'):
 p['operations'].append(dict(type='route',id=i,net=n,layer=l,points=pts,width=w,purpose=purpose))
for n,a,b,topa,bot,topb in [
 ('SPI_SCK',[31.1,30.15],[21.4,29.95],[[32.0252,31],[31.95,31],[31.1,30.15]],[[31.1,30.15],[30.9,29.95],[21.4,29.95]],[[21.4,29.95],[16,29.95],[14.59,28.54],[7,28.54]]),
 ('SPI_MOSI',[31.7,26.2],[14,29.5],[[32.0252,27],[32.0252,26.5252],[31.7,26.2]],[[31.7,26.2],[31.7,27],[30.2,28.5],[15,28.5],[14,29.5]],[[14,29.5],[12.42,31.08],[7,31.08]]),
 ('SPI_MISO',[31.8,28.2],[19.6,31.5],[[32.0252,29],[31.8,28.7748],[31.8,28.2]],[[31.8,28.2],[31.8,30.7],[31,31.5],[19.6,31.5]],[[19.6,31.5],[17.48,33.62],[7,33.62]]),
 ('SPI_NSS',[30.5,33.8],[19,32.9],[[31.2236,33.02],[30.5,33.7436],[30.5,33.8]],[[30.5,33.8],[29.6,32.9],[19,32.9]],[[19,32.9],[15.74,36.16],[7,36.16]])]:
 via(n+'_EAST',n,a,'Signal transition with explicit GND return review');via(n+'_WEST',n,b,'Return to TOP before header')
 route(n+'_EAST_TOP',n,'TOP',topa);route(n+'_BOTTOM_BRIDGE',n,'BOTTOM',bot);route(n+'_WEST_TOP',n,'TOP',topb)
for i,xy in [('G1A',[30.9,28.9]),('G1B',[20.3,29.5]),('GMOSI_W',[14,30.8]),('GMOSI_E',[32.8,25.3]),('GMISO_E',[32.85,28.1]),('G2A',[27.3,30.75]),('G2B',[20.3,30.75]),('G3A',[30,32.2]),('G3B',[20.3,32.2]),('GNSS_E',[29.3,34.7])]:via('SPI_RETURN_'+i,'GND',xy,'Ground transition/guard connection; must prove actual native plane attachment')
route('SPI_GUARD_LOWER','GND','BOTTOM',[[30.9,28.9],[30.6,29.2],[22.4,29.2],[22.2,29],[20.8,29],[20.3,29.5]],.6,'Same-layer continuous GND between MOSI and clock bridge; avoids power-pad TOP reference gap')
route('SPI_GUARD_MID','GND','BOTTOM',[[27.3,30.75],[20.3,30.75]],.6,'Same-layer ground across C8/C9 missing TOP reference between SCK and MISO')
route('SPI_GUARD_UPPER','GND','BOTTOM',[[30,32.2],[20.3,32.2]],.6,'Same-layer ground between MISO and NSS; guarded crossing below V3 prefilter TOP route')
(R/'SPI_external_2L_engineered_v6.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
print(len(p['operations']))