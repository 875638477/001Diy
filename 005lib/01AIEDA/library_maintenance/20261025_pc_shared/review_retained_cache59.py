"""Compare retained actual definitions with pre-all81 source, without an
external-library equivalence claim. New eight names are reported separately.
"""
from pathlib import Path
import csv,sys,hashlib,json,argparse,collections
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
G=R.parent/'cadence_geometry_merge_20261025';sys.path.insert(0,str(G))
import compare_native_geometry as n
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def manifest(p):
 with (p/'manifest.tsv').open(encoding='utf-8-sig',newline='') as f:return {r['name'].casefold():r for r in csv.DictReader(f,delimiter='\t')}
class Context(n.Native):
 def __init__(self,p):
  super().__init__(p)
  for attrs,props in self.nodes.values():
   if 'textBlock' in attrs:
    block=self.textblocks[str(attrs['textBlock'])]
    key='FULL_BLOCK_'+n.digest([(k,self.value(v,k)) for k,v in sorted(block.items()) if k not in ('name','userDefined')])
    self.textblocks[key]=block;attrs['textBlock']=key
ap=argparse.ArgumentParser();ap.add_argument('--actual-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
assert not a.out.exists()
s=manifest(R/'w/final_alt13');t=manifest(a.actual_dir)
assert len(s)==81 and len(t)==59
retained=sorted(s.keys()&t.keys());added=sorted(t.keys()-s.keys())
assert len(retained)==51 and added==['ddr4_dimm_288p_pc','lqfp-48','mount_156a_p4567_pc','qfn32_4x4','smd_3225','sod323','sop-8-e-150mil','sot23-3']
native={};padnames=set()
for name in retained:
 for side,rows in [('source',s),('actual',t)]:
  ob=Context(rows[name]['file']);native[side,name]=ob
  padnames.update(str(attrs['name']) for attrs,p in ob.nodes.values() if attrs.get('objType')=='padstack')
# Same reference identity is sufficient ONLY for actual-source cache comparison.
# Complete embedded padgraph fields remain compared; full external PAD XML
# manufacturing compatibility must be checked by a separate public-library gate.
n.PAD_PUBLIC={name.casefold():'SAME_REFERENCE_IDENTITY:'+name.casefold() for name in padnames}
rows=[]
for name in retained:
 x=native['source',name].signature();y=native['actual',name].signature()
 row={'name':name,'exact':not x['issues'] and not y['issues'] and x['signature']==y['signature'],
  'source_raw':s[name]['file'],'source_raw_sha256':sha(s[name]['file']),
  'actual_raw':t[name]['file'],'actual_raw_sha256':sha(t[name]['file']),
  'source':x,'actual':y}
 rows.append(row)
report={'status':'PASS_ALL51_RETAINED_ACTUAL_CACHED_DEFINITIONS_SOURCE_EXACT' if all(r['exact'] for r in rows) else 'FAIL_RETAINED_CACHE_CHANGED',
 'source_definitions':81,'actual_definitions':59,'retained_source_exact':sum(r['exact'] for r in rows),'removed_duplicate_definitions':22,
 'eight_new_definition_names_require_separate_full_target_review':added,
 'scope':'Complete physical native graph plus full font/block content and properties of51 retained definitions compared against actual49AF source. Only native handles/local textBlock slots and normal graph administrative/instance links are canonicalized. Same external PAD-reference identity supplies no new external library compatibility claim. Whole-board connectivity/route copper/rules are separate gates.',
 'results':rows,'inputs':{str(p):sha(p) for p in (a.actual_dir/'manifest.tsv',R/'w/final_alt13/manifest.tsv',G/'compare_native_geometry.py',Path(__file__))}}
a.out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('results','inputs')},indent=2));print('REPORT',a.out,'SHA256',sha(a.out))
