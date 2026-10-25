from pathlib import Path
import sys,json,hashlib,math,re,csv,collections,datetime
ROOT=Path(r'D:/001DIY/005lib/01AIEDA')
HI=ROOT/'learning/examples/lessonHI_38_50_20261021'
JK=ROOT/'learning/examples/lessonJK_51_59_20261022'
OUT=JK/'audits'; OUT.mkdir(exist_ok=True)
P=HI/'engineering_power'
sys.path[:0]=[str(HI/'tooling/packages'),str(P/'scripts')]
from shapely.geometry import LineString,Point,box
from shapely.ops import unary_union
import cadence_poly
stamp=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
inputs={}; checks=[]
def read(p):
 p=Path(p); b=p.read_bytes();inputs[str(p)]=dict(path=str(p),sha256=hashlib.sha256(b).hexdigest().upper(),bytes=len(b));return b

def js(p):return json.loads(read(p).decode('utf-8-sig'))
def txt(p):return read(p).decode('utf-8-sig')
def put(name,d):
 p=OUT/name;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return str(p)
def ck(name,ok,detail=None):
 checks.append(dict(id=name,passed=bool(ok),detail=detail));return bool(ok)
def layer(s):return s.removeprefix('ETCH/')
def line(r):return LineString(r['startEnd'])

# Re-read the frozen stage instead of silently treating current files as identical.
sealed=js(P/'b019_stage_manifest.json'); integrity=[]
for q in sealed['files']+sealed['inputs']+[sealed['masterNote']]:
 p=Path(q['path']);p=p if p.is_absolute() else P/p
 actual=hashlib.sha256(p.read_bytes()).hexdigest().upper() if p.exists() else None
 integrity.append(dict(path=str(p),expectedSHA256=q['sha256'].upper(),actualSHA256=actual,match=actual==q['sha256'].upper()))
ck('JK51_INPUT_SEALED_FILES',all(x['match'] for x in integrity),dict(count=len(integrity),mismatches=[x for x in integrity if not x['match']]))
report=js(HI/'review/b019_native_report.json')
de=js(ROOT/'learning/examples/de_15_26_20261019/integrated_circuit.json')
spec=js(ROOT/'learning/examples/de_15_26_20261019/power_interface_spec.json')
policy=js(P/'routing_policy_interfaces_04.json')
oldpad=js(P/'readouts/B019_padentry_independent_actual_review.json')
shared=js(P/'readouts/USB_shared_b019_obstacles_and_actual_ground_corridors.json')
mesh=js(P/'readouts/USB_b019_return_multiterminal_actual_vs_derived_03.json')
ck('JK52_USB_14_ACTUAL_GAP_PIECES',len(shared['gapPieces'])==14,len(shared['gapPieces']))
expected_nc={'J2.A8','J2.B8','U2.5','U3.4','U5.5','U5.8'}
expected_open={'GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15'}
USB={'USB_DP','USB_DM','PA11_SHARED','PA12_SHARED'}
DEpins={(c['ref']+'.'+str(k)):(v or '') for c in de['components'] for k,v in c['pins'].items()}
variants={}; pernet=[]; projections=[]; returns=[]; ground_rows=[]; domains=[]
anchors={
 'VIN_INPUT':['J1.1','F1.1','F1.2','D1.2','D1.1','C1.1','C2.1','C3.1','U2.3'],
 'BUCK_CIN_HOT_LOOP':['C3.1','U2.3','U2.1','C3.2'],
 'BUCK_SW_BOOT':['U2.2','L1.1','C4.2','C4.1','U2.6'],
 'BUCK_FEEDBACK':['L1.2','C5.1','R1.1','R1.2','U2.4','R2.1','R2.2'],
 'V5_COUT_LDO':['L1.2','C5.1','C5.2','C6.1','C6.2','C8.1','C8.2','U3.1','U3.2','U3.3'],
 'LDO_V3V3':['U3.5','C9.1','C9.2','U3.2'],
 'MCU_VDD24':['U1.24','C13.1','C13.2','U1.23'],
 'MCU_VDD36':['U1.36','C14.1','C14.2','U1.35'],
 'MCU_VDD48':['U1.48','C15.1','C15.2','C16.1','C16.2','U1.47'],
 'MCU_VBAT':['U1.1','C17.1','C17.2'],
 'VDDA_FILTER':['R26.1','R26.2','C18.1','C18.2','C19.1','C19.2','C20.1','C20.2','U1.9','U1.8'],
 'CAN_LOCAL':['U5.3','U5.2','C11.1','C11.2','C12.1','C12.2'],
 'LIVE_NRST_FEED':['R27.1','R27.2','U1.7','C21.1','C21.2'],
 'USB_VBUS_ESD':['J2.A4_B9','J2.B4_A9','U4.5','C10.1','C10.2','U4.2'],
 'HSE_QUIET':['U1.5','U1.6','Y1.1','Y1.3','Y1.2','Y1.4','C22.1','C22.2','C23.1','C23.2'],
 'HEADER_POWER':['J11.1','J11.2','J12.1','J12.2','J13.1','J13.2','J9.1','J9.2']}
