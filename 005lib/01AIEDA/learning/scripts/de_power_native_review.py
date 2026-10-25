"""Read-only review from native reopened TSV, independently against power source spec.
Does not call Cadence, change design, or promote electrical spec checks to ERC/hardware proof.
"""
from pathlib import Path
import csv,json,hashlib,math
root=Path(__file__).resolve().parents[1]; logs=root/'logs'/'de_15_26_20261019'; ex=root/'examples'/'de_15_26_20261019'
power=json.loads((ex/'power_interface_spec.json').read_text(encoding='utf-8'))
checks=[]
def check(label,got,want,**kw): checks.append(dict(check=label,actual=got,expected=want,passed=got==want,**kw))
def rows(p): return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''),delimiter='\t'))
authority={
 'U_BUCK':{'1':'GND','2':'SW','3':'VIN','4':'FB','5':'EN','6':'BOOT'},
 'U_LDO':{'1':'IN','2':'GND','3':'EN','4':'NC','5':'OUT'},
 'U_CAN':{'1':'TXD','2':'GND','3':'VCC','4':'RXD','5':'NC5','6':'CANL','7':'CANH','8':'NC8'},
 'Q_VBUS':{'1':'G','2':'S','3':'D'},'Q_ATTACH':{'1':'G','2':'S','3':'D'},
 'U_USB_ESD':{'1':'IO1A','2':'GND','3':'IO2A','4':'IO2B','5':'VBUS','6':'IO1B'},
}
versions={}
for version in ['single','eco']:
 inst=rows(logs/f'instances_{version}.tsv'); pins=rows(logs/f'pins_{version}.tsv'); conn=rows(logs/f'connectivity_{version}.tsv')
 props={(r['reference'],r['property']):r['value'] for r in rows(logs/f'properties_{version}.tsv')}
 byid={r['module_id']:r for r in inst}; pinmap={(r['reference'],r['number']):r for r in pins}; netmap={}
 for r in conn: netmap.setdefault((r['reference'],r['number']),[]).append(r['net'])
 subset=[]
 for c in power['components']:
  cid=c['ref']; i=byid.get(cid); check(f'{version}/{cid}/one_native_instance',sum(r['module_id']==cid for r in inst),1)
  if i is None: continue
  ref=i['reference']; actualnumbers=sorted(k[1] for k in pinmap if k[0]==ref)
  check(f'{version}/{cid}/physical_pin_numbers',actualnumbers,sorted(c['pins']))
  for number,expectednet in c['pins'].items():
   key=(ref,number); pr=pinmap[key]; actualnet=netmap.get(key,[])
   check(f'{version}/{cid}.{number}/native_net',actualnet,[] if expectednet is None else [expectednet])
   check(f'{version}/{cid}.{number}/NC_flag',pr['nc'],'1' if expectednet is None else '0')
   if cid in authority: check(f'{version}/{cid}.{number}/vendor_pin_name',pr['name'],authority[cid][number])
  subset.append({'module_id':cid,'reference':ref,'pins':{num:netmap.get((ref,num),[]) for num in c['pins']},'native_value':i['value'],'footprint':i['footprint'],'mpn':i['mpn']})
  if c['kind'] in power['parts']:
   expectedmpn=c.get('mpn',c['kind'])
   check(f'{version}/{cid}/MPN',i['mpn'],expectedmpn)
 for cid,value in {'R_VBUS_GATE':'10k','R_VBUS_GPD':'1M','R_VBUS_READ':'10k','R_ATTACH_OFF':'100k','R_DP_PULLUP':'1.5k','R_CC1':'5.1k','R_CC2':'5.1k','R_CAN_TX_IDLE':'10k','R_FB_HI':'100k','R_FB_LO':'13.5k','R_I2C_SCL':'3.3k' if version=='eco' else '2.2k','R_I2C_SDA':'3.3k' if version=='eco' else '2.2k'}.items():
  check(f'{version}/{cid}/critical_value',byid[cid]['value'],value)
 # MCU nets are independently grounded in the actual F103 LQFP48 physical pin map.
 mref=byid['U_MCU']['reference']
 for n,name in {'18':'VBUS_PRESENT_N','29':'USB_ATTACH_N','30':'PA9_UART_TX','31':'PA10_UART_RX','32':'PA11_SHARED','33':'PA12_SHARED','14':'PA4_SPI_NSS','15':'PA5_SPI_SCK','16':'PA6_SPI_MISO','17':'PA7_SPI_MOSI','42':'I2C_SCL','43':'I2C_SDA'}.items():
  check(f'{version}/MCU_physical{n}/interface_net',netmap[(mref,n)],[name])
 # Assembly/limits/source specification are now actual native property readback as well as BOM.
 bom=list(csv.DictReader((ex/('BOM_eco.csv' if version=='eco' else 'BOM_baseline.csv')).open(encoding='utf-8-sig',newline='')))
 bmap={r['Module_ID']:r for r in bom}
 for cid,state in {'R_USB_DP':'yes','R_USB_DM':'yes','R_CAN_TX':'DNP default USB mode','R_CAN_RX':'DNP default USB mode'}.items():
  check(f'{version}/{cid}/BOM_default_USB_assembly',bmap[cid]['Assembly'],state,evidence='BOM export')
 for c in power['components']:
  cid=c['ref'];ref=byid[cid]['reference']
  check(f'{version}/{cid}/native_saved_ASSEMBLY',props[(ref,'ASSEMBLY')],c['populate'])
  check(f'{version}/{cid}/native_saved_assembly_group',props[(ref,'assembly_group')],c.get('assembly_group',''))
  expectedsourcedesc='3.3k 1%' if version=='eco' and cid in ['R_I2C_SCL','R_I2C_SDA'] else c['value']
  check(f'{version}/{cid}/native_saved_source_description',props[(ref,'source_description')],expectedsourcedesc)
  check(f'{version}/{cid}/native_saved_REQUIREMENTS',props[(ref,'REQUIREMENTS')],c.get('rating',''))
  expectedstatus='REAL_PART' if c.get('mpn') or c['kind'] in power['parts'] else 'SPEC_ONLY_PROCUREMENT_PENDING'
  check(f'{version}/{cid}/native_saved_MPN_STATUS',props[(ref,'MPN_STATUS')],expectedstatus)
  expectedbomspec=c['value']
  if version=='eco' and cid in ['R_I2C_SCL','R_I2C_SDA']: expectedbomspec='3.3k 1%'
  check(f'{version}/{cid}/BOM_full_electrical_spec',bmap[cid]['Specification'],expectedbomspec)
 for cid in ['R_I2C_SCL','R_I2C_SDA']:
  ref=byid[cid]['reference']
  reason=props[(ref,'ECO_REASON')]
  check(f'{version}/{cid}/native_ECO_reason',reason.replace(' ',''), 'I2Cpullupchange;risetimerecheckedat100pF' if version=='eco' else '__ABSENT__',raw=reason)
 for prof,cfg in power['assembly_profiles'].items():
  omitted=set(cfg['DNP']); parent={}
  def find(n):
   parent.setdefault(n,n)
   if parent[n]!=n:parent[n]=find(parent[n])
   return parent[n]
  def union(a,b): parent[find(a)]=find(b)
  for c in power['components']:
   if c['ref'] in omitted:continue
   r=byid[c['ref']]
   if c['kind']=='RES' and r['value'] in {'0R','22R','33R'}:
    ends=[netmap[(r['reference'],n)][0] for n in ['1','2']];union(*ends)
  for lhs,rhs,want in [('PA12_SHARED','USB_DP',prof=='USB'),('PA11_SHARED','USB_DM',prof=='USB'),('PA12_SHARED','CAN_TXD',prof=='CAN'),('PA11_SHARED','CAN_RXD',prof=='CAN')]:
   check(f'{version}/{prof}/assembled_path/{lhs}_to_{rhs}',find(lhs)==find(rhs),want,evidence='native nets plus specified assembly profile')
 versions[version]={'instances_total':len(inst),'physical_pins_total':len(pins),'connected_pin_records_total':len(conn),'nets_total':len(set(r['net'] for r in conn)),'reviewed_power_components':len(subset),'reviewed_power_pin_count':sum(len(s['pins']) for s in subset),'subset':subset}

