"""Prepare bounded54 NIL-route attachment repair; no CAD invocation.

Only existing source-exact NIL straight lines may inherit their frozen PST net
through a positive-area attachment to a new stub wholly inside the target pad.
Source is read first in a private process; public/source files are never saved.
"""
from pathlib import Path
import collections,hashlib,json,sys
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
sys.path.insert(0,str(M));from build_public0010_stub_preflight_v1 import balanced
from prepare_public0010_source_path_stubs_v1 import atom,grid,integer
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
sk=lambda p:json.dumps(str(p).replace('\\','/'))
def jr(p):return json.loads(p.read_text('utf-8-sig'))
def main():
 D=M/'public0010_nil_route_stub_bundle13_v1';assert not D.exists()
 DG=M/'public0010_route_net_diagnostic_run13_v1';PB=M/'public0010_stub_preflight_bundle13_v1';P=M/'public0010_path_stubs_plan13_v1'
 dg=jr(DG/'RUN_RECEIPT.json');assert dg['status']=='COMPLETE_READONLY_ALL_BRANCH_PREFLIGHT' and dg['public_unchanged']
 raw=parse_many((DG/'ACTUAL2068_SOURCE_LINE_CURRENT_OBJECT_NETS.ilist').read_text());assert len(raw)==2068
 nil=[];missing=[];same=0
 for source,objects in raw:
  if isinstance(objects,Atom):assert objects==Atom('nil');missing.append(source);continue
  assert len(objects)==1
  o=objects[0];assert o[1]=='line' and o[3]==source[2] and o[4]==source[3]
  assert sorted(tuple(grid(v) for v in p) for p in o[5])==sorted(tuple(grid(v) for v in p) for p in source[4])
  if o[2]==source[1] and type(o[2])==type(source[1]):same+=1
  else:assert isinstance(o[2],Atom) and o[2]==Atom('nil');nil.append(source)
 assert len(nil)==54 and len(missing)==87 and same==1927
 pst=M/'public0010_frozen_source_and_mapped_pin_net26/SOURCE_MAPPED_PST_FULL_PIN_NET_BINDING.json';pstj=jr(pst)
 assert pstj['status']=='PASS_COMPLETE_2582_LOGICAL_PINS_BOTH_PST_AND_ACTUAL_SOURCE_PHYSICAL_BINDING' and pstj['source_board_sha256']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898'
 nets=set(x[1] for x in nil);nodes={net:[x for x in pstj['source_pin_net_rows'] if x['original_native_declared_net_name']==net and not x['NC_placeholder_only']] for net in nets}
 assert len(nets)==11 and all(nodes.values())
 for rows in nodes.values():
  for r in rows:assert r['source_PST_net_token']==r['candidate_PST_net_token']==r['original_native_declared_net_name'] and r['actual_source_physical_typed_net']==['STRING',r['original_native_declared_net_name']]
 D.mkdir();allowed=D/'EXACT54_SOURCE_LINES_CURRENT_NET_NIL.ilist';allowed.write_text('\n'.join(atom(x) for x in nil)+'\n','utf-8')
 scope=D/'EXACT54_NIL_REPAIR_SOURCE_PST_BINDING.json';scope.write_text(json.dumps(dict(status='FROZEN_NOT_NATIVE_REPAIR_RUN',source_same_net_lines=1927,source_exact_lines_now_NIL=54,source_no_exact_entity_lines=87,non_NIL_wrong_net_lines=0,source_PST_pin_binding=str(pst),source_PST_pin_binding_sha256=sha(pst),nodes_by_original_source_net=nodes,source_54_lines=[atom(x) for x in nil],no_exact_87_lines=[atom(x) for x in missing],method='Only source-exact existing NIL entity; original line+parent all user/allegro props captured from original read-only board before target is opened. Positive native area with whole-new-stub inside actual canonical pad. No new material outside actual target pad.'),indent=2),'utf-8')
 s='load('+sk(M/'public0010_route_net_diagnostic_bundle13_v1/public0010_route_net_diagnostic_v1.il')+')\n'
 s+='''
procedure(pub0010CollectRouteObjects()
 pub0010RouteSeen=makeTable('pub0010RouteSeen nil) pub0010ActualLines=makeTable('pub0010ActualLines nil)
 foreach(n axlDBGetDesign()->nets foreach(b n->branches pub0010RouteObjectsWalk(b)))
 foreach(b axlDBGetLonelyBranches() pub0010RouteObjectsWalk(b)) t)
procedure(pub0010ViaWalk(o)
 let((attrs)
  when(o && !pub0010ViaSeen[o]
   pub0010ViaSeen[o]=t
   when(equal(o->objType "via") pub0010ViaRows=cons(list(o->xy o->name if(o->net then o->net->name else "__NO_NET__") pc13Props(o)) pub0010ViaRows))
   attrs=o->? when(member('children attrs) foreach(x o->children pub0010ViaWalk(x)))
   when(member('segments attrs) foreach(x o->segments pub0010ViaWalk(x))))))
procedure(pub0010ViasSnapshot(path)
 let((rows f)
  pub0010ViaSeen=makeTable('pub0010ViaSeen nil) pub0010ViaRows=nil
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pub0010ViaWalk(b)))
  foreach(b axlDBGetLonelyBranches() pub0010ViaWalk(b))
  rows=sort(foreach(mapcar r pub0010ViaRows sprintf(nil "%L" r)) 'alphalessp)
  unless(length(rows)==1739 error("PUB0010 full1739 via snapshot incomplete\\n"))
  f=outfile(path) foreach(r rows fprintf(f "%s\\n" r)) close(f) rows))
procedure(pub0010NilSourcePrepare(dir)
 let((rows f key objects o)
  sstatus(fullPrecision t) pub403ReadUnits() pub403FullTypedGate(strcat(pub403Bundle "/SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist"))
  pub0010CollectRouteObjects() pub0010OriginalNilProps=makeTable('pub0010OriginalNilProps nil) pub0010NilAllowed=makeTable('pub0010NilAllowed nil)
  rows=pub403Rows(@ALLOWED@) unless(length(rows)==54 error("PUB0010 NIL allowance must be exact54 lines\\n"))
  f=outfile(strcat(dir "/ORIGINAL54_LINE_AND_PARENT_PROPERTIES.ilist"))
  foreach(row rows
   key=pub0010RouteGeomKey(car(row) nth(2 row) nth(3 row) nth(4 row)) objects=pub0010ActualLines[key]
   unless(length(objects)==1 error("PUB0010 original exact line must have unique native object %L\\n" row)) o=car(objects)
   unless(equal(o->net->name nth(1 row)) && equal(o->objType "line") error("PUB0010 frozen original line native source net differs %L\\n" row))
   pub0010OriginalNilProps[key]=list(pc13Props(o) pc13Props(o->parent) o->parent->objType)
   pub0010NilAllowed[key]=nth(1 row)
   fprintf(f "%L\\n" list(row pub0010OriginalNilProps[key]))) close(f)
  pub0010OriginalVias=pub0010ViasSnapshot(strcat(dir "/ORIGINAL_ALL1739_TYPED_VIAS.ilist"))
  f=outfile(strcat(dir "/ORIGINAL_NIL_REPAIR_SOURCE_PREPARED.txt")) fprintf(f "ORIGINAL_SOURCE54_EXACT_NATIVE_LINE_AND_PARENT_PROPERTIES_FROZEN\\nALL1739_TYPED_VIAS_FROZEN\\nNO_SOURCE_MUTATION_OR_SAVE\\n") close(f) t))
procedure(pub0010NilTriggerFits(row)
 prog((key objects o source expected path stub actual overlap)
  key=pub0010RouteGeomKey(nth(4 row) nth(3 row) nth(5 row) nth(6 row))
  expected=pub0010NilAllowed[key] unless(expected && equal(expected nth(2 row)) return(nil))
  objects=pub0010ActualLines[key] unless(length(objects)==1 error("PUB0010 allowed NIL exact line no longer unique %L\\n" row)) o=car(objects)
  unless(null(o->net->name) return(nil))
  unless(equal(pub0010OriginalNilProps[key] list(pc13Props(o) pc13Props(o->parent) o->parent->objType)) error("PUB0010 allowed NIL original line/parent properties changed %L\\n" row))
  path=axlPathStart(list(nth(7 row) nth(8 row)) nth(9 row)) stub=axlPolyFromDB(path ?line2poly t ?endCapType 'ROUND ?holes t)
  when(axlPolyErrorGet() error("PUB0010 NIL attachment stub conversion failed\\n")) stub=remove(nil stub)
  actual=axlPolyFromDB(o ?line2poly t ?endCapType 'ROUND ?holes t)
  when(axlPolyErrorGet() error("PUB0010 existing original-NIL actual line conversion failed\\n")) actual=remove(nil actual)
  unless(stub && actual error("PUB0010 NIL trigger physical stroke empty\\n"))
  overlap=pc13RingOp(stub actual 'AND)
  unless(overlap return(nil)) foreach(p overlap unless(p->area>0.0 return(nil)))
  fprintf(pub0010NilTriggerPort "%L\\n" list(row o "EXACT_ORIGINAL_NIL_LINE_PROPERTIES_AND_POSITIVE_AREA_INTERSECTION")) drain(pub0010NilTriggerPort)
  return(t)))
'''
 old=(PB/'public0010_stub_preflight_v1.il').read_text('utf-8');part=old[old.index('procedure(pub0010StubCandidateStatus('):old.index('procedure(pub0010StubPreflight(')]
 part=part.replace('pub0010StubCandidateStatus','pub0010NilStubCandidateStatus').replace('|| pub0010FrozenStrokeCovered(row) return(', '|| pub0010FrozenStrokeCovered(row) || pub0010NilTriggerFits(row) return(')
 assert '|| pub0010NilTriggerFits(row)' in part;s+=part
 s+='''
procedure(pub0010NilCreateStubs(rows f)
 let((pin path created count)
  count=0
  foreach(row rows
   pin=pc13SotStubPin(car(row) cadr(row))
   unless(pin && equal(pin->xy nth(8 row)) && equal(pin->net->name nth(2 row)) error("PUB0010 frozen stub target changed before creation\\n"))
   path=axlPathStart(list(nth(7 row) nth(8 row)) nth(9 row)) created=axlDBCreatePath(path nth(3 row) nth(2 row))
   unless(created error("PUB0010 exact pad-contained stub creation failed %L\\n" row))
   count=count+1 fprintf(f "%L\\n" list(row created)) drain(f)) count))
procedure(pub0010NilRouteRepair(dir)
 let((f groups row key objects o expected chosen selectedKeys selections failures statusPort status answer geometryKey tested fits failed frozenCount count beforeVias missing)
  sstatus(fullPrecision t) pub403ReadUnits()
  unless(pub0010OriginalVias && pub0010OriginalNilProps error("PUB0010 original source prepare globals absent\\n"))
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  pub0010RepairDRC=axlDBControl('drcEnable) pub0010RepairFill=axlDBControl('dynamicFillMode)
  pub0010CollectRouteObjects() rows=pub403Rows(@ALLOWED@)
  foreach(row rows
   key=pub0010RouteGeomKey(car(row) nth(2 row) nth(3 row) nth(4 row)) objects=pub0010ActualLines[key]
   unless(length(objects)==1 error("PUB0010 allowed exact54 target line must remain unique\\n")) o=car(objects)
   unless(null(o->net->name) && equal(pub0010OriginalNilProps[key] list(pc13Props(o) pc13Props(o->parent) o->parent->objType)) error("PUB0010 target54 must be NIL-only with complete original line/parent properties\\n")))
  beforeVias=pub0010ViasSnapshot(strcat(dir "/TARGET_BEFORE_ALL1739_TYPED_VIAS.ilist"))
  pc13StubSeen=makeTable('pc13StubSeen nil) pc13StubSegments=nil
  foreach(n axlDBGetDesign()->nets foreach(b n->branches pc13SotStubWalk(b))) foreach(b axlDBGetLonelyBranches() pc13SotStubWalk(b))
  pub0010BuildCuIndex() pub0010FrozenKeys=makeTable('pub0010FrozenKeys nil) pub0010StrokeCached=makeTable('pub0010StrokeCached nil) pub0010StrokeCovered=makeTable('pub0010StrokeCovered nil)
  frozenCount=0 f=infile(@FROZEN@)
  while(row=lineread(f) row=car(row) frozenCount=frozenCount+1 pub0010FrozenKeys[pub0010SourceKey(car(row) nth(1 row) nth(2 row) nth(3 row) nth(4 row))]=t) close(f)
  unless(frozenCount==2068 error("PUB0010 whole-sourceCu frozen2068 ledger incomplete\\n"))
  groups=pub403Rows(@PLAN@) unless(length(groups)==877 error("PUB0010 frozen877 source branches incomplete\\n"))
  statusPort=outfile(strcat(dir "/BOUNDED_NIL_ALL_BRANCH_CANDIDATE_STATUS.ilist")) pub0010NilTriggerPort=outfile(strcat(dir "/EXACT54_NIL_STROKE_ATTACHMENT_TRIGGERS.ilist"))
  f=outfile(strcat(dir "/PREFLIGHT_FAILED_BRANCH_GROUPS.ilist")) failed=0 fits=0 tested=0 selections=nil selectedKeys=nil
  foreach(group groups
   chosen=nil
   foreach(candidate cadr(group)
    unless(chosen
     answer=errset(pub0010NilStubCandidateStatus(candidate) t) tested=tested+1
     status=if(answer then car(answer) else "NATIVE_ERROR_SEE_STDOUT") fprintf(statusPort "%L\\n" list(car(group) status candidate)) drain(statusPort)
     when(equal(status "FIT_WHOLE_STROKE_INSIDE_TARGET_REGULAR_PAD") chosen=candidate)))
   if(chosen then fits=fits+1 geometryKey=list(car(chosen) cadr(chosen) nth(2 chosen) nth(3 chosen) nth(7 chosen) nth(8 chosen) nth(9 chosen))
    unless(member(geometryKey selectedKeys) selectedKeys=cons(geometryKey selectedKeys) selections=cons(chosen selections))
   else failed=failed+1 fprintf(f "%L\\n" group) drain(f)))
  close(f) close(statusPort) close(pub0010NilTriggerPort)
  f=outfile(strcat(dir "/BOUNDED_NIL_PREFLIGHT_COMPLETE.txt")) fprintf(f "BRANCHES=877\\nFIT=%d\\nFAILED=%d\\nTESTED=%d\\nUNIQUE_STUBS=%d\\n" fits failed tested length(selections)) close(f)
  when(failed error("PUB0010 all bounded NIL source branches collected; preflight failed count%d, no create/save\\n" failed))
  selections=reverse(selections) f=outfile(strcat(dir "/EXACT_SELECTED_PAD_INTERNAL_STUBS.ilist")) foreach(row selections fprintf(f "%L\\n" row)) close(f)
  f=outfile(strcat(dir "/PAD_INTERNAL_STUBS_CREATED.ilist")) count=axlDBCloak('pub0010NilCreateStubs(selections f) 'shape) close(f)
  unless(count==length(selections) error("PUB0010 bounded pad-internal stub creation batch incomplete\\n"))
  axlDBRefreshId(nil) pub0010CollectRouteObjects() failures=nil
  f=outfile(strcat(dir "/EXACT54_ORIGINAL_ROUTE_NET_AFTER.ilist"))
  foreach(row rows
   key=pub0010RouteGeomKey(car(row) nth(2 row) nth(3 row) nth(4 row)) objects=pub0010ActualLines[key]
   fprintf(f "%L\\n" list(row foreach(mapcar q objects list(q q->net->name pc13Props(q) pc13Props(q->parent)))))
   unless(length(objects)==1 && equal(car(objects)->net->name nth(1 row)) && equal(pub0010OriginalNilProps[key] list(pc13Props(car(objects)) pc13Props(car(objects)->parent) car(objects)->parent->objType)) failures=cons(row failures))) close(f)
  when(failures error("PUB0010 some original54 NIL routes failed exact source-net propagation %L\\n" failures))
  unless(equal(pub0010OriginalVias pub0010ViasSnapshot(strcat(dir "/AFTER_ALL1739_TYPED_VIAS.ilist"))) error("PUB0010 full1739 original typed via XY/pad/net/properties not restored\\n"))
  pub0010BuildCuIndex() pub0010StrokeCached=makeTable('pub0010StrokeCached nil) pub0010StrokeCovered=makeTable('pub0010StrokeCovered nil)
  f=outfile(strcat(dir "/FULL2068_SOURCE_OWN_NET_CU_COVERAGE.ilist")) missing=nil
  foreach(source pub403Rows(@FROZEN@)
   row=list("FULL_SOURCE_CU" "" nth(1 source) nth(2 source) car(source) nth(3 source) nth(4 source))
   answer=errset(pub0010FrozenStrokeCovered(row) t)
   unless(answer && car(answer) missing=cons(source missing)) fprintf(f "%L\\n" list(source answer)) drain(f)) close(f)
  when(missing error("PUB0010 original2068 source-route whole own-net Cu not fully covered %L\\n" missing))
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist")) pub403AllNameGate(nil)
  unless(equal(pub0010RepairDRC axlDBControl('drcEnable)) && equal(pub0010RepairFill axlDBControl('dynamicFillMode)) error("PUB0010 bounded attachments changed DRC/fill mode\\n"))
  unless(axlSaveDesign(?design strcat(dir "/PUB0010_PAD_INTERNAL_ATTACHED.brd") ?noMru t ?noConfirm t) error("PUB0010 bounded attachment candidate save failed\\n"))
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist")) pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist"))
  f=outfile(strcat(dir "/BOUNDED_NIL_ATTACHMENT_COMPLETE.txt")) fprintf(f "PUB0010_BOUND54_NIL_ORIGINAL_ROUTE_ATTACHMENT_COMPLETE\\nPAD_INTERNAL_STUBS=%d\\nALL54_ORIGINAL_SOURCE_LINE_NETS_PROPERTIES_EXACT\\nALL1739_TYPED_SOURCE_VIAS_EXACT\\nALL2068_FULL_SOURCE_OWN_NET_ROUTE_CU_NATIVE_COVERED\\nALL2698_593_TEXT_PROPS_EXACT\\nFULL915_ACTUAL_CONNECTION_PARTITION_AND_CFX_FINAL_GATES_STILL_REQUIRED\\n" count) close(f) count))
'''
 s=s.replace('@ALLOWED@',sk(allowed)).replace('@FROZEN@',sk(P/'SOURCE_FROZEN_REAL_SEGMENTS.ilist')).replace('@PLAN@',sk(P/'PUB0010_STUB_CANDIDATES.ilist'));balanced(s)
 h=D/'public0010_nil_route_stub_repair_v1.il';h.write_text(s,'utf-8')
 original=jr(PB/'MANIFEST.json');files=[Path(x['path']) for x in original['files']]+[Path(x['path']) for x in jr(M/'public0010_route_net_diagnostic_bundle13_v1/MANIFEST.json')['files']]+[DG/'RUN_RECEIPT.json',DG/'ACTUAL2068_SOURCE_LINE_CURRENT_OBJECT_NETS.ilist',DG/'ACTUAL_ALL1739_VIAS.ilist',pst,h,scope,allowed]
 for p,v in pstj['PST_files'].items():assert sha(Path(p))==v;files.append(Path(p))
 man=dict(schema='PUBLIC0010_EXACT54_NIL_SOURCE_NET_PROPAGATION_REPAIR_V1',source_board=str(M/'public_brd_genfeed13/02_0010/0010.brd'),source_sha256=pstj['source_board_sha256'],target_board=original['candidate_board'],target_sha256=original['candidate_board_sha256'],helper=str(h),entry_source='pub0010NilSourcePrepare',entry_target='pub0010NilRouteRepair',source_marker='ORIGINAL_NIL_REPAIR_SOURCE_PREPARED.txt',target_marker='BOUNDED_NIL_ATTACHMENT_COMPLETE.txt',candidate_name='PUB0010_PAD_INTERNAL_ATTACHED.brd',source_units=['millimeters',4],allowed_NIL_lines=54,source_PST_net_count=11,all_source_lines=2068,all_source_vias=1739,all_source_branches=877,files=[dict(path=str(p),sha256=sha(p)) for p in dict.fromkeys(files)])
 (D/'MANIFEST.json').write_text(json.dumps(man,indent=2),'utf-8');print(json.dumps(dict(helper_sha256=sha(h),manifest_sha256=sha(D/'MANIFEST.json'),scope_sha256=sha(scope),allowed_NIL54_sha256=sha(allowed)),indent=2))
if __name__=='__main__':main()
