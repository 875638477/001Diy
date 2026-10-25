from pathlib import Path
import json,hashlib,stat,subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');PTH=R.parent.parent/'tools/python_3_14_0/python.exe';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
protected=[]
for v in ['2L','4L']:
 p=R/f'native/HI_{v}_USB_aux_{v}_b014.brd';protected.append({'path':str(p),'sha256':sha(p),'role':'Existing b014 checkpoint; never opened by write-capable batch'})
for x in json.loads((R/'inputs/source_boards_manifest.json').read_text()):
 p=Path(x['source']);assert sha(p)==x['sha256'];protected.append({'path':str(p),'sha256':sha(p),'role':'Original G training board; never opened or modified'})
(R/'native_candidates').mkdir(exist_ok=True)
for v in ['2L','4L']:
 work=R/f'native_work/source_b015_{v}';work.mkdir(parents=True,exist_ok=False);src=R/f'native/HI_{v}_USB_aux_{v}_b014.brd';scratch=work/'input.brd'
 with scratch.open('xb') as f:f.write(src.read_bytes())
 scratch.chmod(stat.S_IREAD);assert sha(scratch)==sha(src)
 assert scratch.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
 output=R/f'native_candidates/HI_{v}_source_b015.brd';assert not output.exists()
 plan=json.loads((R/f'batches/source_service_{v}_b015.json').read_text());plan['outputBoard']=str(output);plan['executionGuard']={'scratchReadonlyInput':str(scratch),'inputSHA256':sha(scratch),'saveAsOnlyBrandNewCandidate':str(output),'protectedOriginals':protected,'rootAuthorization':'User authorized merged38-50actual training; new task-memory-copy ripup/move/route only. No original b014/G/public/user工程 write. Root explicitly selected stronger readonly scratch + SaveAs-new protection after auto-review rejection.'}
 # Correct only stale metadata layers for three South bottom partial-end proofs, leaving geometric source ops unchanged.
 changes=[]
 for alias in plan['aliases']:
  if alias['id'] in ['NODE_JS_1','NODE_JS_2','NODE_JS_3']:
   changes.append({'id':alias['id'],'beforeLayer':alias['layer'],'afterLayer':'BOTTOM','reason':'These are actual South bottom exit endpoints; expectedProofs omitted targetLayer. Actual frozen route layer authoritative.'});alias['layer']='BOTTOM'
 plan['proofAliasLayerCorrections']=changes
 dest=R/f'batches/source_service_{v}_b015_guarded.json';dest.write_text(json.dumps(plan,indent=2),encoding='utf8');tag=f'source_service_{v}_b015_guarded'
 subprocess.run([str(PTH),str(R/'scripts/compile_batchHI_v21.py'),'--plan',str(dest),'--variant',v,'--tag',tag],check=True)
 meta=R/f'scripts/{tag}_compiled.json';m=json.loads(meta.read_text());assert Path(m['output'])==output
 config={'variant':v,'tag':tag,'scratchReadonlyInput':str(scratch),'scratchSHA256':sha(scratch),'candidateOutput':str(output),'compiledMetadata':str(meta),'compiledMetadataSHA256':sha(meta),'plan':str(dest),'planSHA256':sha(dest),'script':m['script'],'scriptSHA256':sha(Path(m['script'])),'log':m['log'],'protectedOriginals':protected,'allowlistRoot':str(R),'launchMode':'-readonly; new scratch file also WindowsReadOnly; only SaveAs to brand new native_candidates file','aliasUpdatesAllowed':False,'priorReviewRejection':'Original source-launch action was rejected as broad destructive write; this alternative never opens originals in native and cannot overwrite its readonly scratch. Source-stage wire deletions are reversible in-memory exercises only.'}
 (work/'guard_configuration.json').write_text(json.dumps(config,indent=2),encoding='utf8')
 print(v,'isolated readonly input',scratch,'new candidate',output)
