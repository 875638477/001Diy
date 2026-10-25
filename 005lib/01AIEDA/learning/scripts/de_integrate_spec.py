"""Integrate sourced MCU/interface specifications into one reviewable circuit."""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,hashlib,re
root=Path(__file__).resolve().parents[1]
base=root/'examples/de_15_26_20261019'
base.mkdir(parents=True,exist_ok=True)
mcu=json.loads((base/'mcu_spec.json').read_text(encoding='utf-8'))
power=json.loads((base/'power_interface_spec.json').read_text(encoding='utf-8'))
types={'INPUT':0,'BIDIRECTIONAL':1,'BIDIR':1,'OUTPUT':2,'PASSIVE':4,'POWER':7,'NC':4}
aliases={'3V3':'V3V3','VDDA_3V3':'VDDA','ADC0':'ADC0','SPI1_CS_N':'PA4_SPI_NSS','SPI1_SCK':'PA5_SPI_SCK',
 'SPI1_MISO':'PA6_SPI_MISO','SPI1_MOSI':'PA7_SPI_MOSI','UART1_TX':'PA9_UART_TX','UART1_RX':'PA10_UART_RX',
 'I2C1_SCL':'I2C_SCL','I2C1_SDA':'I2C_SDA','USB_DM':'PA11_SHARED','USB_DP':'PA12_SHARED'}
models={};components=[];counts=Counter()
def model(key,footprint,pins,source='Project-specified teaching component, procurement not released'):
    if key in models:return key
    records=[]
    for num,data in pins.items():
        name,kind=data
        records.append(dict(number=str(num),name=name,type=types.get(kind,4),library_nc=(kind=='NC')))
    half=(len(records)+1)//2; width=240 if len(records)>2 else 80
    height=max(40,(half+1)*20)
    for i,pin in enumerate(records):
        left=i<half; y=20*(i+1 if left else i-half+1)
        pin.update(start=[0 if left else width,y],hot=[-20 if left else width+20,y],side='left' if left else 'right')
    models[key]=dict(name='DE_'+re.sub('[^A-Za-z0-9_]','_',key)[:26],footprint=footprint,pins=records,width=width,height=height,source=source)
    return key
def add(id,kind,value,pins,page,footprint=None,mpn='',populate='yes',**props):
    prefix='U' if id.startswith('U_') else id.split('_')[0][0]
    counts[prefix]+=1;ref=prefix+str(counts[prefix])
    components.append(dict(id=id,ref=ref,model=kind,value=value,mpn=mpn,page=page,pins={str(k):v for k,v in pins.items()},populate=populate,properties=props))
    return components[-1]
model('STM32F103C8T6','l09_stm32f103c8_lqfp48', {str(p['number']):(p['name'],p['symbol_electrical_type']) for p in mcu['pins']},'ST DS5319 Rev20 Figure8/Table5')
add('U_MCU','STM32F103C8T6','STM32F103C8T6',{p['number']:aliases.get(p['proposed_net'],p['proposed_net']) for p in mcu['pins']},'MCU_SUPPLY',mpn='STM32F103C8T6')
fp={'TPS54202DDCR':'sot23-6','TLV75533PDBVR':'sot23-5','TCAN332DR':'so8','USBLC6-2SC6':'sot23-6',
    '2N7002':'sot23-3','DMP2035U-7':'sot23-3','SS14-E3/61T':'do-214ac_sma',
    'USB4105-GF-A':'l10_gct_usb4105_gf_a_12land','XAL6060-153MEC':'de_xal6060_2land'}
for key,p in power['parts'].items():
    model(key,fp[key],p['pins'],p['source'])
for n in (2,3,4,6,8):model('HEADER'+str(n),f'pin{n:02d}_2d54MM_1x{n}',{str(i):(str(i),'PASSIVE') for i in range(1,n+1)})
for kind,foot in (('RES','0603'),('RES1206','1206'),('CAP','0603'),('CAP0805','0805'),('CAP1206','1206'),('FUSE','0603'),('CAP_POL','de_capradial_6d3_p2d5')):
    model(kind,foot,{'1':('P' if kind=='CAP_POL' else '1','PASSIVE'),'2':('N' if kind=='CAP_POL' else '2','PASSIVE')})
