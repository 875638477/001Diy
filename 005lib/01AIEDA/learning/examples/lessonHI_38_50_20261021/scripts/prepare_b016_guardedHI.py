from pathlib import Path
import json,hashlib,subprocess,sys,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
protected=[]
for v in ['2L','4L']:
 for p in [R/f'native/HI_{v}_USB_aux_{v}_b014.brd',R/f'native_candidates/HI_{v}_source_b015_DRC_PENDING.brd']:
  protected.append({'path':str(p),'sha256':sha(p),'role':'Prior immutable training checkpoint; never opened by writable new batch'})
for x in json.loads((R/'inputs/source_boards_manifest.json').read_text()):
 p=Path(x['source']);assert sha(p)==x['sha256'];protected.append({'path':str(p),'sha256':sha(p),'role':'Original G training board; never opened or modified'})
for v in ['2L','4L']:
 tag=f'clearance_remaining_{v}_b016_DRC_PENDING_try01';work=R/f'native_work/b016_{v}_try01';work.mkdir(parents=True,exist_ok=False);src=R/f'native_candidates/HI_{v}_source_b015_DRC_PENDING.brd';scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(src.read_bytes())
 output=R/f'native_candidates/HI_{v}_clearance_remaining_b016_DRC_PENDING.brd';assert not output.exists()
 plan=json.loads((R/f'batches/clearance_remaining_{v}_b016_DRC_PENDING.json').read_text());assert sha(src)==plan['sourceExpectedSHA256'];plan['outputBoard']=str(output);plan['executionGuard']={'scratchWritableWorkingCopy':str(scratch),'inputSHA256':sha(scratch),'saveAsOnlyBrandNewCandidate':str(output),'protectedOriginals':protected,'rootAuthorization':'Merged38-50 native training. All exact ripup, moves, construction-order dynamic boundary defer/identical restore occur only in a new disposable writable task copy. Prior b014/G/b015 sources never opened; approved changed nonDP scoped checks only; full wholeboard DRC remains null/pending.'}
 dest=R/f'batches/{tag}.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');subprocess.run([sys.executable,str(R/'scripts/compile_batchHI_v29.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());cfg={'variant':v,'tag':tag,'scratchWritableWorkingCopy':str(scratch),'scratchSHA256':sha(scratch),'candidateOutput':str(output),'compiledMetadata':str(meta),'compiledMetadataSHA256':sha(meta),'plan':str(dest),'planSHA256':sha(dest),'script':m['script'],'scriptSHA256':sha(Path(m['script'])),'log':m['log'],'protectedOriginals':protected,'allowlistRoot':str(R),'launchMode':'Standard writable NEW disposable task working copy only; official KillDesign after fixed SaveAs candidate','aliasUpdatesAllowed':False};(work/'guard_configuration.json').write_text(json.dumps(cfg,indent=2),encoding='utf8')
s=(R/'scripts/launch_source_guardedHI_v11_writable_taskcopy.py').read_text().replace("['_try11']","['_try01']").replace("work=R/f'native_work/source_b015_{a.variant}{a.try_suffix}'","work=R/f'native_work/b016_{a.variant}{a.try_suffix}'");(R/'scripts/launch_b016_guardedHI_v1.py').write_text(s,encoding='utf8')
D=Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS');dst=R/'source/api_b016';dst.mkdir(exist_ok=True);e=[]
for n in ['axlDRCUpdate','axlDRCItem','axlSaveDesign','axlKillDesign','axlDeleteObject','axlShapeRaisePriority','axlShapeDynamicUpdate','axlDBControl','axlGetParam','axlDBGetProperties','axlDBAddProp','axlDBTransactionStart','axlDBTransactionRollback','axlDBTransactionCommit','axlDBRefreshId','axlDBCreatePath']:
 p=D/(n+'.txt');assert p.is_file(),str(p);out=dst/p.name;shutil.copyfile(p,out);e.append({'source':str(p),'copy':str(out),'sha256':sha(p),'scope':'Official17.2 local API used by b016 native construction/review; not API invention.'})
(dst/'manifest.json').write_text(json.dumps(e,indent=2),encoding='utf8');print('Guard+compile and official API archive ready',len(e))