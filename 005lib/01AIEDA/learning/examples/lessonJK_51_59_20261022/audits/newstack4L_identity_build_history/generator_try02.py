"""Read native fresh data; emit only a separate new-stack TRAINING identity package.
Never invoke Cadence, modify sources, or rewrite sealed J55/release-gate products.
Flat CSV checks follow Spreadsheets skill; no workbook or factory angle invented.
"""
from pathlib import Path
import csv, json, re, hashlib, collections, datetime

R = Path(r'D:/001DIY/005lib/01AIEDA')
J = R / 'learning/examples/lessonJK_51_59_20261022'
OLD = J / 'logs/native_j55_4L_reopen_01'
NEW = J / 'logs/native_newstack_4L_reopen_01'
OLD_ASM = J / 'assembly/JK55_4L_corrected_TRAINING'
OUT = J / 'assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING'
NOTE = R / 'learning/notes/lessonJK_newstack4L_identity_20261023.md'
BOARD = J / 'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd'
BOARD_SHA = '471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9'
REVIEW = J / 'review/independent_newstack/review.json'
AUDIT = J / 'audits/jk_newstack4L_assembly_identity_review.json'
SUPPLEMENT = J / 'audits/jk_release_gate_newstack4L_supplement_20261023.json'
MANIFEST = J / 'audits/jk_newstack4L_identity_manifest.json'
NAMES = ['BOM_80_TRAINING_NOT_FOR_ASSEMBLY.csv', 'BOM_grouped_TRAINING_NOT_FOR_ASSEMBLY.csv',
         'coordinates_all80_TRAINING_NOT_FOR_ASSEMBLY.csv', 'SMT_candidates_TRAINING_NOT_FOR_ASSEMBLY.csv',
         'non_SMT_and_DNP_TRAINING_NOT_FOR_ASSEMBLY.csv']
checks = []
sources = {}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def source(p, expected=None):
    p = Path(p); h = sha(p)
    if expected is not None: assert h == expected.upper(), ('source hash mismatch', str(p), h, expected)
    sources[str(p)] = h
    return p

def check(ident, ok, **evidence):
    record = {'id': ident, 'pass': bool(ok), **evidence}; checks.append(record)
    assert ok, record

def load(p): return json.loads(source(p).read_text(encoding='utf-8-sig'))
def write_json(p, data):
    p = Path(p); assert p.is_relative_to(R); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sx(s):
    ts = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', s); i = 0
    def take():
        nonlocal i
        v = ts[i]; i += 1
        if v == '(':
            q = []
            while ts[i] != ')': q.append(take())
            i += 1; return q
        if v.startswith('"'): return json.loads(v)
        if v == 'nil': return None
        if v == 't': return True
        try: return float(v)
        except ValueError: return v
    out = take(); assert i == len(ts), (i,len(ts),s)
    return out

def rows(p):
    with source(p).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t', quotechar='\0'))
def parsed(p): return [{k:sx(v) for k,v in x.items()} for x in rows(p)]
def counter(x): return collections.Counter(json.dumps(v, ensure_ascii=False,sort_keys=True) for v in x)
def same_records(name, drop=()):
    a = [{k:v for k,v in x.items() if k not in drop} for x in rows(OLD/name)]
    b = [{k:v for k,v in x.items() if k not in drop} for x in rows(NEW/name)]
    check('native_exact_' + name, counter(a) == counter(b), oldRows=len(a), newRows=len(b), ignoredTransientFields=list(drop))
    return b

def csv_data(p):
    with source(p).open(encoding='utf-8-sig',newline='') as f:
        r = csv.DictReader(f); out = list(r); fields = r.fieldnames
    check('rectangular_' + str(p.relative_to(J)), all(None not in x and all(v is not None for v in x.values()) for x in out), rows=len(out))
    return fields, out

