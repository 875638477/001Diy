from pathlib import Path
import json,hashlib,re,shutil,datetime,html,csv
R=Path(r'D:/001DIY/005lib/01AIEDA');D=R/'learning/examples/de_15_26_20261019';F=D/'native_flow_final';J=R/'learning/examples/lessonJK_51_59_20261022';E=J/'eco';S=E/'source_inputs';O=E/'DE_REPLAY_ONLY'
assert not S.exists(),'source_inputs exists: do not overwrite another preparation'
for name in ['replay_input_manifest.json','expected_delta.json','execute_plan.json']:assert not (E/name).exists(),name
S.mkdir();copied=[];checks=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def ld(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cp(source,target,role):
 source=Path(source);target=S/target;target.parent.mkdir(parents=True,exist_ok=True);assert not target.exists();before=sha(source);shutil.copy2(source,target);assert sha(target)==sha(source)==before
 copied.append(dict(path=str(target),sha256=before,bytes=target.stat().st_size,source=str(source),sourceSHA256=before,role=role,sourceUnchangedAfterCopy=True));return target
flow=ld(F/'flow_result.json');compare=ld(F/'independent_compare.json');originals=list(flow['originalDsnHashesUnchanged'].items());assert len(originals)==2
for i,(p,h) in enumerate(originals):assert sha(p)==h.upper();cp(p,Path('baseline' if i==0 else 'eco')/'DE_ORIGINAL_SOURCE.dsn','Authored input DSN: same hash as historical untouched-original record')
baseline=cp(F/'DE_BASELINE.brd','DE_BASELINE.brd','Only permitted board input: old80component unplaced DE demonstration; never HI routedboard')
assert sha(baseline)==next(x['sha256'].upper() for x in flow['files'] if Path(x['path']).name=='DE_BASELINE.brd')
for case in ['baseline','eco']:
 for name in ['pstchip.dat','pstxprt.dat','pstxnet.dat']:cp(F/case/'netlist'/name,Path(case)/'netlist'/name,'Historical native pstswp output, copied bytes; fresh replay pending')
 for name in ['native_summary.txt','components.tsv','component_pins.tsv']:cp(F/(case+'_readback')/name,Path('historical_readback')/case/name,'Historical native readonly readback, not new replay evidence')
 rows=list(csv.DictReader((F/(case+'_readback')/'components.tsv').open(),delimiter='\t'));assert len(rows)==80 and all(x['placed']=='nil' for x in rows)
for name in ['flow_result.json','independent_compare.json','allegro.cfg']:cp(F/name,Path('historical_flow')/name,'Historical completed flow/compare or config; source command provenance')
for name in ['import_baseline','import_eco','pst_baseline','pst_eco','feedback_view','feedback_swp','baseline_readback','eco_readback']:cp(F/'logs'/name/'launch.json',Path('historical_commands')/(name+'_launch.json'),'Exact completed official executable argv/exitCode from2026-10-19')
for name in ['integrated_circuit.json','integrated_circuit_eco.json']:cp(D/name,Path('logical_specs')/name,'Logical requirement baseline/expectedECO comparison')
for name in ['de_run_native_flow.py','de_compare_native_flow.py','de_native_cli.py','de_board_read.il','de_skill_syntax.py']:cp(R/'learning/scripts'/name,Path('historical_scripts')/name,'Historical source evidence only; relativeROOT/output assumptions require task-local adaptation before execution')
for p in sorted((D/'library').iterdir()):
 if p.is_file() and p.suffix.lower() in ['.pad','.psm','.dra']:cp(p,Path('library')/p.name,'Isolated package/pad dependency copy; public/source library never modified')
doc=Path(r'C:/Program0/Cadence/spb172/doc/ncoms/nchap.html');cp(doc,'official_docs/nchap.html','Installed Cadence17.2 official N Commands, netrev section')
t=doc.read_text(encoding='utf-8');section=t[t.index('<h2><a name="netrev"'):];section=section[:section.find('<!-- [TOPIC_END]')];plain=html.unescape(re.sub('<[^>]+>',' ',section));plain=re.sub(r'\s+',' ',plain);(S/'official_docs/netrev_section_readonly.txt').write_text(plain+'\n',encoding='utf-8')
# Independent PST read: this is not native invocation.
def pst(folder):
 text=(folder/'pstchip.dat').read_text();primitives={}
 for name,body in re.findall(r"primitive '([^']+)';(.*?)end_primitive;",text,re.S):primitives[name]=dict(re.findall(r"([\w_]+)='([^']*)';",body.split('  body',1)[1]))
 parts={ref:primitives[model] for ref,model in re.findall(r"PART_NAME\s+(\S+) '([^']+)':",(folder/'pstxprt.dat').read_text())};pins={};net=None
 for line in (folder/'pstxnet.dat').read_text().splitlines():
  if line=='NET_NAME':net='NEXT';continue
  if net=='NEXT':net=line.strip().strip("'");continue
  m=re.match(r'NODE_NAME\s+(\S+)\s+(\S+)',line)
  if m:pins[tuple(m.groups())]='' if net=='NC' else net
 return parts,pins
bp,bn=pst(S/'baseline/netlist');ep,en=pst(S/'eco/netlist')
assert set(bp)==set(ep) and len(bp)==80 and set(bn)==set(en) and len(bn)==272
pinchanges=[dict(refdes=r,pin=p,before=bn[(r,p)],after=en[(r,p)]) for r,p in sorted(bn) if bn[(r,p)]!=en[(r,p)]]
propchanges=[dict(refdes=r,before=bp[r],after=ep[r]) for r in sorted(bp) if bp[r]!=ep[r]]
assert pinchanges==compare['pinChanges'] and propchanges==compare['propertyChanges']
assert [(x['refdes'],x['pin'],x['before'],x['after']) for x in pinchanges]==[('J13','7','GPIO_PB8','GPIO_PB9'),('J13','8','GPIO_PB9','GPIO_PB8')]
assert [(x['refdes'],x['before']['VALUE'],x['after']['VALUE']) for x in propchanges]==[('R19','2.2k','3.3k'),('R20','2.2k','3.3k')]
for r in bp:assert bp[r]['JEDEC_TYPE']==ep[r]['JEDEC_TYPE']
assert len({v for v in bn.values() if v})==69 and sum(not v for v in bn.values())==6
expected=dict(status='READ_ONLY_EXPECTED_DELTA_VERIFIED_FROM_COPIED_NATIVE_PST_NOT_NEW_REPLAY',componentsBefore=80,componentsAfter=80,pinsBefore=272,pinsAfter=272,nets=69,NC=6,placedSymbolsBefore=0,placedSymbolsAfterExpected=0,pinChanges=pinchanges,propertyChanges=propchanges,addedComponents=[],removedComponents=[],allOtherPinNetsUnchanged=True,allFootprintsUnchanged=True,remainingUnplacedAndUnrouted=True,expectedBaselineSpec=str(S/'logical_specs/integrated_circuit.json'),expectedECOSpec=str(S/'logical_specs/integrated_circuit_eco.json'),sourceHistoricalCompare=str(S/'historical_flow/independent_compare.json'))
dump(E/'expected_delta.json',expected)
# All commands are vectors, not an executable shell script. Sole native executor must adapt runtime paths first.
exe=r'C:\Program0\Cadence\spb172\tools\bin\netrev.exe';work=O/'DE_BASELINE_WORKING.brd';eco=O/'DE_ECO_REPLAY.brd'
plan=dict(status='PREPARED_ONLY_NOT_EXECUTED_BY_THIS_AGENT',executor='f29 sole native owner',scope='Unplaced DE demonstration only. Never use these PSTs/DSNs on HI b019, newdefault stack trial or routed user boards.',outputRoot=str(O),inputRoot=str(S),preconditions=['Source package allSHA rechecked.','New output dir must be created under JK/eco/DE_REPLAY_ONLY; no overwrite of source_inputs or oldflow.','Copy source_inputs/DE_BASELINE.brd to DE_REPLAY_ONLY/DE_BASELINE_WORKING.brd before any native tool.','Task-local TEMP/TMP/ALLEGRO_PCBENV/cwd/runtime/logs all under outputRoot. No globalHOME edits.','Use copied private library directory for psmpath/padpath; no source public library mutation.','Historical scripts copied as evidence only: their relativeROOT, CLI and library assumptions must be adapted explicitly, not blindly launched.'],historicalOfficialNetrev=dict(sourcePath=str(F/'logs/import_eco/launch.json'),sourceSHA256=sha(F/'logs/import_eco/launch.json'),sourceCopy=str(S/'historical_commands/import_eco_launch.json'),completedHistoricalArgs=ld(F/'logs/import_eco/launch.json')['args'],historicalExitCode=0,officialDocPath=str(doc),officialDocSHA256=sha(doc),copiedOfficialDoc=str(S/'official_docs/nchap.html'),flagSemantics={'-e':'Missing footprint is an error; this is not an ECO enable flag.','-i':'Use the specified PST directory.','-n':'Create a new board during logic import; DO NOT use for applying ECO to copied existing baseline.','-d':'Disables DRC; not part of historical replay command and not proposed here.'}),plannedCommands=[dict(stage='readonly_baseline',method='Use task-local copy of de_board_read.il and Allegro -readonly to export fresh native80/272/69/placed0 before ECO.',board=str(work)),dict(stage='import_eco',executable=exe,args=['-e','-i',str(S/'eco/netlist'),str(work),str(eco)],assertNoFlagN=True),dict(stage='fresh_readonly_eco',method='Export actual component values/package and every272pin-net after native save/close/reopen.',board=str(eco))],optionalRegeneratePST=dict(executable=r'C:\Program0\Cadence\spb172\tools\bin\pstswp.exe',args=['-pst','-d','<workingDSNcopy>','-n','<newOutputNetlist>','-c',str(S/'historical_flow/allegro.cfg'),'-v','3','-l','255','-j','PCB Footprint'],restriction='Only another copy under outputRoot; PST packaging can rewrite workingDSN bytes. Never modify authored source_inputs DSNs.'),optionalFeedback='Historical genfeedformat.exe and pstswp.exe -swp launch vectors are copied. If replaying reverse output, adapt to new output and record actualSWP. Generating SWP is distinct from CaptureGUI applying it.',acceptance=['Native completed exit0 + saved marker is necessary but not sufficient.','Fresh baseline and ECO80component/272pin/69net/6NC and placed0; no additions/removals/package changes.','ExactlyR19/R20 VALUE2.2k->3.3k and exactlyJ13.7/8 PB8/PB9 exchange. Every otherpin-net/value unchanged.','No unexpected reverseSWP deltas if feedback replay included; GUIapply remains separate unless actually observed.','All source_input bytes/source originals unchanged after replay.','Report this as controlled ECO reproducibility exercise, not routed manufacturing/HI completion.'],expectedDelta=str(E/'expected_delta.json'))
dump(E/'execute_plan.json',plan)
manifest=dict(status='COPIED_AND_SHA_VERIFIED_READ_ONLY_REPLAY_INPUTS_READY_NATIVE_NOT_RUN',created=datetime.datetime.now().isoformat(),sourceFlow=str(F),sourceFlowSHA256=sha(F/'flow_result.json'),files=copied,derivedFiles=[dict(path=str(S/'official_docs/netrev_section_readonly.txt'),sha256=sha(S/'official_docs/netrev_section_readonly.txt'))],sourceOriginalDSNHashes=flow['originalDsnHashesUnchanged'],packagedWorkingDSNHashesHistoricalOnly={str(F/c/'DE_CONTROL.dsn'):sha(F/c/'DE_CONTROL.dsn') for c in ['baseline','eco']},dsnHashDistinction='Historical pstswp operated on copiedDSNs and may rewrite their packaged bytes. These differ from untouched authored originalDSNs recorded in flow_result; both identities are explicit. Replay inputs copy authored originals; existingPSTs are exacthistorical native outputs.',sourceBoard=flow['baselineBoard'],sourceBoardSHA256=sha(flow['baselineBoard']),expectedDelta=str(E/'expected_delta.json'),executePlan=str(E/'execute_plan.json'),originalsAndCopiesStillUnchanged=True,noNativeRun=True,noHIOrNewStackMutation=True)
assert all(sha(x['path'])==x['sha256']==sha(x['source']) for x in copied)
dump(E/'replay_input_manifest.json',manifest)
print(json.dumps(dict(files=len(copied),baselineSHA=sha(baseline),plan=str(E/'execute_plan.json'),manifestSHA=sha(E/'replay_input_manifest.json'),expectedSHA=sha(E/'expected_delta.json'),planSHA=sha(E/'execute_plan.json'),officialCommandSourceSHA=sha(F/'logs/import_eco/launch.json'),officialDocSHA=sha(doc)),indent=2))