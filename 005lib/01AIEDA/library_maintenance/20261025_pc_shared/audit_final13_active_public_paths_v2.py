"""Read-only final13 active-file/public-library audit; evidence w is not a search path.
Requires the exact native XML export job and actual saved-board readonly audit.
Does not delete, edit, load CAD, infer absence from file counts, or strip DSN cache.
"""
from pathlib import Path
from collections import Counter
import argparse,csv,hashlib,json,re
import xml.etree.ElementTree as E

ROOT=Path('D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025')
PUBLIC=Path('D:/001DIY/005lib')
FROZEN_SHA='F2A40E1AF0848305F352A75DB13C783406EF48303A8AFE7A53851A35B1863E05'
LIB_EXT={'.olb','.pad','.psm','.dra','.ssm','.fsm'}
ACTIVE_SUFFIX={'.cmd','.bat','.ps1','.tcl','.il','.opj','.cfg','.dml','.ini','.env'}
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def read(p):
 data=Path(p).read_bytes()
 for codec in ['utf-8-sig','gb18030']:
  try:return data.decode(codec)
  except UnicodeDecodeError:pass
 raise ValueError('Unknown active text encoding '+str(p))
def inside(path,parent):return Path(path).resolve().is_relative_to(Path(parent).resolve())
def table(p):
 lines=read(p).splitlines();keys=lines[0].split('\t');rows=[]
 for line in lines[1:]:
  vals=line.split('\t');need(len(vals)==len(keys),'Malformed native table '+str(p));rows.append(dict(zip(keys,vals)))
 return rows
def dec(s):
 return re.sub(r'\\(.)',lambda m:{'t':'\t','n':'\n','r':'\r'}.get(m[1],m[1]),s[1:-1]) if s.startswith('"') and s.endswith('"') else s
def public_file(path,root):
 p=Path(path).resolve();need(inside(p,root),'Library reference outside designated public root '+str(p));need(p.is_file(),'Referenced public file missing '+str(p));return p
