"""Strict source no-op control overlay and selective postnetrev text restoration.
No CAD, no public writes, no layer/name-wide whitelist.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import copy,hashlib,json,shutil,sys
M=Path(__file__).parent;OLD=M/'public0010_native403_bundle13_v5_control';OUT=M/'public0010_native403_bundle13_v6_restore';C=M/'public0010_source_noop_save13';A=M/'public0010_alt403_run13_v4'
sys.path.insert(0,'D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025');from sexpr import parse_many,attrs,Atom
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def val(x):
 if isinstance(x,Decimal):return {'number':str(x.normalize())}
 if isinstance(x,Atom):return {'atom':str(x)}
 if isinstance(x,list):return [val(y) for y in x]
 return {'string':x}
key=lambda x:json.dumps(val(x),sort_keys=True,separators=(',',':'))
def rows(path):return [parse_many(x)[0] for x in Path(path).read_text('utf-8').splitlines()]
def table(xs):
 out={}
 for r in xs:
  ident=(str(r[0]),key(r[1]));need(ident not in out,'Duplicate exact source control identity');out[ident]=r
 return out
def sub(t,a,b):need(t.count(a)==1,'Unexpected v5 runner sequence '+a[:60]);return t.replace(a,b)
RESTORE='''
procedure(pub403TextRecord(ch)
 list(ch->text ch->xy ch->rotation ch->isMirrored ch->justify ch->layer ch->textBlock pc13Props(ch)))
procedure(pub403RestoreTextsSelective(s records)
 let((texts used pending rec ch orient result extra)
  texts=setof(q s->children equal(q->objType "text")) used=nil pending=nil
  ; Reserve every exact original readonly/static text before matching any changed text.
  foreach(rec records
   ch=car(setof(q texts !member(q used) && equal(pub403TextRecord(q) rec)))
   if(ch then used=cons(ch used) else pending=cons(rec pending)))
  foreach(rec reverse(pending)
   ch=car(setof(q texts !member(q used) && equal(q->layer nth(5 rec))))
   orient=make_axlTextOrientation(?textBlock nth(6 rec) ?rotation nth(2 rec) ?mirrored nth(3 rec) ?justify nth(4 rec))
   if(ch then
    used=cons(ch used)
    unless(axlDBChangeText(ch car(rec) orient) error("PUB403 postnetrev text change failed\\n")) axlDBRefreshId(ch)
    unless(axlTransformObject(ch ?move list(xCoord(cadr(rec))-xCoord(ch->xy) yCoord(cadr(rec))-yCoord(ch->xy))) error("PUB403 postnetrev text move failed\\n"))
   else
    result=axlDBCreateText(car(rec) cadr(rec) orient nth(5 rec) s) unless(result error("PUB403 postnetrev text create failed\\n"))
    ch=car(result) when(listp(ch) ch=car(ch)))
   unless(equal(pc13Props(ch) nth(7 rec)) error("PUB403 postnetrev text property differs from exact source\\n")))
  foreach(extra texts unless(member(extra used) unless(axlDeleteObject(extra) error("PUB403 unexpected text removal failed\\n"))))
  axlDBRefreshId(s) foreach(ch s->children axlDBRefreshId(ch))
  unless(equal(sort(foreach(mapcar q records sprintf(nil "%L" q)) 'alphalessp) pc13TextSorted(s)) error("PUB403 selective text exact multiset failed\\n")) t))
procedure(pub403PostNetrevRestore(dir)
 let((rows used row id s count f snapshot)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist")) pub403AllNameGate(nil)
  snapshot=strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist") rows=pub403Rows(snapshot) used=nil count=0
  pub403SnapshotAll(strcat(dir "/POSTNETREV_BEFORE_ALL593_TEXT_PROPS.ilist"))
  foreach(row rows when(equal(car(row) "symbol")
   id=cadr(row) s=car(setof(q axlDBGetDesign()->symbols !member(q used) && pub403SameIdentity(q id t)))
   unless(s error("PUB403 postnetrev source pose/symbol missing %L\\n" id)) used=cons(s used)
   pub403RestoreTextsSelective(s nth(2 row)) count=count+1))
  unless(count==593 error("PUB403 postnetrev all593 text restore coverage failed\\n"))
  ; Component/compdef/symbol user+allegro props and source fonts remain exact gates.
  ; No generic property deletion/addition is performed by this text restoration.
  pub403StateGate(snapshot) pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist")) pub403AllNameGate(nil)
  pub403SnapshotAll(strcat(dir "/POSTNETREV_RESTORED_ALL593_TEXT_PROPS.ilist")) pc13WriteMetadata(dir "postnetrev_restored")
  unless(axlSaveDesign(?design strcat(dir "/PUB0010_NETREV_RESTORED.brd") ?noMru t ?noConfirm t) error("PUB403 postnetrev restored candidate save failed\\n"))
  axlDBRefreshId(nil) pub403StateGate(snapshot) pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist")) pub403AllNameGate(nil)
  pub403SnapshotAll(strcat(dir "/POSTNETREV_SAVED_ALL593_TEXT_PROPS.ilist"))
  f=outfile(strcat(dir "/PUB403_NETREV_RESTORE_COMPLETE.txt")) fprintf(f "POSTNETREV_FULL2698_593POSE_TEXT_PROP_572LOGICAL_NAMES_EXACT_ORIGINAL_NO_AUTOSILK_ALLOWANCE_COMPLETE\\nFRESH_GETCONNECT_COPPER_CFX_REQUIRED\\n") close(f) count))
procedure(pub403RestoredFresh(dir)
 let((f)
  sstatus(fullPrecision t) pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  pub403SnapshotAll(strcat(dir "/FRESH_ALL593_TEXT_PROPS.ilist")) pc13WriteMetadata(dir "restored_fresh")
  pub403Adjacency("target" dir)
  f=outfile(strcat(dir "/PUB403_RESTORED_FRESH_COMPLETE.txt")) fprintf(f "FRESH_FULL2698_593POSE_TEXT_PROP_572LOGICAL_NAMES_806TARGET_ADJ_EXACT_ORIGINAL_NO_AUTOSILK_ALLOWANCE_COMPLETE_NO_SAVE\\nGETCONNECT915_COPPER_CFX_REQUIRED_SEPARATELY\\n") close(f) t))
'''
def main():
 need(not OUT.exists(),'Fresh control overlay bundle required');receipt=jr(C/'RUN_RECEIPT.json');need(receipt['status']=='PASS_NATIVE_CASE_PHASE_ONLY' and receipt['phase']=='no-op-save' and receipt['public_unchanged'],'Actual source no-op save control notPASS');need(receipt['source_sha256_before']==receipt['source_sha256_after']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898','Control source SHA mismatch')
 before=table(rows(C/'CONTROL_BEFORE_ALL593_TEXT_PROPS.ilist'));after=table(rows(C/'CONTROL_AFTER_ALL593_TEXT_PROPS.ilist'));need(set(before)==set(after),'Source control complete row cohort changed');need(sum(r[0]=='symbol' for r in before.values())==593 and sum(r[0]=='component' for r in before.values())==572,'Complete593/572 control snapshot required');changes=[];alladded={}
 for k,s in before.items():
  t=after[k]
  if s[0]!='symbol':need(key(s)==key(t),'Source control component/default-font properties changed');continue
  need(key(s[:2]+s[3:])==key(t[:2]+t[3:]),'Source control symbol identity/pose/properties changed');a,b=Counter(map(key,s[2])),Counter(map(key,t[2]));need(not(a-b),'Source control removed/changed original text');added=b-a
  if added:
   ref=s[1][1];need(s[1][0]=='LOGICAL' and ref in ['Y3','MN14'],'Unapproved source-control derived text object');recs=[]
   for rec in t[2]:
    v=key(rec)
    if added[v]>0:need(rec[5]=='MANUFACTURING/AUTOSILK_TOP','Nonautosilk control text change');recs.append(rec);added[v]-=1
   alladded[ref]=Counter(map(key,recs));changes.append({'ref':ref,'source_identity':val(s[1]),'added_full_exact_records':[val(x) for x in recs]})
 need(not changes,'Actual source no-op control did not remain unchanged; no annotation allowance permitted')
 original572={r[0]:r[1] for r in rows(A/'original_all_text_snapshot.ilist')};need(len(original572)==572,'Original403 logical572 source text coverage invalid')
 for r in before.values():
  if r[0]=='symbol' and r[1][0]=='LOGICAL':need(Counter(map(key,r[2]))==Counter(map(key,original572[r[1][1]])),'Source control before differs from frozen403 original logical text')
 actual={};unapproved=[]
 for r in rows(A/'texts_full_after.ilist'):
  a=attrs(r[1]);actual.setdefault(r[0],[]).append([a['text'],a['xy'],a['rotation'],a['isMirrored'],a['justify'],a['layer'],a['textBlock'],r[2]])
 for r in before.values():
  if r[0]=='symbol' and r[1][0]=='LOGICAL':
   ref=r[1][1];a,b=Counter(map(key,r[2])),Counter(map(key,actual[ref]));need(not(a-b),'V4 dropped/changed source logical text')
   if b-a:
    extras=b-a;unapproved.append({'ref':ref,'added_exact_full_records':[{'record':json.loads(k),'count':v} for k,v in extras.items()]})
 need({r['ref']:sum(x['count'] for x in r['added_exact_full_records']) for r in unapproved}=={'Y3':3,'MN14':7},'V4 unapproved side-effect cohort differs from frozen actual ten')
 shutil.copytree(OLD,OUT);shutil.copyfile(C/'CONTROL_AFTER_ALL593_TEXT_PROPS.ilist',OUT/'SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist');shutil.copyfile(A/'original_all_text_snapshot.ilist',OUT/'ORIGINAL_LOGICAL572_TEXTS.ilist');h=OUT/'public0010_native403_v1.il';h.write_text(h.read_text('utf-8')+RESTORE,encoding='utf-8')
 report={'status':'PASS_EXACT_SOURCE_NOOP_SAVE_UNCHANGED_NO_AUTOSILK_ALLOWANCE','source_sha256':receipt['source_sha256_before'],'source_control_receipt':str(C/'RUN_RECEIPT.json'),'source_control_receipt_sha256':sha(C/'RUN_RECEIPT.json'),'source_control_before_sha256':sha(C/'CONTROL_BEFORE_ALL593_TEXT_PROPS.ilist'),'source_control_after_sha256':sha(C/'CONTROL_AFTER_ALL593_TEXT_PROPS.ilist'),'complete_symbols':593,'complete_components':572,'all_symbol_properties_component_compdef_properties_used_fontblocks_original_unchanged':True,'all_original_text_records_preserved':True,'exact_allowed_additions':changes,'v4_unapproved_sideeffects_to_remove':unapproved,'original_logical572_text_snapshot_sha256':sha(A/'original_all_text_snapshot.ilist'),'not_final_board_approval':'Candidate restored/fresh exact2698/593+915GetConnect/fullcopper/fullCFX still required.'};(OUT/'EXACT_SOURCE_CONTROL_NO_CHANGE_PROOF.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 runner=M/'run_public0010_native403_owned_v6_restore.py';need(not runner.exists(),'Fresh restorerunner required');code=(M/'run_public0010_native403_owned_v5_control.py').read_text('utf-8')
 code=sub(code,"choices=['source-adjacency','apply','canary','target-adjacency','fresh','no-op-save','control-fresh']","choices=['source-adjacency','apply','canary','target-adjacency','fresh','no-op-save','control-fresh','postnetrev-restore','restored-fresh']")
 code=sub(code,"if a.phase=='no-op-save':expression=","if a.phase=='postnetrev-restore':expression='pub403PostNetrevRestore('+quote(a.out)+')';marker='PUB403_NETREV_RESTORE_COMPLETE.txt'\n elif a.phase=='restored-fresh':expression='pub403RestoredFresh('+quote(a.out)+')';marker='PUB403_RESTORED_FRESH_COMPLETE.txt'\n elif a.phase=='no-op-save':expression=")
 need(code.count("a.phase not in ['apply','canary','no-op-save']")==2,'Two readonly checks required');code=code.replace("a.phase not in ['apply','canary','no-op-save']","a.phase not in ['apply','canary','no-op-save','postnetrev-restore']")
 code=sub(code,"'write_candidate':a.phase in ['apply','canary','no-op-save']","'write_candidate':a.phase in ['apply','canary','no-op-save','postnetrev-restore']")
 code=sub(code,"candidate=a.out/('SOURCE_NOOP_SAVE.brd' if a.phase=='no-op-save' else 'PUB0010_CANARY_C90.brd' if a.phase=='canary' else 'PUB0010_ALT403.brd')","candidate=a.out/('PUB0010_NETREV_RESTORED.brd' if a.phase=='postnetrev-restore' else 'SOURCE_NOOP_SAVE.brd' if a.phase=='no-op-save' else 'PUB0010_CANARY_C90.brd' if a.phase=='canary' else 'PUB0010_ALT403.brd')")
 code=sub(code,"if a.phase in ['apply','canary','no-op-save'] and candidate.is_file()","if a.phase in ['apply','canary','no-op-save','postnetrev-restore'] and candidate.is_file()")
 runner.write_text(code,encoding='utf-8');manifest=jr(OLD/'BUNDLE_MANIFEST.json');manifest.update(state='PREPARED_POSTNETREV_RESTORE_ALL593_EXACT_ORIGINAL_SOURCE_ZERO_AUTOSILK_ALLOWANCE',parent_bundle_manifest={'path':str(OLD/'BUNDLE_MANIFEST.json'),'sha256':sha(OLD/'BUNDLE_MANIFEST.json')});manifest['bundle_files']=[{'path':str(p),'sha256':sha(p)} for p in OUT.iterdir() if p.is_file() and p.name!='BUNDLE_MANIFEST.json'];manifest['external_proofs']+=[{'path':str(p),'sha256':sha(p)} for p in [runner,C/'RUN_RECEIPT.json',C/'CONTROL_BEFORE_ALL593_TEXT_PROPS.ilist',C/'CONTROL_AFTER_ALL593_TEXT_PROPS.ilist',A/'original_all_text_snapshot.ilist',A/'texts_full_after.ilist']];(OUT/'BUNDLE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'bundle':str(OUT),'manifest_sha256':sha(OUT/'BUNDLE_MANIFEST.json'),'runner':str(runner),'runner_sha256':sha(runner),'helper_sha256':sha(h),'control_proof_sha256':sha(OUT/'EXACT_SOURCE_CONTROL_NO_CHANGE_PROOF.json')},indent=2))
if __name__=='__main__':main()
