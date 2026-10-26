"""Compare full typed physical pad partitions, not just group/netlist counts.

Requires complete protected native source/candidate readbacks. Does not prove
route/material/CFX or replace the independent full593 text/property gate.
"""
from pathlib import Path
from collections import defaultdict,deque,Counter
from decimal import Decimal as Q
import argparse,csv,hashlib,json,sys
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(R.parent/'cadence_geometry_merge_20261025'))
from sexpr import parse_many,Atom
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
def need(ok,msg):
 if not ok:raise ValueError(msg)
def grid(x):
 y=x.quantize(Q('.0001'));need(abs(x-y)<Q('1e-7'),'Coordinate off frozen millimeters4 grid');return y
def typ(x):return (type(x).__name__,str(x))
def ledger(path):
 rows=parse_many(path.read_text('utf-8-sig'));lookup=defaultdict(list);mechanical=defaultdict(list);byident={}
 for si,(symbol,pins) in enumerate(rows):
  for pi,pin in enumerate(pins):
   ident=(si,pi);key=(typ(symbol[1]),typ(pin[0]),grid(pin[1][0]),grid(pin[1][1]));lookup[key].append(ident);byident[ident]=(symbol,pin)
   if pin[3]==Atom('t') and isinstance(pin[2],Atom) and pin[2]==Atom('nil'):mechanical[key[1:]].append(ident)
 need(len(rows)==593 and len(byident)==2698,'Frozen593/2698 typed source ledger incomplete')
 return lookup,mechanical,byident
