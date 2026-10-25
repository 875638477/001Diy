import pathlib,json,hashlib,copy
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu');H=R.parent;P=R/'plans';P.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
src=H/'scripts/plan_signal_paths.py';s=src.read_text(encoding='utf-8')
s=s.replace("sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))", "sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'scripts'))")
s=s.replace("sp,sourceLeg=scene.endpoint_port(source,width);tp,targetLeg=scene.endpoint_port(target,width)","\n def access(endpoint):\n  pin=scene.pins[endpoint]\n  if pin['ref']=='U1' and pin['net'] in policy.get('allowInwardPinAccess',[]):return list(pin['xy']),[list(pin['xy'])]\n  return scene.endpoint_port(endpoint,width)\n sp,sourceLeg=access(source);tp,targetLeg=access(target)")
s=s.replace("if p['ref']!='U1':continue", "if p['ref']!='U1' or p['net'] in policy.get('allowInwardPinAccess',[]):continue")
(P/'plan_gpio_paths_local.py').write_text(s,encoding='utf-8')
for v in ('4L','2L'):
 p=load(H/f'plans/ordinary_policy_{v}_v5.json');p['status']='GPIO18_POLICY_FRESH_POSTCRITICAL_NOT_NATIVE_APPROVAL';p['manualOnlyNets']=[n for n in p['manualOnlyNets'] if not n.startswith('GPIO_')]
 p['pendingOperations']=[];p['pendingDeleteSegments']=[];p['executedPendingRemovedBecause']='All critical policy_v5 pending geometry already imported in native postcritical_b010 checkpoint. 07b replaced by actual native07c.'
 p['componentAnchors']=[dict(net='GPIO_PC13',key='GPIO_PC13_NATIVE_PARTIAL',xy=[35.8,31.1],layers=['BOTTOM'],connectedTo='U1.2',replacePinAccess=True),dict(net='GPIO_PC14',key='GPIO_PC14_NATIVE_PARTIAL',xy=[45.6,25.2],layers=['TOP'],connectedTo='U1.3',replacePinAccess=True),dict(net='GPIO_PC15',key='GPIO_PC15_NATIVE_PARTIAL',xy=[35.4,30.3],layers=['BOTTOM'],connectedTo='U1.4',replacePinAccess=True)]
 p['allowInwardPinAccess']=['GPIO_PA1','GPIO_PA2','GPIO_PA3','GPIO_PB8','GPIO_PB9']
 p['reservedAreas'].append(dict(id='SPI_SOURCE_BANK_GPIO_EXCLUDED',polygon=[[33.5,26.5],[35.4,26.5],[35.4,33.5],[33.5,33.5]],layers=['TOP','BOTTOM'],allowedNets=['GND','PA4_SPI_NSS','PA5_SPI_SCK','PA6_SPI_MISO','PA7_SPI_MOSI','SPI_NSS','SPI_SCK','SPI_MISO','SPI_MOSI'],basis='Root reserved actual SPI source bank; GPIO search must not consume source escape bank.'))
 p['sourcePolicy']={'path':str(H/f'plans/ordinary_policy_{v}_v5.json'),'sha256':hashlib.sha256((H/f'plans/ordinary_policy_{v}_v5.json').read_bytes()).hexdigest()}
 (P/f'gpio_policy_{v}_01.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
(P/'gpio_helper_provenance.json').write_text(json.dumps({'source':str(src),'sourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest(),'localCopy':str(P/'plan_gpio_paths_local.py'),'changes':['Import original CopperScene from root scripts, no change of obstacles/spacing/shape rules.','Only named difficult U1 GPIO pin starts may search inward on TOP before off-pad via. Forced outward fanout and own-pad blockage relaxed only for these source choices.','All outputs remain geometric candidates; manual return/native graph/DRC/reopen review mandatory.']},indent=2),encoding='utf-8')
print('PREPARED_GPIO_POLICY_AND_OWN_HELPER')
