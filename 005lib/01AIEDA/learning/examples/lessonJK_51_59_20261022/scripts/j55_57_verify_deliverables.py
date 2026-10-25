"""Verify saved flat CSVs and write provenance, assembly contract, and read-only ECO replay reference."""
from pathlib import Path
import json,csv,hashlib,collections,math
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';H=R/'learning/examples/lessonHI_38_50_20261021';D=R/'learning/examples/de_15_26_20261019';sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();load=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
for v in ['2L','4L']:
 S=load(H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING/normalized.json');ps={p['ref']:p for p in S['placements']}
 def ck(label,ok,detail=None):checks.append(dict(variant=v,label=label,passed=bool(ok),detail=detail))
 def rows(f):return list(csv.DictReader((J/f'assembly/{f}').open(encoding='utf-8-sig',newline='')))
 bom=rows(f'BOM_80_{v}_b019_TRAINING.csv');grp=rows(f'BOM_grouped_{v}_b019_TRAINING.csv');co=rows(f'coordinates_all80_{v}_b019_TRAINING.csv');sm=rows(f'SMT_candidates_{v}_b019_TRAINING.csv');exc=rows(f'non_SMT_and_DNP_{v}_b019_TRAINING.csv')
 ck('BOM has80 unique real components',len(bom)==len({q['Reference'] for q in bom})==80 and {q['Reference'] for q in bom}==set(ps));ck('grouped BOM sums to80',sum(int(q['Quantity']) for q in grp)==80);ck('all80 coordinate IDs exactly cover BOM',{q['Reference'] for q in co}==set(ps));ck('SMT65 + excluded15 exact partition',len(sm)==65 and len(exc)==15 and {q['Reference'] for q in sm}.isdisjoint({q['Reference'] for q in exc}) and {q['Reference'] for q in sm+exc}==set(ps))
 ck('DNP onlyR12/R13 in USB profile',{q['Reference'] for q in bom if q['Assembly_USB']=='DNP'}=={'R12','R13'});ck('THT13 includes12headers plusC1',{q['Reference'] for q in bom if q['Process']=='THROUGH_HOLE'}=={f'J{i}' for i in range(1,14) if i!=2}|{'C1'});ck('J2 mixed process retained',next(q for q in bom if q['Reference']=='J2')['Process']=='MIXED_SMD_PTH');ck('12MPNs specified and68pending',sum(bool(q['MPN']) for q in bom)==12 and sum(q['Procurement_Status']=='SPEC_ONLY_PROCUREMENT_PENDING' for q in bom)==68)
 for q in co:
  p=ps[q['Reference']];ck(q['Reference']+' coordinate/rotation/case/side exact',float(q['X_mm'])==p['xy'][0] and float(q['Y_mm'])==p['xy'][1] and float(q['CAD_Rotation_deg'])==p['rotation'] and q['Package']==p['package'] and q['Side']=='TOP' and not p['mirrored'])
 ck('factory rotation left unavailable',all(q['Assembly_Factory_Rotation_deg']=='' for q in co));ck('all rows training marked',all(q['Status']=='TRAINING_NOT_FOR_ASSEMBLY' for q in bom+grp+co+sm+exc));ck('NPTH six separate and excluded',load(J/f'assembly/mechanical_NPTH_{v}_b019_TRAINING.json')['count']==6)
assert all(c['passed'] for c in checks);dump(J/'audits/j57_csv_roundtrip_validation_b019.json',dict(status='PASS_TRAINING_CSV_RELOAD_NOT_FACTORY_APPROVAL',checks=len(checks),passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),details=checks))
raw=load(J/'audits/j55_57_issues_b019.json')['issues'];merged={}
for i in raw:
 key=i['issueID']
 if key not in merged:merged[key]={k:v for k,v in i.items() if k not in ['scope','evidence']};merged[key]['evidenceByScope']={}
 merged[key]['evidenceByScope'][i['scope']]=i['evidence']