def native_values(scope):
    folder = J / 'exports' / ('devicevalues_' + scope + '_TRAINING')
    raw = source(folder/'component_values_source.tsv').read_text(encoding='utf-8-sig')
    check(scope+'_value_export_complete', raw.splitlines()[-1] == 'JK_NATIVE_80_DEVICE_VALUES_COMPLETE')
    rr = list(csv.DictReader(raw.splitlines()[:-1], delimiter='\t', quotechar='\0'))
    result = {}
    for r in rr:
        ref = sx(r['refdes'])
        inst, defi = sx(r['instanceProperties']), sx(r['definitionProperties'])
        ip = dict(inst or []); dp = dict(defi or [])
        value = ip.get('VALUE', dp.get('VALUE'))
        devicefiles = list((folder/ref).glob('*.txt'))
        check(scope+'_'+ref+'_exactly_one_official_device', len(devicefiles) == 1)
        f = source(devicefiles[0]); text = f.read_text(encoding='utf-8-sig')
        vv = re.findall(r'^PACKAGEPROP\s+VALUE\s+(.+?)\s*$', text, re.M)
        check(scope+'_'+ref+'_dual_value', len(vv)==1 and vv[0].strip("'") == value,
              effectiveVALUE=value, instanceVALUE=ip.get('VALUE'), compdefVALUE=dp.get('VALUE'), deviceFile=str(f))
        assert ref not in result; result[ref] = value
    check(scope+'_value_count', len(result)==80)
    return result

def all_manifest_inputs(path):
    data = load(path)
    for key in ('files','sourceHashes','nativeCorrectionSources','sources'):
        for x in data.get(key,[]):
            if isinstance(x,dict) and 'path' in x and 'sha256' in x: source(x['path'],x['sha256'])
    return data

# Existing sealed records are inputs, never outputs of this script.
all_manifest_inputs(J/'audits/j55_57_artifact_manifest.json')
all_manifest_inputs(J/'audits/jk_release_gate_manifest.json')
source(BOARD, BOARD_SHA)
review = load(REVIEW)
check('independent_newstack_final_PASS', str(review.get('status','')).startswith('PASS') and review.get('failed',0) in (0,[]),
      status=review.get('status'), reviewerReport=str(REVIEW))
check('review_board_identity', review.get('boardSHA256')==BOARD_SHA)
for extra in ['manual_route_equivalence.json','actual_reference_footprints.json','reference_conversion_caps_and_vias.json']:
    source(REVIEW.with_name(extra))
launch = load(NEW/'launch.json')
check('fresh_completed', launch.get('completed') is True and launch.get('exitCode')==0 and launch.get('protectedAllUnchanged') is True)
check('fresh_board_identity', launch.get('scratchAfterSHA256')==BOARD_SHA)

components = same_records('components.tsv')
pins = same_records('component_pins.tsv')
placed = same_records('placed_pins.tsv')
texts = same_records('board_instance_texts.tsv', ('attrs',))
geometry = same_records('g_actual_geometry.tsv')
check('counts', (len(components),len(pins),len(placed),len(texts),len(geometry))==(80,272,278,247,573))
syms = []
for directory in (OLD,NEW):
    data = source(directory/'jk55_instance_properties.tsv').read_text(encoding='utf-8-sig')
    syms.append([x for x in data.splitlines() if x.startswith('SYMBOL\t')])
check('native_symbols_pose_exact', counter(syms[0])==counter(syms[1]), totalSymbols=len(syms[1]))
poses = {}
for line in syms[1]:
    _,ref,pkg,xy,rot,mir = line.split('\t')
    ref=sx(ref)
    if ref is not None: poses[ref]={'package':sx(pkg),'xy':sx(xy),'rotation':sx(rot),'mirrored':sx(mir)}
check('native_80_poses', len(poses)==80)
value_old = native_values('J55_4L')
value_new = native_values('newstack_4L')
check('old_new_native_VALUE_exact', value_old==value_new)