# Engineering review: ECO 3.3k retains margin only if the stated 100pF ceiling holds.
rhi=3300*1.01; cb=100e-12; rise=.8473*rhi*cb
check('ECO_I2C_worst_resistor_100pF_tr_below300ns',rise<=300e-9,True)
check('VBUS_min4V75_gate_R10k_Rpd1M_above4V5',4.75*(1e6*.99)/(1e6*.99+10000*1.01)>4.5,True)
check('final_normal_current_budget_allocation_below150mA',power['normal_current_budget_mA']['allocated_subtotal']<power['supply_limits']['V3V3_load_max_A']*1000,True)
check('final_GPIO_plus_header_external_ceiling10mA',power['supply_limits']['external_GPIO_plus_header_load_max_A'],.010)
check('final_ambient_0to40C',power['supply_limits']['ambient_C'],[0,40])
findings=[
 {'severity':'scope','topic':'Raw connectivity includes DNP components','finding':'The saved schematic carries all four USB/CAN selector resistors. Exclusivity is an assembly requirement, independently checked using BOM/profile masks; raw netlist alone does not electrically isolate an incorrectly assembled board.'},
 {'severity':'resolved','topic':'Full electrical specifications in BOM','finding':'Initial review found normalized BOM Value dropped tolerance/voltage/dielectric. Root fixed export with Specification, Procurement_Status and Requirements, then removed duplicate L1/J2 suffixes. Actual native property readback checks all52 power parts in both versions for source_description, ASSEMBLY, group, limits and procurement status. ECO I2C current Value=3.3k, source_description=3.3k1%, ECO_REASON and BOM Specification=3.3k1% state revised assembly; original power spec and baseline preserve2.2k history.'},
 {'severity':'release_gap','topic':'Exact passives and effective capacitance','finding':'Most capacitor/connector MPNs remain unspecified. Effective Buck input/output and LDO capacitance, PCB thermal behavior, loop stability and inrush/fuse coordination have not been measured.'},
 {'severity':'scope','topic':'LDO reverse feed and input protection','finding':'TLV755 is not reverse-blocking. Normal power nets are correct but reverse external header/SWD powering is forbidden, rapid input collapse remains a hardware test; F_IN+SS14 handles specified overcurrent/reversal and does not certify surge/OVP.'},
 {'severity':'resolved_with_scope','topic':'Normal current budget and LDO thermal boundary','finding':'Initial120mA had no reserve after MCU50mA+CAN60mA+external10mA. Final controlled normal ceiling150mA and ambient0-40C accepted; GPIO plus header external draw is combined <=10mA. Allocated136.2mA includes bias/I2C/analog/switching reserves, leaving13.8mA. LDO first-order worst P=.284323W, deltaT65.707C, Tj105.707C at40C using JEDEC231.1C/W; actual PCB thermal validation remains required. Native L1 REQUIREMENTS retains historical covers nominal120mA text; real Isat5.8A/Irms4.5A ratings unchanged, not a120mA inductor limit. CAN bus-fault180mA is outside normal current guarantee.'},
 {'severity':'scope','topic':'VBUS and self-powered USB behavior','finding':'2N7002 gate10k/1M is read back correctly; resistance-guarantee calculation assumes VBUS at connector >=4.75V. Firmware PB0 sense and PA8 attach timing, lower-VBUS operation and powered-off DP/DM behavior are untested.'},
 {'severity':'scope','topic':'CAN 332 pin/function identity','finding':'Pin5 and pin8 correctly NC; no standby control exists. Internal+external TXD pull-up establishes recessive while disconnected. Short bench use and device-level ESD ratings do not imply automotive bus-fault or board-level surge/ESD compliance.'},
 {'severity':'scope','topic':'I2C rate and inconsistent manufacturer footnote','finding':'Default teaching speed is100kHz. DS5319 Rev20 Table41 footnote2 PDF68 says PCLK1 must be a multiple of10MHz for400kHz, while Table42 PDF69 presents36MHz and400kHz/CCR0x801E. Both pages were independently text-read and visually inspected. The calculated282.405ns ECO RC rise at100pF proves only a300ns RC budget, not all MCU Fast-mode timing or hardware operation. <=400kHz on the CAD interface is an upper design envelope, not a passed400kHz runtime claim.'},
]
result={'date':'2026-10-19 Asia/Shanghai','scope':'Independent read-only native TSV review against original power_interface_spec and vendor pin tables; no Cadence API calls','result':'PASS_WITH_DOCUMENTED_RELEASE_GAPS' if all(c['passed'] for c in checks) else 'FAIL','checked':len(checks),'passed':sum(c['passed'] for c in checks),'engineering_metrics':{'I2C_default_teaching_rate_Hz':100000,'ECO_I2C_Rmax_1pct_ohm':rhi,'ECO_I2C_tr_100pF_ns':rise*1e9,'ECO_I2C_Cmax_300ns_pF':300e-9/(.8473*rhi)*1e12,'final_normal_supply_limit_A':.150,'external_GPIO_plus_header_combined_ceiling_A':.010,'normal_current_allocation_mA':136.2,'remaining_margin_mA':13.8,'LDO_power_worst_5V146_3V2505_150mA_W':(5.145986838690542-3.2505)*.15,'LDO_JEDEC_deltaT_C':(5.145986838690542-3.2505)*.15*231.1,'LDO_first_order_Tj_at40C_C':40+(5.145986838690542-3.2505)*.15*231.1},'checks':checks,'versions':versions,'findings':findings,'evidence_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ex/'power_interface_spec.json',*[logs/f'{prefix}_{ver}.tsv' for prefix in ['instances','pins','connectivity','properties'] for ver in ['single','eco']],ex/'BOM_baseline.csv',ex/'BOM_eco.csv',root/'sources/de_15_26_20261019/DS5319.pdf']}}
(logs/'power_native_review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'result':result['result'],'checks':result['checked'],'passed':result['passed'],'metrics':result['engineering_metrics'],'failures':[c for c in checks if not c['passed']]},ensure_ascii=False,indent=2))
