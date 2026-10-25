from pathlib import Path
import json,hashlib,shutil
B=Path(r'D:\001DIY\005lib\01AIEDA')
G=B/'learning/examples/lessonG_30_37_20261020'
R=B/'learning/examples/lessonHI_38_50_20261021/engineering_power'
for x in ['scripts','source','readouts']:(R/x).mkdir(parents=True,exist_ok=True)
srcPath=B/'learning/examples/de_15_26_20261019/integrated_circuit.json'
src=json.loads(srcPath.read_text(encoding='utf-8'))
nets=sorted({n for c in src['components'] for n in c['pins'].values() if n})
groups={
'POWER_INPUT':dict(nets=['VIN_RAW','VIN_FUSED','VIN_PROT'],width=.6,neck=.25,spacing=.3,normalRole='input protection and buck input; .6mm is engineering distribution minimum at bench current, not an ampacity certification'),
'POWER_LV':dict(nets=['V5','V3V3'],width=.6,neck=.25,spacing=.3,normalRole='150mA total distribution, TOP first; no long .25 substitute'),
'VDDA':dict(nets=['VDDA'],width=.3,neck=.2,spacing=.3,normalRole='filtered analog supply only, no digital load current'),
'GROUND':dict(nets=['GND'],width=.6,neck=.25,spacing=.3,normalRole='broad TOP local returns and continuous BOTTOM plane; local quiet-return special paths separately documented'),
'SWITCH':dict(nets=['BUCK_SW','BUCK_BOOT'],width=.6,neck=.25,spacing=.5,normalRole='TOP only by plan; SW compact and BOOT return to SW, not GND'),
'FEEDBACK':dict(nets=['BUCK_FB'],width=.2,neck=.16,spacing=.3,normalRole='quiet TOP feedback small node, no autorouter/no test branch'),
'USB_FS':dict(nets=['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'],width=.2,neck=.16,spacing=.16,normalRole='provisional manufacturable geometry only, not90ohm certification; pair coupling/branches handled explicit USB plan'),
'OSCILLATOR':dict(nets=['OSC_IN','OSC_OUT','XTAL_OUT'],width=.2,neck=.16,spacing=.3,normalRole='TOP sensitive loop, no general bus crossing; ground strategy explicit'),
'ADC':dict(nets=['ADC_IN','ADC0'],width=.2,neck=.16,spacing=.3,normalRole='TOP analog route; no digital common return'),
'CAN_BUS':dict(nets=['CAN_H','CAN_L'],width=.3,neck=.2,spacing=.2,normalRole='short PCB bus pair; external120ohm termination, no impedance claim'),
'USB_VBUS':dict(nets=['USB_VBUS'],width=.4,neck=.2,spacing=.2,normalRole='sense+rail ESD only, never V5/V3V3; clamp ground path broad'),
'USB_AUX':dict(nets=['USB_CC1','USB_CC2','VBUS_GATE','VBUS_PRESENT_N','USB_ATTACH_N','USB_PULLUP_SRC'],width=.2,neck=.16,spacing=.2,normalRole='CC independent Rd and slow sense/attach paths'),
'RESET_BOOT_SWD':dict(nets=['NRST','BOOT0','BOOT1','BOOT_SERVICE','SWDIO','SWCLK','SWO'],width=.2,neck=.16,spacing=.2,normalRole='source and pullup/down topology; SWD Vref sense only'),
'I2C':dict(nets=['I2C_SCL','I2C_SDA'],width=.2,neck=.16,spacing=.2,normalRole='2.2k baseline; rise/capacitance and external cable budget not route matching'),
'SPI':dict(nets=['PA4_SPI_NSS','PA5_SPI_SCK','PA6_SPI_MISO','PA7_SPI_MOSI','SPI_NSS','SPI_SCK','SPI_MISO','SPI_MOSI'],width=.2,neck=.16,spacing=.2,normalRole='R21/22/23 source MCU, R24 zero path with external MISO driver; no arbitrary equal length'),
'UART_CAN_DIGITAL':dict(nets=['PA9_UART_TX','PA10_UART_RX','UART_TX','UART_RX','CAN_TXD','CAN_RXD'],width=.2,neck=.16,spacing=.2,normalRole='UART R16 source damping; CAN DNP profile branches controlled')
}
used={};invalid=[]
for g,d in groups.items():
 d['nets']=[n for n in d['nets'] if n in nets]
 for n in d['nets']:
  if n in used:invalid.append(n)
  used[n]=g