def readgroups(path,expected):
 lookup,mechanical,byident=expected;available={k:deque(v) for k,v in lookup.items()};used={};groups=defaultdict(set)
 with path.open(newline='') as f:
  records=list(csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
 need(len(records)==2698,'Native group output does not cover2698 actual pads')
 for r in records:
  ref=parse_many(r['refdes'])[0];pin=parse_many(r['pin'])[0];net=parse_many(r['net'])[0]
  key=(typ(ref),typ(pin),grid(Q(r['x'])),grid(Q(r['y'])))
  if key in available:
   while available[key] and available[key][0] in used:available[key].popleft()
   need(bool(available[key]),'Repeated native pad beyond frozen duplicate multiplicity');ident=available[key].popleft()
  else:
   need(isinstance(ref,Atom) and ref==Atom('nil') and isinstance(net,Atom) and net==Atom('nil'),'Native group pad does not bind frozen identity')
   matches=[x for x in mechanical[key[1:]] if x not in used];need(bool(matches),'Unowned mechanical pad not found in full physical ledger');ident=matches[0]
  need(ident not in used,'Duplicate physical pad identity in native groups')
  original_net=byident[ident][1][2];need(typ(net)==typ(original_net),'Actual group pad net type/value differs from frozen2698 ledger')
  used[ident]=r['group'];groups[r['group']].add(ident)
 need(len(used)==2698 and set(used)==set(byident),'Incomplete full physical pin identity coverage')
 return [frozenset(x) for x in groups.values()],used
def actual_typed_pad_gate(path,expected):
 _,_,byident=expected;wanted=Counter()
 def token(symbol,ref,comp,num,pad,net,xy,mech,through):
  need(isinstance(symbol,str) and not isinstance(symbol,Atom),'Physical symbol name is not native STRING')
  return (symbol.upper(),typ(ref),typ(comp),typ(num),typ(pad),typ(net),grid(xy[0]),grid(xy[1]),typ(mech),typ(through))
 for symbol,pin in byident.values():wanted[token(symbol[3],symbol[1],symbol[2],pin[0],pin[5],pin[2],pin[1],pin[3],pin[4])]+=1
 with path.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t',quoting=csv.QUOTE_NONE))
 got=Counter()
 for r in rows:
  values={k:parse_many(r[k])[0] for k in ['symbol_name','refdes','component','number','padstack','net','mechanical','through']}
  got[token(values['symbol_name'],values['refdes'],values['component'],values['number'],values['padstack'],values['net'],[Q(r['x']),Q(r['y'])],values['mechanical'],values['through'])]+=1
 need(len(rows)==2698 and got==wanted,'Actual full2698 symbol/ref/component/number/pad/net/XY/mechanical/through typed multiset differs from frozen full ledger')
 return len(rows)
def partition_review(source,candidate):
 S=Counter(source);T=Counter(candidate);missing=list((S-T).elements());added=list((T-S).elements())
 sm={p:i for i,g in enumerate(source) for p in g};tm={p:i for i,g in enumerate(candidate) for p in g}
 splits=[dict(source_group=i,members=len(g),target_groups=sorted({tm[p] for p in g})) for i,g in enumerate(source) if len({tm[p] for p in g})>1]
 merges=[dict(candidate_group=i,members=len(g),source_groups=sorted({sm[p] for p in g})) for i,g in enumerate(candidate) if len({sm[p] for p in g})>1]
 return dict(pass_exact=not missing and not added,source_groups=len(source),candidate_groups=len(candidate),source_partitions_not_preserved=[sorted(g) for g in missing],unexpected_candidate_partitions=[sorted(g) for g in added],split_source_groups=splits,merged_candidate_groups=merges)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate-native',type=Path,required=True);ap.add_argument('--candidate-board',type=Path,required=True);ap.add_argument('--candidate-sha256',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh isolated maintenance output required')
 source=M/'w/public_brd0010_source_full13_v2';B=M/'public0010_native403_bundle13_v6_restore'
 sr=json.loads((source/'launch_report.json').read_text('utf-8-sig'));cr=json.loads((a.candidate_native/'launch_report.json').read_text('utf-8-sig'))
 need(sr['source_sha256_before']==sr['source_sha256_after']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898' and sr['input_unchanged'],'Source native readback protection failed')
 expected=a.candidate_sha256.upper();need(sha(a.candidate_board)==expected and cr['source_sha256_before']==cr['source_sha256_after']==expected and cr['input_unchanged'] and cr['exit_code']==0,'Candidate native readback protection failed')
 for d in [source,a.candidate_native]:
  for marker in ['PUBLIC_BOARD_COMPLETE.txt','ALL_PINS_AUDIT_COMPLETE','SHAPE_SNAPSHOT_COMPLETE.txt']:
   if marker=='ALL_PINS_AUDIT_COMPLETE':need(marker in (d/'summary.txt').read_text(),'All native pins marker absent')
   else:need((d/marker).is_file(),'Native complete marker absent '+str(d/marker))
 sl=B/'SOURCE_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist';tl=B/'TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist'
 source_expected=ledger(sl);target_expected=ledger(tl)
 actual_typed_pad_gate(source/'all_symbol_pins.tsv',source_expected);actual_typed_pad_gate(a.candidate_native/'all_symbol_pins.tsv',target_expected)
 sg,_=readgroups(source/'native_copper_pin_groups.tsv',source_expected);tg,_=readgroups(a.candidate_native/'native_copper_pin_groups.tsv',target_expected);need(len(sg)==915,'Bound source not915 partitions')
 result=partition_review(sg,tg)
 # Meaningful algorithm controls: group count remains equal in a compensated
 # split+merge corruption, which must still fail exact physical membership.
 control=list(sg);big=next(g for g in control if len(g)>1);singles=[g for g in control if len(g)==1];need(len(singles)>=2,'Control source lacks isolated pads')
 control.remove(big);p=next(iter(big));control += [frozenset([p]),big-{p}];control.remove(singles[0]);control.remove(singles[1]);control.append(singles[0]|singles[1])
 negative=partition_review(sg,control);need(len(control)==915 and not negative['pass_exact'] and negative['split_source_groups'] and negative['merged_candidate_groups'],'Equal-count split+merge control was not rejected')
 inputs=[source/'launch_report.json',source/'native_copper_pin_groups.tsv',source/'all_symbol_pins.tsv',a.candidate_native/'launch_report.json',a.candidate_native/'native_copper_pin_groups.tsv',a.candidate_native/'all_symbol_pins.tsv',sl,tl]
 report=dict(status='PASS_FULL2698_TYPED_PHYSICAL_CONNECTION_PARTITION_EXACT' if result['pass_exact'] else 'FAIL_FULL2698_PHYSICAL_CONNECTION_PARTITION',source_board_sha256=sr['source_sha256_before'],candidate_board=str(a.candidate_board),candidate_board_sha256=expected,full_typed_pads=2698,actual_all2698_symbol_ref_component_number_pad_net_XY_mechanical_through_multiset_exact=True,full593_symbol_pose_text_properties_requires_separate_fresh_gate=True,coincident_NIL_mechanical_multiplicity='Exact frozen full593 ledger occurrence count; never merge nil ref keys. Native nil component for logical-owned mechanical pads resolved only mechanical+NIL+same number+XY.',partitions=result,equal_count_split_plus_merge_negative_control='REJECTED_915_GROUPS_STILL_UNEQUAL_MEMBERS',does_not_approve_copper_CFX_text_properties=True,inputs={str(p):sha(p) for p in inputs})
 a.out.mkdir();p=a.out/'FULL2698_ACTUAL_CONNECTION_PARTITION_REVIEW.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(status=report['status'],source_groups=915,candidate_groups=len(tg),splits=len(result['split_source_groups']),merges=len(result['merged_candidate_groups']),report=str(p),sha256=sha(p)),indent=2));return 0 if result['pass_exact'] else 2
if __name__=='__main__':raise SystemExit(main())
