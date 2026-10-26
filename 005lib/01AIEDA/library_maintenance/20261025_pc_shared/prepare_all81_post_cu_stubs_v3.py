"""Add an exact source-Cu coverage alternative to stale route-entity identity.
Only frozen original straight segments qualify; new stub stroke stays in new pad.
"""
from pathlib import Path
import shutil,hashlib,json
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration';A=W/'all81_stubs_post_cu_v2';B=W/'all81_stubs_post_cu_v3'
V5=W/'all81_source_cu_v5/all81_restore_actual_source_cu_v5.il'
assert not B.exists();B.mkdir()
for name in ('ALL81_STUB_CANDIDATES.ilist','ALL81_STUB_PREPARATION.json'):shutil.copy2(A/name,B/name)
s=(A/'all81_repair_stubs.il').read_text().replace('/all81_stubs_post_cu_v2/','/all81_stubs_post_cu_v3/')
s='load("'+str(V5).replace('\\','/')+'")\n'+s
v5=V5.read_text();index=v5[v5.index('procedure(pc13BuildCuIndex('):v5.index('procedure(pc13ViaAllSnapshot(')]
fallback='''; Source body/route ownership may change while actual original Cu remains.
; This is NOT a bbox/tolerance exception: the whole frozen original stroke
; must be covered by current SAME-NET actual regular Cu via native ANDNOT.
procedure(pc13StubFrozenSourceCuCovers(row)
 let((key path polys same covered)
  covered=nil
  when(equal(nth(4 row) "line")
   key=pc13SourceCuKey(nth(4 row) nth(2 row) nth(3 row) nth(5 row) nth(6 row))
   unless(pc13StubFrozenSourceKeys[key] error("Source-Cu fallback is outside frozen actual424 source segments\\n"))
   path=axlPathStart(nth(6 row) nth(5 row))
   polys=axlPolyFromDB(path ?line2poly t ?endCapType 'ROUND ?holes t)
   when(axlPolyErrorGet() error("Frozen whole source stroke conversion failed\\n")) polys=remove(nil polys)
   unless(polys error("Frozen original source stroke is empty\\n")) covered=t
   foreach(poly polys
    same=pc13NearbySameNetCopper(nth(2 row) nth(3 row) poly->bBox)
    when(pc13RingOp(list(poly) same 'ANDNOT) covered=nil))
   when(covered fprintf(pc13StubSourceFallbackPort "%s\\tWHOLE_ORIGINAL_STROKE_NATIVE_SAME_NET_ANDNOT_EMPTY\\n" key) drain(pc13StubSourceFallbackPort)))
  covered))
'''
s=s.replace('procedure(pc13AllStubFits(',index+fallback+'procedure(pc13AllStubFits(',1)
old='unless(matching || (equal(nth(4 row) "line") && pc13SotLineUnionCovers(row)) error("SOT original own-net full source interval not covered %L\\n" row))'
new='unless(matching || (equal(nth(4 row) "line") && pc13SotLineUnionCovers(row)) || pc13StubFrozenSourceCuCovers(row) error("Original source line neither entity-interval nor whole actual same-net Cu covered %L\\n" row))'
assert old in s;s=s.replace(old,new)
needle='  selectedKeys=nil\n  foreach(group groups'
before='''  pc13StubFrozenSourceKeys=makeTable('pc13StubFrozenSourceKeys nil)
  f=infile("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/all81_source_cu_v5/SOURCE_FROZEN_REAL_SEGMENTS.ilist") frozenCount=0
  while(row=lineread(f) row=car(row) frozenCount=frozenCount+1 pc13StubFrozenSourceKeys[pc13SourceCuKey(car(row) nth(1 row) nth(2 row) nth(3 row) nth(4 row))]=t) close(f)
  unless(frozenCount==424 error("Frozen source segment ledger count differs\\n"))
  pc13CuStepPort=outfile(strcat(dir "/STUB_CU_STEP.txt")) pc13BuildCuIndex("STUB_SOURCE_CU_PREFLIGHT")
  pc13StubBeforeVias=pc13ViaAllSnapshot(strcat(dir "/STUB_BEFORE4541_VIAS.ilist"))
  pc13StubSourceFallbackPort=outfile(strcat(dir "/SOURCE_STROKE_ACTUAL_CU_FALLBACK.tsv"))
  selectedKeys=nil
  foreach(group groups'''
assert needle in s;s=s.replace(needle,before)
s=s.replace('  rows=reverse(rows)\n  f=outfile','  rows=reverse(rows) close(pc13StubSourceFallbackPort)\n  f=outfile',1)
needle='  unless(axlSaveDesign(?design'
before='''  pc13BuildCuIndex("STUB_AFTER_ATTACHMENT")
  unless(equal(pc13StubBeforeVias pc13ViaAllSnapshot(strcat(dir "/STUB_AFTER4541_VIAS.ilist"))) error("Pad-internal source stubs changed original4541 vias\\n"))
  close(pc13CuStepPort)
  unless(axlSaveDesign(?design'''
assert needle in s;s=s.replace(needle,before,1)
# Match the project's existing full user+allegro props/typed pin/pose/text guards.
s=s.replace('oldDrc count pc13StubSeen pc13StubSegments)','oldDrc count frozenCount pc13StubSeen pc13StubSegments)')
depth=0;quoted=False;esc=False
for line in s.splitlines():
 for c in line:
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c==';':break
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0,line
assert depth==0 and not quoted
p=B/'all81_repair_stubs_v3.il';p.write_text(s,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
receipt={'status':'PREPARED_NOT_NATIVE_RUN','candidate_sha256':'0E9810AD00E1518A9DA9AC05663917BEC50C1FD9C2221EE86CB47E1BDA98B159',
 'source_segment_count':424,'remaining_source_path_branches':77,'acceptance':'Full original same-net Cu may replace old path entity identity; all new stub strokes still nativeANDNOT entirely inside actual targetpad.',
 'sourceCu_NATIVE_evidence_review_sha256':sha(W/'SOURCE_CU_V6_NATIVE_EVIDENCE_REVIEW.json'),
 'inputs':{str(x):sha(x) for x in (A/'all81_repair_stubs.il',V5,A/'ALL81_STUB_CANDIDATES.ilist')},
 'outputs':{str(x):sha(x) for x in B.iterdir()}}
(B/'POST_SOURCE_CU_STUB_V3_PREPARATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