csvs = {name:csv_data(OLD_ASM/name) for name in NAMES}
bom = {x['Reference']:x for x in csvs[NAMES[0]][1]}
coord = {x['Reference']:x for x in csvs[NAMES[2]][1]}
texts_parsed = parsed(NEW/'board_instance_texts.tsv')
geom_parsed = parsed(NEW/'g_actual_geometry.tsv')
bounds = [x for x in geom_parsed if x['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP']
shape_bounds = [x for x in bounds if x['type']=='shape']
legacy_paths = [x for x in bounds if x['type']=='path']
check('shape_path_count',len(shape_bounds)==80 and len(legacy_paths)==4)
shapes = {x['refdes']:x for x in shape_bounds}
check('height_shape_coverage', len(shapes)==80)
for ref,bb in bom.items():
    pp=poses[ref];cc=coord[ref]
    check('value_'+ref, value_new[ref]==bb['Value']==cc['Value'], value=value_new[ref])
    check('pose_'+ref, pp['package']==cc['Package']==bb['Package'] and pp['xy']==[float(cc['X_mm']),float(cc['Y_mm'])]
          and pp['rotation']==float(cc['CAD_Rotation_deg']) and pp['mirrored'] is None)
    check('coordinate_interpretation_'+ref, cc['Units']=='mm' and cc['Origin']=='CAD_DATABASE_X0_Y0'
          and cc['Position_Meaning']=='SYMBOL_ORIGIN_NOT_VERIFIED_PICK_CENTRE' and cc['Side']=='TOP'
          and cc['Assembly_Factory_Rotation_deg']=='' and cc['Rotation_Status']=='FACTORY_MAPPING_PENDING')
    props=dict(shapes[ref]['props'] or [])
    check('height_'+ref, props.get('PACKAGE_HEIGHT_MAX')==bb['CAD_Height_Max'], CADHeight=props.get('PACKAGE_HEIGHT_MAX'), status=bb['Height_Status'])
    for layer,value in [('REF DES/SILKSCREEN_TOP',ref),('REF DES/ASSEMBLY_TOP',ref),('COMPONENT VALUE/ASSEMBLY_TOP',value_new[ref])]:
        tt=[x for x in texts_parsed if x['refdes']==ref and x['layer']==layer]
        check('origin_text_'+ref+'_'+layer, len(tt)==1 and tt[0]['text']==value and tt[0]['xy']==pp['xy']
              and tt[0]['rotation']==pp['rotation'] and tt[0]['mirrored']==pp['mirrored'])
check('BOM_cardinality',len(bom)==80 and len(coord)==80)
check('grouped_cardinality',len(csvs[NAMES[1]][1])==66 and sum(int(x['Quantity']) for x in csvs[NAMES[1]][1])==80)
check('SMT_split',len(csvs[NAMES[3]][1])==65 and len(csvs[NAMES[4]][1])==15)
check('procurement_pending',sum(x['Procurement_Status']=='SPEC_ONLY_PROCUREMENT_PENDING' for x in bom.values())==68)
check('height_defaults',sum(x['Height_Status']=='USER_DEFAULT_NOT_PHYSICAL_CERTIFICATION' for x in bom.values())==72)
summary=source(NEW/'hi_network_summary.txt').read_text(encoding='utf-8-sig')
check('physical_and_open_contract',all(t in summary for t in ['ALL_PIN_NET_OBJECT_TERMINALS=272','NETS=69','ACTUAL_NETTED_PHYSICAL_TERMINALS=266',
    'NATIVE_REMAINING_CONNECTIONS=7','GRAPH_MIN_TERMINAL_JOINS=7','LONELY_UNNETTED_BRANCHES=nil']))
for n in ['cross_section.tsv','stackup_full.tsv','newstack_fresh_plane_contract.txt','films_full.tsv','physical_pad_layers.tsv','hi_reopen_endpoint_proofs.txt']:
    source(NEW/n)
# Direct old/new VALUE exports add stronger evidence; they do not revise the old sealed manifest retroactively.
pre_write = dict(sources)
OUT.mkdir(parents=True,exist_ok=True)
for name,(fields,rr) in csvs.items():
    rr=[dict(x) for x in rr]
    for x in rr:
        if 'Source_BRD_SHA256' in x: x['Source_BRD_SHA256']=BOARD_SHA
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rr)
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:
        reload=list(csv.DictReader(f))
    check('csv_reload_'+name,reload==rr and all(x['Status']=='TRAINING_NOT_FOR_ASSEMBLY' for x in reload),rows=len(rr))
    if 'Source_BRD_SHA256' in fields: check('csv_new_SHA_'+name,all(x['Source_BRD_SHA256']==BOARD_SHA for x in reload))
