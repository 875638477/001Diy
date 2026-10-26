"""Freeze real source-own-net path branches for public 0010; never launch CAD.

Every branch is independent. A later read-only native preflight must prove each
candidate's entire stroke inside the actual target regular pad. This program
does not approve copper/connection conservation or authorize arbitrary routing.
"""
from pathlib import Path
from decimal import Decimal as Q
import argparse, collections, csv, hashlib, json, math, sys
M=Path(__file__).parent
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration'
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
SOURCE_SHA='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898'
TARGET_SHA='008FEDC680EF5806D2C351CBF819F8A664D833D0A8D68D7A122306EE79C0A9AC'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def jr(p):return json.loads(p.read_text('utf-8-sig'))
def atom(x):
 if isinstance(x,list):return '('+' '.join(atom(v) for v in x)+')'
 if isinstance(x,Atom):return str(x)
 if isinstance(x,str):return json.dumps(x)
 return str(x)
def grid(v):
 q=v.quantize(Q('.0001'));assert abs(v-q)<Q('1e-7'),v
 return q
def integer(v):return int(grid(v)*10000)
def parseadj(p,phase):
 text=p.read_text('utf-8-sig');out={};key=None
 for line in text.splitlines():
  if line.startswith('BEGIN_PIN '):
   selection=parse_many(line[10:])[0];assert len(selection)==4
   key=tuple(selection[:2]);assert key not in out;out[key]={'selection':selection,'rows':[]}
  elif line.startswith('END_PIN '):key=None
  elif key and '\t' in line and not line.startswith('context\t'):
   f=line.split('\t');out[key]['rows'].append([f[0]]+[parse_many(x)[0] for x in f[1:]])
 assert len(out)==806
 assert text.rstrip().endswith('PUB403_ALL806_ADJACENCY_COMPLETE PHASE='+phase)
 return out
def own_segments(rows,net):
 return [x for x in rows if x[0] in ('DIRECT_PATH_SEGMENT','DIRECT_NEIGHBOR','INDIRECT_PATH_SEGMENT','INDIRECT_SOURCE_PATH','INDIRECT_OWN_NET_PATH') and x[2] in ('line','arc') and type(x[3])==type(net) and x[3]==net and isinstance(x[8],list) and len(x[8])==2]
def line_covered(source,targets):
 a,b=[[integer(v) for v in p] for p in source[8]];dx=b[0]-a[0];dy=b[1]-a[1]
 if not(dx or dy):return False
 axis=0 if abs(dx)>=abs(dy) else 1;lo=min(a[axis],b[axis]);hi=max(a[axis],b[axis]);ranges=[]
 divisor=math.gcd(dx,dy);dx//=divisor;dy//=divisor
 for t in targets:
  if t[2]!='line' or t[7]!=source[7] or t[9]!=source[9]:continue
  c,d=[[integer(v) for v in p] for p in t[8]]
  if (c[0]-a[0])*dy-(c[1]-a[1])*dx or (d[0]-a[0])*dy-(d[1]-a[1])*dx:continue
  l=max(lo,min(c[axis],d[axis]));h=min(hi,max(c[axis],d[axis]))
  if l<=h:ranges.append((l,h))
 reach=lo
 for l,h in sorted(ranges):
  if reach>=hi:return True
  if l>reach:return False
  reach=max(reach,h)
 return reach>=hi
def direct_retained(sr,tr,net):
 ss=own_segments(sr,net);tt=own_segments(tr,net)
 if not ss or not tt:return False
 for x in ss:
  if x[2]=='line':
   if not line_covered(x,tt):return False
  elif not any(t[2]=='arc' and t[7]==x[7] and t[9]==x[9] and t[8] in [x[8],list(reversed(x[8]))] for t in tt):return False
 return True
def ledger(path):
 rows=parse_many(path.read_text('utf-8-sig'));byref={};lookup=collections.defaultdict(list);identities={}
 for si,(ident,pins) in enumerate(rows):
  for pi,pin in enumerate(pins):
   key=(ident[1],pin[0],grid(pin[1][0]),grid(pin[1][1]))
   if key in lookup:
    # Coincident unnamed mechanical pads are not any selected ordinary pin.
    # Preserve their duplicate multiplicity/physical row identity; no source
    # copper or ordinary-net equivalence is inferred from this tie-break.
    assert ident[0]=='NONLOGICAL' and isinstance(pin[2],Atom) and pin[2]==Atom('nil') and pin[3]==Atom('t'),key
   lookup[key].append((si,pi));identities[(si,pi)]=(ident,pin)
   if ident[0]=='LOGICAL':
    k=(ident[1],pin[0])
    if k in byref:assert pin[0]=='' and pin[3]==Atom('t'),k
    else:byref[k]=(si,pi,pin)
 assert len(rows)==593 and sum(map(len,lookup.values()))==2698 and sum(len(pins) for ident,pins in rows if ident[0]=='LOGICAL')==2688
 return byref,lookup,identities