groups['GPIO']=dict(nets=[n for n in nets if n not in used],width=.2,neck=.16,spacing=.2,normalRole='remaining low-load GPIO routed only after critical corridors')
for n in groups['GPIO']['nets']:used[n]='GPIO'
profiles=[]
for g,d in groups.items():
 profiles.append({'id':'HI2L_'+g,'nets':d['nets'],'physicalClass':'HI2L_'+g+'_P','spacingClass':'HI2L_'+g+'_S','electricalClass':'HI2L_'+g+'_E','physicalCSet':'HI2L_P_'+g,'spacingCSet':'HI2L_S_'+g,'width_min_mm':d['width'],'neckwidth_min_mm':d['neck'],'necklength_max_mm':1.0,'allowed_layers':['TOP'] if g in ['SWITCH','FEEDBACK','OSCILLATOR','ADC'] else ['TOP','BOTTOM'],'preferred_layer':'TOP','viaList':['L28_VIA030_C060'],'spacingFields_mm':{k:d['spacing'] for k in ['smdpin_line','line_line','via_line','line_shape','via_shape','shape_shape']},'preserveOtherPairFields':'copy local2L manufacturing baseline, not entire4L CSet','purpose':d['normalRole']})
report={'status':'PROPOSED_COMPLETE_2L_69NET_PROFILE_REQUIRE_NATIVE_READBACK','netCount':len(nets),'assignedNetCount':len(used),'duplicates':invalid,'groups':profiles,'classClass':[{'a':'SWITCH','b':b,'spacing_mm':1.0} for b in ['USB_FS','OSCILLATOR','ADC','FEEDBACK']]+[{'a':'USB_FS','b':b,'spacing_mm':.5} for b in ['GPIO','RESET_BOOT_SWD','SPI','UART_CAN_DIGITAL','I2C','USB_AUX']],'retainedG31Exceptions':'rebind/recreate from new2L POWER_LV/GROUND CSet, only original3TOP rectangles maxneck1.4; newCSet copies not dynamic-parent; validate fields and challenge inside/outside','newBuckException':{'id':'HI_U2_SW_ESCAPE','group':'SWITCH','layer':'TOP','polygon':[[22.95,20.55],[24.9,20.55],[24.9,21.45],[22.95,21.45]],'onlyDelta':{'necklength_max_mm':[1.0,1.2]},'plannedNeck_mm':1.15},'manufacturingBasis':{'twoLayerTarget':'existing OSH2L teaching target in F28, not fabrication approval','publicMinimumTrackGap_mm':.1524,'chosenGeneralNeck_mm':.16,'reason':'.16 stays above .1524; do not inherit4L .15 blindly','throughViaDrillCopper_mm':[.3,.6],'unresolved':'USB footprint .100 mask web vs published.1016 remains open, and connector stake/1.6board assembly not qualified'},'USBTarget':{'impedance':'90ohm target pending approved stackup/geometry','outerWidth_mm':.2,'minimumGap_mm':.16,'notValidatedImpedance':True,'electrical':{'maxVia':2,'phaseTolerance_mm':1,'uncoupledMax_mm':6},'note':'Keep existing design intent but USB author may require justified local breakout exception; no length-only certification'},'viaAndPlaneRules':['BOTTOM copper is real GND, every added signal slot requires connected-component/neck/detour review','through via not blind, verify padstack TOP/BOTTOM span and layer names','no physicalMASK, full15Film unchanged'],'noDefaultFallback':True}
assert len(nets)==69 and len(used)==69 and not invalid
assert all(n.startswith('GPIO_') for n in groups['GPIO']['nets'])
(R/'rules_profile_2L_69nets.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
manifest=[]
for p in [srcPath,G/'inventory/normalized_actual_2L.json',G/'inventory/normalized_actual_4L.json']:
 dest=R/'source'/p.name;shutil.copy2(p,dest);manifest.append({'source':str(p),'copy':str(dest),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()})
(R/'source/input_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'nets':len(nets),'groups':len(groups),'groupCounts':{g:len(d['nets']) for g,d in groups.items()},'defaultFallback':False}))