identity={
    'status':'TRAINING_NOT_FOR_ASSEMBLY','board':str(BOARD),'sha256':BOARD_SHA,
    'rawReadback':str(NEW),'nativeValues':str(J/'exports/devicevalues_newstack_4L_TRAINING'),
    'independentStructureReview':str(REVIEW),'sourceJ55Assembly':str(OLD_ASM),
    'oldJ55BoardSHA256':'9DEC773FE106E09C9844FEF5F160E1A1B3348BFC693926579F0CAF0A6A18DCF0',
    'variantStack':'TOP_SIGNAL_L2_GND_L3_V3V3_BOTTOM_SIGNAL',
    'sourceCSVFieldsPreserved':True,'onlyCoordinateSourceSHAChanged':True,
    'assemblyIdentityPreserved':{'components':80,'logicalPins':272,'placedPinsIncludingNPTH':278,'instanceTexts':247,'heightShapes':80,'legacyBoundPaths':4},
    'nativeValueDualCheck':'compdef/instance effective VALUE AND official axlWriteDeviceFile PACKAGEPROP VALUE, old/new/BOM identical',
    'pickupCentreApproval':False,'factoryCentroidRotationMapping':False,'physicalHeightCertification':False,
    'wholeboardDRC':'PENDING_NOT_APPROVED','remainingGPIOJoins':7,'hardwareCertification':False}
write_json(OUT/'source_identity.json',identity)
(OUT/'README.md').write_text('''# 鏂板洓灞傝閰嶈韩浠藉壇鏈紙浠呰缁冿級

**TRAINING_NOT_FOR_ASSEMBLY / NOT_RELEASED銆?* 鏈洰褰曠粦瀹氬疄闄呮柊鏍堟澘锛歚TOP-L2-L3-BOTTOM`锛孡2鍏卞湴銆丩3瀹為檯V3V3銆傚畠涓庢棫J55瑁呴厤鍖呭垎鍒繚瀛樸€?
80浠躲€?6缁勩€?0鍧愭爣銆?5璐磋鍊欓€夈€?5闈濻MT鎴朌NP椤癸紱鎵€鏈夊厓浠跺€肩敱鍘熺敓VALUE灞炴€у強瀹樻柟璁惧鏂囦欢鍙屾牳銆?浠紺SV闄?涓潗鏍囩被鏂囦欢鐨勬簮鏉縎HA澶栵紝鍏朵綑瀛楁涓庢棫J55_4L涓€鑷淬€傚叿浣撴澘韬唤鍙婄嫭绔嬬粨鏋勬姤鍛婅[source_identity.json](source_identity.json)銆?
鍧愭爣涓簃m銆佹暟鎹簱X0/Y0涓嬬殑灏佽symbol鍘熺偣锛涘師鐢熸棆杞笉鏄伐鍘傛棆杞€傚伐鍘傛棆杞垪鍒绘剰鐣欑┖锛屾湭鏍稿噯鍚稿彇涓績鎴朚PN锛?8浠朵粛闇€閲囪喘閫夊瀷銆?3涓猅HT椤瑰拰2涓狣NP椤逛笉杩涘叆SMT鍊欓€夛紝J2娣峰悎缁撴瀯闇€鍗曠嫭宸ヨ壓纭銆?涓狽PTH鏈烘瀛斾笉灞炰簬BOM鍣ㄤ欢銆?
72涓?mm鏄敤鎴烽粯璁AD楂樺害锛?涓棦鏈夋樉寮忛珮搴︿繚鐣欙紱鍧囦笉鑷姩绛変簬瀹炵墿楂樺害璁よ瘉銆傞樆鐒婃ˉ銆侀挗缃戝帤搴︺€丏NP寮€鍙ｆ姂鍒躲€佹彃瑁呰剼闀裤€佸瓧浣?瑁呴厤浣欓噺绛夋棫寮€鏀鹃」缁х画閫傜敤銆傛柊SHA缁戝畾鍜屽疄闄呭唴灞傛洿鏀逛笉绛変簬宸ュ巶鎵瑰噯銆乁SB90惟銆丼I/PI鎴栧畬鏁碊RC閫氳繃锛涗粛鏈?涓狦PIO杩炴帴寰呭畬鎴愩€?''',encoding='utf-8')