model('XTAL_ABM3B','de_abm3b_5032',{'1':('X1','PASSIVE'),'2':('GND2','PASSIVE'),'3':('X2','PASSIVE'),'4':('GND4','PASSIVE')},'Abracon ABM3B RevU PDF3')
for c in power['components']:
    k=c['kind']
    if k=='INDUCTOR':k='XAL6060-153MEC'
    if k=='RES' and c['ref']=='R_CAN_TERM':k='RES1206'
    if k=='CAP':
        if c['value'].startswith('22uF'):k='CAP1206'
        elif c['value'].startswith(('2.2uF','4.7uF')):k='CAP0805'
    val=c['value'].split()[0] if k.startswith(('RES','CAP','FUSE','HEADER')) else c['value']
    add(c['ref'],k,val,c['pins'],c['page'],mpn=c.get('mpn',c['kind'] if c['kind'] in power['parts'] else ''),
        populate=c['populate'],source_description=c['value'],requirements=c.get('rating',''),layout=c.get('layout',''),
        nc_reason=c.get('nc_reason',{}),assembly_group=c.get('assembly_group',''))
def passive(id,value,a,b,page='MCU_SUPPLY',kind='CAP',**extra):return add(id,kind,value,{'1':a,'2':b},page,**extra)
for n in (24,36,48):passive('C_VDD'+str(n),'100nF','V3V3','GND',requirements='X7R >=10V; own pin-local return loop at VDD'+str(n))
passive('C_MCU_BULK','10uF','V3V3','GND',kind='CAP0805',requirements='Effective >=4.7uF; at VDD3 pin48 per DS5319 Figure14')
passive('C_VBAT','100nF','V3V3','GND',requirements='No battery; VBAT1 tied to V3V3, local capacitor')
passive('R_VDDA_LINK','0R','V3V3','VDDA',kind='RES',requirements='Default zero-ohm link; no automatic ferrite substitution; continuous GND')
for id,val,kind in [('C_VDDA_HF','10nF','CAP'),('C_VDDA_MID','100nF','CAP'),('C_VDDA_BULK','2.2uF','CAP0805')]:
    passive(id,val,'VDDA','GND',kind=kind,requirements='Local VDDA9/VSSA8 loop; bulk effective>=1uF')
passive('R_NRST','10k','V3V3','NRST','CLOCK_RESET','RES',requirements='External optional pull-up; internal pull-up remains')
passive('C_NRST','100nF','NRST','GND','CLOCK_RESET',requirements='Does not guarantee reset release delay; debugger must sink reset')
add('J_RESET','HEADER2','RESET_SHUNT',{'1':'NRST','2':'GND'},'CLOCK_RESET',requirements='Normally open service shunt; >=20us low; not pushbutton footprint')
passive('R_BOOT0_PD','10k','BOOT0','GND','CLOCK_RESET','RES')
passive('R_BOOT1_PD','10k','BOOT1','GND','CLOCK_RESET','RES')
passive('R_BOOT_SERVICE','1k','V3V3','BOOT_SERVICE','CLOCK_RESET','RES')
add('J_BOOT','HEADER2','BOOT0_SERVICE',{'1':'BOOT_SERVICE','2':'BOOT0'},'CLOCK_RESET',requirements='Open=flash default; short with BOOT1 low=USART1 ROM loader; no USB ROM DFU')
add('J_SWD','HEADER6','SWD_LOCAL_1X6',{'1':'V3V3','2':'GND','3':'SWDIO','4':'SWCLK','5':'NRST','6':'SWO'},'CLOCK_RESET',requirements='Local labelled 2.54mm header, not standard keyed ARM10; pin1 VTREF output/sense only; no back-power')
add('Y_HSE','XTAL_ABM3B','8MHz',{'1':'OSC_IN','2':'GND','3':'XTAL_OUT','4':'GND'},'CLOCK_RESET',mpn='ABM3B-8.000MHZ-D2Y-T')
passive('R_HSE_SER','0R','OSC_OUT','XTAL_OUT','CLOCK_RESET','RES',requirements='Drive-level tuning position; do not raise without startup/drive measurement')
passive('C_HSE_IN','16pF','OSC_IN','GND','CLOCK_RESET',requirements='C0G +/-5%; stray10pF assumption, prototype tuning required')
passive('C_HSE_OUT','16pF','XTAL_OUT','GND','CLOCK_RESET',requirements='Same as C_HSE_IN')
add('J_ADC','HEADER2','ADC_0_TO_3V0',{'1':'ADC_IN','2':'GND'},'ADC_GPIO',requirements='Only controlled <=1Hz 0..3.0V source, Rout<=1k, board powered, no hotplug/negative input')
passive('R_ADC','1k','ADC_IN','ADC0','ADC_GPIO','RES')
passive('C_ADC','100nF','ADC0','GND','ADC_GPIO',requirements='X7R >=10V, low-frequency source only; not 100Sps anti-alias filter')
spares=[['GPIO_PC13','GPIO_PC14','GPIO_PC15','GPIO_PA1','GPIO_PA2','GPIO_PA3'],
 ['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14'],
 ['GPIO_PB15','GPIO_PA15','GPIO_PB4','GPIO_PB5','GPIO_PB8','GPIO_PB9']]
