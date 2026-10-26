"""Independent original0010 no-op SaveAs control; no annotation whitelist, no CAD."""
from pathlib import Path
import hashlib,json,shutil
M=Path(__file__).parent;OLD=M/'public0010_native403_bundle13_v4';OUT=M/'public0010_native403_bundle13_v5_control'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def need(v,m):
 if not v:raise ValueError(m)
def sub(t,a,b):need(t.count(a)==1,'Unexpected v4 runner sequence '+a[:60]);return t.replace(a,b)
CONTROL='''
procedure(pub403NoOpSave(dir)
 let((f)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403SnapshotAll(strcat(dir "/CONTROL_BEFORE_ALL593_TEXT_PROPS.ilist")) pc13WriteMetadata(dir "control_before")
  unless(axlSaveDesign(?design strcat(dir "/SOURCE_NOOP_SAVE.brd") ?noMru t ?noConfirm t) error("PUB403 source control save failed\\n"))
  axlDBRefreshId(nil)
  pub403FullTypedGate(strcat(pub403Bundle "/SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403SnapshotAll(strcat(dir "/CONTROL_AFTER_ALL593_TEXT_PROPS.ilist")) pc13WriteMetadata(dir "control_after")
  f=outfile(strcat(dir "/PUB403_NOOP_SAVE_COMPLETE.txt")) fprintf(f "ORIGINAL_SOURCE680500_NOOP_SAVEAS_ALL2698_TYPED_FULL593_SNAPSHOT_BEFORE_AFTER_COMPLETE\\nNO_TEXT_DIFFERENCE_APPROVAL\\n") close(f) t))
procedure(pub403ControlFresh(dir)
 let((f)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403SnapshotAll(strcat(dir "/CONTROL_FRESH_ALL593_TEXT_PROPS.ilist")) pc13WriteMetadata(dir "control_fresh")
  f=outfile(strcat(dir "/PUB403_CONTROL_FRESH_COMPLETE.txt")) fprintf(f "SOURCE_NOOP_SAVED_FRESH_FULL2698_FULL593_SNAPSHOT_COMPLETE_NO_SAVE\\nNO_TEXT_DIFFERENCE_APPROVAL\\n") close(f) t))
'''
def main():
 need(not OUT.exists(),'Fresh controlv5 bundle required');shutil.copytree(OLD,OUT);h=OUT/'public0010_native403_v1.il';h.write_text(h.read_text('utf-8')+CONTROL,encoding='utf-8');runner=M/'run_public0010_native403_owned_v5_control.py';need(not runner.exists(),'Fresh controlrunner required');code=(M/'run_public0010_native403_owned_v4.py').read_text('utf-8')
 code=sub(code,"choices=['source-adjacency','apply','canary','target-adjacency','fresh']","choices=['source-adjacency','apply','canary','target-adjacency','fresh','no-op-save','control-fresh']")
 code=sub(code,"if a.phase in ['source-adjacency','apply','canary']:","if a.phase in ['source-adjacency','apply','canary','no-op-save']:")
 code=sub(code,"if a.phase=='source-adjacency':expression='pub403SourceOnly('+quote(a.out)+')';marker='PUB403_SOURCE_COMPLETE.txt'","if a.phase=='no-op-save':expression='pub403NoOpSave('+quote(a.out)+')';marker='PUB403_NOOP_SAVE_COMPLETE.txt'\n elif a.phase=='control-fresh':expression='pub403ControlFresh('+quote(a.out)+')';marker='PUB403_CONTROL_FRESH_COMPLETE.txt'\n elif a.phase=='source-adjacency':expression='pub403SourceOnly('+quote(a.out)+')';marker='PUB403_SOURCE_COMPLETE.txt'")
 need(code.count("a.phase not in ['apply','canary']")==2,'Expected two readonly-phase checks');code=code.replace("a.phase not in ['apply','canary']","a.phase not in ['apply','canary','no-op-save']")
 code=sub(code,"'write_candidate':a.phase in ['apply','canary']","'write_candidate':a.phase in ['apply','canary','no-op-save']")
 code=sub(code,"candidate=a.out/('PUB0010_CANARY_C90.brd' if a.phase=='canary' else 'PUB0010_ALT403.brd')","candidate=a.out/('SOURCE_NOOP_SAVE.brd' if a.phase=='no-op-save' else 'PUB0010_CANARY_C90.brd' if a.phase=='canary' else 'PUB0010_ALT403.brd')")
 code=sub(code,"if a.phase in ['apply','canary'] and candidate.is_file():receipt.update(candidate=str(candidate),candidate_sha256=sha(candidate))","if a.phase in ['apply','canary','no-op-save'] and candidate.is_file():receipt.update(candidate=str(candidate),candidate_sha256=sha(candidate))")
 runner.write_text(code,encoding='utf-8');manifest=json.loads((OLD/'BUNDLE_MANIFEST.json').read_text('utf-8'));manifest.update(state='PREPARED_SOURCE_NOOP_SAVE_AND_FRESH_COMPLETE593_SNAPSHOTS_NO_ANNOTATION_APPROVAL',parent_bundle_manifest={'path':str(OLD/'BUNDLE_MANIFEST.json'),'sha256':sha(OLD/'BUNDLE_MANIFEST.json')});manifest['bundle_files']=[{'path':str(p),'sha256':sha(p)} for p in OUT.iterdir() if p.is_file() and p.name!='BUNDLE_MANIFEST.json'];manifest['external_proofs']+=[{'path':str(runner),'sha256':sha(runner)}];(OUT/'BUNDLE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'bundle':str(OUT),'manifest_sha256':sha(OUT/'BUNDLE_MANIFEST.json'),'runner':str(runner),'runner_sha256':sha(runner),'helper_sha256':sha(h)},indent=2))
if __name__=='__main__':main()