supplement={
 'status':'NEWSTACK_STRUCTURE_APPLIED_ASSEMBLY_IDENTITY_VERIFIED_NOT_PRODUCTION_RELEASE',
 'board':str(BOARD),'boardSHA256':BOARD_SHA,'freshReadback':str(NEW),'independentStructureReview':str(REVIEW),
 'sealedGateRegister':str(J/'audits/jk_release_gate_register.json'),
 'interpretation':'This is a later board-identity-specific supplement. Original issue payloads/status and old legacy-stack evidence are retained without modification.',
 'updates':[
  {'issueID':'K4L_NEW_STACK_REQUIRED','oldObservation':'No completed new-stack evidence consumed at sealed gate snapshot',
   'newObservation':'New board has actual L2 GND and L3 V3V3 planes, native fresh readback and independent structure review PASS',
   'currentGate':'STRUCTURE_APPLIED; ROUTING_REFERENCE_AND_FULL_COMPLETION_OPEN'},
  {'issueID':'JK52_STACK_LEGACY','newObservation':'Legacy L3_GND still describes original b019/J55 identities; current new-stack SHA is a separate real L3_V3V3 product',
   'currentGate':'NEWSTACK_SEPARATE_IDENTITY_NOT_RETROACTIVE_CLOSURE'},
  {'issueID':'JK53_STACK_LEGACY','newObservation':'Old L3_GND reference sampling cannot certify new L3_V3V3 bottom-layer return',
   'currentGate':'NEWSTACK_REFERENCE_RETURN_REVIEW_REQUIRED'},
  {'issueID':'JK57-006','newObservation':'New identity-bound assembly CSV copies now reference the actual changed stack board',
   'currentGate':'IDENTITY_REBOUND; MANUFACTURING_AND_HARDWARE_APPROVAL_OPEN'}],
 'HSEChange':'Old quiet L2 island/void retired for continuous L2 application GND. Deleting the old anchor no longer isolates it. Do not inherit former single-anchor HSE proof as current topology.',
 'stillOpen':['7 GPIO joins','USB4 constraints/field solver and whole-board fresh DRC',
              'BOTTOM return to L3 power and actual V3V3-GND decoupling path; transitions, SI/PI/EMI',
              'fabricator-approved impedance, mask bridges, stencil/assembly process and MPN/pickup-angle mapping',
              'K59 physical measurements'],
 'factoryApproval':False,'sealedSourcesModified':False}
