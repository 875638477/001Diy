import pathlib,json,sys
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from routing_geometry import load,LineString,Polygon
# This policy is for ordinary candidates. All geometry is exported explicitly and still requires native validation.
base=load(R/'plans/ordinary_routing_policy_v0.json');mcu=load(R/'engineering_mcu/plans/mcu_critical_routes_v6.json')
for variant in ('2L','4L'):
 d=json.loads(json.dumps(base));d['status']='CONSTRAINED_ORDINARY_POLICY_V1_MCU6';d['variant']=variant
 d['bottomCost']=2.0 if variant=='2L' else 1.25;d['viaCostMM']=15. if variant=='2L' else 7.
 d['manualOnlyNets']=sorted(set(d['manualOnlyNets']+['GPIO_PC13','GPIO_PC14','GPIO_PC15']))
 d['reservedAreas']=[a for a in d['reservedAreas'] if a['id']!='HSE_PLANNING_ENVELOPE']
 moat=mcu['oscillatorReference']['applicationGroundVoidPolygon']
 d['reservedAreas'].append({'id':'HSE_ACTUAL_MOAT_AND_STEM','polygon':moat,'layers':['TOP','BOTTOM'],'allowedNets':['OSC_IN','OSC_OUT','XTAL_OUT','GND'],'basis':'Executed MCU6 quiet island and sole reference anchor. No ordinary traversal or stitches.'})
 d['noGlobalGroundViaAreas']=[moat,[[36.45,36.05],[48.2,36.05],[48.2,40.45],[36.45,40.45]]]
 # Prevent new ordinary bottom slots directly below the critical top analogue path; upper SPI route remains available.
 for o in mcu['operations']:
  if o['type']=='route' and o['net'] in ('ADC0','ADC_IN'):
   p=LineString(o['points']).buffer(.65,quad_segs=8)
   d['reservedAreas'].append({'id':'ADC_REFERENCE_'+o['id'],'polygon':list(map(list,p.exterior.coords)),'layers':['BOTTOM'],'allowedNets':['GND','ADC0','ADC_IN'],'basis':'Protect actual bottom reference below the short sensitive TOP ADC path.'})
 # Native north region copies modify only finepitch pin/line spacing for the listed classes.
 north=mcu['regions'][0]['polygon']
 d['regionOverrides'].append({'id':'HI_MCU_NORTH_ESCAPE','polygon':north,'layer':'TOP','nets':['GND','V3V3','VDDA','ADC0','ADC_IN','NRST','OSC_IN','OSC_OUT','XTAL_OUT'],'kinds':['smdpin','line'],'gap':.2,'basis':'Match executed MCU6 finite north spacing override; no via/other-spacing waiver.'})
 # Reserve the USB trunk and MCU source entrance while its own batch is being validated.
 d['reservedAreas'].append({'id':'USB_TRUNK','polygon':[[38.0,7.9],[42.6,7.9],[42.6,18.0],[38,18.0]],'layers':['TOP','BOTTOM'],'allowedNets':['USB_DP','USB_DM','USB_VBUS','GND'],'basis':'Keep ordinary signals away from protected USB trunk and its opposite-layer reference.'})
 d['pendingOperations']=[]
 for name in ('gpio_north_escape_v3.json','usb_critical_routes_v6.json'):
  p=load(R/'engineering_mcu/plans'/name)
  d['pendingOperations']+=p.get('operations',[])+p.get('commonOperations',[])+p.get('variantOperations',{}).get(variant,[])
 d['scope']='Candidate search only. Actual dynamic plane, all region/class interactions, native DRC, graph and return geometry remain required. Future literal critical paths are temporary obstacles, never treated as electrically executed.'
 (R/'plans'/('ordinary_policy_'+variant+'_v1.json')).write_text(json.dumps(d,indent=2),encoding='utf8')
p=R/'scripts/plan_signal_paths.py';s=p.read_text(encoding='utf8')
s=s.replace("assert snapshot['readbackDirectory']==networks.get('nativeLog',networks.get('readback')),'Do not combine different native checkpoints'", "assert snapshot['readbackDirectory']==networks.get('nativeLog',networks.get('readback')),'Do not combine different native checkpoints'\nfor pending in policy.get('pendingOperations',[]):scene.add_operation(pending)")
p.write_text(s,encoding='utf8');print('Prepared conservative policies for2L/4L ordinary paths')