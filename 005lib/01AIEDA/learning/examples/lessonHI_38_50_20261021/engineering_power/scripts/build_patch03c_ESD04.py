from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
def save(n,o):(R/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
s=json.loads((R/'power_star_03b.json').read_text())
s['revision']='03c: native03b left/south region1.3 overrode historicalG31 outward1.3657; retain inherited1.4 only in these two local regions.'
for r in s['rules']:
 if r['id'] in ['HI_U1_INNER_LEFT','HI_U1_INNER_SOUTH']:
  r['physicalOnlyDelta']['necklength_max_mm']=1.4
  r['inheritedOutwardMeasuredNeck_mm']=1.365685
s['scopeNotes'].append('Native03b10endpoint proofs true; two MaxNeck are original1.3657 outward tracks under newly overlapping1.3 localregions. No2.6 merged-neck evidence.03c restores1.4 locallyLEFT/SOUTH, NE1.5 unchanged, global1.0 unchanged, no otherfield relaxation.')
save('power_star_03c.json',s)
p=json.loads((R/'routing_policy_interfaces_04.json').read_text())
for i in p['interfaces']:
 i['nets']=['BOOT_SERVICE' if n=='BOOT0_SEL' else n for n in i['nets']]
p['errata']=['BOOT_SERVICE is the actual native service net; earlier draftBOOT0_SEL was not a real net and has been corrected before ordinary routing.']
save('routing_policy_interfaces_04.json',p)
ops=[]
def route(i,points,f,t,purpose):
 ops.append(dict(type='route',id=i,net='GND',layer='TOP',points=points,widths=[.6]*(len(points)-1),**{'from':f,'to':t,'purpose':purpose}))
def via(i,p,purpose):ops.append(dict(type='via',id=i,net='GND',xy=p,padstack='L28_VIA030_C060',purpose=purpose))
route('ESD_U4_RETURN',[[40.25,12.7],[40.25,11.8],[40,11.4]],'U4.2','V_HI_ESD_A','Shortest bodyward return avoids protected pair at y>13.6; GND supply track not through thin digitaltrace.')
via('V_HI_ESD_A',[40,11.4],'Offpad body ground via, clear DMx39.3 and VBUSpin5.')
route('ESD_U4_SECOND_VIA',[[40.25,11.8],[40.5,11.6]],'ESD_U4_RETURN','V_HI_ESD_B','Parallel body via retained without old40.9 data collision.')
via('V_HI_ESD_B',[40.5,11.6],'Offpad .3drill/.6copper, pairdrill gap .2385mm; native hole rules must verify.')
route('ESD_C10_RETURN',[[42.7,10.7764],[43.8,10.7764],[43.8,11.5764]],'C10.2','V_HI_C10_B','ESD VBUS decoupling capacitor local HFground, physical return joins actual commonplane.')
via('V_HI_C10_A',[43.8,10.7764],'Offpad C10ground directly next to pad.')
via('V_HI_C10_B',[43.8,11.5764],'Secondcapgroundvia .8pitch, not a via in solder aperture.')
e={'status':'CONDITIONAL_CANDIDATE_AWAITING_U4_MOVE_AND_FULL_USB_GEOMETRY',
 'prerequisites':['U4 actualposition(40.25,11.4)180 andGND2(40.25,12.7); must not execute on oldU4y10.0.',
 'USBdataflowthrough routesx41.2/39.3 y10.1..12.7 merged from MCUagent; oldGNDvia40.9,11.5 forbidden.',
 'VBUS U4.5->C10.1 route coordinated with USB inputescape, noTOPcrossing ofDPcolumn.',
 'Groundplanes freshgenerated on actualL2/L3 or2Lbottom; everyvia reference reach and returnslot reviewed.'],
 'operations':ops,'rules':[],
 'geometryNotes':['TwoU4GNDvia copper rings overlap same-net, drillgap~.2385>=.2032 but doesnot automatically approve manufacturing.',
 'No claim idealinductance or systemESDcertification;2L1.524mm return-height is materiallylarger than4L.2104mm.',
 'C10VBUSpad5route stillnot in this file; do not claimESDrail complete fromground-only candidate.']}
save('ESD_ground_routes_04.json',e)
print('saved03c, correctedpolicyBOOT_SERVICE, conditionalESDground04')
