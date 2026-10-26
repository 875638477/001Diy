"""Restore Alt-lost side using documented symbol mirror, then exact source angle.
Creates independent v3 and single C90 mixed2698 canary. Never launches CAD.
"""
from pathlib import Path
import hashlib,json,shutil,sys
M=Path(__file__).parent;OLD=M/'public0010_native403_bundle13_v2';OUT=M/'public0010_native403_bundle13_v3'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
 if not v:raise ValueError(m)
def substitute(t,a,b):need(t.count(a)==1,'Unexpected v2 source sequence '+a[:70]);return t.replace(a,b)
MIRROR='''
  ; Alt may reset a source bottom symbol to top. Restore side before text coordinates.
  unless(equal(s->isMirrored nth(2 pose))
   unless(axlTransformObject(s ?mirror t ?origin car(pose)) error("PUB403 source mirror restore failed %s\\n" ref))
   axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol pub403Trace(ref "AFTER_SOURCE_MIRROR_RESTORE"))
  unless(equal(s->xy car(pose)) error("PUB403 mirror changed source XY %s\\n" ref))
  delta=cadr(pose)-s->rotation
  unless(zerop(delta)
   unless(axlTransformObject(s ?angle delta ?origin car(pose)) error("PUB403 source angle restore failed %s\\n" ref))
   axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol pub403Trace(ref "AFTER_SOURCE_ANGLE_RESTORE"))
  unless(equal(pose pc13Pose(s)) error("PUB403 source pose could not be restored %s\\n" ref))
'''
CANARY='''
procedure(pub403Canary(dir)
 let((snapshot f result row c)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  snapshot=strcat(dir "/SOURCE_ALL593_TEXT_PROPS.ilist") pub403SnapshotAll(snapshot)
  pc13LoadExpected(strcat(pub403Bundle "/TARGET_LOGICAL572_EXPECTED_PINS.ilist"))
  pub403Debug=outfile(strcat(dir "/REF_STAGE_DEBUG.ilist")) f=outfile(strcat(dir "/applied.tsv"))
  fprintf(f "refdes\\tfrom_package\\ttarget_package\\tpose_pin_text_preserved\\n")
  row=list("C90" "C0805" "c0805_pc" 0.0)
  result=axlDBCloak('pc13ReplaceRows(list(row) f) 'shape)
  unless(result==1 error("PUB403 singleC90 cloak failed\\n")) close(f) close(pub403Debug)
  pub403FullTypedGate(strcat(pub403Bundle "/CANARY_C90_FULL2698.ilist")) pub403StateGate(snapshot)
  c=pc13Comp("C90") unless(equal(upperCase(c->symbol->name) "C0805_PC") && equal(upperCase(c->symbol->definition->name) "C0805_PC") error("PUB403 C90 targetphysical name failed\\n"))
  unless(axlSaveDesign(?design strcat(dir "/PUB0010_CANARY_C90.brd") ?noMru t ?noConfirm t) error("PUB403 C90 canary save failed\\n"))
  f=outfile(strcat(dir "/PUB403_CANARY_COMPLETE.txt")) fprintf(f "C90_SOURCE_SIDE_POSE_RESTORED_ALL2698_MIXED_TYPED_PINS_FULL593TEXT_PROPS_COMPLETE\\nNO_FULL403_OR_CONNECTION_APPROVAL\\n") close(f) t))
'''
def main():
 need(not OUT.exists(),'Fresh v3 bundle required');shutil.copytree(OLD,OUT);helper=OUT/'public0010_native403_v1.il';text=helper.read_text('utf-8')
 text=substitute(text,'let((ref from target c s pose texts props oldalt)(','let((ref from target c s pose texts props oldalt delta)(') if 'let((ref from target c s pose texts props oldalt)(' in text else text
 text=substitute(text,'let((ref from target c s pose texts props oldalt)\n','let((ref from target c s pose texts props oldalt delta)\n')
 text=substitute(text,'axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol pub403Trace(ref "AFTER_ALT_BEFORE_TEXT")\n  pc13TextRestore(s texts)','axlDBRefreshId(nil) c=pc13Comp(ref) s=c->symbol pub403Trace(ref "AFTER_ALT_BEFORE_MIRROR_RESTORE")\n'+MIRROR+'  pc13TextRestore(s texts)')+CANARY
 helper.write_text(text,encoding='utf-8')
 sys.path.insert(0,str(Path('D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')));from sexpr import parse_many
 src=(OUT/'SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist').read_text('utf-8').splitlines();dst=(OUT/'TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist').read_text('utf-8').splitlines();lookup={parse_many(x)[0][0][1]:x for x in dst if parse_many(x)[0][0][1]!='nil'}
 count=0;lines=[]
 for line in src:
  if parse_many(line)[0][0][1]=='C90':line=lookup['C90'];count+=1
  lines.append(line)
 need(count==1 and len(lines)==593,'C90 mixed-source2698 cohort invalid');(OUT/'CANARY_C90_FULL2698.ilist').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 runner=M/'run_public0010_native403_owned_v3.py';need(not runner.exists(),'Fresh v3 runner required');code=(M/'run_public0010_native403_owned_v2.py').read_text('utf-8')
 code=substitute(code,"choices=['source-adjacency','apply','target-adjacency','fresh']","choices=['source-adjacency','apply','canary','target-adjacency','fresh']")
 code=substitute(code,"if a.phase in ['source-adjacency','apply']:","if a.phase in ['source-adjacency','apply','canary']:")
 code=substitute(code,"if a.phase=='apply':\n  reuse=man['source_adjacency_reuse']","if a.phase in ['apply','canary']:\n  reuse=man['source_adjacency_reuse']")
 code=substitute(code,"elif a.phase=='apply':expression='pub403Apply('+quote(a.out)+')';marker='PUB403_APPLY_COMPLETE.txt'","elif a.phase=='apply':expression='pub403Apply('+quote(a.out)+')';marker='PUB403_APPLY_COMPLETE.txt'\n elif a.phase=='canary':expression='pub403Canary('+quote(a.out)+')';marker='PUB403_CANARY_COMPLETE.txt'")
 code=substitute(code,"if a.phase!='apply':args.append('-readonly')","if a.phase not in ['apply','canary']:args.append('-readonly')")
 code=substitute(code,"if a.phase!='apply':need(sha(copy)==expected,'Readonly native input copy changed')","if a.phase not in ['apply','canary']:need(sha(copy)==expected,'Readonly native input copy changed')")
 code=substitute(code,"'write_candidate':a.phase=='apply'","'write_candidate':a.phase in ['apply','canary']")
 code=substitute(code,"if a.phase=='apply' and (a.out/'PUB0010_ALT403.brd').is_file():receipt.update(candidate=str(a.out/'PUB0010_ALT403.brd'),candidate_sha256=sha(a.out/'PUB0010_ALT403.brd'))","candidate=a.out/('PUB0010_CANARY_C90.brd' if a.phase=='canary' else 'PUB0010_ALT403.brd')\n if a.phase in ['apply','canary'] and candidate.is_file():receipt.update(candidate=str(candidate),candidate_sha256=sha(candidate))")
 runner.write_text(code,encoding='utf-8');manifest=jr(OLD/'BUNDLE_MANIFEST.json');manifest.update(state='PREPARED_V3_RESTORE_SOURCE_MIRROR_BEFORE_TEXT_EXACT_ANGLE_AND_MIXED2698_C90_CANARY',parent_bundle_manifest={'path':str(OLD/'BUNDLE_MANIFEST.json'),'sha256':sha(OLD/'BUNDLE_MANIFEST.json')})
 manifest['bundle_files']=[{'path':str(p),'sha256':sha(p)} for p in OUT.iterdir() if p.is_file() and p.name!='BUNDLE_MANIFEST.json'];manifest['external_proofs']+=[{'path':str(runner),'sha256':sha(runner)},{'path':'C:/Program0/cadence/SPB172/doc/algroskill/06intedt.html','sha256':sha('C:/Program0/cadence/SPB172/doc/algroskill/06intedt.html')}]
 (OUT/'BUNDLE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'bundle':str(OUT),'manifest_sha256':sha(OUT/'BUNDLE_MANIFEST.json'),'runner':str(runner),'runner_sha256':sha(runner),'helper_sha256':sha(helper)},indent=2))
if __name__=='__main__':main()