for n,nets in enumerate(spares,1):
    add('J_GPIO'+str(n),'HEADER8','GPIO_3V3',dict(zip(map(str,range(1,9)),['V3V3','GND']+nets)),'ADC_GPIO',requirements='3.3V logic only, combined header load<=10mA; PA15/PB4 require JTAG disabled with SWD kept; PC13-15 limited drive')
# Source kind may leave headers or passives marked as NC; only actual device NC is library NC.
for key in ('USB4105-GF-A',):
    for p in models[key]['pins']:
        if p['number'] in ('A8','B8'):p['library_nc']=False
for c in components:
    assert c['model'] in models,c
    expected={p['number'] for p in models[c['model']]['pins']}
    assert set(c['pins'])==expected,(c['id'],expected,set(c['pins']))
    c['properties']['MODULE_ID']=c['id']
    c['properties']['ASSEMBLY']=c['populate']
    c['properties']['MPN_STATUS']='REAL_PART' if c['mpn'] else 'SPEC_ONLY_PROCUREMENT_PENDING'
    c['properties']['REQUIREMENTS']=c['properties'].get('requirements','')
    c['properties']['Manufacturer Part Number']=c['mpn']
    c['properties']={k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else str(v) for k,v in c['properties'].items()}
pages=sorted({c['page'] for c in components})
page_nets=defaultdict(set)
for c in components:
    for n in c['pins'].values():
        if n:page_nets[n].add(c['page'])
spec=dict(schema='DE_integrated_circuit_v1',date='2026-10-19 Asia/Shanghai',status='CAD_LEARNING_NOT_FABRICATION_RELEASE',
 source_hashes={n:hashlib.sha256((base/n).read_bytes()).hexdigest() for n in ('mcu_spec.json','power_interface_spec.json')},
 models=models,components=components,pages=pages,cross_page_nets={n:sorted(p) for n,p in page_nets.items() if len(p)>1},
 assembly_profiles=power['assembly_profiles'],constraints=power['supply_limits'],footprint_policies={'unselected_passives':'Explicit electrical specifications plus teaching geometry; exact MPN and DC-bias/thermal/mechanical review pending'},
 schematic_style='Visible pins and labelled short wires; explicit off-page connector for each shared page net; no hidden power assumptions')
(base/'integrated_circuit.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
with (base/'BOM_baseline.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['Reference','Module_ID','Value','MPN','Footprint','Assembly','Page','Requirements'])
    for c in components:w.writerow([c['ref'],c['id'],c['value'],c['mpn'],models[c['model']]['footprint'],c['populate'],c['page'],c['properties']['REQUIREMENTS']])
def q(v):
    return '"'+str(v).replace('\\','\\\\').replace('"','\\"').replace('$','\\$').replace('[','\\[').replace(']','\\]').replace('\n','\\n')+'"'
def expr(v):
    if isinstance(v,dict):return '[dict create '+' '.join(q(k)+' '+expr(x) for k,x in v.items())+']'
    if isinstance(v,list):return '[list '+' '.join(expr(x) for x in v)+']'
    if v is None:return q('')
    if isinstance(v,bool):return '1' if v else '0'
    return q(v)
target=root/'staging/de_15_26_20261019/integrated_spec.tcl';target.parent.mkdir(parents=True,exist_ok=True)
target.write_text('set ::DEspec '+expr(spec)+'\n',encoding='utf-8')
print(json.dumps(dict(components=len(components),models=len(models),pages=pages,logical_ids={c['id']:c['ref'] for c in components},spec=str(base/'integrated_circuit.json')),ensure_ascii=True))
