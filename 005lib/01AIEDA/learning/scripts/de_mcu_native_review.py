"""Independent, read-only review of native Capture exports against D15-19 sources.

Does not import the integrated-circuit generator or execute Cadence APIs.
"""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'examples'/'de_15_26_20261019'
LOG=ROOT/'logs'/'de_15_26_20261019'
SOURCE=json.loads((BASE/'mcu_spec.json').read_text(encoding='utf-8'))
CHECKS=[]
def ck(section,name,ok,evidence):
    CHECKS.append({'section':section,'check':name,'pass':bool(ok),'evidence':evidence})
def rows(path):
    return list(csv.DictReader(path.open(encoding='utf-8-sig',newline=''),delimiter='\t'))
def h(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dataset(tag):
    inst=rows(LOG/f'instances_{tag}.tsv'); pins=rows(LOG/f'pins_{tag}.tsv'); nets=rows(LOG/f'connectivity_{tag}.tsv')
    byref={x['reference']:x for x in inst}
    bymodule={x['module_id']:x for x in inst}
    pindict={(x['reference'],x['number']):x for x in pins}
    pin_net={(x['reference'],x['number']):x['net'] for x in nets}
    modnet={}
    for x in nets:modnet.setdefault(byref[x['reference']]['module_id'],{})[x['number']]=x['net']
    return dict(inst=inst,pins=pins,nets=nets,byref=byref,bymodule=bymodule,pindict=pindict,pin_net=pin_net,modnet=modnet)
single=dataset('single');eco=dataset('eco')

# These are explicit naming translations, independently reviewed from the function
# allocation; they do not import or compare root's generated wiring dictionary.
ALIASES={'3V3':'V3V3','VDDA_3V3':'VDDA','SPI1_CS_N':'PA4_SPI_NSS','SPI1_SCK':'PA5_SPI_SCK','SPI1_MISO':'PA6_SPI_MISO','SPI1_MOSI':'PA7_SPI_MOSI','UART1_TX':'PA9_UART_TX','UART1_RX':'PA10_UART_RX','I2C1_SCL':'I2C_SCL','I2C1_SDA':'I2C_SDA'}

for tag,d in [('single',single),('eco',eco)]:
    sec=f'{tag}:nativeinventory'
    ck(sec,'Reference and module identity unique',len(d['inst'])==len(d['byref'])==len(d['bymodule'])==80 and all(x['reference'] and x['module_id'] for x in d['inst']),{'instances':len(d['inst']),'ref_unique':len(d['byref']),'module_unique':len(d['bymodule'])})
    ck(sec,'Every native pin belongs to a known instance and has a unique physical key',len(d['pins'])==len(d['pindict'])==272 and all(x['reference'] in d['byref'] for x in d['pins']),{'physical_pins':len(d['pins'])})
    nc={(x['reference'],x['number']) for x in d['pins'] if x['nc']=='1'}
    ck(sec,'Connected and explicit NC pins partition the design',len(nc)==6 and len(d['pin_net'])==266 and not(nc&set(d['pin_net'])) and set(d['pindict'])==nc|set(d['pin_net']) and len(d['nets'])==266,{'connected':len(d['pin_net']),'NC':sorted(nc),'flatnets':len({x['flat_id'] for x in d['nets']})})
    u=d['bymodule']['U_MCU'];ur=u['reference']
    ck(sec,'MCU physical package and MPN',ur=='U1' and u['value']=='STM32F103C8T6' and u['mpn']=='STM32F103C8T6' and u['footprint']=='l09_stm32f103c8_lqfp48',u)
    observed=[x for x in d['pins'] if x['reference']==ur]
    ck(sec,'Exactly 48 physical MCU pins, all connected',len(observed)==48 and {int(x['number']) for x in observed}==set(range(1,49)) and not any(x['nc']=='1' for x in observed),{'count':len(observed),'source':'DS5319 Rev20 Figure8 PDF26'})
    pinchecks=[]
    for sourcepin in SOURCE['pins']:
        n=str(sourcepin['number']);actual=d['pindict'].get((ur,n),{}); net=d['pin_net'].get((ur,n)); expectednet=ALIASES.get(sourcepin['proposed_net'],sourcepin['proposed_net'])
        ok=(actual.get('name')==sourcepin['name'] and actual.get('type')==str(sourcepin['capture_type']) and net==expectednet)
        pinchecks.append({'pin':int(n),'name':actual.get('name'),'type':actual.get('type'),'net':net,'expected_net':expectednet,'pass':ok})
    ck(sec,'Every MCU pin name, electrical type and assigned net agrees with original source pin table',all(x['pass'] for x in pinchecks),{'source':'mcu_spec.json pins; DS5319 Rev20 Figure8/Table5 visually reviewed independently before integration','pin_checks':pinchecks})

def topology(d,tag):
    sec=f'{tag}:MCUtopology'
    def part(module,pairs,value=None):
        actual=d['modnet'].get(module,{})
        instance=d['bymodule'].get(module,{})
        return actual=={str(n):net for n,net in pairs.items()} and (value is None or instance.get('value')==value)
    power={1:'V3V3',8:'GND',9:'VDDA',23:'GND',24:'V3V3',35:'GND',36:'V3V3',47:'GND',48:'V3V3'}
    ck(sec,'VBAT and all three VDD/VSS pairs plus VDDA/VSSA are correctly connected',all(d['modnet']['U_MCU'][str(n)]==net for n,net in power.items()),{'physical_pin_nets':power,'source':'DS5319 PDF26/36/74'})
    for n in (24,36,48):
        ck(sec,f'100nF bypass for VDD{n}',part(f'C_VDD{n}',{1:'V3V3',2:'GND'},'100nF'),{'module':f'C_VDD{n}','ref':d['bymodule'][f'C_VDD{n}']['reference'],'scope':'electrical presence only; own pin-local PCB loop remains layout requirement'})
    ck(sec,'VDD3 bulk and VBAT bypass exist',part('C_MCU_BULK',{1:'V3V3',2:'GND'},'10uF') and part('C_VBAT',{1:'V3V3',2:'GND'},'100nF'),{'bulk':'10uF nominal/effective>=4.7uF requirement','VBAT':'tied V3V3; notfloating','placement_at_pin48':'constraint recorded, PCB placement not claimed'})
    ck(sec,'Analog supply link and all local analog bypass capacitors',part('R_VDDA_LINK',{1:'V3V3',2:'VDDA'},'0R') and part('C_VDDA_HF',{1:'VDDA',2:'GND'},'10nF') and part('C_VDDA_MID',{1:'VDDA',2:'GND'},'100nF') and part('C_VDDA_BULK',{1:'VDDA',2:'GND'},'2.2uF'),{'bulk':'2.2uF nominal; effective>=1uF still a component-selection condition','source':'DS5319 Figure14/40 and AN2586 Figure2; no exposedVCAP/VREF pins'})
    ck(sec,'Reset pull-up, ground capacitor and normally-open service shunt',part('R_NRST',{1:'V3V3',2:'NRST'},'10k') and part('C_NRST',{1:'NRST',2:'GND'},'100nF') and part('J_RESET',{1:'NRST',2:'GND'}) and d['modnet']['U_MCU']['7']=='NRST',{'R':'10k optional external to internal30-50k','C':'100nF','service_shunt':'header is normally open by user practice; no pushbutton model','timing':'20us external reset requirement not measured'})
    ck(sec,'BOOT defaults and service selection correct',part('R_BOOT0_PD',{1:'BOOT0',2:'GND'},'10k') and part('R_BOOT1_PD',{1:'BOOT1',2:'GND'},'10k') and part('R_BOOT_SERVICE',{1:'V3V3',2:'BOOT_SERVICE'},'1k') and part('J_BOOT',{1:'BOOT_SERVICE',2:'BOOT0'}) and d['modnet']['U_MCU']['44']=='BOOT0' and d['modnet']['U_MCU']['20']=='BOOT1',{'open':'Flash default','short':'BOOT0high/BOOT1low USART1systemROM','source':'AN2586 PDF16-17; noROMUSBDFU claim'})
    ck(sec,'SWD header voltage, ground, data, clock, reset and optional trace',part('J_SWD',{1:'V3V3',2:'GND',3:'SWDIO',4:'SWCLK',5:'NRST',6:'SWO'}) and all(d['modnet']['U_MCU'][str(n)]==net for n,net in {34:'SWDIO',37:'SWCLK',7:'NRST',39:'SWO'}.items()),{'connector':'local6pin2.54mm exactpinmap; notARM10 compatible','VTREF':'sense/output contract; no hardwarereverseblock inferred','source':'DS5319 Figure8/Table5, AN2586 PDF18-20'})
    ck(sec,'Crystal resonator and case-ground pin topology',part('Y_HSE',{1:'OSC_IN',2:'GND',3:'XTAL_OUT',4:'GND'},'8MHz') and part('R_HSE_SER',{1:'OSC_OUT',2:'XTAL_OUT'},'0R') and d['modnet']['U_MCU']['5']=='OSC_IN' and d['modnet']['U_MCU']['6']=='OSC_OUT',{'crystal_mpn':d['bymodule']['Y_HSE']['mpn'],'source':'AbraconABM3B RevU PDF3 TOPVIEW:1/3 resonator,2/4ground','physical_land_orientation':'separate footprint acceptance; TSVdoesnotrevalidategeometry'})
    ck(sec,'Crystal load capacitors follow calculated initial values',part('C_HSE_IN',{1:'OSC_IN',2:'GND'},'16pF') and part('C_HSE_OUT',{1:'XTAL_OUT',2:'GND'},'16pF'),{'CL_pF':18,'stray_assumed_pF':10,'calculated_equal_cap_pF':16,'startup_gain_margin':SOURCE['clock']['gain_margin'],'drive_frequency_startup_measurement':'pending'})
    ck(sec,'ADC physical input, series resistor and shunt filter',part('J_ADC',{1:'ADC_IN',2:'GND'}) and part('R_ADC',{1:'ADC_IN',2:'ADC0'},'1k') and part('C_ADC',{1:'ADC0',2:'GND'},'100nF') and d['modnet']['U_MCU']['10']=='ADC0',{'source_limits':'0..3.0V <=1Hz, Rout<=1k, poweredboard','100Sps':'firmwareintent, notrun','RC_antialias':'notclaimed:fc796..1592Hz exceeds50HzNyquist','ADC_clock_sampling':'12MHz/71.5cycles designcondition, nothardwaremeasured'})
    ck(sec,'VBUS sensing isolates 5V from PB0 and attach is off by pull-up',part('R_VBUS_GATE',{1:'USB_VBUS',2:'VBUS_GATE'},'10k') and part('Q_VBUS',{1:'VBUS_GATE',2:'GND',3:'VBUS_PRESENT_N'}) and part('R_VBUS_READ',{1:'V3V3',2:'VBUS_PRESENT_N'},'10k') and part('R_ATTACH_OFF',{1:'V3V3',2:'USB_ATTACH_N'},'100k') and part('Q_ATTACH',{1:'USB_ATTACH_N',2:'V3V3',3:'USB_PULLUP_SRC'}) and part('R_DP_PULLUP',{1:'USB_PULLUP_SRC',2:'USB_DP'},'1.5k') and d['modnet']['U_MCU']['18']=='VBUS_PRESENT_N' and d['modnet']['U_MCU']['29']=='USB_ATTACH_N',{'PB0':'no direct USB5V connection','PA8':'P-channel gate; highoff','VBUS_logic':'firmwaremustdetachwhenVBUSabsent; notruntimevalidated'})
    branch={'R_USB_DP':({1:'PA12_SHARED',2:'USB_DP'},'22R'),'R_USB_DM':({1:'PA11_SHARED',2:'USB_DM'},'22R'),'R_CAN_TX':({1:'PA12_SHARED',2:'CAN_TXD'},'0R'),'R_CAN_RX':({1:'PA11_SHARED',2:'CAN_RXD'},'0R')}
    ck(sec,'USB and CAN branch selectors connect intended shared MCU pins',all(part(k,*v) for k,v in branch.items()) and d['modnet']['U_MCU']['32']=='PA11_SHARED' and d['modnet']['U_MCU']['33']=='PA12_SHARED' and part('R_CAN_TX_IDLE',{1:'V3V3',2:'CAN_TXD'},'10k'),{'USB':'nativeR5/R6 22ohm','CAN':'nativeR12/R13 0ohm; DNPdefault','CANidle':'TXDpulledrecessivewhileMCUbranchopen','sharedRAM':'RM0008 Rev21 PDF622 +AN4879 cannotconcurrentlyenable'})
topology(single,'single');topology(eco,'eco')

bom=list(csv.DictReader((BASE/'BOM_baseline.csv').open(encoding='utf-8-sig',newline='')))
bm={x['Module_ID']:x for x in bom}
ck('assembly','BOM reference identity agrees with native instances',len(bom)==80 and all(single['bymodule'][x['Module_ID']]['reference']==x['Reference'] for x in bom),{'BOM_count':len(bom),'source':'native instance identities independently joined to BOM, no generated wiring comparison'})
ck('assembly','Default USB selectors fitted and CAN selectors DNP',all(bm[x]['Assembly']=='yes' for x in ['R_USB_DP','R_USB_DM']) and all('DNP' in bm[x]['Assembly'] for x in ['R_CAN_TX','R_CAN_RX']),{x:{'ref':bm[x]['Reference'],'assembly':bm[x]['Assembly']} for x in ['R_USB_DP','R_USB_DM','R_CAN_TX','R_CAN_RX']})
pol=json.loads((BASE/'power_interface_spec.json').read_text(encoding='utf-8'))['assembly_profiles']
ck('assembly','Alternative USB/CAN population profiles are mutually exclusive',set(pol['USB']['fit'])=={'R_USB_DP','R_USB_DM'} and set(pol['USB']['DNP'])=={'R_CAN_TX','R_CAN_RX'} and set(pol['CAN']['fit'])=={'R_CAN_TX','R_CAN_RX'} and set(pol['CAN']['DNP'])=={'R_USB_DP','R_USB_DM'},pol)

changes_values=[{'reference':r,'before':single['byref'][r]['value'],'after':eco['byref'][r]['value']} for r in single['byref'] if single['byref'][r]['value']!=eco['byref'][r]['value']]
changes_nets=[{'reference':r,'pin':n,'before':single['pin_net'][(r,n)],'after':eco['pin_net'].get((r,n))} for r,n in single['pin_net'] if single['pin_net'][(r,n)]!=eco['pin_net'].get((r,n))]
ck('ECO','MCU all48 pin names/types/nets stay identical',all(single['pindict'][('U1',str(n))]==eco['pindict'][('U1',str(n))] and single['pin_net'][('U1',str(n))]==eco['pin_net'][('U1',str(n))] for n in range(1,49)),{'scope':'physicalMCU identity andwiring, notflatIDstableassumption'})
ck('ECO','Only intended two I2C pull-up values change',sorted(changes_values,key=lambda x:x['reference'])==[{'reference':'R19','before':'2.2k','after':'3.3k'},{'reference':'R20','before':'2.2k','after':'3.3k'}],changes_values)
ck('ECO','Only intended spare-header PB8/PB9 positions exchange',sorted(changes_nets,key=lambda x:(x['reference'],x['pin']))==[{'reference':'J13','pin':'7','before':'GPIO_PB8','after':'GPIO_PB9'},{'reference':'J13','pin':'8','before':'GPIO_PB9','after':'GPIO_PB8'}],changes_nets)
ck('ECO','All80 reference/module/footprint/MPN identities retained',set(single['byref'])==set(eco['byref']) and all(all(single['byref'][r][k]==eco['byref'][r][k] for k in ['module_id','footprint','mpn']) for r in single['byref']),{'components':80,'footprint_changes':[]})

be=list(csv.DictReader((BASE/'BOM_eco.csv').open(encoding='utf-8-sig',newline='')))
be={x['Reference']:x for x in be}
eco_metadata=json.loads((BASE/'integrated_circuit_eco.json').read_text(encoding='utf-8'))
eco_desc={x['ref']:x['properties'].get('source_description') for x in eco_metadata['components'] if x['ref'] in ['R19','R20']}
for tag,d in [('single',single),('eco',eco)]:
    ps=rows(LOG/f'properties_{tag}.tsv')
    propmap={(x['reference'],x['property']):x['value'] for x in ps}
    ck('assembly',f'{tag} native ASSEMBLY and assembly_group persisted correctly',all(propmap.get((r,'ASSEMBLY'))==a and propmap.get((r,'assembly_group'))==g for r,a,g in [('R5','yes','USB_ONLY'),('R6','yes','USB_ONLY'),('R12','DNP default USB mode','CAN_ONLY'),('R13','DNP default USB mode','CAN_ONLY')]),{'source':f'properties_{tag}.tsv','native_selectors':{r:{p:propmap.get((r,p)) for p in ['ASSEMBLY','assembly_group']} for r in ['R5','R6','R12','R13']}})
    ck('assembly',f'{tag} all80 assembly attributes agree with baseline policy',all(propmap.get((x['Reference'],'ASSEMBLY'))==x['Assembly'] for x in bom),{'count':80,'source':f'native properties_{tag}.tsv vs assembly BOM'})
    if tag=='eco':
        ck('ECO','Native I2C source_description, Value and procurement Specification agree',all(propmap.get((r,'source_description'))=='3.3k 1%' and d['byref'][r]['value']=='3.3k' and be[r]['Specification']=='3.3k 1%' and eco_desc[r]=='3.3k 1%' for r in ['R19','R20']),{r:{'native_value':d['byref'][r]['value'],'native_source_description':propmap.get((r,'source_description')),'BOM_specification':be[r]['Specification'],'ECO_JSON_description':eco_desc[r],'native_ECO_reason':propmap.get((r,'ECO_REASON'))} for r in ['R19','R20']})
tr=0.8473*3333*100e-12
ck('ECO','3.3k 1pct I2C pull-up meets300ns RC rise condition only within100pF budget',tr<300e-9,{'formula':'30-70pct RC rise=0.8473*R*C','R_max_ohm':3333,'C_bus_max_F':100e-12,'worst_R_rise_ns':tr*1e9,'criterion_ns':300,'scope':'notphysicalI2Cmeasurement; buscapmustincludeMCU/header/cable/receiver; sinkcurrentandVOLcheckedseparately'})
paths=[BASE/'mcu_spec.json',BASE/'BOM_baseline.csv',BASE/'BOM_eco.csv',BASE/'integrated_circuit_eco.json',BASE/'native'/'de_integrated_single.dsn',BASE/'native'/'de_integrated_eco_final.dsn']+[LOG/f'{kind}_{tag}.tsv' for kind in ['instances','pins','connectivity','properties'] for tag in ['single','eco']]
report={'date_client':'2026-10-19 Asia/Shanghai','review_scope':'IndependentoriginalMCUpintable+nativeTSVtopology+nativeassemblyattributes+BOMprofile+ECOdiff; noCadenceAPI','pass':all(x['pass'] for x in CHECKS),'check_count':len(CHECKS),'checks':CHECKS,'inputs':[{'path':str(p.relative_to(ROOT)),'sha256':h(p)} for p in paths], 'limitations':['NoGPIO/clock/ADCfirmwareexecution','Nocrystaldrive/frequency/startup, analognoise, thermal, EMC orhardwaremeasurement','Decouplingloopposition/returngeometryandVDD3bulkplacementarePCBconstraints, notprovedbycommonV3V3net','NominalbulkvaluesdonotproveeffectivecapacitanceafterDCbias/tolerance/temperature','NativeCADcontainsallDNPcomponents; preservedassemblyattributesdo notproveassembledhardwarepopulation','StandardGUIERCstillnotverified; thisisindependentpin/topologyreview'],'unsafe_calls_executed':False}
(LOG/'mcu_native_review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pass':report['pass'],'checks':len(CHECKS),'failures':[x for x in CHECKS if not x['pass']]},ensure_ascii=True,indent=2))
if not report['pass']:raise SystemExit(1)
