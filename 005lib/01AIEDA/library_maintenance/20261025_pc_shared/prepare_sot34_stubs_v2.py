"""Accept exact same-net collinear source interval unions, not just entities."""
from pathlib import Path
import hashlib
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration\sot34_migration')
s=(W/'sot34_repair_stubs.il').read_text(encoding='utf-8')
start=s.index('procedure(pc13SotStubValidate(')
helper=r''' ; Coordinate normalization is to the DECLARED mils2 database grid.
; No cross-line distance/bbox tolerance is allowed in interval coverage.
procedure(pc13StubGridPoint(p)
 let((x y ix iy)
  x=xCoord(p) y=yCoord(p) ix=round(x*100.0) iy=round(y*100.0)
  unless(abs(x-ix/100.0)<0.0000001 && abs(y-iy/100.0)<0.0000001
   error("Manual source/target route endpoint is off declared mils2 grid %L\n" p))
  list(ix iy)))
procedure(pc13StubGcd(a b)
 let((r) a=abs(a) b=abs(b)
  while(b!=0 r=mod(a b) a=b b=r) a))
procedure(pc13SotLineUnionCovers(row)
 let((ab a b dx dy divisor axis lo hi ranges c d cx cy dx2 dy2 first low high reach ok)
  ab=nth(6 row) a=pc13StubGridPoint(car(ab)) b=pc13StubGridPoint(cadr(ab))
  dx=car(b)-car(a) dy=cadr(b)-cadr(a)
  unless(dx!=0 || dy!=0 error("Degenerate frozen source line\n"))
  axis=if(abs(dx)>=abs(dy) then 0 else 1)
  divisor=pc13StubGcd(dx dy) dx=dx/divisor dy=dy/divisor
  lo=min(nth(axis a) nth(axis b)) hi=max(nth(axis a) nth(axis b)) ranges=nil
  foreach(seg pc13StubSegments
   when(equal(car(seg) "line") && equal(nth(1 seg) nth(2 row)) && equal(nth(2 seg) nth(3 row)) && equal(nth(3 seg) nth(5 row))
    c=pc13StubGridPoint(car(nth(4 seg))) d=pc13StubGridPoint(cadr(nth(4 seg)))
    cx=car(c)-car(a) cy=cadr(c)-cadr(a) dx2=car(d)-car(a) dy2=cadr(d)-cadr(a)
    when(cx*dy-cy*dx==0 && dx2*dy-dy2*dx==0
     low=max(lo min(nth(axis c) nth(axis d))) high=min(hi max(nth(axis c) nth(axis d)))
     when(low<=high ranges=cons(list(low high) ranges)))))
  ranges=sort(ranges lambda((u v) car(u)<car(v))) reach=lo ok=t
  foreach(r ranges
   when(reach<hi
    if(car(r)>reach then ok=nil else reach=max(reach cadr(r)))))
  ok && reach>=hi))
'''
s=s[:start]+helper+s[start:]
old='unless(matching error("SOT original own-net route segment missing %L\\n" row))'
new='unless(matching || (equal(nth(4 row) "line") && pc13SotLineUnionCovers(row)) error("SOT original own-net full source interval not covered %L\\n" row))'
assert old in s
s=s.replace(old,new)
depth=0;string=False;escape=False
for line in s.splitlines():
 for c in line:
  if string:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':string=False
  elif c==';':break
  elif c=='"':string=True
  elif c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0,line
assert depth==0 and not string
out=W/'sot34_repair_stubs_v2.il';assert not out.exists();out.write_text(s,encoding='utf-8')
print(out);print(hashlib.sha256(out.read_bytes()).hexdigest().upper())
