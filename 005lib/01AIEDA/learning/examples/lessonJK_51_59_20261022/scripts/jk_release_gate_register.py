"""New JK release-gate view. Preserve every inherited issue status/payload; never modify sealed reviews."""
from pathlib import Path
import json,csv,hashlib,datetime,collections,re
R=Path('D:/001DIY/005lib/01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';NOTE=R/'learning/notes/lessonJK_release_gate_20261023.md'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def writejson(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat();sources={};entries=[]
protected=[J/'audits/j51_54_artifact_manifest.json',J/'audits/j55_57_artifact_manifest.json',J/'audits/j51_54_issues.json',J/'audits/j51_54_issues.csv',J/'audits/j55_57_issue_registry.json',R/'learning/notes/lessonJK_51_54_20261022.md',R/'learning/notes/lessonJK_55_57_20261022.md'];before={str(p):sha(p) for p in protected}
def source(p):
 p=Path(p).resolve();assert p.is_relative_to(R.resolve());key=str(p)
 if key not in sources:sources[key]=dict(path=key,bytes=p.stat().st_size,sha256=sha(p))
 return sources[key]
def evidence_refs(raw,parent):
 result=[]
 for s in raw if isinstance(raw,list) else []:
  if not isinstance(s,str):continue
  candidates=[parent/s,J/s]
  found=next((p for p in candidates if p.is_file()),None)
  result.append(dict(originalReference=s,resolved=source(found) if found else None))
 return result
sets=[('J51_54',J/'audits/j51_54_issues.json','id','nature'),('J55_57',J/'audits/j55_57_issue_registry.json','issueID','status')]
inheritedByID={}
for group,p,idkey,statuskey in sets:
 obj=read(p);ss=source(p)
 for i,q in enumerate(obj['issues']):
  id=q[idkey];assert id not in inheritedByID;inheritedByID[id]=q
  entries.append(dict(stableID=id,recordType='INHERITED_SOURCE_RECORD',sourceGroup=group,lesson=q.get('lesson'),variant=q.get('variant','BOTH_OR_PER_SOURCE_EVIDENCE'),title=q['title'],status=q[statuskey],sourceStatusField=statuskey,sourceStatusValue=q[statuskey],sourcePriority=q.get('priority'),source=ss,sourceJSONPointer='/issues/'+str(i),sourceEvidenceReferences=evidence_refs(q.get('evidence',[]),p.parent),originalIssue=q,releaseInterpretation='Inherit original source status. Evidence-verified or locally closed is not overall manufacturing/lesson completion approval.'))
assert len(entries)==71 and len(inheritedByID)==71
cpaths={v:J/f'review/independent_CAM_J55/{v}/report.json' for v in ['2L','4L']};cppaths={v:J/f'review/companion_and_J55_CAM/{v}/report.json' for v in ['2L','4L']};cams={v:read(p) for v,p in cpaths.items()};companions={v:read(p) for v,p in cppaths.items()}
for v in ['2L','4L']:
 assert not cams[v]['failed'] and not companions[v]['failures']
 assert cams[v]['passed']==(77 if v=='2L' else 85)
 assert companions[v]['passed']==(22 if v=='2L' else 24)
 assert [x['film'] for x in companions[v]['changedOriginalFilms']]==['PDFTOP']
 assert len(companions[v]['companionFilms'])==3 and companions[v]['nativeTextInstanceCountPerRequestedLayer']==80
 assert all(Path(x['file']).is_file() and sha(Path(x['file']))==x['sha256'].upper() for x in companions[v]['companionFilms'])
# The six gates below are new assessment entries; original records above are left verbatim.
def gate(id,title,status,priority,lesson,variant,paths,evidence,nextAction,acceptance,related=()):
 ss=[source(p) for p in paths]
 item=dict(stableID=id,recordType='ADDITIONAL_RELEASE_OR_COMPLETION_GATE',sourceGroup='JK_RELEASE_GATE_20261023',lesson=lesson,variant=variant,title=title,status=status,sourceStatusField='NEW_GATE_STATUS',sourceStatusValue=status,sourcePriority=priority,source=ss[0],sourceJSONPointer='',sourceEvidenceFiles=ss,evidence=evidence,nextAction=nextAction,nextAcceptance=acceptance,relatedStableIDs=list(related),releaseInterpretation='Training evidence may pass while this manufacturing/completion gate remains open.')
 entries.append(item)
gate('K56_TEMPLATE_TEXT','三文字伴随Film已出，原模板未自动包含全部文字','COMPANION_EXPORT_VERIFIED_TEMPLATE_HANDOFF_OPEN','BLOCKS_RELEASE',56,'2L+4L',list(cpaths.values())+list(cppaths.values())+ [J/'audits/j55_corrected_independent_summary.json'],dict(correctedCAMPassed={'2L':77,'4L':85},perFilmActualGeometryChecksPassed={'2L':22,'4L':24},changedOriginalFilms=['PDFTOP'],allOtherOriginalFilmGeometryUnchanged=True,originalSKILTOP=['PACKAGE GEOMETRY/SILKSCREEN_TOP'],originalPDFTOP=['REF DES/ASSEMBLY_TOP','PACKAGE GEOMETRY/SILKSCREEN_TOP','BOARD GEOMETRY/OUTLINE'],companionFilms={v:[{k:x[k] for k in ['file','sha256','headerLayers','objects']} for x in companions[v]['companionFilms']] for v in ['2L','4L']},nativeInstancesPerRequestedLayer=80,strokeObjectsAreNotTextCount=True,originalTemplateChanged=False),'生产包须明确纳入三份补充图或经批准形成完整输出约定；原01env/主15或17Film保持。','最终生产包目录、三文字class映射、源BRD SHA和对应独立CAM/目视核对一致；不能只发原SKILTOP就称REF丝印齐全。',['JK55-001','JK55-002','JK57-003','JK57-005','JK56-TEMPLATE-TEXT'])
logs=[J/f'exports/J55_corrected_{v}_TRAINING_NOT_FOR_FAB/photoplot.log' for v in ['2L','4L']]
ood=[]
for v,p in zip(['2L','4L'],logs):
 text=p.read_text(encoding='utf-8-sig',errors='replace');matches=[line for line in text.splitlines() if 'DRC_OUT_OF_DATE' in line.upper() or ('DRC' in line.upper() and 'OUT OF DATE' in line.upper())];ood.append(dict(variant=v,source=source(p),warningLines=matches));assert matches
summaryPath=J/'audits/j51_54_summary.json';jsummary=read(summaryPath)
gate('K56_NATIVE_OOD','原生光绘有DRC_OUT_OF_DATE，整板当前检查待完成','OPEN_NATIVE_OOD_AND_WHOLE_BOARD_DRC','BLOCKS_RELEASE',56,'2L+4L',logs+[summaryPath]+list(cpaths.values()),dict(nativePhotoplotWarnings=ood,wholeBoardDRC={v:cams[v]['wholeBoardDRC'] for v in cams},boardConnectionComplete={v:cams[v]['boardConnectionComplete'] for v in cams},filesDecodeSuccessfully=True),'完成剩余布线/铜更新/实际原生检查和问题闭环，再从最终源版重出CAM。','最终原生更新检查有明确通过/处置记录、实际连接完成；新制造包绑定该版SHA，OOD原因关闭。',['JK51-002','JK51-003'])
gate('K58_FULL_TWO_BOARD_COMPLETION','两套完整PCB工程尚未综合结课','NOT_COMPLETE_TWO_BOARDS','BLOCKS_COMPLETION',58,'2L+4L',[summaryPath,J/'audits/j51_all69_net_matrix.json',J/'audits/j55_corrected_independent_summary.json'],dict(currentReviewBasis='b019 lineage and J55 instance-corrected copies',sevenGPIOJoinsPerBoard=jsummary['sevenUnconnectedPerBoard'],wholeBoardDRCStillNone=jsummary['wholeBoardDRCStillNone'],instanceFix1644ChecksPassed=True,scope='J55 text/height and CAM format success do not complete remaining routing/SI/PI/EMI/manufacturing gates.'),'完成13课程遗留的7GPIO网/板、USB及整板DRC、真实回路/参考与工艺问题闭环，并形成两套源和输出一致的版本包。','两板需求→库→原理图→PCB→BOM/坐标/CAM全链可复现且最终电气/几何/制造验收有证据。',['K56_NATIVE_OOD','K4L_NEW_STACK_REQUIRED'])
ecoPath=J/'eco/DE_REPLAY_ONLY/native_replay_result.json';eco=read(ecoPath)
ecoReviewPath=J/'review/independent_K58/review.json';ecoReview=read(ecoReviewPath);assert ecoReview['status']=='PASS_INDEPENDENT_THIS_ROUND_ECO_REPLAY' and ecoReview['checkCount']==1453 and not ecoReview['failed'] and ecoReview['allSource119CopiedAndOriginalFilesUnchanged']
gate('K58_ISOLATED_ECO_REPLAY','隔离DE原生ECO示范已通过，完整两板结课仍开放','VERIFIED_ISOLATED_ECO_REPLAY_NOT_FULL_BOARD_COMPLETION','INFO',58,'DE_REPLAY_ONLY',[ecoReviewPath,ecoPath,J/'eco/expected_delta.json',J/'eco/replay_input_manifest.json'],dict(independentStatus=ecoReview['status'],independentChecks=ecoReview['checkCount'],independentFailures=ecoReview['failed'],actualNativeValueMethod=ecoReview['actualNativeValueMethod'],allSource119Unchanged=ecoReview['allSource119CopiedAndOriginalFilesUnchanged'],actualPinChanges=ecoReview['actualPinChanges'],actualValueChanges=ecoReview['actualNativeValueChanges'],nativeProcessReportStatus=eco['status'],output=eco['output'],outputSHA256=eco['outputSHA256'],allProtectedOriginalsAndCopiesUnchanged=eco['allProtectedOriginalsAndCopiesUnchanged'],processes=[dict(stage=x['tag'],exitCode=x['exitCode'],pid=x['pid']) for x in eco['runs']],scope='Imported/unplaced DE replay. Not a routed J55 two-board ECO and not proof that current two boards are complete.'),'保留本轮1453项独立比对和受保护119源身份；任何应用到真实已布线板的新ECO须重新完整验收。','本轮已确认80件/272针/69网/6NC/placed0，仅2个VALUE+2个PIN变化；通过范围限定隔离未布局DE示范，不关闭完整两板门槛。',['K58_FULL_TWO_BOARD_COMPLETION'])
benchPaths=[J/f'bench/{v}_bench_plan.json' for v in ['2L','4L']];bench={v:read(p) for v,p in zip(['2L','4L'],benchPaths)}
for v,d in bench.items():assert all(x['measurement'] is None and x['result']=='NOT_RUN' for x in d['points'])
gate('K59_NOT_RUN','打样、限流上电与功能测量尚未执行','NOT_RUN_PHYSICAL_MEASUREMENTS','BLOCKS_PHYSICAL_CLOSURE',59,'2L+4L',benchPaths+[J/f'bench/{v}_measurement_sheet_NOT_RUN.csv' for v in ['2L','4L']],dict(planStatus={v:d['status'] for v,d in bench.items()},measurementPoints={v:len(d['points']) for v,d in bench.items()},actualMeasuredPoints=0,initialCurrentLimitA={v:d['initialCurrentLimitA'] for v,d in bench.items()},pointsAreCertifiedTestPoints=False,scope='Test plans and probe candidates only; no physical board, instrument readings or hardware change closure is claimed.'),'取得符合批准版本的实物及装配/上电前检查，基于真实启动和负载预算确定限流，再记录供电/时钟/复位/下载/接口测量。','仪器、负载/线缆/环境、预期与实测值、波形/故障/回改版本可追溯；测量不得只写模拟PASS。',['JK55-009'])
stackPaths=[J/'audits/j52_53_fourlayer_default_application_review.json',J/'audits/j52_53_newstack_native_contract.json',J/'review/user_four_layer_function_rule_20261022.json']
gate('K4L_NEW_STACK_REQUIRED','新四层TOP/L2完整GND/L3电源/BOTTOM尚待最终验证','OPEN_NEW_STACK_NATIVE_AND_REFERENCE_REVIEW','BLOCKS_COMPLETION',52,'4L',stackPaths,dict(required=dict(TOP='components/signals',L2='continuous GND',L3='power',BOTTOM='signals'),fixedLayerNames=['TOP','L2','L3','BOTTOM'],latestSealedJ55Role='LEGACY_L2_GND_L3_GND',newNativeWork='Preparation/approval retry per parent update; no completed new-stack native/fresh evidence consumed by this register',legacyReviewsAutomaticallyClose=False,L2SignalBridge95='HISTORICAL_COMPARISON_NOT_ADOPTED'),'消费新板真实L3电源域/馈电/负载、L2实际连续地、BOTTOM参考/换层去耦和全铜/端点/规则/fresh/CAM证据后再逐项评审。','独立实铜与回流复核通过并绑定新板SHA；保持原层名/原模板，不将旧L3_GND投影/共地结果套作L3电源版合格。',['JK52_STACK_LEGACY','JK53_STACK_LEGACY','JK57-006'])
assert len(entries)==77 and len({e['stableID'] for e in entries})==77
statusCounts={group:dict(collections.Counter(e['sourceStatusValue'] for e in entries if e['sourceGroup']==group)) for group,_,_,_ in sets}
result=dict(status='TRAINING_REVIEW_COMPLETE_PRODUCTION_AND_FULL_COURSE_RELEASE_NOT_APPROVED',createdUTC=now,scope='New derived register only. Original J51-54/J55 issue files, sealed manifests, notes and CAD are unchanged. Each inherited payload/status is retained exactly; source nature versus status is explicit.',counts=dict(total=77,inherited=71,sourceJ51_54=54,sourceJ55_57=17,additionalGates=6,sourceStatusCounts=statusCounts),courseCompletion=dict(fullTwoBoardConclusion=False,manufacturingRelease=False,physicalMeasurementRun=False,sourceSnapshotMeaning='Evidence and local fixes completed; unresolved gates remain. New4L work is not prematurely closed.'),entries=entries,sourceFiles=list(sources.values()))
jsonPath=J/'audits/jk_release_gate_register.json';csvPath=J/'audits/jk_release_gate_register.csv';writejson(jsonPath,result)
fields=['Stable_ID','Record_Type','Source_Group','Lesson','Variant','Source_Status_Field','Source_Status_Value','Source_Priority','Title','Source_File','Source_SHA256','Source_JSON_Pointer','Evidence_References_JSON','Next_Action','Next_Acceptance','Release_Interpretation'];csvRows=[]
for e in entries:
 q=e.get('originalIssue',{})
 csvRows.append(dict(Stable_ID=e['stableID'],Record_Type=e['recordType'],Source_Group=e['sourceGroup'],Lesson=e['lesson'] if e['lesson'] is not None else '',Variant=e['variant'],Source_Status_Field=e['sourceStatusField'],Source_Status_Value=e['sourceStatusValue'],Source_Priority=e['sourcePriority'] or '',Title=e['title'],Source_File=e['source']['path'],Source_SHA256=e['source']['sha256'],Source_JSON_Pointer=e['sourceJSONPointer'],Evidence_References_JSON=json.dumps(e.get('sourceEvidenceReferences',e.get('sourceEvidenceFiles',q.get('evidenceByScope',{}))),ensure_ascii=False),Next_Action=q.get('nextAction',e.get('nextAction','')),Next_Acceptance=q.get('nextAcceptance',e.get('nextAcceptance','')),Release_Interpretation=e['releaseInterpretation']))
with csvPath.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(csvRows)
with csvPath.open(encoding='utf-8-sig',newline='') as f:got=list(csv.DictReader(f))
assert len(got)==77 and {r['Stable_ID'] for r in got}=={e['stableID'] for e in entries}
for row,e in zip(got,entries):assert row['Source_Status_Field']==e['sourceStatusField'] and row['Source_Status_Value']==e['sourceStatusValue'] and row['Source_SHA256']==e['source']['sha256']
for e in entries:
 if e['recordType']=='INHERITED_SOURCE_RECORD':assert e['originalIssue']==inheritedByID[e['stableID']]
for p,s in before.items():assert sha(p)==s,p
for s in sources.values():assert sha(s['path'])==s['sha256'],s['path']
note='''# J/K 结课与生产门槛登记

2026-10-23。本文件只汇总已取得证据和仍需满足的门槛；未执行Cadence、未改原问题或封存清单。当前完整两板结课、生产释放、实物测量均未通过。

[JSON登记](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_register.json) 与 [CSV登记](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_register.csv) 共77条：J51—54来源54条、J55/57来源17条、新门槛6条。每条保原ID、原完整payload、来源路径/SHA和JSON位置；J51—54原状态字段叫nature，J55/57叫status，CSV明确分列，未私自重写原状态。77条包含已验证事实、已闭环实例问题和开放问题，数量不等于77个待修缺陷。

J55三文字/原点/缺省高度的JK55-001/002/003已由两板实际保存、fresh和1644项独立检查关闭；原71条中的其它状态保持来源。BOM/坐标是TRAINING_NOT_FOR_ASSEMBLY，68件采购及工厂吸取/角度等仍待定。

| 新门槛 | 当前证据和未完成条件 |
| --- | --- |
| K56_TEMPLATE_TEXT | 修正CAM两板独立77/85项通过；逐Film22/24项通过，仅PDFTOP目标文字几何改变，其他原Film几何完全相同。每板另3份非空MM3.6伴随图，分别映射80个原生REF丝印/REF装配/VALUE装配实例。原SKILTOP只含PACKAGE GEOMETRY丝印，PDFTOP未含VALUE装配，最终生产包必须明确纳入补充图或另经批准的完整约定。 |
| K56_NATIVE_OOD | 实际photoplot.log保留DRC_OUT_OF_DATE；USB/整板当前检查和剩余连接待完成。CAM可解析不代表已消除OOD。 |
| K58_FULL_TWO_BOARD_COMPLETION | 两板现有审查谱系各7个GPIO连接待做，完整源→PCB→输出及SI/PI/EMI/制造门槛尚未闭环。 |
| K58_ISOLATED_ECO_REPLAY | DE未布局工程已在隔离目录原生netrev重演并fresh，本轮独立1453项/0失败；devfile VALUE与原生compdef双核、80/272/69/6NC/placed0，仅2个VALUE+2个PIN变化，119源保持。该示范通过，与完整两套已布线板结课分开。 |
| K59_NOT_RUN | 两板各17个候选测点、共34项实际测量均NOT_RUN/null；限流值未擅填，候选pad未认证为量产测试点。下一步须有合格实物、仪器和可追溯记录。 |
| K4L_NEW_STACK_REQUIRED | 新推荐固定TOP-L2-L3-BOTTOM，L2完整GND/L3电源；原J55仍历史L2/L3 GND。新四层仍在准备/审批重试，本登记尚未消费原生完成证据，因此旧栈问题保持开放，不能提前关闭。 |

每个门槛的来源文件和SHA见登记内sourceEvidenceFiles；原问题的当前状态、优先级、下一步及验收条件保留完整。来源证据更新或新四层完成后，只对这份派生登记建立新版/新快照，不回写旧sealed审查。更新记录还需重新核来源SHA、CSV行数/状态、源payload逐项一致及旧文件未改。

[生成/重读验证](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_validation.json) 和 [独立清单](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_manifest.json) 提供复现与完整性记录，脚本是scripts/jk_release_gate_register.py。此汇总保留软件训练、完整工程结课和生产/实物验收各自的证据边界。
'''
NOTE.write_text(note,encoding='utf-8');links=re.findall(r'\[[^\]]+\]\(([^)]+)\)',note)
validationPath=J/'audits/jk_release_gate_validation.json';manifestPath=J/'audits/jk_release_gate_manifest.json'
validation=dict(status='PASS_NEW_DERIVED_REGISTER_DATA_VALIDATION',createdUTC=now,sourcePayloadsPreserved=71,CSVReloadRows=len(got),uniqueStableIDs=77,originalSourceStatusFieldsAndValuesPreserved=True,allSourceHashesStillMatch=True,protectedSealedFilesBeforeAfter=[dict(path=p,sha256=s,unchanged=sha(p)==s) for p,s in before.items()],noCadenceExecuted=True,noOriginalIssueOrManifestModified=True,manufacturingRelease=False)
writejson(validationPath,validation)
outputs=[jsonPath,csvPath,validationPath,NOTE,J/'scripts/jk_release_gate_register.py'];manifest=dict(status='DERIVED_RELEASE_GATE_REGISTER_ONLY_NOT_PRODUCTION_RELEASE',createdUTC=now,files=[dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for p in outputs],sources=list(sources.values()),protectedInputsBeforeAfterUnchanged=before);writejson(manifestPath,manifest)
for l in links:assert (NOTE.parent/l).exists(),l
for x in manifest['files']+manifest['sources']:assert sha(x['path'])==x['sha256']
print(json.dumps(dict(totalEntries=77,inheritedIssues=71,newGates=6,sourceFiles=len(sources),CSVReload='PASS',sourcePayloadAndStatus='71 EXACT',sealedFilesUnchanged=len(before),outputsManifestFiles=len(outputs),localNoteLinks=len(links)),indent=2))