def issue(id,title,evidence,action):merged[id]=dict(issueID=id,title=title,status='OPEN_RELEASE',evidenceByScope={'BOTH':evidence},nextAction=action)
issue('JK55-004','丝印文字到开窗仍须真实字形审核',{'b019TextBBoxCandidatesPerBoard':190,'bboxIntersectionsAreNotInkViolations':True},'三文字按用户原点修正后重新审核实际Gerber字形；不擅自挪到器件外侧。')
issue('JK55-010','LDO电容附近阻焊窄桥及定位孔开窗',{'C8_2_to_U3_2_3_and_C9_2_to_U3_4_BBoxLowerBoundMM':.0635,'roundedRectangleRadiusAvailable':False,'J2_NPTH_to_GND_nominalWebMM':.075,'source':'j55_{v}_nominal_mask_web_under025_b019.csv'},'比较真实SOLDTOP fullContact后开窗、圆角和最小桥工艺；不能把包围框下界冒称实际字形/阻焊已失败或通过。')
issue('JK55-011','继承丝印字体低于JLC所选公开高度',{'officialSource':str(R/'learning/examples/lesson28_stackup_20261019/source/jlc_capabilities_20261019.txt'),'sourceLineRange':'345..361','minimumTextHeightMM':1.0,'minimumLineWidthMM':.15,'padToSilkscreenMM':.15,'CADFonts':'Real35TEXTBLOCK parameters retained; common0.508/0.635/0.7874mm; photoWidth0 is native inherited behavior, not assumed zero ink.'},'本次保持字体实现来源一致；制造版另行决定字体/原点重叠与工厂细字能力，不能把1mm器件缺省高度当文字高度。')
issue('JK57-004','CAD符号原点不是已核准的吸取中心',{'coordinateMeaning':'unchanged native symbol origin','nonCentredLibraryOrigins':'0603 local pads1=.1016,2=1.6764mm; not symmetric about origin0','factoryAngleMapping':'unavailable'},'以最终选定MPN吸取位置和机器零度作受控转换，保持CAD原始坐标另列，实机首件方向核准。')
issue('JK57-005','三文字同原点不能直接作为可读叠印装配图',{'userConvention':'REFDES ASSEMBLY and VALUE ASSEMBLY both anchor at symbol origin'},'出分别显示REF与VALUE的装配核对视图或与BOM配套；不要为图面清晰擅改用户要求的CAD锚点。')
issue('JK57-006','四层本轮源为L3_GND历史栈',{'currentJ55Source':'LEGACY_4L_L3_GND','newUserPreferredStack':'TOP parts/signals - L2 GND - L3 power - BOTTOM signals','L2SignalBridge95':'HISTORY_ONLY_NOT_ADOPTED'},'本轮文字/高度和制造导出练习保历史铜层身份；真正L3电源层重建、返回和输出必须另行完整验证，不以本次输出冒充新默认实现。')
# Reconcile independently parsed actual artwork; preserve the earlier bbox-only evidence as history.
cam={}
for variant in ['2L','4L']:
 p=J/f'review/independent_CAM/{variant}/actual_mask_stencil_review.json'
 if p.exists():cam[variant]=dict(path=str(p),sha256=sha(p),actual=load(p))
if cam:
 merged['JK55-010']['title']='真实SOLDTOP窄阻焊桥低于所选公开工艺目标'
 merged['JK55-010']['status']='CONFIRMED_GEOMETRY_DFM_RELEASE_OPEN'
 merged['JK55-010']['evidenceByScope']['ACTUAL_GERBER']=cam
 merged['JK55-010']['evidenceByScope']['FACTORY_CONDITIONS']=dict(OSH2L_minBridgeMM=.1016,JLC4L_1oz_colours_green_red_yellow_blue_purple_minMM=.10,JLC4L_blackWhite_1oz_minMM=.13,JLC2oz_minMM=.20,source=str(R/'learning/examples/lesson28_stackup_20261019/source/jlc_capabilities_20261019.txt'))
 merged['JK55-010']['nextAction']='真实Gerber边界C8.2/U3.2=.0635、C9.2/U3.4=.0854268867mm低于所选最低目标；生产前需板厂确认或受控改padmask/位置。保留bbox下界历史，本次只文字高度批不改开窗或公库。'
 merged['JK55-007']['evidenceByScope']['ACTUAL_STENCIL']=dict(R12_1=1,R12_2=1,R13_1=1,R13_2=1,source='independent_CAM actual_mask_stencil_review.json')
