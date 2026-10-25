from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
ops=[]
def rt(i,n,p,f,t,purpose,w=.6):
 ops.append(dict(type='route',id=i,net=n,layer='TOP',points=p,widths=[w]*(len(p)-1),**{'from':f,'to':t,'purpose':purpose}))
rt('CAN_VCC_LOCAL','V3V3',[[59.8,13.46],[61.8,13.46],[64,13.46]],'C12.1','U5.3','Independent main-source supply must reachC12positive; C11.1 inline local100nF toVCC, .6not throughMCUescape.')
rt('CAN_GND_LOCAL','GND',[[64,14.73],[62.7,14.73],[61.8,15.0348],[59.8,15.0348]],'U5.2','C12.2','DirectTOPwide GNDlink fromC11/C12negative totransceiverGND, not depend only on distantplane.')
rt('CAN_GND_VIA_A','GND',[[62.7,14.73],[62.6,14.73]],'CAN_GND_LOCAL','V_HI_CAN_GND_A','Offpad nearU5GND andC11 HFloop.')
ops.append(dict(type='via',id='V_HI_CAN_GND_A',net='GND',xy=[62.6,14.73],padstack='L28_VIA030_C060',purpose='LocalGNDreference via, powercurrentnotthin signalreturn.'))
rt('CAN_GND_VIA_B','GND',[[60.8,15.0348],[60.8,15.8348]],'CAN_GND_LOCAL','V_HI_CAN_GND_B','Second groundvia offC11/C12negativepads.')
ops.append(dict(type='via',id='V_HI_CAN_GND_B',net='GND',xy=[60.8,15.8348],padstack='L28_VIA030_C060',purpose='Common reference parallelgroundvia, actualplane connectivity required.'))
rt('CAN_TX_PULLUP_V3','V3V3',[[59.8,13.46],[58.2,13.46],[58.2,17.9],[60.4016,17.9]],'C12.1','R14.1','10kTXDidle pullup receives independent3V3; do not call a33ohm dampingresistor.')
o=dict(status='CANDIDATE_NEEDS_MAIN_V3_FEED_AND_GROUP_NATIVE_REVIEW',operations=ops,rules=[],sourceEndpoint='C12.1 requires separatelyplanned.6mainV3V3feed fromC9/mainstar takeoff, not from U1pad/decapneck.',
 scopeNotes=['C11=100nF/C12=1uF. DirectTOP supplyandground form localcurrentloop plusreference vias. No guarantee of actual capMPN/DCbias/ESD/EMC.',
 'OrdinaryUART/I2C/SPI/SWD routes must not thread through CANH/LbetweenU5andJ3 or throughdecouplingloop. MAXCAN60mA includednormal150mA budget.'])
(R/'CAN_local_supply_05.json').write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
print(len(ops))
