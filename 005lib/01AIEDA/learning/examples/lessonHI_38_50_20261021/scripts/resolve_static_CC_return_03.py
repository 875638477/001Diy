import pathlib,json,math
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/USB_aux_returns_{v}_02.json').read_text(encoding='utf8'))
 if v=='4L':
  assert len(d['failures'])==1 and d['failures'][0]['signalVia']=='CC2_ENTRY_V'
  d['automaticUnresolvedCases']=d.pop('failures');d['failures']=[]
  d['engineeringResolutions']=[{'signalVia':'CC2_ENTRY_V','net':'USB_CC2','sourceXY':[41.75,8.3],'existingCommonReturnXY':[41.7,5.8],'distanceMM':math.dist([41.75,8.3],[41.7,5.8]),'decision':'STATIC_RD_CONFIG_EXCEPTION_PENDING_ACTUAL_REFERENCE','basis':'CC2 connects only passive Rd R4 to common ground. This training circuit has no PD/BMC or clock/data driver on CC. The1.5mm local stitch target used for fast signal transitions is not a universal requirement for a DC attach-resistor node. Preserve actual common L3 reference and existing return via; do not squeeze an unmanufacturable extra drill between VBUS/data pads. Native common-ground graph, actual anti-pad/DP-entry reference and connector ESD/assembly limitations remain separately checked.','notAppliedTo':['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED','SPI','SWD','MCU_GPIO']}]
  d['status']='GEOMETRIC_RETURNS_WITH_EXPLICIT_STATIC_CC_ENGINEERING_EXCEPTION'
 (h/f'plans/USB_aux_returns_{v}_03.json').write_text(json.dumps(d,indent=2),encoding='utf8')