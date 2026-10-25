from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
ops=[]
def route(id,pts,layer='TOP'):
 ops.append({'type':'route','id':id,'net':'PA4_SPI_NSS','layer':layer,'points':pts,'width':.2,'purpose':'Explicit source-first NSS and pullup branch, preserves west SPI corridor; native/reference validation pending'})
def via(id,xy,net='PA4_SPI_NSS'):ops.append({'type':'via','id':id,'net':net,'xy':xy,'padstack':'L28_VIA030_C060','purpose':'Offpad layerchange; nearby actual GND return and reference review required'})
route('NSS_SOURCE_SERIES',[[35.75,29.25],[34.8,29.25],[34.8,31.15],[32.93,33.02],[32.7984,33.02]])
route('NSS_PULLUP_INWARD',[[35.75,29.25],[36.8,29.25],[39,27.05],[39,26.2]])
via('NSS_PULLUP_INNER_VIA',[39,26.2]);via('NSS_PULLUP_WEST_VIA',[32,22.2])
route('NSS_PULLUP_BOTTOM',[[39,26.2],[39,21.3],[32,21.3],[32,22.2]],'BOTTOM')
route('NSS_PULLUP_RESISTOR',[[32,22.2],[32,21]])
via('NSS_PULLUP_GND_RETURN',[32,23.2],'GND')
d={'status':'EXPLICIT_NSS_CANDIDATE_REPLACES_REJECTED_WEST_BLOCKING_SEARCH','operations':ops,'proofs':[{'from':'U1.14','to':'R23.1','connected':True},{'from':'U1.14','to':'R25.2','connected':True}],'pending':['Full future critical copper precheck','Native DRC and exact endpoints','2L actual TOP reference gaps under internal BOTTOM branch; never claim uniformly continuous reference','Final GND return and all-board HSE anchor challenge']}
(R/'plans/SPI_NSS_explicit_v3.json').write_text(json.dumps(d,indent=2),encoding='utf8');print('NSS engineering candidate written')