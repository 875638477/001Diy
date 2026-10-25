"""JK this-round ECO independent read-only verification. No native calls."""
from pathlib import Path
import json,csv,re,hashlib,datetime
R=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonJK_51_59_20261022');E=R/'eco';S=E/'source_inputs';B=E/'DE_REPLAY_ONLY';O=R/'review/independent_K58';O.mkdir(parents=True,exist_ok=True)
files={};checks=[]
def raw(p):
 p=Path(p);b=p.read_bytes();files[str(p)]={'path':str(p),'sha256':hashlib.sha256(b).hexdigest().upper(),'bytes':len(b)};return b

def txt(p):return raw(p).decode('utf-8-sig')
def js(p):return json.loads(txt(p))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def tab(p):return list(csv.DictReader(txt(p).splitlines(),delimiter='\t'))
def ck(k,ok,detail=None):checks.append({'id':k,'passed':bool(ok),'detail':detail})
def out(name,d):(O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
m=js(E/'replay_input_manifest.json');ex=js(E/'expected_delta.json');plan=js(E/'execute_plan.json');native=js(B/'native_replay_result.json')
for f in m['files']:ck('INPUT_'+str(Path(f['path']).relative_to(S)),sha(f['path'])==f['sha256']==sha(f['source']))
for stage in ['baseline_readonly','import_eco','eco_readonly']:
 d=js(B/'logs'/stage/'launch.json');argv=d['args'];ck(stage+'_native_exit0',d['exitCode']==0 and bool(d.get('finishUTC')))
 ck(stage+'_not_historical',all('native_flow_final'not in str(a)for a in argv));ck(stage+'_protected',d.get('protectedAllUnchanged') is True)
 if stage=='import_eco':
  ck('netrev_correct_executable',argv[0].lower().endswith('netrev.exe'));ck('netrev_no_newboard_no_disableDRC','-e'in argv and '-i'in argv and '-n'not in argv and '-d'not in argv);ck('netrev_correct_PST',str(S/'eco/netlist').replace('\\','/').lower()in [str(a).replace('\\','/').lower()for a in argv])
 else:
  ck(stage+'_readonly','-readonly'in argv);ck(stage+'_readonly_SHA',d.get('boardBeforeSHA256')==d.get('boardAfterSHA256'))
ck('workingbaseline_source_SHA',sha(B/'DE_BASELINE_WORKING.brd')==m['sourceBoardSHA256']);ck('eco_actual_SHA',sha(B/'DE_ECO_REPLAY.brd')==native['outputSHA256']);raw(B/'DE_BASELINE_WORKING.brd');raw(B/'DE_ECO_REPLAY.brd')
actual={}
for case,stage,specfile in [('baseline','baseline_readonly','integrated_circuit.json'),('eco','eco_readonly','integrated_circuit_eco.json')]:
 d=B/'logs'/stage;spec=js(S/'logical_specs'/specfile);expected={c['ref']:c for c in spec['components']};ep={(c['ref'],str(p)):n or ''for c in spec['components']for p,n in c['pins'].items()}
 cc={x['refdes']:x for x in tab(d/'components.tsv')};pp={(x['refdes'],x['pin']):x['net']for x in tab(d/'component_pins.tsv')};nn=tab(d/'nets.tsv');vs={x['refdes']:x for x in tab(d/'component_values_source.tsv')};summary=txt(d/'native_summary.txt');values={}
 ck(case+'_80_exact_components',len(cc)==80 and set(cc)==set(expected));ck(case+'_272_exact_pin_keys',len(pp)==272 and set(pp)==set(ep));ck(case+'_69_exact_net_names',len(nn)==69 and {x['net']for x in nn}=={x for x in ep.values()if x});ck(case+'_6_NC',sum(not x for x in pp.values())==6);ck(case+'_placed0',all(x['placed']=='nil'for x in cc.values())and'symbols=0'in summary)
 for key,net in ep.items():ck(case+'_PIN_'+'.'.join(key),pp.get(key)==net)
 for ref,x in cc.items():
  paths=list((d/'devices'/ref).glob('*.txt'));vv=[]
  for p in paths:vv+=[z.strip().strip(chr(39)) for z in re.findall(r"(?im)^PACKAGEPROP\s+VALUE\s+([^\r\n]+)",txt(p))]
  ck(case+'_native_device_VALUE_unique_'+ref,len(vv)==1,[str(p)for p in paths]);value=vv[0] if len(vv)==1 else None;values[ref]=value
  pv=re.findall(r'\bVALUE\s+"([^"]*)"',vs[ref]['definitionProps']);ck(case+'_compdef_VALUE_matches_device_'+ref,len(pv)==1 and pv[0]==value)
  ck(case+'_VALUE_'+ref,value is not None and value.upper()==expected[ref]['value'].upper(),{'actual':value,'expected':expected[ref]['value']})
  package=spec['models'][expected[ref]['model']]['footprint'];ck(case+'_package_'+ref,x['package'].lower()==package.lower())
 actual[case]={'components':cc,'pins':pp,'values':values}
b,e=actual['baseline'],actual['eco'];pc=[dict(refdes=r,pin=p,before=b['pins'][r,p],after=e['pins'][r,p])for r,p in sorted(b['pins'])if b['pins'][r,p]!=e['pins'][r,p]];vc=[dict(refdes=r,before=b['values'][r],after=e['values'][r])for r in sorted(b['values'])if b['values'][r]!=e['values'][r]]
ck('exact_only_J13_7_8_pin_changes',pc==ex['pinChanges'],pc);ck('exact_only_R19_R20_native_values',vc==[dict(refdes=r,before='2.2k',after='3.3k')for r in ['R19','R20']],vc)
ck('no_other_package_or_pin_count_or_placement_delta',all(b['components'][r]['package']==e['components'][r]['package']and b['components'][r]['pins']==e['components'][r]['pins']and b['components'][r]['placed']==e['components'][r]['placed']for r in b['components']))
for f in m['files']:ck('POST_INPUT_'+str(Path(f['path']).relative_to(S)),sha(f['path'])==f['sha256']==sha(f['source']))
r={'status':'PASS_INDEPENDENT_THIS_ROUND_ECO_REPLAY'if all(x['passed']for x in checks)else'INDEPENDENT_REVIEW_REQUIRED','created':datetime.datetime.now().isoformat(),'checkCount':len(checks),'checks':checks,'failed':[x for x in checks if not x['passed']],'actualPinChanges':pc,'actualNativeValueChanges':vc,'actualOutputBoard':str(B/'DE_ECO_REPLAY.brd'),'actualOutputSHA256':sha(B/'DE_ECO_REPLAY.brd'),'actualNativeValueMethod':'Perref axlWriteDeviceFile PACKAGEPROP VALUE independently matches raw native compdef property and expected requirement; never inferred from deviceType suffix.','allSource119CopiedAndOriginalFilesUnchanged':all(x['passed']for x in checks if x['id'].startswith(('INPUT_','POST_INPUT_'))),'netPinCountSemantics':'Unplaced logical design: nets.tsv net->pins=0 is not no terminals; compare all272 comp->pins instead. 80components/69nets/6NC/placed0 verified.','nativeExecutionOwner':'f29','thisAgentOnlyRead':True,'historical1578NotThisRound':True,'scope':'Controlled unplaced DE ECO only; no HI/newstack netlist, GUI SWP application, routed board or release acceptance.','inputs':list(files.values())}
out('review.json',r);print(json.dumps({k:r[k]for k in ['status','checkCount','actualPinChanges','actualNativeValueChanges','actualOutputSHA256']},ensure_ascii=False))