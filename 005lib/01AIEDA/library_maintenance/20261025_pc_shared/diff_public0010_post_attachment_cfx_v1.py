"""Full ordered CFX diagnostic after geometry-only attachment changes.

Does not bless origin/date/revision differences. Only full named outer object
collections and unique whole Pin objects are aligned for a precise diff; all
payload fields and nested order remain visible. No CAD or design writes.
"""
from pathlib import Path
import argparse,copy,hashlib,json,xml.etree.ElementTree as E
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
local=lambda tag:tag.rsplit('}',1)[-1]
def need(v,m):
 if not v:raise ValueError(m)
def text(x):return (x or '').strip()
def align(source,target):
 ledger=[]
 for kind in ['Gate','Part','PartDefn']:
  aa=[e for e in source.iter() if local(e.tag)=='xml-objects' and e.get('Name')==kind];bb=[e for e in target.iter() if local(e.tag)=='xml-objects' and e.get('Name')==kind]
  need(len(aa)==len(bb) and len(aa)<=1,'Native independent collection wrapper cohort changed '+kind)
  if not aa:continue
  need(len(aa[0])==len(bb[0])==1,'Malformed independent collection wrapper')
  a,b=aa[0][0],bb[0][0];xa={e.get('Name'):e for e in a};xb={e.get('Name'):e for e in b}
  need(None not in xa and len(xa)==len(a) and len(xb)==len(b) and set(xa)==set(xb),'Whole independent object names lost/duplicated '+kind)
  if kind=='Gate':
   for name,u in xa.items():
    v=xb[name];up=[(i,c) for i,c in enumerate(u) if local(c.tag)=='children' and c.get('Kind')=='Pin'];vp=[(i,c) for i,c in enumerate(v) if local(c.tag)=='children' and c.get('Kind')=='Pin']
    if len(up)==len(vp)==1 and up[0][0]==vp[0][0]:
     up,vp=up[0][1],vp[0][1];keys=lambda z:[(e.get('Name'),e.get('AltName')) for e in z];ka,kb=keys(up),keys(vp)
     if len(ka)==len(set(ka)) and len(kb)==len(set(kb)) and set(ka)==set(kb):
      bykey=dict(zip(kb,list(vp)));vp[:]=[bykey[k] for k in ka]
      if ka!=kb:ledger.append(dict(kind='whole_Pin_outer_order',gate=name,source_order=ka,candidate_order=kb))
  order=[e.get('Name') for e in a];actual=[e.get('Name') for e in b];b[:]=[xb[n] for n in order]
  if order!=actual:ledger.append(dict(kind='whole_'+kind+'_outer_order',source_order=order,candidate_order=actual))
 return ledger
def diff(a,b,path=''):
 name=local(a.tag);selector='[@Name='+repr(a.get('Name'))+']' if a.get('Name') is not None else ''
 path=path+'/'+name+selector;out=[]
 if a.tag!=b.tag:out.append(dict(path=path,field='tag',before=a.tag,after=b.tag))
 for key in sorted(set(a.attrib)|set(b.attrib)):
  if a.get(key)!=b.get(key):out.append(dict(path=path,field='@'+key,before=a.get(key),after=b.get(key)))
 for fld in ['text','tail']:
  if text(getattr(a,fld))!=text(getattr(b,fld)):out.append(dict(path=path,field=fld,before=text(getattr(a,fld)),after=text(getattr(b,fld))))
 if len(a)!=len(b):out.append(dict(path=path,field='child_count',before=len(a),after=len(b)))
 for i,(x,y) in enumerate(zip(a,b)):out+=diff(x,y,path+'['+str(i+1)+']')
 return out
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--candidate-native',type=Path,required=True);ap.add_argument('--candidate-sha256',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh output required')
 source=M/'w/module0010_after403_full24';sourceSHA='008FEDC680EF5806D2C351CBF819F8A664D833D0A8D68D7A122306EE79C0A9AC';targetSHA=a.candidate_sha256.upper()
 for d,h in [(source,sourceSHA),(a.candidate_native,targetSHA)]:
  q=json.loads((d/'launch_report.json').read_text('utf-8-sig'));need(q['source_sha256_before']==q['source_sha256_after']==q['staged_sha256']==h and q['input_unchanged'] and not q['write_candidate'] and q['exit_code']==0,'Protected native complete CFX source/candidate binding failed')
  need(sha(d/'INPUT_COPY.brd')==h and (d/'PUBLIC_BOARD_COMPLETE.txt').exists(),'Native staged bytes/completion marker failed')
 result={};inputs=[]
 for ext in ['dcfx','tcfx']:
  sp=source/('ACTUAL_SUPPLEMENT.'+ext);tp=a.candidate_native/('ACTUAL_SUPPLEMENT.'+ext);inputs += [sp,tp]
  x=E.parse(sp).getroot();y=E.parse(tp).getroot();alignments=align(x,y);changes=diff(x,y)
  result[ext]=dict(strict_equal_after_whole_independent_object_alignment=not changes,ordered_differences=changes,whole_object_outer_order_ledger=alignments)
 report=dict(status='PASS_ALL_POST_ATTACHMENT_CFX_FIELDS_STRICT_EXACT' if all(v['strict_equal_after_whole_independent_object_alignment'] for v in result.values()) else 'DIAGNOSTIC_CFX_DIFFERENCES_UNAPPROVED',source_board_sha256=sourceSHA,candidate_board_sha256=targetSHA,extensions=result,no_origin_date_revision_waivers_applied=True,not_original_source_CFX_gate='This compares geometry-stage008FED to candidate. Complete680500 source rule/PartDefn/Gate/PST inverse remains a separate mandatory gate.',inputs={str(p):sha(p) for p in inputs+[source/'launch_report.json',a.candidate_native/'launch_report.json']})
 a.out.mkdir();p=a.out/'POST_ATTACHMENT_COMPLETE_CFX_STRICT_DIFF.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(status=report['status'],changes={k:len(v['ordered_differences']) for k,v in result.items()},report=str(p),sha256=sha(p)),indent=2))
if __name__=='__main__':main()
