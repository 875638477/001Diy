"""Actual full-native retirement reference scanner. Never substitutes plans for observed references."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re,xml.etree.ElementTree as E,importlib.util
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared');R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');LIB=Path(r'D:\001DIY\005lib')
CATEGORIES=('project_capture','project_brd_declared','project_brd_placed','public_olb','public_dsn','public_brd_declared','public_brd_placed','active_device_map')
s=importlib.util.spec_from_file_location('native_s_expression_complete_parser',R.parent/'cadence_geometry_merge_20261025/sexpr.py');SX=importlib.util.module_from_spec(s);s.loader.exec_module(SX)
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def norm(p):return str(Path(p).resolve()).casefold()
def local(t):return t.rsplit('}',1)[-1]
def file(v,evidence):
 p=Path(v['path']);need(p.is_file() and sha(p)==v['sha256'],'Frozen artifact missing/changed '+str(p));evidence[str(p)]=v['sha256'];return p

def stem(value):
 v=value.strip()
 if len(v)>=2 and v[0]==v[-1] and v[0] in ['\"',"'"]:v=v[1:-1]
 v=v.replace('\\','/').rsplit('/',1)[-1]
 if v.casefold().endswith(('.psm','.dra')):v=v.rsplit('.',1)[0]
 return v.casefold()
def capture(path):
 root=E.parse(path).getroot();need(local(root.tag) in {'Lib','Design'},'Complete native Capture source class missing');out=[];traces=[];coverage=Counter()
 def visit(e,p):
  tag=local(e.tag);coverage[tag]+=1
  for key,value in e.attrib.items():
   if key.casefold()=='pcbfootprint':out.append({'path':p+'/@'+key,'value':value,'kind':'native_pcbFootprint_attribute'})
  if tag=='Defn' and str(e.get('name','')).casefold() in {'pcb footprint','footprintname'}:
   keys=[k for k in ['val','value','Value'] if k in e.attrib];need(len(keys)==1,'Named native footprint UserProp has missing/ambiguous value field '+p);row={'path':p+'/@'+keys[0],'value':e.get(keys[0]),'kind':'complete_UserProp_native_definition'}
   (out if e.get('name').casefold()=='pcb footprint' else traces).append(row)
  counts=Counter()
  for child in e:counts[local(child.tag)]+=1;visit(child,p+'/'+local(child.tag)+'['+str(counts[local(child.tag)])+']')
 visit(root,'/'+local(root.tag)+'[1]');need(coverage['Defn']>0,'Complete native Capture definitions absent');return out,traces,dict(coverage)

def native_scalar(s):
 v=SX.parse_many(s);need(len(v)==1,'Malformed native scalar');x=v[0]
 if isinstance(x,SX.Atom):need(str(x)=='nil','Unexpected non-string footprint reference');return None
 need(isinstance(x,str),'Native footprint scalar not string/nil');return x

def table(path,fields):
 lines=path.read_text(encoding='utf-8-sig').splitlines();need(lines and lines[0].split('\t')==fields,'Exact complete native fields missing '+str(path));rows=[]
 for line in lines[1:]:
  v=line.split('\t');need(len(v)==len(fields),'Malformed complete native row');rows.append(dict(zip(fields,v)))
 return rows

def readonly_job(row,evidence,marker):
 p=file(row,evidence);q=load(p);d=p.parent;need(q['exit_code']==0 and q['input_unchanged'] and not q['write_candidate'] and '-readonly' in q['arguments'],'Native evidence is not source-protected readonly');h=q['source_sha256_before'];need(h==q['source_sha256_after']==q['staged_sha256']==sha(d/'INPUT_COPY.brd')==sha(q['source']),'Native original/copy SHA changed');need(sha(q['script'])==q['script_sha256'],'Native executed inventory helper changed');need((d/marker).is_file(),'Complete native inventory marker missing');need('*Error*' not in (d/'stdout.txt').read_text(encoding='utf-8-sig'),'Native inner inventory error');evidence[str(d/marker)]=sha(d/marker);return q

def capture_binding(row,evidence):
 xml=file(row['xml'],evidence);need(sha(row['native_input'])==row['public_sha256'],'Native XML input is not byte-identical to current actual source')
 mode=row['binding_mode']
 if mode=='protected_native_capture_export':
  p=file(row['native_job'],evidence);q=load(p);need(q['status']=='COMPLETE' and q['exit_code']==0 and q['protected_unchanged'],'Native Capture export did not complete unchanged');need(q['protected_before'].get(row['native_input'])==q['protected_after'].get(row['native_input'])==row['public_sha256'],'Native Capture original/staged source byte identity unbound')
 elif mode=='frozen_original_native_export_bindings':
  p=file(row['frozen_bindings'],evidence);items=load(p);matches=[r for r in items if norm(r['path'])==norm(row['public_path'])];need(len(matches)==1 and matches[0]['sha256']==row['public_sha256'] and norm(matches[0]['xml'])==norm(xml) and matches[0]['xml_sha256']==sha(xml),'Original native XML reuse does not match complete frozen binding')
 else:raise ValueError('Unrecognized native Capture source identity binding')
 for p in row['acceptance_proofs']:
  v=load(file(p,evidence));need(str(v['status']).startswith('PASS'),'Independent native/publication acceptance is not PASS')
 return xml

def board_references(row,evidence):
 out=[];mode=row['inventory_mode']
 if mode=='complete_native_reference_inventory_v1':
  q=readonly_job(row['native_job'],evidence,'ALL_NATIVE_REFERENCE_INVENTORY_COMPLETE.txt');need(q['source_sha256_before']==row['public_sha256'],'Current BRD is not identical to inventoried native input');files={k:file(v,evidence) for k,v in row['inventory_files'].items()};need(set(files)=={'components','symbols','symdefs'},'Missing complete BRD source class');c=table(files['components'],['refdes','device_type','package','placed']);sy=table(files['symbols'],['symbol_name','definition_name','refdes','objType']);defs=table(files['symdefs'],['name','objType','usedCount']);marker=(Path(row['native_job']['path']).parent/'ALL_NATIVE_REFERENCE_INVENTORY_COMPLETE.txt').read_text();need(all((k+'='+str(n)+'\n') in marker for k,n in [('COMPONENTS',len(c)),('SYMBOLS',len(sy)),('DEFINITIONS',len(defs))]),'Actual BRD full class counts differ from native completion')
 elif mode=='main13_complete1066_plus_all59_symdefs':
  q=readonly_job(row['native_job'],evidence,'ALL81_FINAL_FRESH_COMPLETE.txt');need(q['source_sha256_before']==row['public_sha256'],'Main current BRD byte binding differs');files={k:file(v,evidence) for k,v in row['inventory_files'].items()};need(set(files)=={'components','symbols','symdefs'},'Main complete source class missing');lines=files['components'].read_text().splitlines();need(len(lines)==1066,'Main declaration table omitted unplaced/source components');c=[]
  for line in lines:
   v=line.split('\t');need(len(v)==6,'Main complete component metadata schema changed');c.append({'refdes':v[0],'package':v[1]})
  sy=table(files['symbols'],['symbol_name','refdes','component','definition','x','y','rotation','mirrored','pin_count']);sy=[{'symbol_name':r['symbol_name'],'definition_name':r['definition']} for r in sy];defs=table(files['symdefs'],['name','objType','usedCount']);q2=readonly_job(row['all_symdefs_job'],evidence,'DEFINITION_INVENTORY_COMPLETE.txt');need(q2['source_sha256_before']==row['public_sha256'] and len(defs)==59 and sum(int(v['usedCount']) for v in defs)==1066,'Main all cached definitions including unused not bound')
 else:raise ValueError('Complete final BRD inventory mode missing')
 refs=[{'scope':'declared','field':'component.package','owner':r['refdes'],'value':native_scalar(r['package'])} for r in c]
 for r in sy:
  for k in ['symbol_name','definition_name']:refs.append({'scope':'placed','field':k,'value':native_scalar(r[k])})
 for r in defs:refs.append({'scope':'placed','field':'all_saved_symdef.name_including_unused','value':native_scalar(r['name']),'usedCount':int(r['usedCount'])})
 for p in row['acceptance_proofs']:need(str(load(file(p,evidence))['status']).startswith('PASS'),'Final BRD semantic/publication acceptance not passed')
 return refs,{'declared_components':len(c),'placed_symbols':len(sy),'all_saved_symdefs':len(defs),'unused_symdefs':sum(int(r['usedCount'])==0 for r in defs)}

def decode(path):
 data=path.read_bytes()
 for enc in ['utf-8-sig','utf-16','gb18030','cp1252']:
  try:return data.decode(enc)
  except UnicodeError:pass
 raise ValueError('Active device/config text cannot be decoded '+str(path))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest',type=Path,required=True);ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--preflight',action='store_true');ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh closure output required');a.out.mkdir(parents=True);r={'status':'FAIL_NATIVE_REFERENCE_CLOSURE'};evidence={};hits=[];traces=[];coverage=[]
 try:
  need(sha(a.manifest)==a.manifest_sha256.upper(),'Frozen final source manifest SHA changed');m=load(a.manifest);need(m['schema']=='FINAL_NATIVE_REFERENCE_SOURCES_V1' and (m['source_state']=='FINAL_PUBLIC_FILES_MATCH_MANIFEST' or a.preflight),'Final public/candidate source coverage not frozen')
  rp=file(m['retirement_plan'],evidence);plan=load(rp);names=plan['accepted_source_stems'];need(plan['accepted_alias_count']==len(names)==1067 and len(set(names))==1067 and all(n==n.casefold() for n in names),'Full1067 retirement stem set missing');counts={n:{k:0 for k in CATEGORIES} for n in names}
  guard=file(m['public_guard'],evidence);g=load(guard);entries=g['files'];gi={norm(v['path']):v for v in entries};need(len(gi)==len(entries),'Duplicate current public guard path')
  for v in entries:need(Path(v['path']).is_file() and Path(v['path']).stat().st_size==v['bytes'] and sha(v['path'])==v['sha256'],'Current complete public guard differs '+v['path'])
  expected_counts={'project_capture':1,'project_brd':1,'public_olb':37,'public_dsn':2,'public_brd':7};ss=m['sources'];need(Counter(v['kind'] for v in ss)==Counter(expected_counts),'Missing/duplicate final actual source classes')
  for kind,root,ext in [('public_olb',LIB/'01captureLib','.olb'),('public_dsn',LIB/'01captureLib','.dsn'),('public_brd',LIB/'01brdlib','.brd')]:
   want={norm(v['path']) for v in entries if root.resolve() in Path(v['path']).resolve().parents and Path(v['path']).suffix.casefold()==ext};have={norm(v['public_path']) for v in ss if v['kind']==kind};need(have==want and len(have)==expected_counts[kind],'Actual full public source paths differ from current frozen guard '+kind)
  def add(category,value,record):
   if value is None:return
   key=stem(value)
   if key in counts:counts[key][category]+=1;hits.append({'stem':key,'category':category,**record})
  source_issues=[]
  for row in ss:
   try:
    need(row['public_sha256'] and sha(row['public_path'])==row['public_sha256'],'Actual public design/library does not match final native input '+row['public_path'])
    if row['kind'].startswith('public_'):need(gi[norm(row['public_path'])]['sha256']==row['public_sha256'],'Native source is not in expected current guard')
    need(row['acceptance_proofs'] or row.get('acceptance_mode') in {'UNCHANGED_SOURCE_SHA_FROM_FROZEN_NATIVE_BINDING','UNCHANGED_PUBLIC_SOURCE_NATIVE_READONLY_EXPORT'},'Independent byte identity/semantic acceptance source coverage missing')
    if row['kind'] in {'project_capture','public_olb','public_dsn'}:
     xml=capture_binding(row,evidence);refs,tt,cc=capture(xml)
     for v in refs:add(row['kind'],v['value'],{'source':row['public_path'],'native_xml':str(xml),**v})
     for v in tt:
      if stem(v['value']) in counts:traces.append({'source':row['public_path'],**v})
     coverage.append({'kind':row['kind'],'source':row['public_path'],'sha256':row['public_sha256'],'native_actual_FP_fields':len(refs),'historical_FootprintName_trace_fields':len(tt),'complete_object_coverage':cc})
    else:
     refs,cc=board_references(row,evidence);prefix='project_brd' if row['kind']=='project_brd' else 'public_brd'
     for v in refs:add(prefix+'_'+v['scope'],v['value'],{'source':row['public_path'],**v})
     coverage.append({'kind':row['kind'],'source':row['public_path'],'sha256':row['public_sha256'],**cc})
   except Exception as ex:
    if not a.preflight:raise
    source_issues.append({'source':row['public_path'],'kind':row['kind'],'error':str(ex)})
  # Explicitly selected self-device TXT retirements are not active device maps.
  excluded={norm(v['path']):v for v in plan['assets'] if Path(v['path']).suffix.casefold()=='.txt'};need(len(excluded)==937,'Exact937 self-device retirement exclusion cohort missing');excluded_rows=[]
  for v in excluded.values():need(sha(v['path'])==v['sha256'] and norm(v['path']) in gi,'Exact self-device retirement exclusion not byte-bound to current guard');excluded_rows.append({'path':v['path'],'sha256':v['sha256'],'source_stem':v['source_stem']})
  active=m['active_device_map'];need(active['source_state']=='COMPLETE_ACTIVE_PATH_AND_DEVICE_ENUMERATION' and active['configs'] and active['device_roots'],'Actual active devpath/config source class missing')
  roots=[Path(p).resolve() for p in active['device_roots']];seen=set()
  for root in roots:
   need(root.is_dir(),'Active device root missing')
   for p in root.rglob('*'):
    if not p.is_file() or p.suffix.casefold() not in {'.txt','.dev','.dml','.map','.cfg','.ini'}:continue
    k=norm(p)
    if k in seen or k in excluded:continue
    seen.add(k);need(k in gi and sha(p)==gi[k]['sha256'],'Active device file is outside final guarded source coverage '+str(p));text=decode(p);evidence[str(p)]=sha(p)
    # Full native device bodies use one real PACKAGE declaration. Other files
    # must be explicitly classified by the frozen manifest, never silently zero.
    if text.lstrip().startswith('(DEVICE FILE:'):
     pp=[(i,line) for i,line in enumerate(text.splitlines(),1) if re.match(r'^\s*PACKAGE\s+',line,re.I)];need(len(pp)==1,'Complete active DEVICE PACKAGE field missing/ambiguous');i,line=pp[0];value=line.strip().split(None,1)[1].strip().strip("\"'");add('active_device_map',value,{'source':str(p),'line':i,'field':'native_DEVICE.PACKAGE','value':value})
    else:
     need('\x00' not in text,'Binary active device/map requires native full-definition extraction '+str(p))
     for i,line in enumerate(text.splitlines(),1):
      code=line.strip()
      if not code or code.startswith(('#',';','//','rem ','REM ')):continue
      for match in re.finditer(r'(?<![A-Za-z0-9_+.-])([A-Za-z0-9_+.-]+)(?![A-Za-z0-9_+.-])',code):
       if match.group(1).casefold() in counts:add('active_device_map',match.group(1),{'source':str(p),'line':i,'field':'active_text_device_map_exact_alias_token','value':match.group(1)})
  for v in active['configs']:
   p=file(v,evidence);text=decode(p)
   for i,line in enumerate(text.splitlines(),1):
    code=line.strip()
    if not code or code.startswith(('#',';','//','rem ','REM ')):continue
    for match in re.finditer(r'(?<![A-Za-z0-9_+.-])([A-Za-z0-9_+.-]+)(?![A-Za-z0-9_+.-])',code):
     if match.group(1).casefold() in counts:add('active_device_map',match.group(1),{'source':str(p),'line':i,'field':'active_config_exact_alias_token_requires_review','value':match.group(1)})
  targets=m['canonical_target_proofs']
  if not(targets and m['canonical_target_coverage_state']=='ALL_REQUIRED_TARGET_COLD_NATIVE_AND_FULL_PAD_PROOFS_BOUND'):
   if a.preflight:source_issues.append({'source_class':'canonical_target_proofs','error':'Canonical target cold/native/PAD index pending'})
   else:raise ValueError('Canonical target proof source class missing')
  for v in targets:need(str(load(file(v,evidence))['status']).startswith('PASS'),'Canonical target native/PAD proof not passed')
  need(all(set(v)==set(CATEGORIES) and all(type(n) is int and n>=0 for n in v.values()) for v in counts.values()),'Eight explicit integer reference categories missing')
  r.update({'status':'FAIL_INCOMPLETE_NATIVE_SOURCE_COVERAGE' if source_issues else ('PASS_NATIVE_REFERENCE_CLOSURE' if not hits else 'FAIL_ACTUAL_RETIRED_STEM_REFERENCES_REMAIN'),'retirement_plan_sha256':sha(rp),'covered_source_stems':names,'active_reference_counts':counts,'incomplete_sources':source_issues,'source_coverage_complete':not source_issues,'preflight_only':a.preflight,'actual_matches':hits,'all_source_coverage':coverage,'historical_FootprintName_not_active_reference':traces,'excluded_self_device_files_planned_exact_same_retirement':excluded_rows,'canonical_target_proofs':targets,'current_public_guard':m['public_guard'],'counts_are_actual_scanned_native_fields_not_plan_counts':True})
 except Exception as ex:r['error']=str(ex)
 r['native_evidence']=[{'path':p,'sha256':h} for p,h in evidence.items()];r['source_manifest']={'path':str(a.manifest),'sha256':sha(a.manifest)};r['script_sha256']=sha(__file__);r['public_files_written']=0;p=a.out/'NATIVE_REFERENCE_CLOSURE.json';p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'status':r['status'],'error':r.get('error'),'matches':len(hits),'report':str(p)}));return 0 if r['status']=='PASS_NATIVE_REFERENCE_CLOSURE' else 2
if __name__=='__main__':raise SystemExit(main())