def group_members(path,lookup,identities):
 g=collections.defaultdict(set);keys={};available={k:collections.deque(v) for k,v in lookup.items()};mechanical=collections.defaultdict(list)
 for ident,(symbol,pin) in identities.items():
  if pin[3]==Atom('t') and isinstance(pin[2],Atom) and pin[2]==Atom('nil'):
   mechanical[(pin[0],grid(pin[1][0]),grid(pin[1][1]))].append(ident)
 with path.open(newline='') as f:
  for r in csv.DictReader(f,delimiter='\t'):
   ref=Atom('nil') if r['refdes']=='nil' else r['refdes']
   number=parse_many(r['pin'])[0] if r['pin'].startswith('"') else r['pin']
   key=(ref,number,grid(Q(r['x'])),grid(Q(r['y'])))
   if key in available:
    while available[key] and available[key][0] in keys:available[key].popleft()
    assert available[key],key
    ident=available[key].popleft()
   else:
    assert isinstance(ref,Atom) and ref==Atom('nil') and r['net']=='nil',key
    matches=[x for x in mechanical[key[1:]] if x not in keys];assert matches,key
    # Native GetConnect emits nil component for logical-owned mechanical pads.
    # Coincident exact NIL-mechanical rows retain physical multiplicity.
    ident=matches[0]
   assert ident not in keys;keys[ident]=r['group'];g[r['group']].add(ident)
 assert len(keys)==2698
 return {k:g[v] for k,v in keys.items()},len(g)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();D=a.out
 assert D.resolve().is_relative_to(M.resolve()) and not D.exists()
 B=M/'public0010_native403_bundle13_v6_restore'
 source=M/'public0010_source806_probe13/PUB403_source_pin_adjacency.ilist'
 target=M/'public0010_restored_fresh24/PUB403_target_pin_adjacency.ilist'
 for path,expected in [(source.parent/'RUN_RECEIPT.json',SOURCE_SHA),(target.parent/'RUN_RECEIPT.json',TARGET_SHA)]:
  receipt=jr(path);assert receipt['status']=='PASS_NATIVE_CASE_PHASE_ONLY' and receipt['source_sha256_before']==receipt['source_sha256_after']==expected and receipt['public_unchanged']
 candidate=M/'public0010_netrev_text_restore13/PUB0010_NETREV_RESTORED.brd';assert sha(candidate)==TARGET_SHA
 sp,sl,si=ledger(B/'SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist')
 tp,tl,ti=ledger(B/'TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist')
 sg,sc=group_members(M/'w/public_brd0010_source_full13_v2/native_copper_pin_groups.tsv',sl,si)
 tg,tc=group_members(M/'w/module0010_after403_full24/native_copper_pin_groups.tsv',tl,ti)
 assert sc==915 and tc==1658
 sr=parseadj(source,'source');tr=parseadj(target,'target');assert sr.keys()==tr.keys()
 frozen={};groups=[];decisions=[];issues=[]
 for key,data in sr.items():
  old_id,old_pi,old=sp[key];new_id,new_pi,new=tp[key];assert (old_id,old_pi)==(new_id,new_pi)
  srows=data['rows'];trows=tr[key]['rows'];before=next(x for x in srows if x[0]=='TARGET');after=next(x for x in trows if x[0]=='TARGET')
  assert type(before[3])==type(after[3])==type(old[2])==type(new[2]) and before[3]==after[3]==old[2]==new[2]
  assert [grid(x) for x in before[6]]==[grid(x) for x in old[1]] and [grid(x) for x in after[6]]==[grid(x) for x in new[1]],(key,before[6],old[1],after[6],new[1])
  changed=sg[(old_id,old_pi)]!=tg[(new_id,new_pi)]
  paths=[x for x in srows if x[0] in ('DIRECT_NEIGHBOR','INDIRECT_SOURCE_PATH','INDIRECT_OWN_NET_PATH') and x[2] in ('path','cline','line','arc')]
  targetpaths=[x for x in trows if x[0] in ('DIRECT_NEIGHBOR','INDIRECT_SOURCE_PATH','INDIRECT_OWN_NET_PATH') and x[2] in ('path','cline','line','arc')]
  for seg in own_segments(srows,old[2]):
   raw=[seg[2],seg[3],seg[7],seg[9],[[grid(v) for v in p] for p in seg[8]]];frozen[atom(raw)]=raw
  if not paths:
   decisions.append(dict(ref=key[0],pin=key[1],action='NO_SOURCE_PATH',partition_changed=changed,source_direct=len([x for x in srows if x[0]=='DIRECT_NEIGHBOR']),target_direct=len([x for x in trows if x[0]=='DIRECT_NEIGHBOR'])))
   if changed:issues.append(dict(ref=key[0],pin=key[1],kind='CHANGED_PARTITION_NO_SOURCE_REAL_PATH',source_rows=[atom(x) for x in srows]))
   continue
  if (not changed and targetpaths) or direct_retained(srows,trows,old[2]):
   decisions.append(dict(ref=key[0],pin=key[1],action='ALREADY_ATTACHED_OR_FULL_SOURCE_PATH_RETAINED',partition_changed=changed));continue
  if isinstance(old[2],Atom) or old[2]=='':
   issues.append(dict(ref=key[0],pin=key[1],kind='SOURCE_NIL_OR_EMPTY_NET_NO_COPPER_AUTHORIZED'));continue
  seenpaths=set()
  for source_path in paths:
   if source_path[1] in seenpaths:continue
   seenpaths.add(source_path[1]);branch=[x for x in own_segments(srows,old[2]) if x[11]==source_path[1] or x[1]==source_path[1]]
   if not branch:issues.append(dict(ref=key[0],pin=key[1],kind='SOURCE_BRANCH_SEGMENTS_MISSING',path=str(source_path[1])));continue
   if direct_retained(branch,trows,old[2]):
    decisions.append(dict(ref=key[0],pin=key[1],path=str(source_path[1]),action='SOURCE_BRANCH_ALREADY_FULLY_RETAINED'));continue
   choices=[];seen=set()
   for seg in branch:
    if seg[7] not in ('ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM') or not isinstance(seg[9],Q) or seg[9]<=0:continue
    se=[[grid(v) for v in p] for p in seg[8]]
    if se[0]==se[1]:continue
    for point in se:
     if point==new[1]:continue
     row=[key[0],key[1],old[2],seg[7],seg[2],seg[9],se,point,new[1],min(Q('.127'),seg[9]),old[1],new[5]]
     s=atom(row)
     if s in seen:continue
     seen.add(s);distance=sum((point[k]-new[1][k])**2 for k in range(2));choices.append((point!=old[1],distance,row))
   if not choices:issues.append(dict(ref=key[0],pin=key[1],kind='NO_REAL_ENDPOINT_CANDIDATE',path=str(source_path[1])));continue
   choices.sort(key=lambda x:(x[0],x[1]));groups.append([[key[0],key[1],old_pi,str(source_path[1])],[x[2] for x in choices]])
   decisions.append(dict(ref=key[0],pin=key[1],path=str(source_path[1]),action='NATIVE_BRANCHWISE_CONTAINED_STROKE_SELECTION',partition_changed=changed,candidates=len(choices)))
 assert groups
 D.mkdir();plan=D/'PUB0010_STUB_CANDIDATES.ilist';plan.write_text('\n'.join(atom(x) for x in groups)+'\n','utf-8')
 frozenfile=D/'SOURCE_FROZEN_REAL_SEGMENTS.ilist';frozenfile.write_text('\n'.join(sorted(frozen))+'\n','utf-8')
 inputs=[source,target,source.parent/'RUN_RECEIPT.json',target.parent/'RUN_RECEIPT.json',B/'SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist',B/'TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist',M/'w/public_brd0010_source_full13_v2/native_copper_pin_groups.tsv',M/'w/module0010_after403_full24/native_copper_pin_groups.tsv']
 report=dict(status='PREPARED_NO_NATIVE_RUN',source_board_sha256=SOURCE_SHA,candidate_board=str(candidate),candidate_sha256=TARGET_SHA,units=['millimeters',4],source_groups=sc,target_groups=tc,selected_pins=806,branch_groups=len(groups),candidate_rows=sum(len(x[1]) for x in groups),frozen_actual_source_segments=len(frozen),decisions=decisions,unresolved_issues=issues,inputs={str(p):sha(p) for p in inputs},outputs={p.name:sha(p) for p in D.iterdir()})
 (D/'PUB0010_STUB_PREPARATION.json').write_text(json.dumps(report,indent=2,default=str),'utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ('decisions','inputs')},indent=2,default=str))
if __name__=='__main__':main()
