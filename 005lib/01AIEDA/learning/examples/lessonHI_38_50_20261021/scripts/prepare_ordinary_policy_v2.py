import pathlib,json,sys,hashlib
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scripts'))
from routing_geometry import load,LineString
profiles=load(R/'engineering_power/rules_profile_2L_69nets.json');groups={g['id'].removeprefix('HI2L_'):g['nets'] for g in profiles['groups']}
paths=['engineering_mcu/plans/gpio_north_escape_v3.json','engineering_mcu/plans/usb_critical_routes_v8.json','engineering_power/ESD_ground_routes_04c.json','engineering_power/STAR_reroute_07b.json','engineering_power/V3_peripheral_distribution_06b.json','engineering_power/interface_CAN_routes_04.json','engineering_power/CAN_local_supply_05.json']
for variant in ['2L','4L']:
 d=load(R/'plans'/('ordinary_policy_'+variant+'_v1.json'));d['status']='ORDINARY_POLICY_V2_CRITICAL_REWORK_EXPLICIT_PENDING'
 d['pendingOperations']=[];d['pendingDeleteSegments']=[];d['sourcePlans']=[]
 for path in paths:
  p=load(R/path);ops=p.get('operations',[])+p.get('commonOperations',[])+p.get('variantOperations',{}).get(variant,[])
  d['pendingDeleteSegments'] += [o for o in ops if o['type']=='deleteSegment']
  d['pendingOperations'] += [o for o in ops if o['type']!='deleteSegment']
  d['sourcePlans'].append({'path':path,'sha256':hashlib.sha256((R/path).read_bytes()).hexdigest()})
 usb=load(R/paths[1]);fs=groups['USB_FS']
 if variant=='2L':
  d['netPairSpacing']=[{'netsA':groups[x['a']],'netsB':groups[x['b']],'gap':x['spacing_mm']} for x in profiles['classClass']]
  digital=sum([groups[g] for g in ['GPIO','RESET_BOOT_SWD','SPI','UART_CAN_DIGITAL','I2C','USB_AUX']],[])
 else:
  br=load(R/'inventory/checkpoints/mcu_4L_b006/base_net_rules.json')['rules'];digital=sorted({r['net'] for r in br if r['spacingClass']=='NC_DIGITAL_GENERAL_S'})
  d['netPairSpacing']=[{'netsA':fs,'netsB':digital,'gap':.5},{'netsA':groups['SWITCH'],'netsB':groups['ADC']+groups['OSCILLATOR']+fs,'gap':1.}]
 d['regionOverrides'].append({'id':'HI_USB_MCU_ESCAPE','layer':'TOP','polygon':[[39.8,21.2],[41.6,21.2],[41.6,23.4],[39.8,23.4]],'netPairs':[[a,b] for a in fs for b in digital],'kinds':['smdpin','line'],'gap':.2,'basis':'Finite native USB to ordinary digital Class-Class escape; outside .5 retained; native geometry check required.'})
 for o in usb['commonOperations']+usb['variantOperations'][variant]:
  if o['type']=='route' and o['net'] in ('PA11_SHARED','PA12_SHARED') and o['layer']=='TOP':
   g=LineString(o['points']).buffer(.5,quad_segs=8)
   d['reservedAreas'].append({'id':'USB_SHARED_REFERENCE_'+o['id'],'polygon':list(map(list,g.exterior.coords)),'layers':['BOTTOM'],'allowedNets':fs+['GND'],'basis':'No ordinary BOTTOM slot through the TOP shared USB reference corridor.'})
 d['routeWindows']=[{'nets':['SPI_SCK','SPI_MOSI','SPI_NSS','SPI_MISO'],'layers':['TOP','BOTTOM'],'polygon':[[6,25.8],[33.5,25.8],[33.5,37.8],[6,37.8]],'basis':'Reject unreasonably long detours around the switching stage; revise copper/layout if this corridor fails.'}]
 (R/'plans'/('ordinary_policy_'+variant+'_v2.json')).write_text(json.dumps(d,indent=2),encoding='utf8')
p=R/'scripts/routing_geometry.py';s=p.read_text(encoding='utf8')
s=s.replace("  return float(value)","  for pair in self.policy.get('netPairSpacing',[]):\n   if (net in pair['netsA'] and other in pair['netsB']) or (other in pair['netsA'] and net in pair['netsB']):value=max(value,pair['gap'])\n  return float(value)")
s=s.replace("      g=g.difference(poly).union(local.intersection(poly))","      insideOther=a['geometry'].intersection(poly);outsideOther=a['geometry'].difference(poly)\n      outsideFootprint=outsideOther.buffer(gap+radius+gridMargin,quad_segs=8).union(insideOther.buffer(float(r['gap'])+radius+gridMargin,quad_segs=8))\n      g=g.intersection(outsideFootprint).difference(poly).union(local.intersection(poly))")
s=s.replace("  return unary_union(out),allowed","  for window in self.policy.get('routeWindows',[]):\n   if net in window['nets'] and layer in window.get('layers',LAYERS):allowed=allowed.intersection(Polygon(window['polygon']).buffer(-(radius+gridMargin),quad_segs=8))\n  return unary_union(out),allowed")
p.write_text(s,encoding='utf8');print('Prepared explicit pending STAR07b/USB8 power reservations and SPI corridor limits')