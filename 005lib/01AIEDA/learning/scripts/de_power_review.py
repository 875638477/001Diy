"""Independent pre-CAD critical-net review; does not assert Capture/ERC/PCB success."""
from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parents[1]
example=root/'examples'/'de_15_26_20261019'
p=example/'power_interface_spec.json'; spec=json.loads(p.read_text(encoding='utf-8'))
byref={c['ref']:c for c in spec['components']}; checks=[]
def ck(name,got,expected): checks.append({'check':name,'actual':got,'expected':expected,'pass':got==expected})
ck('unique_reference_designators',len(byref),len(spec['components']))
# Cross-check literal vendor pin names, independently transcribed from source pin tables.
vendor={
 'TPS54202DDCR':['GND','SW','VIN','FB','EN','BOOT'],
 'TLV75533PDBVR':['IN','GND','EN','NC','OUT'],
 'TCAN332DR':['TXD','GND','VCC','RXD','NC5','CANL','CANH','NC8'],
 '2N7002':['G','S','D'],
 'DMP2035U-7':['G','S','D'],
 'USBLC6-2SC6':['IO1A','GND','IO2A','IO2B','VBUS','IO1B'],
}
for kind,pins in vendor.items():
 ck('vendor_pin_names_'+kind,[spec['parts'][kind]['pins'][str(i+1)][0] for i in range(len(pins))],pins)
for ref,pins in {
 'U_BUCK':{'1':'GND','2':'BUCK_SW','3':'VIN_PROT','4':'BUCK_FB','5':None,'6':'BUCK_BOOT'},
 'U_LDO':{'1':'V5','2':'GND','3':'V5','4':None,'5':'V3V3'},
 'U_CAN':{'1':'CAN_TXD','2':'GND','3':'V3V3','4':'CAN_RXD','5':None,'6':'CAN_L','7':'CAN_H','8':None},
 'Q_VBUS':{'1':'VBUS_GATE','2':'GND','3':'VBUS_PRESENT_N'},
 'Q_ATTACH':{'1':'USB_ATTACH_N','2':'V3V3','3':'USB_PULLUP_SRC'},
 'U_USB_ESD':{'1':'USB_DP','2':'GND','3':'USB_DM','4':'USB_DM','5':'USB_VBUS','6':'USB_DP'},
 'D_REV':{'1':'VIN_PROT','2':'VIN_FUSED'},
}.items(): ck('critical_net_'+ref,byref[ref]['pins'],pins)
ck('bootstrap_is_between_BOOT_and_SW',set(byref['C_BOOT']['pins'].values()),{'BUCK_BOOT','BUCK_SW'})
ck('cc1_dedicated_Rd',set(byref['R_CC1']['pins'].values()),{'USB_CC1','GND'})
ck('cc2_dedicated_Rd',set(byref['R_CC2']['pins'].values()),{'USB_CC2','GND'})
ck('SBU_explicit_NC',[byref['J_USB']['pins']['A8'],byref['J_USB']['pins']['B8']],[None,None])
ck('VBUS_gate_R_is10k',byref['R_VBUS_GATE']['value'],'10k 1%')
ck('VBUS_net_only_expected_endpoints',sorted(c['ref'] for c in byref.values() if 'USB_VBUS' in c['pins'].values()),sorted(['J_USB','U_USB_ESD','C_USB_VBUS','R_VBUS_GATE']))
ck('I2C_open_drain_pullups_identical',[byref['R_I2C_SCL']['value'],byref['R_I2C_SDA']['value']],['2.2k 1%','2.2k 1%'])
ck('inductor_real_MPN',byref['L_BUCK']['kind'],'XAL6060-153MEC')
ck('inductor_shortlead_1_is_SW',byref['L_BUCK']['pins']['1'],'BUCK_SW')
for profile,cfg in spec['assembly_profiles'].items():
 fit=set(cfg['fit']); omitted=set(cfg['DNP'])
 ck(profile+'_profile_fit_DNP_disjoint',sorted(fit & omitted),[])
 ck(profile+'_selects_exactly_one_driver_path',sorted(fit|omitted),sorted(['R_USB_DP','R_USB_DM','R_CAN_TX','R_CAN_RX']))
 parent={}
 def find(x):
  parent.setdefault(x,x)
  if parent[x]!=x: parent[x]=find(parent[x])
  return parent[x]
 def join(a,b): parent[find(a)]=find(b)
 for c in byref.values():
  if c['ref'] in omitted: continue
  if c['kind']=='RES' and c['value'].split()[0] in {'0R','22R','33R'}:
   join(*c['pins'].values())
 same=lambda a,b:find(a)==find(b)
 ck(profile+'_PA12_USB_path',same('PA12_SHARED','USB_DP'),profile=='USB')
 ck(profile+'_PA11_USB_path',same('PA11_SHARED','USB_DM'),profile=='USB')
 ck(profile+'_PA12_CAN_path',same('PA12_SHARED','CAN_TXD'),profile=='CAN')
 ck(profile+'_PA11_CAN_path',same('PA11_SHARED','CAN_RXD'),profile=='CAN')
 ck(profile+'_VBUS_not_power_short',same('USB_VBUS','V5'),False)
ck('buck_static_max_below_LDO_5V5',spec['calculations']['buck_V_max']<5.5,True)
ck('I2C_R2k2_within_limits',spec['calculations']['i2c_Rmin_3mA_3V465_0V4_ohm']<2178<2222<spec['calculations']['i2c_Rmax_300ns_100pF_ohm'],True)
ck('VBUS_gate_min_above_spec4V5',spec['calculations']['vbus_gate_at4V75_V']>4.5,True)
result={'scope':'independent critical electrical spec review, no native CAD/ERC/hardware claim','source_spec_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'count':len(checks),'pass_count':sum(c['pass'] for c in checks),'checks':checks}
# Sets are for human-readable unordered net membership checks.
def enc(o):
 if isinstance(o,set): return sorted(o)
 raise TypeError(type(o).__name__)
(example/'power_interface_review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=enc),encoding='utf-8')
files=[]
for q in sorted((root/'sources'/'de_15_26_20261019').glob('*.pdf')):
 files.append({'file':q.name,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
(root/'staging'/'de_15_26_20261019'/'power_sources'/'local_pdf_hashes.json').write_text(json.dumps(files,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{result["pass_count"]}/{result["count"]} critical checks passed')
if result['pass_count']!=result['count']: raise SystemExit(1)
