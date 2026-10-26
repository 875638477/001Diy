"""Offline bounded negative controls; fixtures stay in a new maintenance folder."""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,importlib.util,json
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args();assert not args.out.exists();args.out.mkdir(parents=True)
 sp=M/'tools/scan_retirement_native_references_v6_27.py';vp=M/'tools/verify_retirement_canonical_targets_v2_27.py'
 S=mod('retirement_actual_scanner_under_test',sp);V=mod('retirement_canonical_index_under_test',vp)
 ip=M/'canonical_retirement_target127_v127/REQUIRED_CANONICAL_NATIVE_TARGET_INDEX.json';pp=M/'public_retirement_all_confirmed_plan13/PUBLIC_RETIREMENT_EXACT_PLAN.json';gp=M/'public_olb_final13_published13/PUBLIC_GUARD_AFTER_EXACT13_OLB.json'
 index,plan,guard=load(ip),load(pp),load(gp);tests=[]
 def expect_error(name,fn):
  try:fn()
  except (ValueError,KeyError,AssertionError) as e:tests.append({'name':name,'result':'REJECTED_AS_REQUIRED','error':str(e)});return
  raise AssertionError('Invalid fixture was accepted '+name)
 def xml(name,text):
  p=args.out/(name+'.xml');p.write_text(text,encoding='utf-8');return p
 # All real native Footprint locations, including nested cache defaults and
 # instance overrides, must be observed. Historical FootprintName is separate.
 fields=[('package_default','<Package><Defn name="P" pcbFootprint="r0402_2"/></Package>'),('cell_userprop','<Package><Cell><SymbolUserProp><Defn name="PCB Footprint" val="r0402_2"/></SymbolUserProp></Cell></Package>'),('nested_cache_default','<Cache><Package><DefaultValues><UserProp><Defn name="PCB Footprint" val="r0402_2"/></UserProp></DefaultValues></Package></Cache>'),('placed_override','<Page><PartInst><UserProp><Defn name="PCB Footprint" val="r0402_2"/></UserProp></PartInst></Page>')]
 for name,body in fields:
  refs,traces,cov=S.capture(xml(name,'<Lib>'+body+'</Lib>'));assert any(v['value']=='r0402_2' for v in refs);tests.append({'name':'DETECT_RETIRED_REFERENCE_'+name,'result':'ACTUAL_REFERENCE_OBSERVED'})
 refs,traces,cov=S.capture(xml('display_selector','<Lib><SymbolDisplayProp><Defn name="PCB Footprint" locX="1" locY="2" rotation="0"/></SymbolDisplayProp></Lib>'));assert not refs and cov['name_only_SymbolDisplayProp_PCB Footprint']==1;tests.append({'name':'NAME_ONLY_DISPLAY_SELECTOR_IS_PRESENTATION_NOT_VALUE','result':'CLASSIFIED_BY_OFFICIAL_OLB_XSD'})
 refs,traces,cov=S.capture(xml('historical_trace','<Lib><SymbolUserProp><Defn name="FootprintName" val="r0402_2"/></SymbolUserProp></Lib>'));assert not refs and len(traces)==1;tests.append({'name':'HISTORICAL_TRACE_REMAINS_EXPLICIT_AND_SEPARATE','result':'TRACE_OBSERVED_NOT_ACTIVE_FP'})
 expect_error('REAL_USERPROP_MISSING_VALUE',lambda:S.capture(xml('missing_val','<Lib><SymbolUserProp><Defn name="PCB Footprint"/></SymbolUserProp></Lib>')))
 expect_error('REAL_USERPROP_AMBIGUOUS_VALUE',lambda:S.capture(xml('ambiguous_val','<Lib><SymbolUserProp><Defn name="PCB Footprint" val="r0402_pc" value="r0402_2"/></SymbolUserProp></Lib>')))
 expect_error('MISSING_NATIVE_DEFINITION_CLASS',lambda:S.capture(xml('missing_defs','<Lib/>')))
 assert S.native_scalar('nil') is None and S.native_scalar('""')=='';tests.append({'name':'NATIVE_NIL_AND_EMPTY_STRING_REMAIN_DISTINCT','result':'EXACT_TYPED_VALUE_PRESERVED'})
 expect_error('INVALID_NATIVE_SCALAR',lambda:S.native_scalar('oops'))
 table=args.out/'duplicate_native_rows.tsv';table.write_text('name\tobjType\tusedCount\n"r0402_2"\t"symdef"\t0\n"r0402_2"\t"symdef"\t0\n',encoding='utf-8');rows=S.table(table,['name','objType','usedCount']);assert len(rows)==2 and all(S.native_scalar(r['name'])=='r0402_2' and int(r['usedCount'])==0 for r in rows);tests.append({'name':'UNUSED_CACHE_AND_MULTIPLICITY_NOT_DROPPED','result':'BOTH_REAL_NATIVE_ROWS_PRESERVED'})
 expect_error('WRONG_COMPLETE_NATIVE_HEADER',lambda:S.table(table,['name','usedCount','objType']))
 # Every canonical-index corruption changes only an isolated JSON fixture.
 # Cache SHA work for repeatedly read, unmodified files; record stat+SHA and
 # require all observed files retain their exact size/mtime after controls.
 cache={};original_sha=V.sha
 def frozen_sha(p):
  p=Path(p);k=str(p.resolve());st=p.stat();sig=(st.st_size,st.st_mtime_ns)
  if k in cache:assert cache[k][0]==sig,'Evidence changed during negative controls';return cache[k][1]
  value=original_sha(p);cache[k]=(sig,value);return value
 V.sha=frozen_sha
 positive=V.validate_index(index,plan,guard);assert positive['status'].startswith('PASS')
 cases=[]
 def case(name,fn):x=copy.deepcopy(index);fn(x);cases.append((name,x))
 case('MISSING_TARGET',lambda x:x['targets'].pop())
 case('DUPLICATE_TARGET',lambda x:x['targets'].__setitem__(1,copy.deepcopy(x['targets'][0])))
 case('TARGET_PSM_SHA_CHANGED',lambda x:x['targets'][0]['public_psm'].__setitem__('sha256','0'*64))
 case('TARGET_NATIVE_INPUT_SHA_CHANGED',lambda x:x['targets'][0].__setitem__('native_source_psm_sha256','0'*64))
 case('FULL_NATIVE_GRAPH_SHA_CHANGED',lambda x:x['targets'][0]['native_graph'].__setitem__('sha256','0'*64))
 case('FULL_NATIVE_GRAPH_FINGERPRINT_CHANGED',lambda x:x['targets'][0].__setitem__('full_ordered_graph_fingerprint','0'*64))
 case('PAD_CURRENT_SHA_CHANGED',lambda x:x['targets'][0]['pads'][0]['public_pad'].__setitem__('sha256','0'*64))
 case('PAD_COMPLETE_XML_SHA_CHANGED',lambda x:x['targets'][0]['pads'][0]['native_xml'].__setitem__('sha256','0'*64))
 case('PAD_MANUFACTURING_PAYLOAD_CHANGED',lambda x:x['targets'][0]['pads'][0]['complete_manufacturing'].__setitem__('parts',{}))
 case('PAD_DEPENDENCY_REMOVED',lambda x:x['targets'][0]['pads'].pop())
 case('PAD_DEPENDENCY_DUPLICATED',lambda x:x['targets'][0]['pads'].append(copy.deepcopy(x['targets'][0]['pads'][0])))
 case('CANONICALIZER_CODE_IDENTITY_CHANGED',lambda x:x['canonicalizer'].__setitem__('sha256','0'*64))
 for name,x in cases:expect_error(name,lambda x=x:V.validate_index(x,plan,guard))
 for path,(sig,h) in cache.items():p=Path(path);assert (p.stat().st_size,p.stat().st_mtime_ns)==sig
 report={'status':'PASS_RETIREMENT_NATIVE_PARSERS_AND127_TARGET_BOUNDED_NEGATIVE_CONTROLS','tests':tests,'test_count':len(tests),'positive_current_native_and_PAD_recheck':positive,'current_unmodified_file_hash_cache':len(cache),'cache_note':'Only repeated reads of immutable evidence bytes are cached; stat identity checked on every access and after tests. No public file is edited.','target_index':{'path':str(ip),'sha256':sha(ip)},'scanner':{'path':str(sp),'sha256':sha(sp)},'target_validator':{'path':str(vp),'sha256':sha(vp)},'CAD_started':False,'public_files_written':0}
 out=args.out/'RETIREMENT_NATIVE_NEGATIVE_CONTROLS.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':report['status'],'tests':len(tests),'report':str(out),'sha256':sha(out)}))
if __name__=='__main__':main()
