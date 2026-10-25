from pathlib import Path
import json,hashlib,subprocess,sys,copy
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
h='''
procedure(hiScopedPhysicalNeckChallenge(out name netName)
 let((f net before count hits strictCount result)
  f=outfile(strcat(out "/strict_neck_" netName ".txt")) net=axlDBFindByName('net netName) before=axlCNSGetPhysical(name "TOP" nil)
  unless(abs(axlCNSGetPhysical(name "TOP" 'necklength_max)-2.0)<0.00001 error("Normal local neck budget differs\\n"))
  count=axlDRCItem(nil net) fprintf(f "NECK_NORMAL_BEFORE net=%L cset=%L result=%L allTOPFields=%L\\n" netName name count before)
  unless(numberp(count) && count==0 error("Normalized route still violates normal rules\\n"))
  unwindProtect(progn(
   unless(axlCNSSetPhysical(name "TOP" 'necklength_max 1.7) error("Cannot tighten local physical neck only\\n"))
   strictCount=axlDRCItem(nil net) hits=nil f29DumpDRC(f "PAD_INTERNAL_NORMALIZATION_STRICT_NATIVE")
   foreach(d axlDBGetDesign()->drcs
    when(equal(d->name "Maximum Neck Length") && equal(d->source name) && d->actual && abs(atof(d->actual)-1.7414)<0.001 && d->expected && abs(atof(d->expected)-1.7)<0.0001
     hits=cons(d hits) fprintf(f "NATIVE_NORMALIZED_NECK_ACTUAL=%L\\n" d->??)))
   unless(numberp(strictCount) && strictCount>0 && hits error("Stricter1.7 did not expose expected1.7414 native neck\\n")) t)
   progn(
    axlCNSSetPhysical(name "TOP" 'necklength_max 2.0) result=axlDRCItem(nil net)
    fprintf(f "NECK_NORMAL_RESTORED result=%L allTOPFieldsExactlyRestored=%L actualNeckBudget=%L\\n" result equal(before axlCNSGetPhysical(name "TOP" nil)) axlCNSGetPhysical(name "TOP" 'necklength_max))
    unless(numberp(result) && result==0 && equal(before axlCNSGetPhysical(name "TOP" nil)) error("Neck strict challenge restore failed\\n"))))
  fprintf(f "NATIVE_NECK_NORMALIZATION_CHALLENGE_COMPLETE EXTERIOR_NARROW_COPPER_NOT_SHORTENED=t\\n") close(f) t))
'''
(R/'scripts/batchHI_padentry_neck_challenge_v1.il').write_text(h,encoding='ascii');s=(R/'scripts/compile_batchHI_v36.py').read_text();s=s.replace(" elif check['type']=='hseIsolation':", " elif check['type']=='physicalNeckChallenge':statements.append(f'hiScopedPhysicalNeckChallenge({q(out.as_posix())} {q(check[\"cset\"])} {q(check[\"net\"])})')\n elif check['type']=='hseIsolation':");s=s.replace("R/'scripts/batchHI_intermediate_drc_pending.il',il]", "R/'scripts/batchHI_padentry_neck_challenge_v1.il',R/'scripts/batchHI_intermediate_drc_pending.il',il]");(R/'scripts/compile_batchHI_v39.py').write_text(s,encoding='utf8')
for v,tr,expected in [('4L',4,'9E4B6E3D0C31C43D042A5C8223311346219E9054D2ADB2C7012F38E5D618DA73'),('2L',6,'1AC3902C0B130E0F7AD91A5EA8ADD51E499E96225F6ED1BD0AC1614C4D30D80A')]:
 ep=R/f'engineering_power/RIGHT_PADENTRY_NORMALIZE_{v}_01.json';assert sha(ep)==expected;e=json.loads(ep.read_text(encoding='utf8'));old=json.loads((R/f'batches/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING_try{tr:02d}.json').read_text());om=json.loads((R/f'scripts/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING_try{tr:02d}_compiled.json').read_text());C=R/f'inventory/checkpoints/TOP_trial_{v}_b018_PRE_ALL69_DRC_PENDING';identity=json.loads((C/'networks.json').read_text());assert sha(identity['board'])==e['sourceExpectedSHA256']==identity['sha256'];cfg=json.loads((R/f'native_work/b018_{v}_try{tr:02d}/guard_configuration.json').read_text());protected=copy.deepcopy(cfg['protectedOriginals'])
 for vv in ['2L','4L']:
  ii=json.loads((R/f'inventory/checkpoints/TOP_trial_{vv}_b018_PRE_ALL69_DRC_PENDING/networks.json').read_text());protected.append({'path':ii['board'],'sha256':ii['sha256'],'role':'Immutable physically validated b018 TOP trial'})
 ops=[o for o in e['operations'] if o['type']=='deleteSegment']+[o for o in e['operations'] if o['type']!='deleteSegment'];assert len(ops)==12;proofs=copy.deepcopy(old['proofs'])+e['connectivityProofs'];unique={}
 for p in proofs:unique.setdefault((p['from'],p['to'],p.get('connected',True)),p)
 # Also derive all actual currently-connected physical pin edges from saved b018 graph.
 for n in identity['nets']:
  for cc in n['components']:
   pp=[x['key'] for x in cc['terminals']]
   for p in pp[1:]:unique.setdefault((pp[0],p,True),{'from':pp[0],'to':p,'connected':True})
 aliases=[{'id':k,'net':a[0],'layer':a[1],'xy':a[2],'type':a[3]} for k,a in om['endpointDefinitions'].items()];checks=[c for c in old['postChecks'] if c['type'] in ['allGroundCommonHealth','hseIsolation']]
 cmap={'BOOT0':'HI_JS_P016_4L' if v=='4L' else 'HI_JS_P042_2L','GPIO_PA15':'HI_JS_P016_4L' if v=='4L' else 'HI_JS_P043_2L','GPIO_PB4':'HI_JS_P016_4L' if v=='4L' else 'HI_JS_P043_2L','I2C_SCL':'HI_JS_P016_4L' if v=='4L' else 'HI_JS_P044_2L'};checks += [{'type':'physicalNeckChallenge','net':n,'cset':c} for n,c in cmap.items()];names=[n for n in old['all69ScopedDeferredToIndependentReadonlyProcess'] if n not in ['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED']];assert len(names)==65;checks.append({'type':'changedNetworks','nets':names});output=R/f'native_candidates/HI_{v}_padentry_normalized_b019_DRC_PENDING.brd';assert not output.exists();work=R/f'native_work/b019_{v}_try01';work.mkdir(exist_ok=False);scratch=work/'input.brd';scratch.write_bytes(Path(identity['board']).read_bytes());d={'status':'ROOT_APPROVED_PAD_INTERNAL_PATH_NORMALIZATION_EXTERIOR_COPPER_UNCHANGED_CSET_BUDGET_UNCHANGED','nativeVariant':v,'inputBoardIdentity':identity,'sourceExpectedSHA256':identity['sha256'],'engineeringPlan':str(ep),'engineeringPlanSHA256':expected,'operations':ops,'constraintOperations':[],'aliases':aliases,'proofs':list(unique.values()),'terminalContract':old['terminalContract'],'postChecks':checks,'all69ScopedDeferredToIndependentReadonlyProcess':old['all69ScopedDeferredToIndependentReadonlyProcess'],'wholeBoardDRC':None,'outputBoard':str(output),'executionGuard':{'scratchWritableWorkingCopy':str(scratch),'protectedOriginals':protected},'physicalMeaning':'Normal .20 centeranchor fully covered by existing land, .16 object neck 2.141421 to1.741421; exterior .16copper neck stays1.541421, all copper union unchanged. Not signal integrity improvement by shortening exterior.','retainedStageVoidManifests':[str(R/f'review/b018_{v}_stage_island_void_manifest.json')]};tag=f'padentry_{v}_b019_DRC_PENDING_try01';p=R/f'batches/{tag}.json';p.write_text(json.dumps(d,indent=2));subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v39.py'),'--plan',str(p),'--variant',v,'--tag',tag],check=True);mp=R/f'scripts/{tag}_compiled.json';m=json.loads(mp.read_text());cfg.update(tag=tag,scratchWritableWorkingCopy=str(scratch),scratchSHA256=sha(scratch),candidateOutput=str(output),plan=str(p),planSHA256=sha(p),compiledMetadata=str(mp),compiledMetadataSHA256=sha(mp),script=m['script'],scriptSHA256=sha(m['script']),log=m['log'],protectedOriginals=protected);(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2))
s=(R/'scripts/launch_b018_guardedHI_v1.py').read_text().replace('native_work/b018_{a.variant}','native_work/b019_{a.variant}');(R/'scripts/launch_b019_guardedHI_v1.py').write_text(s,encoding='utf8')
