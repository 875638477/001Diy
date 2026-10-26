"""Prepare read-only native copper checker v5; never launches CAD."""
from pathlib import Path
import hashlib

W = Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
p = W / 'pc13_native_changed_rings_v4.il'
s = p.read_text(encoding='utf-8')
s = s.replace("cond((null(a) if(equal(op 'ANDNOT) then nil else b))", "cond((null(a) if(equal(op 'OR) then b else nil))")
start = s.index('procedure(pc13AddedCuCrossNet(')
end = s.index('\nprocedure(pc13NativeChangedMaterialChecked(', start)
s = s[:start] + r''' ; Read-only fallback: an expanded bbox is a stricter search/AND guard,
; not an allowed-difference envelope. The native ANDNOT proof below must be
; empty, and all other-net copper must miss the conservative rectangle.
procedure(pc13CuConservativeBox(p)
 let((bb x0 y0 x1 y1 path rect rb residual)
  bb=p->bBox unless(bb error("Missing added-copper bbox\n"))
  x0=caar(bb)-0.03 y0=cadar(bb)-0.03
  x1=caadr(bb)+0.03 y1=cadadr(bb)+0.03
  path=axlPathStart(list(x0:y0 x1:y0 x1:y1 x0:y1 x0:y0) 0.0)
  unless(path error("Conservative guard rectangle path failed\n"))
  rect=axlPolyFromDB(path)
  when(axlPolyErrorGet() error("Conservative guard rectangle conversion error\n"))
  rect=remove(nil rect)
  unless(length(rect)==1 error("Conservative guard rectangle missing/fragmented\n"))
  rb=car(rect)->bBox
  ; Assert native rounding still leaves >=0.02mil on EVERY side. This
  ; contains an axis-aligned 0.01mil guard, including every source arc.
  unless(caar(rb)<=caar(bb)-0.02 && cadar(rb)<=cadar(bb)-0.02 && caadr(rb)>=caadr(bb)+0.02 && cadadr(rb)>=cadadr(bb)+0.02
   error("Native conservative bbox margin shrank unexpectedly\n"))
  residual=pc13RingOp(list(p) rect 'ANDNOT)
  when(residual error("Conservative bbox does not contain actual added copper\n"))
  rect))
procedure(pc13CuGuard(p key mf ms)
 let((expanded e method residual)
  unless(p && p->area>0.0 && length(p->vertices)>=3
   error("Added copper must have positive native area and valid vertices\n"))
  pc13RingWrite(mf key "POSITIVE_ADDED_COPPER_INPUT" list(p)) drain(mf)
  e=axlPolyErrorGet() when(e error("Unconsumed native polygon error before margin %L\n" e))
  expanded=axlPolyExpand(list(p) 0.01 'ACU_BLUNT)
  e=axlPolyErrorGet() when(e error("Cross-net margin expansion error %L\n" e))
  unless(expanded error("Cross-net margin returned bareNIL (not empty placeholder)\n"))
  expanded=remove(nil expanded)
  method="NATIVE_EXPAND_0D01MIL"
  unless(expanded
   printf("PC13_MARGIN_EMPTY_FALLBACK %s area=%L bbox=%L vertices=%d\n" key p->area p->bBox length(p->vertices))
   method="CONSERVATIVE_BBOX_0D03MIL_MIN_NATIVE_MARGIN_0D02MIL"
   expanded=pc13CuConservativeBox(p))
  unless(expanded error("Cross-net margin/fallback unexpectedly empty\n"))
  residual=pc13RingOp(list(p) expanded 'ANDNOT)
  when(residual error("Cross-net guard lost source added copper\n"))
  pc13RingWrite(mf key method expanded)
  fprintf(ms "%s\t%s\t%L\t%L\t%d\n" key method p->area p->bBox length(expanded)) drain(ms) drain(mf)
  expanded))
procedure(pc13AddedCuCrossNet(added netName layer key f sf mf ms)
 let((p others direct expanded guarded hitcount)
  hitcount=0
  foreach(p added
   expanded=pc13CuGuard(p key mf ms)
   others=nil
   foreach(e expanded others=append(others pc13NearbyOtherNetCopper(netName layer e->bBox)))
   direct=pc13RingOp(list(p) others 'AND)
   guarded=pc13RingOp(expanded others 'AND)
   pc13RingWrite(f key "ACTUAL_ADDITION_INTERSECTS_OTHER_NET" direct)
   pc13RingWrite(f key "ADDITION_PLUS_0D01MIL_INTERSECTS_OTHER_NET" guarded)
   fprintf(sf "%s\t%d\t%d\n" key length(direct) length(guarded)) drain(sf) drain(f)
   hitcount=hitcount+length(direct)+length(guarded))
  hitcount))
''' + s[end:]
s = s.replace('procedure(pc13NativeChangedMaterialChecked(', 'procedure(pc13NativeChangedMaterialCheckedV5(')
s = s.replace('cf sf crossf crosss crosshits)', 'cf sf crossf crosss crosshits marginf margins)')
s = s.replace('fprintf(crosss "key\\tdirect_intersections\\tmargin_intersections\\n")', 'marginf=outfile(strcat(outDir "/margin_validation_polygons.jsonl")) margins=outfile(strcat(outDir "/margin_validation_methods.tsv"))\n  fprintf(margins "key\\tmethod\\tinput_native_area\\tinput_bbox\\tguard_polys\\n")\n  fprintf(crosss "key\\tdirect_intersections\\tmargin_intersections\\n")')
s = s.replace('key crossf crosss)', 'key crossf crosss marginf margins)')
s = s.replace('close(cf) close(sf) close(crossf) close(crosss)', 'close(cf) close(sf) close(crossf) close(crosss) close(marginf) close(margins)')
s = s.replace('CROSS_NET_INTERSECTIONS_INCLUDING_0D01MIL_MARGIN=%d\\n"', 'CROSS_NET_INTERSECTIONS_INCLUDING_0D01MIL_MARGIN=%d\\nGUARD_VERSION=5\\n"')

# Strings/comments are excluded; reject unbalanced source before giving root
# an Allegro entry point. This is a syntax sanity check, not a native run.
depth = 0
string = False
escape = False
for line in s.splitlines():
    for c in line:
        if string:
            if escape: escape = False
            elif c == '\\': escape = True
            elif c == '"': string = False
        elif c == ';': break
        elif c == '"': string = True
        elif c == '(': depth += 1
        elif c == ')':
            depth -= 1
            assert depth >= 0, line
assert depth == 0 and not string, (depth, string)
assert 'marginf=outfile' in s and 'key crossf crosss marginf margins)' in s
out = W / 'pc13_native_changed_rings_v5.il'
assert not out.exists(), 'Keep generated versions immutable'
out.write_text(s, encoding='utf-8')
print(out)
print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
