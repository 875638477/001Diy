"""Derive explicit UNAPPROVED partial stage; never edit frozen v1, never CAD."""
from pathlib import Path
import hashlib,json,sys
M=Path(__file__).parent;sys.path.insert(0,str(M))
from build_public0010_stub_preflight_v1 import balanced
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def main():
 V=M/'public0010_nil_route_stub_bundle13_v1';D=M/'public0010_nil_route_stub_bundle13_v2_partial';assert not D.exists()
 old=json.loads((V/'MANIFEST.json').read_text());s=(V/'public0010_nil_route_stub_repair_v1.il').read_text();D.mkdir()
 def replace(a,b):
  nonlocal s
  assert s.count(a)==1,a;s=s.replace(a,b)
 replace('pub0010OriginalVias=pub0010ViasSnapshot(strcat(dir "/ORIGINAL_ALL1739_TYPED_VIAS.ilist"))','pub0010OriginalVias=pub0010ViasSnapshot(strcat(dir "/ORIGINAL_ALL1739_TYPED_VIAS.ilist")) pub0010OriginalViaNativeRows=pub0010ViaRows')
 replace('beforeVias=pub0010ViasSnapshot(strcat(dir "/TARGET_BEFORE_ALL1739_TYPED_VIAS.ilist"))','beforeVias=pub0010ViasSnapshot(strcat(dir "/TARGET_BEFORE_ALL1739_TYPED_VIAS.ilist")) pub0010InputViaNativeRows=pub0010ViaRows pub0010FrozenInputViaGate(beforeVias)')
 replace('when(failed error("PUB0010 all bounded NIL source branches collected; preflight failed count%d, no create/save\\n" failed))','printf("PUB0010_PARTIAL_ALLOWED_UNRESOLVED_BRANCHES=%d_ONLY_NATIVE_PAD_CONTAINED_SELECTIONS_WILL_CREATE\\n" failed)')
 replace('when(failures error("PUB0010 some original54 NIL routes failed exact source-net propagation %L\\n" failures))','pub0010Unresolved54=failures printf("PUB0010_PARTIAL_ORIGINAL54_POSTCHECK_UNRESOLVED=%d\\n" length(failures))')
 replace('unless(equal(pub0010OriginalVias pub0010ViasSnapshot(strcat(dir "/AFTER_ALL1739_TYPED_VIAS.ilist"))) error("PUB0010 full1739 original typed via XY/pad/net/properties not restored\\n"))','pub0010ViasSnapshot(strcat(dir "/AFTER_ALL1739_TYPED_VIAS.ilist")) pub0010PartialViaGate(dir)')
 replace('when(missing error("PUB0010 original2068 source-route whole own-net Cu not fully covered %L\\n" missing))','pub0010MissingCuRows=missing printf("PUB0010_PARTIAL_SOURCE2068_OWN_NET_CU_UNCOVERED=%d\\n" length(missing))')
 replace('"/PUB0010_PAD_INTERNAL_ATTACHED.brd"','"/PUB0010_PARTIAL_UNAPPROVED.brd"')
 replace('f=outfile(strcat(dir "/BOUNDED_NIL_ATTACHMENT_COMPLETE.txt")) fprintf(f "PUB0010_BOUND54_NIL_ORIGINAL_ROUTE_ATTACHMENT_COMPLETE\\nPAD_INTERNAL_STUBS=%d\\nALL54_ORIGINAL_SOURCE_LINE_NETS_PROPERTIES_EXACT\\nALL1739_TYPED_SOURCE_VIAS_EXACT\\nALL2068_FULL_SOURCE_OWN_NET_ROUTE_CU_NATIVE_COVERED\\nALL2698_593_TEXT_PROPS_EXACT\\nFULL915_ACTUAL_CONNECTION_PARTITION_AND_CFX_FINAL_GATES_STILL_REQUIRED\\n" count) close(f) count))',
 '''f=outfile(strcat(dir "/UNAPPROVED_PARTIAL_SAVED_COMPLETE.txt")) fprintf(f "PUB0010_UNAPPROVED_PARTIAL_ONLY\\nPAD_INTERNAL_STUBS=%d\\nSOURCE_BRANCH_GROUPS=877\\nUNRESOLVED_BRANCHES=%d\\nUNRESOLVED54_EXACT_ENTITY_POSTCHECK=%d\\nSOURCE_VIAS_STILL_PENDING_ORIGINAL_NET=%d\\nSOURCE2068_STROKES_NOT_COVERED_CURRENT_OWN_NET=%d\\nALL2698_593_TEXT_PROPS_EXACT\\nALL1739_VIA_XY_PAD_PROPS_EXACT_AND_NET_ONLY_FROZEN_SOURCE_OR_FROZEN_INPUT_NIL\\nFULL915_ACTUAL_CONNECTION_PARTITION_SOURCE_CU_AND_CFX_FINAL_GATES_NOT_APPROVED\\n" count failed length(pub0010Unresolved54) pub0010ViaPendingCount length(pub0010MissingCuRows)) close(f) count))''')
 s+='''
procedure(pub0010FrozenInputViaGate(actual)
 let((rows expected)
  rows=pub403Rows("D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_route_net_diagnostic_run13_v1/ACTUAL_ALL1739_VIAS.ilist")
  expected=nil
  foreach(r rows expected=cons(sprintf(nil "%L" list(car(r) nth(1 r) nth(2 r) sort(nth(3 r) lambda((a b) alphalessp(sprintf(nil "%L" a) sprintf(nil "%L" b)))))) expected))
  expected=sort(expected 'alphalessp)
  unless(length(rows)==1739 && equal(actual expected) error("PUB0010 partial input is not frozen exact1739via set with only9 known NIL nets\\n")) t))
; Partial stage is NOT permission for an unbounded via/net change. Every via
; has exactly its original XY/pad/properties. Only the nine already-frozen input
; NIL nets may remain NIL; no third net, missing/extra via or multiplicity loss.
procedure(pub0010PartialViaGate(dir)
 let((source current before consumed f pending sourceKey candidates)
  unless(length(pub0010OriginalViaNativeRows)==1739 && length(pub0010InputViaNativeRows)==1739 && length(pub0010ViaRows)==1739 error("PUB0010 bounded partial via coverage incomplete\\n"))
  consumed=nil pending=0 f=outfile(strcat(dir "/ALL1739_VIA_SOURCE_OR_FROZEN_INPUT_STATE_REVIEW.ilist"))
  foreach(source pub0010OriginalViaNativeRows
   candidates=setof(v pub0010ViaRows equal(car(v) car(source)) && equal(nth(1 v) nth(1 source)))
   unless(length(candidates)==1 error("PUB0010 partial via exactXY/pad identity missing/duplicate\\n")) current=car(candidates)
   before=car(setof(v pub0010InputViaNativeRows equal(car(v) car(source)) && equal(nth(1 v) nth(1 source))))
   unless(before && equal(nth(3 source) nth(3 current)) && equal(nth(3 before) nth(3 current)) error("PUB0010 partial via original full properties changed\\n"))
   unless(equal(nth(2 before) nth(2 source)) || equal(nth(2 before) "__NO_NET__") error("PUB0010 partial input via differs beyond source-or-NIL\\n"))
   unless(equal(nth(2 current) nth(2 source)) || equal(nth(2 before) "__NO_NET__") && equal(nth(2 current) "__NO_NET__") error("PUB0010 partial via acquired unapproved third net\\n"))
   unless(equal(nth(2 current) nth(2 source)) pending=pending+1)
   consumed=cons(current consumed) fprintf(f "%L\\n" list(source before current))) close(f)
  unless(length(consumed)==1739 error("PUB0010 partial typed via multiplicity differs\\n"))
  pub0010ViaPendingCount=pending t))
'''
 balanced(s);h=D/'public0010_nil_route_stub_partial_v2.il';h.write_text(s,'utf-8')
 man=dict(old);man.update(schema='PUBLIC0010_EXACT54_NIL_SOURCE_NET_PROPAGATION_UNAPPROVED_PARTIAL_V2',helper=str(h),target_marker='UNAPPROVED_PARTIAL_SAVED_COMPLETE.txt',candidate_name='PUB0010_PARTIAL_UNAPPROVED.brd',save_scope='PRIVATE_UNAPPROVED_PARTIAL_ONLY_915_CU_CFX_PENDING',files=[e for e in old['files'] if Path(e['path'])!=V/'public0010_nil_route_stub_repair_v1.il'])
 man['files'] += [dict(path=str(h),sha256=sha(h)),dict(path=str(V/'MANIFEST.json'),sha256=sha(V/'MANIFEST.json'))]
 (D/'MANIFEST.json').write_text(json.dumps(man,indent=2),'utf-8')
 runner=(M/'run_public0010_nil_route_stub_owned_v1.py').read_text().replace("PUBLIC0010_EXACT54_NIL_SOURCE_NET_PROPAGATION_REPAIR_V1","PUBLIC0010_EXACT54_NIL_SOURCE_NET_PROPAGATION_UNAPPROVED_PARTIAL_V2").replace("'PASS_BOUNDED_NIL_ATTACHMENT_PHASE_ONLY' if complete", "'SAVED_UNAPPROVED_PARTIAL_NOT_FINAL_CONNECTION_CU_CFX_APPROVED' if complete")
 rp=M/'run_public0010_nil_route_stub_owned_v2_partial.py';assert not rp.exists();rp.write_text(runner,'utf-8')
 print(json.dumps(dict(helper_sha256=sha(h),manifest_sha256=sha(D/'MANIFEST.json'),runner=str(rp),runner_sha256=sha(rp)),indent=2))
if __name__=='__main__':main()