write_json(SUPPLEMENT,supplement)
NOTE.parent.mkdir(parents=True,exist_ok=True)
NOTE.write_text('''# 鏂板洓灞傚疄闄呮爤鐨勮閰嶈韩浠借ˉ鍏咃紙2026-10-23锛?
鏈ˉ鍏呯粦瀹?`JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd`锛孲HA256 `'''+BOARD_SHA+'''`銆傚疄闄呭眰鍚嶄粛鏄?**TOP-L2-L3-BOTTOM**锛汱2鍏卞湴銆丩3宸插疄浣淰3V3锛岀嫭绔嬬粨鏋勫鏌ラ€氳繃銆傛湰娆℃病鏈夊惎鍔–adence锛屽彧瀹″師鐢熸柊杩涚▼璇诲洖骞剁敓鎴愮嫭绔嬭閰嶅壇鏈€傛棫J55鍙婃斁琛岄棬妲涘皝瀛樿褰曚繚鎸佸師韬唤鍜屽師鐘舵€併€?
瀵规棫J55_4L閫愰」鏍稿锛?0浠秗ef/package/pose銆?72鐢垫皵pin銆?78鍚満姊板瓟鐨勫疄闄卲in璁板綍銆?47瀹炰緥鏂囧瓧鍙?73灏佽鍑犱綍璁板綍瀹屽叏鐩稿悓銆?47鏂囧瓧鍚?40涓笁鏂囧瓧鐩爣鍜?涓寘瑁呬笣鍗版枃瀛楋紱80涓狿laceBound shape楂樺害涓?2涓敤鎴?mm榛樿銆?涓師鏄惧紡鍊间繚鐣欙紝鍙?涓猯egacy path淇濇寔銆傚瓧浣?鏃嬭浆/闀滃儚/浣嶇疆瀛楁鍧囨湭鏀瑰彉銆?
80浠禫ALUE鐢辨柊鏃т袱鏉跨殑鍘熺敓instance/compdef灞炴€т笌瀹樻柟`axlWriteDeviceFile`鐨刞PACKAGEPROP VALUE`鍙岄噸鏍稿锛岄€愪欢涓嶣OM鐩稿悓锛涙病鏈変粠璁惧鏂囦欢鍚嶆垨deviceType鎷煎啓鎺ㄦ祴鍊笺€傚皝瑁呭師鐐瑰潗鏍囥€佸師鐢熸棆杞強pin1瀹為檯鍧愭爣淇濇寔锛屽伐鍘傛棆杞户缁┖鐧斤紝涓嶆妸灏佽鍘熺偣璁や綔宸叉牳鍑嗗惛鍙栦腑蹇冦€?
[鏂拌閰嶅寘](../examples/lessonJK_51_59_20261022/assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/)鍚?0浠禕OM銆?6缁凚OM銆?0浠跺潗鏍囥€?5涓猄MT鍊欓€夊拰15涓潪SMT/DNP椤广€傞櫎3浠藉潗鏍囩被CSV鐨勬簮鏉縎HA澶栵紝瀛楁涓庢棫鍖呬竴鑷达紱BOM鐢╗source_identity.json](../examples/lessonJK_51_59_20261022/assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/source_identity.json)鍜屾柊娓呭崟缁戝畾姝ゆ澘銆?8浠朵粛闇€閲囪喘閫夊瀷锛?涓狽PTH鏈烘瀛斾笉璁′负BOM鍏冧欢銆?
鏂癓2杩炵画鍏卞湴宸叉浛浠ｆ棫鎸崱鍣ㄧ嫭绔嬪矝/void锛屾棫anchor鍒犻櫎鍚庝粛鍏卞湴锛屾棫鍗昦nchor闅旂缁撹涓嶅啀閫傜敤銆侺3浠嶨ND鏀筕3V3涔熸敼鍙楤OTTOM鍙傝€冿細鏂版爤缁撴瀯閫氳繃涓嶈兘鏇夸唬鐪熷疄鍥炴祦/鍘昏€︺€乁SB/SI/PI/EMI璇勫銆備粛鏈?涓狦PIO杩炴帴锛孶SB4涓庡畬鏁碊RC寰呴獙鏀讹紱闃荤剨妗ャ€侀挗缃戙€丏NP寮€鍙ｃ€佹彃瑁?瀹炵墿楂樺害銆佸伐鍘傛棆杞瓑寮€鏀鹃」缁х画淇濈暀銆傚叏閮ㄨ緭鍑哄潎涓?**TRAINING_NOT_FOR_ASSEMBLY**锛屼笉鑳芥姇浜с€?
渚濇嵁瑙乕瑁呴厤韬唤閫愰」瀹¤](../examples/lessonJK_51_59_20261022/audits/jk_newstack4L_assembly_identity_review.json)銆乕鏂版爤鐙珛缁撴瀯鎶ュ憡](../examples/lessonJK_51_59_20261022/review/independent_newstack/review.json)銆乕鏂拌韩浠芥斁琛岄棬妲涜ˉ鍏匽(../examples/lessonJK_51_59_20261022/audits/jk_release_gate_newstack4L_supplement_20261023.json)鍙奫鏈ˉ鍏匰HA娓呭崟](../examples/lessonJK_51_59_20261022/audits/jk_newstack4L_identity_manifest.json)銆傚師J55娓呭崟鍜屽師77椤归棬妲涙湭鏀瑰啓銆?''',encoding='utf-8')
# Validate links and blank-vs-zero/CSV field semantics without producing an unsolicited XLSX.
write_json(AUDIT,{'status':'BUILDING_NEW_IDENTITY_AUDIT_NOT_RELEASED'})
links=re.findall(r'\]\(([^)]+)\)',NOTE.read_text(encoding='utf-8'))
for link in links:
    if link.endswith('jk_newstack4L_identity_manifest.json'): continue
    check('note_link_'+link,(NOTE.parent/link).resolve().exists())
