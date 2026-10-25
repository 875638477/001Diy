import pathlib,json
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');q=json.loads((P/'NSS_pullup_local_relayout_01.json').read_text());
for c in q['placementChanges']:
 if c['ref']=='R23':c['xy']=[33.3,32.2]
 if c['ref']=='R25':c['xy']=[31,33.7]
for o in q['operations']:
 if o['id']=='NSS01_MAIN_SOURCE':o['points']=[[34.8,31.15],[33.75,32.2],[33.1984,32.2]]
 if o['id']=='NSS01_LOCAL_PULLUP_STUB':o['points']=[[33.1984,32.2],[33.1984,32.9],[32.6764,33.422],[32.6764,33.7]]
 if o['id']=='NSS01_ADC_SERIES_TO_LOCAL_CAP':o['points']=[[34.8,33],[34.5,33],[33.65,33.85],[33.65,35.5],[32.6764,35.5]]
 if o['id']=='NSS01_R25_SUPPLY_TOP':o['points']=[[30.4,33.7],[31.1016,33.7]]
for ops in q['variantOperations'].values():
 for o in ops:
  if o['type']=='route' and o['net']=='SPI_NSS':o['points'][0]=[31.6236,32.2]
q['newPullupStubCenterlineMM']=.7+(.522**2*2)**.5+.278
q['reason']+=' Candidate precheck moved R23+.4X to avoid C9 PlaceBound and R25-.2X/ADC verticalx33.65 to clear actual existing C24 .6GND return, preserving exact MCU-to-C24 copper.'
(P/'NSS_pullup_local_relayout_01.json').write_text(json.dumps(q,indent=2),encoding='utf8')
s=(P/'prepare_gpio_future_11.py').read_text(encoding='utf-8-sig').replace('RIGHT10_FULL_{v}_v8','RIGHT10_FULL_{v}_v10').replace('_11_','_12_')
s=s.replace("filled=True,generated=False,boundary=island,holes=[],futureCandidate='NEW_QUIET_ISLAND'","filled=True,generated=False,vertices=[dict(type='line',start=a,end=b) for a,b in zip(island,island[1:]+island[:1])],holes=[],futureCandidate='NEW_QUIET_ISLAND'")
(P/'prepare_gpio_future_12.py').write_text(s,encoding='utf8');exec(compile(s,str(P/'prepare_gpio_future_12.py'),'exec'))
