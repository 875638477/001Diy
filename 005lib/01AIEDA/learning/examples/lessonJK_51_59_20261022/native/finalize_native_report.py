from pathlib import Path
import hashlib,json,re,csv,collections,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');N=R.parent.parent/'notes/lessonJK_native56_20261022.md';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=N.read_text(encoding='utf-8-sig');s=s.replace('固定铜线/过孔/铜形、原 CSet/net/class/Film/层叠、symdef 与机械数据','过孔/铜形、原 CSet/net/class/Film/层叠、symdef 与机械数据；固定手工线段另由实际 route_geometry/role/CAM 独立对比闭合（见下方空采样勘误）')
s+='''

## 8. 保存后补证与空集合勘误（2026-10-23）

新栈 fresh readonly 完成于 `logs/native_newstack_4L_reopen_01`，输入 SHA 保持 `471176A9...31F3F9`。原生实际 L2 GND 为 1 块共地 fill，56 个真实 GND pin、76 个实际 GND via 共通；L3 V3V3 为 1 块 fill，32 个 V3 pin、3 个 V3 via 共通，无 GND/V3 铜图短路。build 初次填充后有未刷新缓存的 via=0 摘要，不作“全部过孔已核”证据，以 fresh 实际表/图及独立复核为准。

首个 `newstack_reference_samples.tsv` 实际 manualSegments=0/samples=0，**NOT_EVIDENCE，不是零缺失或参考已通过**。其原因是 GetConnect 图返回 path 父对象，而新补 reader 没有递归 `path->segments`。同一缺陷使外层 manual-LINE 子守卫未覆盖实际手工线段，不能沿用“全部线段指纹严格相同”的口头结论。已有原生 `route_geometry.tsv` 与 `hi_route_roles.tsv` 实际包含完整铜段，因此固定铜保真由这些非空数据及 CAM 的独立 multiset 比较闭合，不能靠原空集合判断。

原空表与首次日志原样保留。修正版 `native/native_segments_reader_v2.il` 明确读取 path/cline 的 segments，另行 readonly 导到 `logs/native_newstack_reference_segments_01`：932 个实际总段 = 750 个 manual + 182 个 generated thermal；非 GND 外层 manual 658 段、18,854 个实际中心线样点，步长不超过 0.1 mm，参考网明确 TOP→L2 GND、BOTTOM→L3 V3V3。计数必须非空并与实际 fgeo/role 表核对；中心线采样仍不等于完整线宽足迹/HF 返回通过。没有为补采样修改 BRD 或覆写第一次 fresh。

新栈完整制造训练输出已独立重导到 `exports/newstack_4L_TRAINING_NOT_FOR_FAB`：真实新 17 Film、PTH/NPTH、4 条槽。其参数沿原生已验证格式，只改新文件前缀。L2/L3 文件从新实际铜层产生，不混用旧 legacy GND/GND 文件。真实 artwork rc=1 警告与 NC rc=0 均留存。

三板的实际 VALUE 后又独立只读导到 `exports/devicevalues_J55_2L_TRAINING`、`devicevalues_J55_4L_TRAINING`、`devicevalues_newstack_4L_TRAINING`；每个 ref 的 native device 文件与 compdef 原属性均在，不从 deviceType 后缀或旧 inventory 猜值。主板文字、height、铜、层名和 Film 身份仍不变。
'''
N.write_text(s,encoding='utf8')
boards={}
for label,v,name,read in [('J55_2L','2L','JK_2L_J55_text_height_review_NOT_RELEASED.brd','native_j55_2L_reopen_01'),('J55_4L_LEGACY_L3_GND','4L','JK_4L_J55_text_height_review_NOT_RELEASED.brd','native_j55_4L_reopen_01'),('NEWSTACK_4L','4L','JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd','native_newstack_4L_reopen_01')]:
 p=R/'native'/v/name;boards[label]={'path':str(p),'sha256':sha(p),'freshReadonlyDirectory':str(R/'logs'/read),'components':80,'logicalPins':272,'realNettedPins':266,'NC':6,'nets':69,'actualLayers':['TOP','BOTTOM'] if v=='2L' else ['TOP','L2','L3','BOTTOM'],'filmCount':15 if v=='2L' else 17,'requiredInstanceTexts':240,'allInstanceTextsIncludingPackageMarkings':247,'defaultHeightShapes':72,'preservedExplicitHeightShapes':8,'preservedPlaceBoundPaths':4,'wholeBoardDRC':None,'USB4':'PENDING_UNRESOLVED_SOLVER','remainingUnconnectedGPIO':7}