for v in ['2L','4L']:
 b=report['boards'][v];cp=Path(b['checkpointDirectory']);n=js(cp/'normalized.json');w=js(cp/'networks.json');rules=js(cp/'base_net_rules.json')
 board_sha=hashlib.sha256(read(b['path'])).hexdigest().upper();ck(f'JK51_{v}_BOARD_SHA',board_sha==b['sha256']==w['sha256'])
 by={c['ref']:c for c in n['placements']};pins={c['ref']+'.'+str(p['number']):dict(p,ref=c['ref']) for c in n['placements'] for p in c['pins'] if p.get('number')}
 actual={k:(p['net'] or '') for k,p in pins.items()}
 mismatches=[dict(pin=k,schematic=DEpins.get(k),pcb=actual.get(k)) for k in sorted(DEpins.keys()|actual.keys()) if DEpins.get(k)!=actual.get(k)]
 ck(f'JK51_{v}_SOURCE_272_PIN_NET_IDENTITY',not mismatches,dict(sourcePins=len(DEpins),actualPins=len(actual),mismatches=mismatches))
 ck(f'JK51_{v}_80_ELECTRONIC_COMPONENTS',len(by)==80==len(de['components']))
 nc={k for k,p in pins.items() if not p.get('net')};ck(f'JK51_{v}_6_EXPLICIT_NC',nc==expected_nc,sorted(nc))
 ck(f'JK51_{v}_266_REAL_TERMINALS',sum(x['terminalCount'] for x in w['nets'])==266)
 ck(f'JK51_{v}_69_NETS',len(w['nets'])==69)
 opens=[x for x in w['nets'] if x['minTerminalJoins']>0]
 ck(f'JK51_{v}_7_UNFINISHED_NETS',len(opens)==7 and {x['net'] for x in opens}==expected_open and sum(x['minTerminalJoins'] for x in opens)==7)
 build=Path(b['buildLog']);fresh=Path(b['freshReadback'])
 rawdrc=txt(build/'changed_nets_scoped_drc.txt')
 results=re.findall(r'SCOPED_CHANGED_NETWORK_RESULT net="([^"]+)" result=([^ ]+)',rawdrc)
 ck(f'JK51_{v}_65_RAW_PER_NET_DRC_COMPLETE_ZERO',len(results)==65 and len(set(a for a,z in results))==65 and all(float(z)==0 for a,z in results) and {a for a,z in results}=={x['net'] for x in w['nets']}-USB)
 scoped={a:float(z) for a,z in results}
 ck(f'JK51_{v}_RAW_RESULT_EQUALS_NATIVE_REPORT',scoped=={x['net']:x['result'] for x in b['scoped']['actualPerNetResults']})
 ck(f'JK51_{v}_WHOLE_DRC_STILL_UNKNOWN',w['summary']['nativeDRC'] is None and b['wholeBoardDRC'] is None)
 proofs=txt(fresh/'hi_reopen_endpoint_proofs.txt');pf=re.findall(r'HI_ENDPOINT_PROOF from="([^"]+)" to="([^"]+)" expected=(\w+) actual=(\w+)',proofs)
 ck(f'JK51_{v}_FRESH_CUMULATIVE_PROOFS',len(pf)==b['proofCount'] and len(set(pf))==len(pf) and all(e==a for _,_,e,a in pf),dict(count=len(pf),expectedReport=b['proofCount']))
 groundtrials=[]
 for trial in [1,2]:
  gtxt=txt(build/f'hi_all_ground_common_trial_{trial}.txt')
  gpin=re.findall(r'ALL_GND_PHYSICAL_PIN ref="([^"]+)" number="([^"]+)" xy=\(([-\d.]+) ([-\d.]+)\) globalC1_2Reached=(\w+)',gtxt)
  gv=re.findall(r'ALL_GND_ACTUAL_VIA xy=\(([-\d.]+) ([-\d.]+)\) padstack="([^"]+)" commonC1_2=(\w+)',gtxt)
  expectg={k for k,p in pins.items() if p.get('net')=='GND'}
  ck(f'JK51_{v}_56_ACTUAL_GND_PINS_TRIAL{trial}',len(gpin)==56 and {r+'.'+p for r,p,*_ in gpin}==expectg and all(z[-1]=='t' for z in gpin))
  expectedvias=84 if v=='2L' else 76
  ck(f'JK51_{v}_ALL_GND_VIAS_TRIAL{trial}',len(gv)==expectedvias and all(z[-1]=='t' for z in gv))
  if trial==2:
   ground_rows.extend(dict(variant=v,kind='physicalPin',key=r+'.'+p,xy=[float(x),float(y)],commonTo='C1.2',nativeResult=z) for r,p,x,y,z in gpin)
   ground_rows.extend(dict(variant=v,kind='actualVia',key=pad,xy=[float(x),float(y)],commonTo='C1.2',nativeResult=z) for x,y,pad,z in gv)
  modes=re.search(r'designModes=(.*)',gtxt)
  groundtrials.append(dict(trial=trial,pins=len(gpin),vias=len(gv),allNativeResultsTrue=all(z[-1]=='t' for z in gpin+gv),designModeRaw=modes.group(1) if modes else None))
 # Exact raw layer names; MASK absence does not remove pad mask apertures.
 stack=txt(fresh/'stackup_full.tsv');films=txt(fresh/'films_full.tsv');outline=txt(fresh/'outline_exact.tsv')
 rows=list(csv.DictReader(stack.splitlines(),delimiter='\t'));cu=[x['name'].strip('"') for x in rows if x['type'].strip(chr(34))=='CONDUCTOR'];expected=['TOP','BOTTOM'] if v=='2L' else ['TOP','L2','L3','BOTTOM']
 ck(f'JK51_{v}_UPPERCASE_COPPER_ORDER',cu==expected,cu)
 ck(f'JK51_{v}_NO_PHYSICAL_MASK',not any('MASK' in x['type'] for x in rows))
 filmnames=re.findall(r'^"([^"]+)"\t',films,re.M);ck(f'JK51_{v}_FULL_FILM_COUNT',len(filmnames)==(15 if v=='2L' else 17),filmnames)
 ck(f'JK51_{v}_ROOT_AND_TEMPLATE_REAL_OUTLINES','AUTHORITATIVE_ROOT' in outline and 'NON_ROOT_COPY' in outline and outline.count('((0.0 0.0) (80.0 60.0))')==2)
 ck(f'JK51_{v}_4_MECHANICAL_MOUNTING_HOLES',sorted(tuple(x['xy']) for x in n['mechanical'])==[(5.,5.),(5.,55.),(75.,5.),(75.,55.)])
 # Read-back property/model values must be reported separately from net consistency.
 valdiff=[]
 for c in de['components']:
  if c['value']!=by[c['ref']]['value']:valdiff.append(dict(ref=c['ref'],sourceValue=c['value'],pcbValue=by[c['ref']]['value']))
 # Actual plane parser; all holes retained. Explicitly exclude local quiet static copper from common-reference screen.
 ground={z:[] for z in cu};areas=[]
 for i,s in enumerate(n['planes']):
  if s['net']!='GND' or not s.get('filled'):continue
  poly=cadence_poly.plane_from_native(dict(s,holes=s.get('holes') or []));error=poly.area-s['area'];ck(f'JK52_{v}_PLANE_AREA_{i}',abs(error)<.01,dict(errorMM2=error))
  areas.append(dict(index=i,layer=layer(s['layer']),nativeAreaMM2=s['area'],parsedAreaMM2=poly.area,errorMM2=error,excludedLocalQuiet=not s.get('generated')))
  if s.get('generated'):ground[layer(s['layer'])].append(poly)
 ground={z:unary_union(q) for z,q in ground.items()}
 groundvias=[x for x in n['vias'] if x['net']=='GND']
 manual=[r for r in n['routes'] if not r.get('generatedThermal')]
 for net in w['nets']:
  name=net['net'];rs=[r for r in manual if r['net']==name];vs=[x for x in n['vias'] if x['net']==name]
  row=dict(variant=v,net=name,terminalCount=net['terminalCount'],terminalComponents=net['terminalComponents'],remainingMinJoins=net['minTerminalJoins'],nativeUnconnected=net['nativeUnconnected'],scopedDRCResult=scoped.get(name),scopedDRCState='CHECKED_EXISTING_RULES_ZERO' if name in scoped else 'USB_CHECK_NOT_COMPLETED',manualSegmentCount=len(rs),manualCenterlineTotalMM=sum(line(x).length for x in rs),manualWidthSetMM=sorted({x['width'] for x in rs}),manualLayers=sorted({layer(x['layer']) for x in rs}),viaCount=len(vs),physicalTerminalPartitions=[[dict(key=p['key'],xy=p['xy']) for p in c['terminals']] for c in net['components']])
  row['lengthScope']='Sum of all manual segment centerlines, includes branches; not a single end-to-end flight length or propagation delay.'
  pernet.append(row)
  for l in sorted({layer(x['layer']) for x in rs}):
   segs=[x for x in rs if layer(x['layer'])==l];reference=('BOTTOM' if l=='TOP' else 'TOP') if v=='2L' else ('L2' if l=='TOP' else 'L3')
   lines=unary_union([line(x) for x in segs]);foot=unary_union([line(x).buffer(x['width']/2,quad_segs=16) for x in segs]);missing=lines.difference(ground[reference].buffer(.0001));outside=foot.difference(ground[reference].buffer(.0001));
   projections.append(dict(variant=v,net=name,signalLayer=l,referenceLayer=reference,manualLineUnionLengthMM=lines.length,centerlineOutsideGeneratedReferenceMM=missing.length,manualFootprintAreaMM2=foot.area,footprintOutsideGeneratedReferenceMM2=outside.area,missingCenterlineBounds=list(missing.bounds) if not missing.is_empty else None,definition='Actual generated GND planes+holes only; local quiet island excluded. Does not include co-planar/trace/pad/via return; an opening is a geometric finding, not automatically SI fail. No simulation.'))
  for vv in vs:
   if name=='GND':continue
   nearest=sorted((math.dist(vv['xy'],g['xy']),g) for g in groundvias)
   dist,g=nearest[0]
   returns.append(dict(variant=v,net=name,signalVia=vv['xy'],padstack=vv['padstack'],nearestActualGroundVia=g['xy'],distanceMM=dist,withinTeaching15mmTarget=dist<=1.5,allGroundViasHaveStoredNativeCommonProof=True,scope='Euclidean nearby via only; not HF current path, not guaranteed common plane on signal segment. Actual nearest GND pad/shell may be closer; do not impose1.5mm as universal DRC.'))
 for domain,keys in anchors.items():
  missing=[k for k in keys if k not in pins];ck(f'JK53_{v}_DOMAIN_{domain}_REAL_PIN_ANCHORS',not missing,missing)
  aa=[dict(key=k,net=pins[k]['net'],xy=pins[k]['xy'],padBBox=pins[k].get('padBBox')) for k in keys if k in pins]
  nets=sorted({x['net'] for x in aa if x['net']});stats=[x for x in pernet if x['variant']==v and x['net'] in nets]
  domains.append(dict(variant=v,domain=domain,physicalAnchors=aa,netStats=stats,localGroundVias=[dict(xy=g['xy'],padstack=g['padstack']) for g in groundvias if aa and min(math.dist(g['xy'],a['xy']) for a in aa)<2.0],connectionScope='Stored actual terminal graph membership only. Internal IC paths/component impedance are not invented copper shorts. GND common is not low-inductance proof.'))
 # Record every original strict challenge; copper equivalence is directly preserved in frozen independent review.
 strict={}
 for name in ['BOOT0','GPIO_PA15','GPIO_PB4','I2C_SCL']:
  raw=txt(build/f'strict_neck_{name}.txt');ck(f'JK51_{v}_STRICT_NECK_{name}_ACTUAL17414', '1.7414' in raw and b['strictNativeNeckChallenges'][name]['allTOPFieldsExactlyRestored'])
  strict[name]=dict(originalObjectMM=2.1414213562373092,normalizedObjectMM=1.7414213562373095,unchangedPhysicalExteriorMM=1.5414213562373096,strictTemporaryLimitMM=1.7,normalFinalLimitMM=2.0,allFieldsRestored=b['strictNativeNeckChallenges'][name]['allTOPFieldsExactlyRestored'],actualCopperUnionDifferenceMM2=b['sameNetActualCopperUnionChecks'][name]['TOPSameNetCuSymmetricDifferenceMM2'])
 # Key critical facts do not depend on a guessed schematic pin number.
 ck(f'JK53_{v}_BOOT_CAP_RETURNS_TO_SW_NOT_GROUND',pins['C4.2']['net']=='BUCK_SW' and pins['C4.1']['net']=='BUCK_BOOT')
 ck(f'JK53_{v}_R27_LIVE_V3_SUPPLY',pins['R27.1']['net']=='V3V3' and next(x for x in w['nets'] if x['net']=='V3V3')['minTerminalJoins']==0)
 ck(f'JK53_{v}_USB_VBUS_DISTINCT_FROM_V5_V3',pins['U4.5']['net']=='USB_VBUS' and pins['U3.1']['net']=='V5' and pins['U3.5']['net']=='V3V3')
 ck(f'JK52_{v}_NONGND_NO_INNER_MANUAL_ETCH',not any(layer(x['layer']) in ['L2','L3'] and x['net']!='GND' for x in manual))
 variants[v]=dict(boardSHA256=board_sha,board=str(b['path']),checkpoint=str(cp),readOnlyCurrentRound=True,newNativeProcess=False,counts=dict(components=len(by),pins=len(pins),nettedPins=len(pins)-len(nc),NC=len(nc),nets=len(w['nets']),remainingJoins=sum(x['minTerminalJoins'] for x in w['nets']),groundPins=56,groundVias=len(groundvias),groundShapes=len(n['planes']),vias=len(n['vias']),manualSegments=len(manual)),missingNets=[x for x in pernet if x['variant']==v and x['remainingMinJoins']>0],componentValueDifferences=valdiff,scopedResults=scoped,USBUncompleted=sorted(USB),wholeDRC=None,rawStoredForensicOnly=b['rawStoredDRCsForensicOnly'],groundTrialEvidence=groundtrials,copperOrder=cu,filmNames=filmnames,planeParserAreas=areas,padRepresentationCorrection=strict,loadedSchemaScope=n['scope'])
