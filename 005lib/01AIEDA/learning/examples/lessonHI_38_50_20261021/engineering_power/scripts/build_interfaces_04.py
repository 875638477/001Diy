from pathlib import Path
import json,math,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
def save(n,o):(R/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
s=json.loads((R/'power_star_03.json').read_text())
s['revision']='03b preserves original03 history; fixes ADC_INPUT crossing by rerouting low-current prefilter supply'
s['prerequisites'][0]='power_paths_02d C9 output and ground network implemented'
for o in s['operations']:
 if o['id']=='V3_VDDA_PRE_FILTER':
  o['points']=[[29.8,30.95],[28.4,32.35],[22,32.35],[22,37],[29.5,37]]
  o['widths']=[.6]*5
  o['widths']=[.6]*(len(o['points'])-1)
  o['purpose']='Low-current prefilter V3V3 feed detours left of J10, preserving short TOP ADC_INPUT path; no digital loads downstream of R26. Additional length belongs before filter and local C18/C19 decoupling.'
  o['length_mm']=sum(math.dist(a,b) for a,b in zip(o['points'],o['points'][1:]))
s['scopeNotes'].append('03 original x28.4 y32.35..37 crossed ADC_INPUT at y34. Original rejected,03b detours x22. Full-group geometry and native DRC must confirm J10 PTH clearance and actual ground return.')
save('power_star_03b.json',s)
check=(R/'scripts/precheck_power_geometry.py').read_text()
check=check.replace("'power_star_03.json'","'power_star_03b.json'").replace("'readouts/power_geometry_precheck.json'","'readouts/power_geometry_precheck_03b.json'")
(R/'scripts/precheck_power_geometry_03b.py').write_text(check)
def route(i,n,p,w,f,t,purpose):
 return dict(type='route',id=i,net=n,layer='TOP',points=p,widths=[w]*(len(p)-1),**{'from':f,'to':t,'purpose':purpose})
ops=[
route('CAN_H_U5_TERM','CAN_H',[[69.588,14.73],[71.5,14.75]],.3,'U5.7','R15.1','Short branch joins end-node termination next to J3; retain two-end-only population rule.'),
route('CAN_H_TERM_J3','CAN_H',[[71.5,14.75],[74,14.54]],.3,'R15.1','J3.1','Main connector route via termination pad; no long T stub.'),
route('CAN_L_U5_TERM','CAN_L',[[69.588,13.46],[70.8,13.46],[71.5,12.76],[71.5,11.702]],.3,'U5.6','R15.2','Horizontal escape avoids U5 NC5 copper before descending, remain beside CANH corridor without crossing.'),
route('CAN_L_TERM_J3','CAN_L',[[71.5,11.702],[72.5,11.702],[74,12]],.3,'R15.2','J3.2','Direct short route to bus connector; preserve connector GND3.'),
route('CAN_TX_IDLE_BRANCH','CAN_TXD',[[64,16],[62.9,16],[61.9764,16.9236],[61.9764,17.9]],.2,'U5.1','R14.2','10k idle pullup branch near TXD; main TXD approaches U5 from left, do not route digital track between CAN bus pins.')
]
can={'status':'ENGINEERING_CANDIDATE_NEEDS_GROUP_GEOMETRY_AND_NATIVE','operations':ops,'placementChanges':[],'rules':[],
 'scopeNotes':['TOP only, no CAN bus vias planned. Width.3 gap>=.2 per class; PCB differential impedance not certified, no forced serpentines.',
 'H/L different pin and termination coordinates yield modest length imbalance; 500kbps<=1m isolated bench contract does not remove fast-edge reference requirement.',
 'R15=120ohm>=.25W populated only at physical two cable ends, DNP at intermediate nodes. One board termination is not complete bus topology.',
 'TCAN332 100nF C11 and1uF C12/local GND must be connected before bus test; no arbitrary bus TVS justified by internal ESD rating.']}
save('interface_CAN_routes_04.json',can)
sources=[
dict(id='TI_TCAN33x_RevF',url='https://www.ti.com/lit/ds/symlink/tcan332.pdf',revision='SLLSEQ7F May2025',sections=['7.4 Power supply','7.5 Layout','7.3 application and termination'],checked='2026-10-21',usage='100nF local decoupling, layout/short stubs and reference; source evidence distinct from our chosen coordinates.'),
dict(id='ST_DS5319_Rev20',url='https://www.st.com/resource/en/datasheet/stm32f103c8.pdf',revision='DS5319Rev20 July2025',sections=['I/O characteristics','I2C characteristics Tables41/42','SPI characteristics','pin assignment'],checked='2026-10-21',usage='Pin functionality/electrical boundaries. Interface speed limits below are teaching system contracts, not IC maxima.'),
dict(id='ST_AN2586_Rev8',url='https://www.st.com/resource/en/application_note/an2586-getting-started-with-stm32f10xxx-hardware-development-stmicroelectronics.pdf',revision='AN2586Rev8 Dec2022',sections=['reset','boot','debug'],checked='2026-10-21',usage='Reset/boot/SWD hardware requirements. J9 custom pinout remains different from Cortex10.'),
dict(id='DE_FINAL_CONTRACT',path='learning/examples/de_15_26_20261019/power_interface_spec.json',usage='Existing500kbps<=1m CAN, SPI<=1MHz<=10cm, I2C default100kHz and total100pF envelope; original component values/assembly populations.'),
dict(id='HI2L_PROFILE',path='engineering_power/rules_profile_2L_69nets.json',usage='All69 nets classified; physical width/space/neck explicit, not DEFAULT fallback.')]
policy={'status':'ENGINEERING_POLICY_FOR_CONSTRAINED_GEOMETRY_PLANNING','units':'mm','sources':sources,
 'common':{
 'layers':{'2L':['TOP','BOTTOM'],'4L':['TOP','BOTTOM'],'nonGNDInnerRouting':False},
 'preferredLayer':'TOP','bottomUse':'Only deliberate short crossover or documented corridor. Avoid bottom route under critical TOP clocks/data and do not turn solid2L ground into long parallel slots.',
 'reference':{'2L':'Actual BOTTOM GND. Every new signal/power slot requires regenerated connected ground and nearby TOP GND crossing/ground stitching where needed; no quiet-island crossing.',
 '4L':'Actual L2 GND forTOP. BOTTOM requires actual L3 GND after02d, not layer-name intent. Crossing reference/island boundary is forbidden unless explicit return reviewed.'},
 'layerTransition':'L28_VIA030_C060 only; add nearbyGNDvia that reaches same actual common reference, avoid isolated HSE island. Via targetdistance<=1.5mm is teachingreviewtarget notSI/EMIcert; export actual offset and plane path.',
 'spacing':'Use actual group CSet/classclass; normaldigital .2, power.3, SW.5 and SW-sensitive1.0; USB-digitalisolation .5 unless expressly reviewed finepitchregion. No global spacing relaxation to clear congestion.',
 'edgeRate':'Baud/clock frequency alone does not set edge rate. Firmware must choose lowest adequate GPIO outputspeed and verify voltage/timing; no firmware implemented, no assumed2MHz slew guarantee.',
 'length':'Direct, few bends, avoid coils. Report actual net/pin-to-pin path lengths and branch lengths. No universal matching on unrelated UART/I2C/SWD nets.',
 'forbiddenCorridors':['TPS54202 SW/L/BOOT reserved area','HSE quietground island and its moat','ADC input/filter region','USB paired corridor','mounting-hole and connector mating keepouts'],
 'powerSeparation':'No digital main supply through .25 MCU pad escapes. Header combined external current remains10mA total; V3V3 normal150mA/Ta0..40C thermal unverified.'
 },
 'interfaces':[
 {'id':'CAN_BUS','nets':['CAN_H','CAN_L'],'contract':'500kbps<=1m bench; controller bit timing/physical cable not yet verified.',
  'drivers':'U5.7H/U5.6L bidirectional transceiver; J3.1H/J3.2L/J3.3GND.',
  'topology':'Use interface_CAN_routes_04: U5 -> short R15 end termination junction -> J3. End-only120ohm, intermediateDNP.',
  'preferredCorridor':[69,11,75,16],'width':.3,'space':.2,'viasPlanned':0,
  'lengthPolicy':'No deliberate serpentine. Short paired local routes, expose actual H/L imbalance; no claim120ohm PCB impedance.'},
 {'id':'CAN_DIGITAL','nets':['CAN_TXD','CAN_RXD'],
  'contract':'OnlyCAN assembly profile. R12/R13 populate and USB R5/R6/R11 DNP; PA8 attach heldhigh. No simultaneousUSB/CAN.',
  'topology':'PA12_SHARED->R12->U5.1TXD. U5.4RXD->R13->PA11_SHARED. R14.2idle10k short branch nearU5.1; no arbitrary source damping role for0ohmselectors.',
  'preferredCorridor':[44.8,16.5,64,19.7],'width':.2,'space':.2,
  'branchAudit':'Both selected and unselected PCB selection footprints/branches physically exist. Measure residual PA11/12 stubs, retain USB branch limits; DNP does not delete copper.',
  'avoid':'USB pair area x38..42 belowR5/R6 and buck/FB left side; a shortBOTTOM bridge allowed only with return.'},
 {'id':'UART','nets':['PA9_UART_TX','UART_TX','PA10_UART_RX','UART_RX'],
  'contract':'3.3V logic, UART baud/cable not finalized. Proposed bringup115200bps<=10cm with adjacentGND is a condition for initial test, not original approved performance.',
  'sourceSeries':'U1.30PA9->R16.1, R16=33ohm nearMCU, R16.2->J4.2 long route. Preserve R16 as source-first, value requires real edge/receiver/cable test.',
  'receive':'J4.3->R17.2->R17.1->U1.31. R17=0 at MCU is selection/debug, not source termination for external transmitter. R18=10k idle pullup atconnector-sideUART_RX can shortbranch.',
  'preferredCorridor':[36,19.5,74,26.5],'width':.2,'space':.2,'matching':'NoTX/RX lengthmatch; neither signal crossesUSB/HSE/ADC.',
  'ground':'ConnectJ4.4 tocommonGND, noRS232levels, no probe/header power injection.'},
 {'id':'SPI','nets':['PA5_SPI_SCK','SPI_SCK','PA7_SPI_MOSI','SPI_MOSI','PA4_SPI_NSS','SPI_NSS','PA6_SPI_MISO','SPI_MISO'],
  'contract':'ExistingSPI<=1MHz, externalcable<=10cm; actualGPIOedge/loadandreceive setup/hold unverified.',
  'sourceFirst':['U1.15->R21.1(33R)->R21.2->J6.2SCK','U1.17->R22.1(33R)->R22.2->J6.3MOSI','U1.14->R23.1(33R)->R23.2->J6.5NSS'],
  'receive':'J6.4MISO->R24.2(0R)->R24.1->U1.16. R24 nearMCU not source termination for external driver.',
  'preferredCorridor':[7,27,34,36.8],'width':.2,'space':.2,
  'topology':'Pointtopoint each, SCK noTbranch. RouteSCK with continuousreference; do not thread beneathinductor/SW. Put source-side short routes before long header segments.',
  'matching':'No arbitrary equal lengths. DocumentSCK/MOSI flighttime/skew vs externalreceiver setuphold only after cable/edge/delay known. R25pullup belongs PA4NSS short branch, not extra long clockbus.',
  'return':'J6.6GND is physicalheaderreturn; cable<=10cm is teaching envelope, singleGNDpin insufficient to certify fastedges/EMI.'},
 {'id':'I2C','nets':['I2C_SCL','I2C_SDA'],
  'contract':'Default100kHz. <=400kHz is RC envelope only: DS5319Rev20 Table41footnote2 vsTable42 timing condition discrepancy retained. No400k certification.',
  'topology':'U1PB6/7 -> R19/20 pullup junction -> J5SCL/SDA. Pullups2.2k toV3V3, no pushpull driver assumption; branch to pullup keptshort.',
  'preferredCorridor':[45,27,74,41],'width':.2,'space':.2,
  'lengthPolicy':'NoSCL/SDAmatching. Short common corridor withcontinuousGND; budget totalC<=100pF including MCU/PCB/connector/cable/externaldevice, checkVol/Iol and tR.',
  'return':'J5.4GND actualreturn, noarbitrary external additionalpullups without recalculation.'},
 {'id':'SWD_RESET_BOOT','nets':['SWDIO','SWCLK','SWO','NRST','BOOT0','BOOT1','BOOT0_SEL'],
  'contract':'No final debugger clock. ProposedinitialSWCLK<=1MHz shortprobe cable is bringupcondition, notproven limit. KeepSWDenabled, JTAGmaybedisabledwhenusingPA15/PB3/PB4.',
  'topology':'J9 custom1x6 VTREF,GND,SWDIO,SWCLK,NRST,SWO. VTREFsenseonly; SWDIO/SWCLK freeofnormalGPIOloads. SWO optional, no blanketmatching.',
  'preferredCorridor':[44.8,20,64,28],'width':.2,'space':.2,
  'reset':'NRSTcap localatMCU; J7isresetjumper/header, notphysicalpushbutton. Shortservicebranch J9NRST connectsunderreset; no PORdelay claim fromRC.',
  'boot':'10kpulldowns nearestpinsBOOT0/1. ServiceJ8via1k to3V3. F103C8ROMUSART1boot, noROMUSBDFU claim.',
  'return':'J9.2GND continuousreference, do not carrydebuggerreturn throughquietHSEisland.'},
 {'id':'USB_AUX','nets':['USB_CC1','USB_CC2','VBUS_GATE','VBUS_PRESENT_N','USB_ATTACH_N','USB_PULLUP_SRC','USB_VBUS'],
  'contract':'USBdatasignals handled separately byf27. NoUSBpoweredboard:USBVBUS onlydetect/ESDrail; cannotshortVBUSintoV5.',
  'cc':'CC1/2 each own5.1kRd toGND nearJ2; nojoiningCC1/2. ESDarray protectsD+/D- only, no inventedCC/SBU systemESDcoverage.',
  'attach':'Q2PMOS sourceV3V3, drainUSB_PULLUP_SRC->R11->USB_DP; gatepulluptosource defaultdetach, PA8active-lowattach. R11branch keptshort byf27, controlroutes .2 awayfromdatapair.',
  'sense':'Q1VBUSgate viaR7 etc preserve positive/negative logic and powerofflimit; slow gate/controlpreferTOP nearJ2 side, avoidrouting underdatapair.',
  'width':.2,'USB_VBUS_width':.4,'space':.2,
  'ESDground':'Separateground04plan follows actualU4position. Bodyvias40.0/11.4 and40.5/11.6 underreview, old40.9/11.5 discardedbecauseflowthroughDPcollision.'}
 ],
 'acceptance':['All ordinary nets retain correct pin endpoints, source resistor order and assembly profile.',
 'Every layerchange/via explicitlylisted and connected to actual reference; regenerateplanes/OOD0 and export geometry.',
 'Actual DRCallcategories0 plus independentgeometry/no copperoverlap, 69net272logicalpins/6NC identity, remaining count/BFS agree.',
 'Longest .25powerneck, plane/thermal bottleneck, groundslotdetours reviewed separately; DRC0 is not electrical/EMI/USB certification.']}
save('routing_policy_interfaces_04.json',policy)
# Start durable lesson note; factual current state only, native latest checkpoints are referenced not assumed final.
note=Path(r'D:\001DIY\005lib\01AIEDA\learning\notes\lessonHI_power_20261021.md')
text='''# HI38-50 power and ordinary-interface routing study, 2026-10-21

Scope: engineering path planning and read-only copper review. f29 is sole Cadence executor. Root owns final combined records and final acceptance. All new scripts/sources/intermediate records are inside01AIEDA.

Current evidence: first buck batch ran on4L with0DRC,0OOD,8/8 endpoint proofs, remaining171->163. f29 reports02d implemented both2L/4L with0DRC and24/24 endpoint proofs, remaining163->142; fresh snapshots must be checked before independent acceptance. 03b innerMCU star remains a candidate until actual native neck measurements, plane connectivity and DRC readback.

Power choices: input C3 shiftedy18.6->18.0 to open .6VIN corridor; C3negative/U2GND each use paired offpad groundvias into actual reference. TOP SW/BOOT remain local. C4returnsSW, notGND. FB staysTOP and quiet; output sense uses a deliberately routedBOTTOM branch and explicitTOPground bridge across its2L slot. .6V3main distribution does not pass throughMCU .25escapes; local regionexceptions must retain measured lengths and fields. 4LactualL3ground is generated in02d;2Lbottomground is far1.524mm, versus4LTOP-L2 .2104mm: same connectivity does not imply equal looparea/highfrequencyreturn.

Failures preserved:02TOPV5sense crossedVIN;02bVIN_D1_C2 crossedC2GNDvia/trace;02c input routing not selected because longerbroadside overlap withBOTTOMsense;02d detoursinputy10.6.03originalVDDAprefilterfeed crossedADC_INPUTy34;03b rerouteslowcurrentfeed leftofJ10x22. Rejectedfiles are historical, never the current execution entry.

Authoritative current candidates: power_critical_paths_01.json;power_paths_02d.json;power_star_03b.json. Two-layer complete69net classification: rules_profile_2L_69nets.json. Interface policy: routing_policy_interfaces_04.json. ExplicitCANbus/termination branches: interface_CAN_routes_04.json. All candidates require merged-group geometry and actual native checks.

Ordinary interface lesson: CAN500kbps<=1m bench and end-only120ohm; SPI<=1MHz<=10cm with source-first33ohm SCK/MOSI/NSS; UARTTXsource33ohm, RX0ohm atMCU notsource damping; I2Cdefault100kHz/2.2k,total100pF envelope,400k timingunverified; SWDcustom1x6 VTREFsense-only, J7resetjumper, BOOTROMUSART1. No blanket lengthmatching; edge configuration and actual reference continuity matter even at lowbaud.

Open gates: USB22ohm historicalchoice/90ohmgeometrystillunconfirmed; USB4105 .95stakefromseatingplane versus1.6board assemblyunqualified;2LOSH .100mmmaskweb vs .1016minimum unresolved; actualR/C/headersMPNheight andcapDCbias/ESR/effectivecap unselected; LDOreversebackfeed forbidden,150mA/Ta0..40Cthermaltestpending; inputbench9..16V currentlimited, fuse notprecisionlimiter; CANbusfault+/-14V/internalIC ESD doesnotcertifysystemEMI/ESD. DRC0/remaining0 alone never proves SI/PI/EMI.
'''
note.write_text(text,encoding='utf-8')
print(json.dumps({'saved':['power_star_03b.json','routing_policy_interfaces_04.json','interface_CAN_routes_04.json',str(note)]}))
