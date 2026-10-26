"""New diagnostic bundle/runner; preserves frozenv1 and reuses actualsource806 proof."""
from pathlib import Path
import copy,hashlib,json,shutil
M=Path(__file__).parent;OLD=M/'public0010_native403_bundle13';OUT=M/'public0010_native403_bundle13_v2';P=M/'public0010_source806_probe13'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
TRACE=r'''
; Diagnostic v2: trace inside cloak so the exact per-ref error is not masked by nil.
procedure(pub403Trace(ref stage)
 let((c s pins)
  c=pc13Comp(ref) s=c->symbol
  pins=foreach(mapcar p s->pins list(p->number p->xy p->name p->net->name p->isMech p->isThrough p->isExploded))
  fprintf(pub403Debug "%L\n" list(ref stage c->package s->name s->definition->name pc13Pose(s) "EXPECTED_TARGET" pc13Expected[ref] "ACTUAL_PINS" pins "COMPDEF_PROPS" pc13Props(c->compdef) "COMP_PROPS" pc13Props(c) "SYMBOL_PROPS" pc13Props(s) "TEXT" pc13TextSnapshot(s))) drain(pub403Debug)
  printf("PUB403_REF_STAGE %s %s\n" ref stage) t))
procedure(pc13ReplaceOne(row f)
 let((ref from target c s pose texts props oldalt)
  ref=car(row) from=cadr(row) target=caddr(row) c=pc13Comp(ref) s=c->symbol
  pose=pc13Pose(s) texts=pc13TextSnapshot(s) props=pc13Props(c->compdef)
  pub403Trace(ref "BEFORE_ALT_PROP") oldalt=assoc('ALT_SYMBOLS props)
  unless(axlDBAddProp(list(c->compdef) list("ALT_SYMBOLS" strcat("(" target ")"))) error("PUB403 ALT_SYMBOLS add failed %s\n" ref))
  pub403Trace(ref "BEFORE_ALT_REPLACE")
  unless(axlAltSymbolReplace(c target) error("PUB403 Alt replace returnednil %s\n" ref))
  axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol pub403Trace(ref "AFTER_ALT_BEFORE_TEXT")
  pc13TextRestore(s texts) pub403Trace(ref "AFTER_TEXT_BEFORE_ALT_PROP_RESTORE")
  if(oldalt then axlDBAddProp(list(c->compdef) list("ALT_SYMBOLS" cadr(oldalt))) else axlDBDeleteProp(c->compdef "ALT_SYMBOLS"))
  axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol pub403Trace(ref "AFTER_ALT_PROP_BEFORE_POSE")
  unless(equal(pose pc13Pose(s)) error("PUB403 pose changed %s\n" ref))
  pub403Trace(ref "BEFORE_EXPECTED_PINS") pc13ExpectedPins(ref s) pub403Trace(ref "AFTER_EXPECTED_PINS_BEFORE_TEXT_GUARD")
  unless(equal(sort(foreach(mapcar r texts sprintf(nil "%L" r)) 'alphalessp) pc13TextSorted(s)) error("PUB403 text changed %s\n" ref))
  unless(equal(props pc13Props(c->compdef)) error("PUB403 compdef props/ALT changed %s\n" ref))
  pub403Trace(ref "ALL_PER_REF_GUARDS_PASS") fprintf(f "%s\t%s\t%s\tTRUE\n" ref from target) drain(f) t))
procedure(pc13ReplaceRows(rows f)
 let((count row result)
  count=0
  foreach(row rows
   result=errset(pc13ReplaceOne(row f) t)
   unless(result && car(result)
    pub403Trace(car(row) "PER_REF_ERRSET_REJECTED")
    error("PUB403 detailed per-ref migration failed %s; preserve REF_STAGE_DEBUG.ilist\n" car(row)))
   count=count+1)
  count))
'''
def main():
 need(not OUT.exists(),'Fresh v2 bundle required');source=jr(P/'RUN_RECEIPT.json');need(source['status']=='PASS_NATIVE_CASE_PHASE_ONLY' and source['phase']=='source-adjacency' and source['public_unchanged'],'Source806 actualnative receipt notPASS')
 need(source['source_sha256_before']==source['source_sha256_after']==jr(OLD/'BUNDLE_MANIFEST.json')['source_board_sha256'],'Source806 bound another board')
 adj=P/'PUB403_source_pin_adjacency.ilist';summary=P/'PUB403_source_pin_adjacency_summary.tsv';need(adj.read_text('utf-8').rstrip().endswith('PUB403_ALL806_ADJACENCY_COMPLETE PHASE=source'),'Source806 actualadjacency incomplete');need(len(summary.read_text('utf-8').splitlines())==807,'Source806 summary count incorrect')
 shutil.copytree(OLD,OUT)
 helper=OUT/'public0010_native403_v1.il';text=helper.read_text('utf-8')
 token='snapshot=strcat(dir "/SOURCE_ALL593_TEXT_PROPS.ilist") pub403SnapshotAll(snapshot) pub403Adjacency("source" dir)'
 need(text.count(token)==1,'v1 apply sourceprobe sequence changed')
 text=text.replace(token,'snapshot=strcat(dir "/SOURCE_ALL593_TEXT_PROPS.ilist") pub403SnapshotAll(snapshot)\n  printf("PUB403_BOUND_SOURCE806_EVIDENCE_REUSED_NO_REPROBE\\n")\n  pub403Debug=outfile(strcat(dir "/REF_STAGE_DEBUG.ilist"))')
 token='pub403Adjacency("target" dir)\n  f=outfile(strcat(dir "/PUB403_APPLY_COMPLETE.txt"))';need(text.count(token)==1,'v1 targetcomplete sequence changed')
 text=text.replace(token,'pub403Adjacency("target" dir) close(pub403Debug)\n  f=outfile(strcat(dir "/PUB403_APPLY_COMPLETE.txt"))')+TRACE
 helper.write_text(text,encoding='utf-8')
 runner=M/'run_public0010_native403_owned_v2.py';need(not runner.exists(),'Fresh v2 runner required');code=(M/'run_public0010_native403_owned.py').read_text('utf-8')
 token="a.out.mkdir(parents=True);copy=a.out/'INPUT_COPY.brd';shutil.copyfile(inp,copy);need(sha(copy)==expected,'Independent board copy SHA mismatch')"
 need(code.count(token)==1,'v1 sourcecopy sequence changed')
 add='''
 if a.phase=='apply':
  reuse=man['source_adjacency_reuse'];proof=jr(reuse['receipt']['path'])
  for record in [reuse['receipt']]+reuse['artifacts']:need(sha(record['path'])==record['sha256'],'Bound source806 artifact changed')
  need(proof['status']=='PASS_NATIVE_CASE_PHASE_ONLY' and proof['phase']=='source-adjacency' and proof['public_unchanged'],'Reusable source806 proof notnativePASS')
  need(proof['source_sha256_before']==proof['source_sha256_after']==expected and proof['guard_sha256']==sha(a.guard),'Reusable source806 proof binds another source or public guard')
  need(Path(reuse['artifacts'][0]['path']).read_text('utf-8').rstrip().endswith('PUB403_ALL806_ADJACENCY_COMPLETE PHASE=source'),'Reusable adjacency marker absent')
  need(len(Path(reuse['artifacts'][1]['path']).read_text('utf-8').splitlines())==807,'Reusable806 summary incomplete')
  for record in reuse['artifacts']:shutil.copyfile(record['path'],a.out/Path(record['path']).name)
  (a.out/'SOURCE806_REUSE_PROVENANCE.json').write_text(json.dumps(reuse,indent=2),encoding='utf-8')
'''
 code=code.replace(token,token+'\n'+add);runner.write_text(code,encoding='utf-8')
 manifest=jr(OLD/'BUNDLE_MANIFEST.json');manifest['state']='PREPARED_V2_VERBOSE_ERRSET_DIAGNOSTIC_REUSE_PROVEN_SOURCE806_NO_PUBLIC_WRITES';manifest['parent_bundle_manifest']={'path':str(OLD/'BUNDLE_MANIFEST.json'),'sha256':sha(OLD/'BUNDLE_MANIFEST.json')}
 manifest['source_adjacency_reuse']={'receipt':{'path':str(P/'RUN_RECEIPT.json'),'sha256':sha(P/'RUN_RECEIPT.json')},'artifacts':[{'path':str(x),'sha256':sha(x)} for x in [adj,summary]],'source_board_sha256':source['source_sha256_before'],'guard_sha256':source['guard_sha256']}
 manifest['bundle_files']=[{'path':str(p),'sha256':sha(p)} for p in OUT.iterdir() if p.is_file() and p.name!='BUNDLE_MANIFEST.json'];manifest['external_proofs']+=[{'path':str(runner),'sha256':sha(runner)}]
 (OUT/'BUNDLE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'bundle':str(OUT),'manifest_sha256':sha(OUT/'BUNDLE_MANIFEST.json'),'helper_sha256':sha(helper),'runner':str(runner),'runner_sha256':sha(runner)},indent=2))
if __name__=='__main__':main()