check('protected_inputs_unchanged',all(sha(Path(p))==h for p,h in pre_write.items()), files=len(pre_write))
write_json(AUDIT,{
 'status':'PASS_ASSEMBLY_IDENTITY_ONLY_TRAINING_NOT_FOR_ASSEMBLY', 'board':str(BOARD),'sha256':BOARD_SHA,
 'checks':len(checks),'failed':sum(not x['pass'] for x in checks),'details':checks,
 'nativeVALUEPerRef':value_new,'identity':identity,
 'CSVSkillBoundary':'CSV source/reference/field-count/reload/blank-vs-zero checks; no Excel formulas or workbook created.',
 'protectedInputCount':len(pre_write),'physicalStackChangeReviewedBy':str(REVIEW),
 'assemblyGeometryChanged':False,'copperAndReferencesSameAsOldStack':False,
 'wholeBoardOrFactoryAcceptance':False})
outputs=[*OUT.glob('*'),AUDIT,SUPPLEMENT,NOTE,Path(__file__),*(J/'audits/newstack4L_identity_build_history').glob('*')]
write_json(MANIFEST,{
 'status':'NEWSTACK4L_IDENTITY_SUPPLEMENT_TRAINING_NOT_RELEASED', 'createdUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'boardSHA256':BOARD_SHA, 'checks':len(checks), 'failed':0,
 'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in outputs if p.is_file()],
 'sources':[{'path':p,'sha256':h} for p,h in sorted(sources.items())],
 'sealedJ55AndReleaseGateSourcesUnchanged':True,
 'scope':'Separate identity-only assembly supplement after new-stack independent PASS. Does not close seven GPIO, USB4/full DRC, SI/PI, fab approval or K59.'})
assert all((NOTE.parent/link).resolve().exists() for link in links), 'Final note links'
print(json.dumps({'status':'PASS','checks':len(checks),'failed':0,'protectedInputs':len(pre_write),'outputs':len(outputs),
 'assembly':str(OUT),'note':str(NOTE),'manifest':str(MANIFEST)},ensure_ascii=False))