def file_record(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def source_freeze(path):
 need(sha(path)==FROZEN_SHA,'SOURCE_FREEZE bytes changed after initial freeze')
 q=load(path);out=[]
 for field,hkey in [('schematic_source','schematic_sha256'),('pcb_source','pcb_sha256'),('formal12_board','formal12_board_sha256'),('source_common_olb','source_common_sha256')]:
  p=Path(q[field]);need(p.is_file() and sha(p)==q[hkey],'Protected original source changed '+field);out.append(file_record(p))
 return out
def inspect_capture_job(job,xml,dsn):
 q=load(job/'job_result.json');owned=load(job/'owned_process.json');cmd=owned['command']
 need(q['status']=='COMPLETE' and q['exit_code']==0 and q['protected_unchanged'] and q['protected_before']==q['protected_after'],'Capture native export protection failed')
 need(len(cmd)==4 and Path(cmd[1]).name.lower()=='export_dsn.tcl','Expected exact full DSN native export command')
 source=Path(cmd[2]);out=Path(cmd[3]);need((out/'native_design.xml').resolve()==xml.resolve(),'Provided XML is not export job output')
 before={str(Path(k).resolve()).upper():v for k,v in q['protected_before'].items()}
 need(str(source.resolve()).upper() in before,'Export DSN was not protected by wrapper')
 h=before[str(source.resolve()).upper()];need(h==sha(source)==sha(dsn),'Final DSN is not exact native-exported design bytes')
 return {'job':str(job),'source_dsn':str(source),'source_and_formal_sha256':h,'native_xml_sha256':sha(xml),'job_result_sha256':sha(job/'job_result.json'),'owned_process_sha256':sha(job/'owned_process.json'),'native_export_script':file_record(Path(cmd[1]))}
def capture_sources(xml):
 root=E.parse(xml).getroot();sources=[];cache=Counter();instances=Counter()
 for kind in ['Package','GlobalSymbol','OffPageSymbol']:
  for e in root.findall('./Cache/'+kind):
   d=e.find('Defn');need(d is not None and d.get('sourceLibName'),'Missing cache source identity')
   p=public_file(d.get('sourceLibName'),PUBLIC/'01captureLib');cache[kind]+=1;sources.append({'kind':'Cache/'+kind,'name':d.get('name'),'source':str(p)})
 for kind in ['PartInst','Global','OffPageConnector']:
  for e in root.findall('.//'+kind):
   d=e.find('Defn');need(d is not None and d.get('libName'),'Missing placed source identity')
   p=public_file(d.get('libName'),PUBLIC/'01captureLib');instances[kind]+=1;sources.append({'kind':kind,'dbId':d.get('dbId'),'source':str(p)})
 need(cache=={'Package':55,'GlobalSymbol':3,'OffPageSymbol':1},'Unexpected complete embedded cache cohort')
 need(instances['PartInst']==1131 and sum(instances.values())==3118,'Unexpected placed source cohort')
 # Catch additional source-identity fields outside the known schema rather than
 # treating their strings as harmless because the primary 3177 rows passed.
 actual=[(e.tag,k,v) for e in root.iter() for k,v in e.attrib.items() if k in {'sourceLibName','libName'}]
 need(len(actual)==len(sources),'Unknown additional source identity field')
 return {'cache':dict(cache),'placed':dict(instances),'source_identity_rows':len(sources),'public_OLBs':[file_record(Path(p)) for p in sorted({s['source'] for s in sources})],'embedded_cache_note':'The DSN necessarily contains its embedded Design Cache. This is native design content, not an external private OLB. All placed and cached source identity fields point to the public Capture library.'}
def active_text_files():
 result=[p for p in ROOT.iterdir() if p.is_file() and p.suffix.lower() in ACTIVE_SUFFIX]
 for folder in ['sch','pcb','pcbenv']:
  for p in (ROOT/folder).rglob('*'):
   if p.is_file() and (p.suffix.lower() in ACTIVE_SUFFIX or (folder=='pcbenv' and p.suffix.lower() not in LIB_EXT)):
    result.append(p)
 return sorted(set(result))
def config_check():
 env=ROOT/'pcbenv/env';text=read(env);records={};lastsource=-1;assign={}
 for i,line in enumerate(text.splitlines()):
  if re.match(r'^\s*source\s+',line,re.I):lastsource=i
  m=re.fullmatch(r'\s*set\s+(psmpath|padpath|devpath)\s*=\s*(.*?)\s*',line,re.I)
  if m:assign[m[1].lower()]=(i,m[2].strip('"'))
 for key,sub in [('psmpath','01Psm_lib'),('padpath','01Pad_lib'),('devpath','01brdlib')]:
  need(key in assign,'Missing explicit final '+key);i,value=assign[key]
  need(i>lastsource,'Later sourced environment can override public path '+key)
  need(Path(value).resolve()==(PUBLIC/sub).resolve(),'Effective '+key+' differs from public library root')
  need(Path(value).is_dir(),'Public library directory missing '+key);records[key]=value
 texts=[];absrefs=[]
 for p in active_text_files():
  t=read(p);texts.append(file_record(p))
  for m in re.finditer(r'[A-Za-z]:[\\/][^"\r\n;()]*?\.(?:olb|psm|pad|dra|ssm|fsm)\b',t,re.I):
   ref=m[0].strip();target=Path(ref)
   parent=PUBLIC/'01captureLib' if target.suffix.lower()=='.olb' else PUBLIC/'01Pad_lib' if target.suffix.lower()=='.pad' else PUBLIC/'01Psm_lib'
   public_file(target,parent);absrefs.append({'active_file':str(p),'reference':ref})
  need(not re.search(r'(?i)(?:%~dp0|\$LGA1700_PROJECT_ROOT)[^\r\n"]*(?:lib[\\/]psm|lib[\\/]pad|lib[\\/]device)',t),'Active private library directory reference '+str(p))
 opj=ROOT/'sch/LGA1700_RULES.opj';refs=re.findall(r'\(File\s+"([^"]+)"',read(opj));need(bool(refs),'No OPJ references')
 for ref in refs:
  p=Path(ref) if Path(ref).is_absolute() else opj.parent/ref
  need(p.is_file(),'OPJ referenced file missing '+ref)
  if p.suffix.lower()=='.olb':public_file(p,PUBLIC/'01captureLib')
  elif p.suffix.lower()=='.dsn':need(p.resolve()==(ROOT/'sch/LGA1700.DSN').resolve(),'OPJ points at other schematic')
  else:raise ValueError('Unreviewed OPJ file reference '+ref)
 need('ALLEGRO_PCBENV=%~dp0pcbenv'.lower() in read(ROOT/'打开PCB.cmd').lower(),'PCB launcher does not select final project public-only environment')
 return {'effective_final_environment':records,'active_text_files':texts,'absolute_library_references':absrefs,'OPJ_references':refs,'w_evidence_not_scanned_as_active_configuration':True}
def external_libraries():
 live=[];evidence=[]
 for p in ROOT.rglob('*'):
  if not p.is_file() or p.suffix.lower() not in LIB_EXT:continue
  rel=p.relative_to(ROOT)
  if rel.parts[0].lower()=='w':evidence.append(file_record(p))
  else:live.append(file_record(p))
 need(not live,'External library files remain outside w evidence: '+repr(live[:10]))
 return {'active_external_library_files':live,'w_evidence_library_files':evidence,'excluded_extensions':sorted(LIB_EXT),'w_is_evidence_only_not_a_library_search_path':True}
def pcb_and_pst(audit,pst,brd):
 launch=load(audit/'launch_report.json');h=sha(brd)
 need(launch['exit_code']==0 and launch['input_unchanged'] and launch['write_candidate'] is False and '-readonly' in launch['arguments'],'Final PCB native audit not readonly complete')
 need(launch['source_sha256_before']==launch['source_sha256_after']==h==sha(audit/'INPUT_COPY.brd'),'Final saved BRD not bound to actual audited bytes')
 need((audit/'COMPOSITE_COMPLETE.txt').is_file(),'Final composite PCB audit incomplete')
 import importlib.util
 parser=ROOT.parent/'12electrical_fixed_20261025/tools/verify_eco12.py';s=importlib.util.spec_from_file_location('complete_pst_parser_active',parser);P=importlib.util.module_from_spec(s);s.loader.exec_module(P)
 model=P.load_bundle(pst);symbols=table(audit/'symbols.tsv');pins=table(audit/'all_symbol_pins.tsv');refs={};footprints={}
 for row in symbols:
  ref=dec(row['refdes']);need(ref not in refs,'Duplicate placed PCB symbol ref');refs[ref]=row
  fp=P.property_value(model['parts'][ref]['body'],'JEDEC_TYPE');need(dec(row['symbol_name']).upper()==fp.upper(),'PCB/PST footprint differs '+ref)
  public_file(PUBLIC/'01Psm_lib'/(fp+'.psm'),PUBLIC/'01Psm_lib');footprints[fp]={'PSM':file_record(PUBLIC/'01Psm_lib'/(fp+'.psm')),'DRA_exists':(PUBLIC/'01Psm_lib'/(fp+'.dra')).is_file()}
 need(set(refs)==set(model['parts']),'PCB/PST full physical ref cohort differs')
 numbered={};pads={}
 for row in pins:
  ref,pin=dec(row['refdes']),dec(row['number']);pad=dec(row['padstack']);p=public_file(PUBLIC/'01Pad_lib'/(pad+'.pad'),PUBLIC/'01Pad_lib');pads[pad]=file_record(p)
  if not pin:continue
  key=(ref,pin);need(key not in numbered,'Duplicate numbered physical PCB pad');numbered[key]=row
  net=model['pinmap'][key];net='' if net=='NC' else net;need(dec(row['net'])==net,'Actual PCB pin net differs from final PST '+'.'.join(key))
 need(set(numbered)==set(model['pinmap']),'Actual PCB numbered pad cohort differs from final PST')
 return {'saved_board_sha256':h,'physical_refs':len(refs),'numbered_pads':len(numbered),'all_pad_objects':len(pins),'public_PSM_resolution':footprints,'public_PAD_resolution':pads,'actual_pin_nets_match_formal_PST':True,'scope':'Library path/name resolution and actual stored pin net assignment only. PCB geometric ECO and actual copper continuity require their separate native delta proof.'}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--native-xml',type=Path,required=True);ap.add_argument('--capture-job',type=Path,required=True);ap.add_argument('--board-audit',type=Path,required=True);ap.add_argument('--xml-proof',type=Path,required=True);ap.add_argument('--pst-proof',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ar=ap.parse_args()
 need(not ar.out.exists(),'Fresh output required');ar.out.mkdir(parents=True);report={'status':'FAIL','script_sha256':sha(__file__),'CAD_started':False,'files_deleted':0}
 try:
  report['source_freeze_protection']=source_freeze(ROOT/'verification/SOURCE_FREEZE.json')
  xp,pp=load(ar.xml_proof),load(ar.pst_proof)
  need(xp['status']=='PASS_PUBLIC_LIBRARY_FP_AND_EXACT_SEVEN_CACHE_DEFAULTS_FULL_ORDERED_XML' and pp['status']=='PASS_COMPLETE_PST_FP_AND_SOURCE_PATH_ONLY','Final XML/PST proofs not PASS')
  need(xp['inputs']['candidate_xml_sha256']==sha(ar.native_xml),'Final native XML not bound to passing proof')
  need(pp['inputs']['xml_proof_sha256']==sha(ar.xml_proof) and pp['inputs']['plan_sha256']==xp['inputs']['plan_sha256'],'Final PST and XML proofs not same frozen case')
  report['native_schematic_binding']=inspect_capture_job(ar.capture_job,ar.native_xml,ROOT/'sch/LGA1700.DSN')
  need(pp['native_export_binding']['source_dsn_sha256']==sha(ROOT/'sch/LGA1700.DSN'),'Formal DSN is not untouched native PST source; packaged temporary DSN must not be published')
  need({n:sha(ROOT/'sch/netlist'/n) for n in ['pstchip.dat','pstxprt.dat','pstxnet.dat']}==pp['inputs']['candidate_sha256'],'Formal PST files not actual passing candidate')
  report['Capture_public_sources']=capture_sources(ar.native_xml);report['active_configuration']=config_check();report['external_library_residuals']=external_libraries()
  report['PCB_public_resolution']=pcb_and_pst(ar.board_audit,ROOT/'sch/netlist',ROOT/'pcb/LGA1700_RULES.brd')
  report['proof_bindings']={'xml_proof':file_record(ar.xml_proof),'pst_proof':file_record(ar.pst_proof),'source_freeze':file_record(ROOT/'verification/SOURCE_FREEZE.json')}
  report['status']='PASS_FINAL_ACTIVE_PUBLIC_LIBRARY_PATHS_AND_SOURCE_PROTECTION'
 except Exception as ex:report['error']=str(ex)
 (ar.out/'ACTIVE_PUBLIC_LIBRARY_PATH_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'status':report['status'],'error':report.get('error'),'report':str(ar.out/'ACTIVE_PUBLIC_LIBRARY_PATH_AUDIT.json')},ensure_ascii=False));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