E=R/'eco/DE_REPLAY_ONLY/DE_ECO_REPLAY.brd';report={'status':'NATIVE_TRAINING_ARTIFACTS_FRESH_READ_COMPLETE_NOT_RELEASED','updatedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'boards':boards,'baselineExports':[str(R/'exports'/f'native_{v}_TRAINING_NOT_FOR_FAB') for v in ['2L','4L']],'correctedExports':[str(R/'exports'/f'J55_corrected_{v}_TRAINING_NOT_FOR_FAB') for v in ['2L','4L']],'companionExports':[str(R/'exports'/f'supplement_{v}_THREE_TEXTS_TRAINING') for v in ['2L','4L']],'newstackExports':str(R/'exports/newstack_4L_TRAINING_NOT_FOR_FAB'),'newstackArchitecture':{'TOP':'components+signals','L2':'actual continuous common GND, no signal bridge','L3':'actual single V3V3 power plane','BOTTOM':'signals with real V3 power reference; HF transition returns remain engineering review','commonGroundPins':56,'commonGroundVias':76,'commonV3Pins':32,'commonV3Vias':3,'actualFilledShapes':{'L2_GND':1,'L3_V3V3':1},'permissionChange':'V3V3-only static copy of P_POWER_060, only L3 allow_etch=true; all original CSet fields retained','oldHSEExpectationRetired':True,'newHSEAnchorDeletionStillCommon':True,'scopedDRC':{'GND':0,'V3V3':0},'wholeBoardDRC':None,'oldEmptySampling':'NOT_EVIDENCE','fixedManualGuardOriginalEmptySubset':'NOT_EVIDENCE_USE_INDEPENDENT_ACTUAL_ROUTE_MULTISET_DIFF','correctedNativeSegmentSupplement':str(R/'logs/native_newstack_reference_segments_01'),'actualSegments':{'all':932,'manual':750,'generatedThermal':182},'actualReferenceSamples':{'nonGroundOuterManualSegments':658,'samples':18854,'maxCenterlineStepMM':0.1,'scope':'native actual common-reference centerline diagnostic; not full-width/HF certification'}},'ECO':{'path':str(E),'sha256':sha(E),'scope':'DE_UNPLACED_REPLAY_ONLY_NOT_HI_NOT_FOR_FAB','changes':['R19 and R20 VALUE 2.2k to 3.3k','J13.7/8 GPIO_PB8/PB9 swap; MCU45/46 unchanged'],'nativeResult':str(R/'eco/DE_REPLAY_ONLY/native_replay_result.json'),'independentReview':str(R/'review/independent_K58/review.json')},'nativeDeviceValueExports':[str(R/'exports'/f'devicevalues_{x}_TRAINING') for x in ['J55_2L','J55_4L','newstack_4L']],'CAMReturnCodes':{'artwork':1,'interpretation':'actual warnings retained: DRC out of date and missing photoplot rectangle, output generated','nctape':0,'ncroute':0},'unmodifiedOriginalGuard':str(R/'native/source_guard.json'),'independentReviews':{'J55':str(R/'audits/j55_corrected_independent_summary.json'),'ECO':str(R/'review/independent_K58/review.json'),'newstack':'PENDING_F28_INDEPENDENT_REPORT'},'limitations':['7 unfinished GPIO nets','4 USB data/shared nets and whole-board DRC unresolved/null','old Film mapping omits required text classes; separate companion Films are review supplements','default height1mm is not actual MPN height','real material/impedance/hardware/EMI qualification pending','BOTTOM V3 plane reference transitions require actual nearby decoupling evaluation, not GND-via distance alone']}
(R/'native/native56_final_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
readme='''# JK native training artifacts

Read `native56_final_report.json` and `../../notes/lessonJK_native56_20261022.md` before replay. These are training copies, not fabrication release. Existing output paths/tags deliberately refuse overwrite.

- Baseline full CAM: `run_native56_v6.py` historical run, outputs `exports/native_*_TRAINING_NOT_FOR_FAB`.
- J55: `prepare_j55_sources.py`, actual `j55_apply_core_v2.il`, `j55_outer.il`, `run_j55.py`; successful2L try06,4L try01, then separate readonly reopen. Original fingerprint's missing path segments is documented; actual route/role/CAM independent comparisons close manual-copper preservation.
- Corrected CAM: `run_j55_cam_serial.py`, launcher v7.
- Three separate text-review Films: `run_companion_serial.py`, launcher v8, generator boards only. Main15/17 mapping remains unchanged.
- Controlled unplaced ECO: `run_eco_replay.py`; read `eco/execute_plan.json` and native replay result. Never use these PSTs for routed HI/J55/newstack boards.
- Actual new layer functions: final `newstack.il`, successful `run_newstack_try03.py`, then `run_newstack_reopen.py`. L2 actual GND/L3 actual V3V3; old HSE disconnection contract retired. No L2 signal permission.
- Corrected nonempty reference/segment supplement: `native_segments_reader_v2.il` and `newstack_segments_read.scr`. Original empty sample is NOT_EVIDENCE and retained.
- Actual native VALUE exports and new-stack full CAM: `run_values_and_newstack_cam.py`, launcher v9 with official readonly mode for read jobs.

All runtime/environment/output paths must remain inside JK. No globalHOME/01env/public library changes. Independent unrelated user GUIs can coexist; never touch their process/window/files. Only one task-owned native process at a time, identity uses PID plus creation/executable/command/task path.
'''
(R/'native/README.md').write_text(readme,encoding='utf8')
print('report',R/'native/native56_final_report.json')