# Existing expert-screen artifacts are reused only after stage SHA validation and b018→b019 Cu-invariance checks.
prior={v:js(P/f'readouts/TOP_b018_{v}_actual_reference_audit.json') for v in ['2L','4L']}
references=[dict(id='TI_TPS54202_C',url='https://www.ti.com/lit/ds/symlink/tps54202.pdf',revision='SLVSD26C, Rev C',sections='Layout Guidelines / Layout Example, input/output capacitor and feedback placement',local=str(P/'source/tps54202_revC.pdf')),dict(id='TI_TLV755P_D',url='https://www.ti.com/lit/ds/symlink/tlv755p.pdf',revision='SBVS320D Rev D',sections='7.1.1 capacitor selection;7.4 layout; package-specific thermal data',local=str(P/'source/tlv755p_revD.pdf')),dict(id='TI_TCAN33x_F',url='https://www.ti.com/lit/ds/symlink/tcan332.pdf',revision='SLLSEQ7F Rev F',sections='Application, power supply and layout; termination/stub/decoupling',local=str(P/'source/tcan332_revF.pdf')),dict(id='ST_DS5319_20',url='https://www.st.com/resource/en/datasheet/stm32f103c8.pdf',revision='DS5319 Rev20 July2025',sections='Pinouts footnote5 p33; GPIO/I2C/SPI characteristics; supply/USB',local=str(HI/'source/DS5319_Rev20_STM32F103x8xB_ST_20261022.pdf')),dict(id='ST_DS4260',url='https://www.st.com/resource/en/datasheet/usblc6-2.pdf',revision='Local inherited DS4260; online official currently20pages; no claim bytes match',sections='PCB layout/ESD return; pin1/6 IO1,3/4 IO2,2GND,5VBUS',local=str(HI/'engineering_mcu/source/USBLC6_DS4260.pdf'))]
for x in references:read(x['local']);x['localSHA256']=inputs[x['local']]['sha256'];x['onlineVerificationDate']='2026-10-22';x['onlineVerification']='Official primary PDF page re-opened in this J audit; local archive remains unchanged; revisions are explicit, no silent replacement.'
put('j51_54_sources.json',dict(created=stamp,sources=references,localSpecification=dict(path=str(ROOT/'learning/examples/de_15_26_20261019/power_interface_spec.json'),supplyLimits=spec['supply_limits'],normalCurrentBudget_mA=spec['normal_current_budget_mA']),interfacePolicy=policy))
put('j51_54_input_integrity.json',dict(status='PASS_SEALED_INPUT_RECHECK' if all(x['match'] for x in integrity) else 'INPUT_MISMATCH_REVIEW_REQUIRED',created=stamp,sealedManifest=str(P/'b019_stage_manifest.json'),sealedManifestSHA256=inputs[str(P/'b019_stage_manifest.json')]['sha256'],entries=integrity,readThisRound=True,noOriginalModified=True))
put('j51_consistency_and_drc.json',dict(status='READ_ONLY_EVIDENCE_REVIEW_BOARD_REMAINS_INCOMPLETE',created=stamp,variants=variants,checks=checks,checkCount=len(checks),failedChecks=[x for x in checks if not x['passed']],newNativeCheck=False,newDRCRun=False,distinction='Evidence-check PASS is not all-nets-connected, whole-board DRC0, SI/PI/EMI certification, manufacturing release or hardware test.'))
put('j51_all69_net_matrix.json',dict(status='ALL_69_ACTUAL_NETS_PER_BOARD_REVIEWED',rows=pernet))
put('j51_all56_ground_pins_and_all_vias.json',dict(status='STORED_NATIVE_POSITIVE_COMMON_EVIDENCE_REPARSED_ALL_ROWS',rows=ground_rows,notHFReturnCertification=True))
put('j52_actual_reference_projection.json',dict(status='RECOMPUTED_READ_ONLY_GEOMETRIC_SCREEN_FROM_B019_NOT_NATIVE_SI_CHECK',rows=projections,geometry='Actual generated native planes and all holes, halfdegree signed arcs, bounded mm4 tangent handling;0.0001mm outward numerical tolerance. Co-planar return and via/trace ground deliberately not treated as a reference plane.',parserSHA256=hashlib.sha256(read(P/'scripts/cadence_poly.py')).hexdigest().upper(),roundedArcEvents=cadence_poly.ROUNDED_ARC_FLATTENED,coincidentArcEvents=cadence_poly.COINCIDENT_ARC_ENDPOINTS))
put('j52_signal_via_return_candidates_actual.json',dict(status='ALL_ACTUAL_NON_GND_VIAS_WITH_NEAREST_NATIVE_COMMON_GND_VIA_NOT_HF_ACCEPTANCE',rows=returns))
put('j52_USB14_gap_piece_register.json',dict(status='REUSED_SEALED_ACTUAL_14_PIECES_B019_CU_PRESERVED',sourceSHA256=inputs[str(P/'readouts/USB_shared_b019_obstacles_and_actual_ground_corridors.json')]['sha256'],pieces=[dict(id=f'JK52-USB2L-GAP-{i:02d}',**x) for i,x in enumerate(shared['gapPieces'],1)],priorActualReference=prior,actualGroundMesh=mesh,important='Prior screens and current re-computation are reads of actual stored geometry, not new Cadence checks. centerline/footprint/comparative mesh are not impedance/EMI measurements.'))
put('j53_actual_power_domains.json',dict(status='ACTUAL_PIN_NET_WIDTH_LAYER_VIA_AND_RETURN_REVIEW',domains=domains,currentBudget_mA=spec['normal_current_budget_mA'],supplyLimits=spec['supply_limits'],actualNetMetricsDefinition='Manual centerline sums include branches and are not a single supply current path. Existing full native DRC/graph is distinct from load/thermal/edge validity.',thermalArithmetic=dict(nominalLDO_VIN=5,nominalLDO_VOUT=3.3,currentA=.150,nominalDissipationW=.255,scope='Only (5-3.3)*.150 arithmetic, excludes IQ, voltage/part tolerance and actual thermal resistance/temperature; not junction-temperature approval.')))
put('j51_54_consumed_input_files.json',dict(created=stamp,files=list(inputs.values()),script=str(Path(__file__)),readOnlyNativeInputs=True))
print(json.dumps(dict(checks=len(checks),failed=[x for x in checks if not x['passed']],sealedEntries=len(integrity),consumedFiles=len(inputs),netRows=len(pernet),projectionRows=len(projections),viaReturnRows=len(returns),domainRows=len(domains)),ensure_ascii=False))