freshPath=J/'audits/j55_corrected_independent_summary.json'
if freshPath.exists():
 fresh=load(freshPath)
 if fresh.get('bothVariantsReviewed') and fresh.get('failed')==0:
  for id in ['JK55-001','JK55-002','JK55-003']:
   merged[id]['status']='CLOSED_JK_INSTANCE_CORRECTION_FRESH_VERIFIED'
   merged[id]['evidenceByScope']['JK_FRESH']=dict(report=str(freshPath),sha256=sha(freshPath),checks=fresh['checks'],variants=fresh['variants'])
   merged[id]['nextAction']='本轮JK实例已整改并独立fresh验收；公共库不改，未来refresh/ECO需复核。'
dump(J/'audits/j55_57_issue_registry.json',dict(status='TRAINING_NOT_FOR_ASSEMBLY',issues=list(merged.values()),course55='TRAINING_INSTANCE_CORRECTION_FRESH_PASS; MANUFACTURING_RELEASE_OPEN',course57='TRAINING_CSV_RELOAD_AND_CURRENT_BOARD_IDENTITY_PASS; FACTORY_MAPPING_OPEN'))
F=D/'native_flow_final';flow=load(F/'flow_result.json');steps=flow['nativeProcesses'];srcfiles=[R/'learning/scripts'/f for f in ['de_apply_eco.tcl','de_eco_spec_attributes.tcl','de_verify_eco.tcl','de_prepare_eco.py']]+[F/'flow_result.json',F/'independent_compare.json',F/'feedback/DE_ECO.swp']
dump(J/'eco/K58_DE_native_replay_reference.json',dict(status='READ_ONLY_REPRODUCTION_REFERENCE_NOT_EXECUTED_BY_THIS_AGENT',scope='Replay imported-unplaced DE learning design in JK isolation only; do not netrev routed b019. Existing evidence is historical until new native replay/readback.',exactLogicalDelta=flow['logicalECOChanges'],expected=dict(components=80,physicalPins=272,nets=69,NC=6,placedSymbols=0,noOtherValueOrNetChanges=True),historicalNativeArgs=[dict(stage=x['stage'],args=x['args'],historicalExitCode=x['exitCode']) for x in steps],environment=dict(allWorkAndTemp='JK/eco isolated subdirectory inside01AIEDA',sameDsnBasename='DE_CONTROL.dsn in separate baseline and eco directories',pcbenv='source $TELENV then set task padpath/psmpath; do not replace global environment with two path lines',missingFootprint='netrev -e required'),safeSequence=['Hash source DSNs/OLB/PAD/PSM dependencies and copy only into JK/eco new working dirs. Check source identities against current files, not only historical flow hashes.','If reproducing the source edit, copy/rewrite Tcl outputs to JK paths, initialize GetRootOccurrence before page iterator, require exactly R19/R20 and J13.7/8 changes; update source_description to3.3k1%.','Export actual baseline and ECO DSNs to PST using native pstswp. Require full netlist log success and parse all three actual DAT files.','netrev -n -e -i baseline/netlist NEW_BASELINE.brd; then netrev -e -i eco/netlist NEW_BASELINE.brd NEW_ECO.brd.','Fresh readonly native compare every ref/physical pin/net/package/value. Only four intended logical deltas; MCU45/46 unchanged.','genfeedformat -x -b NEW_ECO.brd -o feedback; pstswp -swp with exact generated PST and fourVIEW; inspect SWP Flags/DesignName-only.','Retain nonfatal absent feedbackview.cdsz diagnostic separately. GUI SWP apply/GUI ERC remain unverified. Hash original inputs unchanged; log PID/args/completion and preserve failures.'],referenceFiles=[dict(path=str(p),sha256=sha(p)) for p in srcfiles]))
print('CSV checks',len(checks),'PASS; stable issues',len(merged),'ECO reference saved')
