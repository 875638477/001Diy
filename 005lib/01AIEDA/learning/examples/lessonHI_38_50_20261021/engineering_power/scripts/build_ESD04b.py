from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
e=json.loads((R/'ESD_ground_routes_04.json').read_text())
e['revision']='04b adds shortVBUSbridge as agreed withUSB route owner; no TOP data crossing'
e['prerequisites']=[p for p in e['prerequisites'] if'VBUS U4.5->C10.1' not in p]
e['prerequisites'].append('MergedUSBgeometry must contain .4TOP U4.5escape to40,8.95 andBOTTOMbridge toC10; finalplanevoid/reference audit needed2L.')
def route(i,p,w,f,t,purpose,layer='TOP'):
 return dict(type='route',id=i,net='USB_VBUS',layer=layer,points=p,widths=[w]*(len(p)-1),**{'from':f,'to':t,'purpose':purpose})
e['operations'] += [
route('ESD_VBUS_U4_ESCAPE',[[40.25,10.1],[40.25,9.2],[40,8.95]],.4,'U4.5','V_HI_ESD_VBUS_LEFT','Normal.4width avoids .3neck length1.2536 exceeding1.0. Do not use.6diagonal nearDMpad4.'),
dict(type='via',id='V_HI_ESD_VBUS_LEFT',net='USB_VBUS',xy=[40,8.95],padstack='L28_VIA030_C060',purpose='Offpad ESDrail crosses belowDPonBOTTOM; keepTOP data continuous.'),
route('ESD_VBUS_BOTTOM_BRIDGE',[[40,8.95],[43.8,9.2016]],.6,'V_HI_ESD_VBUS_LEFT','V_HI_C10_VBUS','Short bridge crossespairedTOPdata only once;2LBOTTOMreference void must be measured and localgroundreturn checked.','BOTTOM'),
dict(type='via',id='V_HI_C10_VBUS',net='USB_VBUS',xy=[43.8,9.2016],padstack='L28_VIA030_C060',purpose='Offpad C10VBUS via separated1.5748fromC10GND via at43.8,10.7764.'),
route('ESD_VBUS_C10',[[43.8,9.2016],[42.7,9.2016]],.6,'V_HI_C10_VBUS','C10.1','Short local rail capacitorfeed, no USBVBUSpoweringV5/V3.')
]
e['geometryNotes']=[x for x in e['geometryNotes'] if'C10VBUSpad5route stillnot' not in x]
e['geometryNotes'].append('4L TOP seesactualL2 even acrossBOTTOMVBUS bridge.2L TOP_DP crosses finiteBOTTOMreference slot; this is explicittradeoff, not equivalentHFreturn or USB90ohm certification.')
(R/'ESD_ground_routes_04b.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
p=json.loads((R/'routing_policy_interfaces_04.json').read_text())
for i in p['interfaces']:
 if i['id']=='CAN_BUS':i['spaceByVariant']={'2L':.2,'4L':.25};i['space']='actualCANclass:2L.2,4L.25; do not weaken4L class to.2'
(R/'routing_policy_interfaces_04.json').write_text(json.dumps(p,indent=2)+'\n',encoding='utf-8')
print('savedESD04b12ops; correctedCANspacingpolicy')
