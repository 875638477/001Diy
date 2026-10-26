"""Read-only non-OLB references for public footprint consolidation. No CAD or library write."""
from pathlib import Path
from collections import Counter
import csv, hashlib, json, re

M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
P=M/'global_suffix_inventory_v1'
OUT=M/'global_suffix_reference_audit_v1'
OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jread=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
plan=jread(P/'PSM_NATIVE_AUDIT_PLAN.json')
guard=jread(plan['public_guard_manifest'])
entries=guard['files']
reps=plan['representatives']
byname={r['stem'].lower():r for r in reps}
names=sorted(byname,key=lambda x:(-len(x),x))
pat=re.compile(r'(?<![A-Za-z0-9_.-])(?:'+ '|'.join(re.escape(n) for n in names)+r')(?=(?:\.(?:psm|dra|txt|olb)\b)|[^A-Za-z0-9_.-]|$)',re.I)
text_ext={'.txt','.ini','.bat','.cmd','.scr','.il','.tcl','.md','.cfg','.prf','.par','.dml','.dat','.csv','.xml','.json','.py','.pxml','.dcm','.dsn','.map','.jrl','.log','.rpt','.html','.htm','.xsd','.asc','.dxf',''}
known_binary={'.psm':'NATIVE_PSM_AUDIT_SEPARATE','.dra':'NATIVE_DRA_PACKAGE_SOURCE_BINARY','.pad':'NATIVE_PADSTACK_DEPENDENCY','.olb':'NATIVE_OLB_AUDIT_BY_BASELINE','.brd':'NATIVE_PUBLIC_BOARD_REFERENCE_AUDIT_SEPARATE','.opj':'CAPTURE_PROJECT_BINARY_OR_TEXT_CONTAINER'}
rows=[]; scanned=[]; excluded=[]; fails=[]
for g in entries:
 p=Path(g['path']);ext=re.sub(r',\d+$','',p.suffix.lower())
 if ext not in text_ext and not (ext=='.scr,1'):
  excluded.append({**g,'reason':known_binary.get(ext,'BINARY_OR_UNREVIEWED_CONTAINER_NO_NO_REFERENCE_CLAIM')});continue
 raw=p.read_bytes()
 if sha(p)!=g['sha256']:raise RuntimeError('guard source changed '+str(p))
 if raw.startswith((b'\xff\xfe',b'\xfe\xff')):enc='utf-16'
 elif b'\0' in raw:
  excluded.append({**g,'reason':known_binary.get(ext,'NUL_CONTAINING_BINARY_REQUIRES_NATIVE_OR_CONTAINER_REVIEW')});continue
 else:
  enc=None
  for e in ('utf-8-sig','gb18030','latin-1'):
   try:raw.decode(e);enc=e;break
   except UnicodeDecodeError:pass
 try:txt=raw.decode(enc)
 except Exception as e:fails.append({**g,'error':str(e)});continue
 own_device=ext=='.txt' and '(DEVICE FILE:' in txt.upper() and re.search(r'^\s*PACKAGE\s+\S+',txt,re.M|re.I)
 found=0
 for no,line in enumerate(txt.splitlines(),1):
  for match in pat.finditer(line):
   alias=match.group().lower();found+=1
   selfref=bool(own_device and alias==p.stem.lower())
   comment=bool(re.match(r'^\s*(?:#|;|//|REM\b|\()',line,re.I))
   if selfref:kind='DEVICE_SELF_DECLARATION_ARCHIVE_WITH_ALIAS_ASSET'
   elif byname[alias]['family']=='NUMERIC_WITHOUT_COMPONENT_CATEGORY':kind='AMBIGUOUS_NUMERIC_TOKEN_NOT_CONFIRMED_FOOTPRINT_REFERENCE'
   elif ext in {'.md','.log','.jrl','.rpt','.html','.htm'} or comment:kind='INFORMATIONAL_OR_COMMENT_REFERENCE_REVIEW'
   else:kind='POTENTIALLY_ACTIVE_EXTERNAL_REFERENCE_REVIEW'
   rows.append({'path':str(p),'sha256':g['sha256'],'encoding':enc,'line':no,'column':match.start()+1,'name':match.group(),'canonical_hint':byname[alias]['canonical_candidate'],'family':byname[alias]['family'],'classification':kind,'line_text':line})
 scanned.append({**g,'encoding':enc,'matches':found,'device_self_declaration_file':bool(own_device)})
actual=[r for r in rows if r['classification']=='POTENTIALLY_ACTIVE_EXTERNAL_REFERENCE_REVIEW']
textreport={'status':'READONLY_REFERENCE_INVENTORY_NO_APPLY','plan':str(P/'PSM_NATIVE_AUDIT_PLAN.json'),'plan_sha256':sha(P/'PSM_NATIVE_AUDIT_PLAN.json'),'guard_manifest_sha256':sha(plan['public_guard_manifest']),'candidate_names':len(names),'scanned_files':len(scanned),'matched_files':len(set(r['path'] for r in rows)),'matches':len(rows),'classification_counts':dict(Counter(r['classification'] for r in rows)),'potentially_active_external_files':sorted(set(r['path'] for r in actual)),'exact_matches':rows,'scanned_inputs':scanned,'excluded_inputs':excluded,'decode_failures':fails,'limits':['Read-only text token references are not proof of native electrical or geometric equivalence.','Self-device declarations belong to the alias asset set, not independent proof another design needs that alias.','Native OLB fields are separately audited by baseline agent; native public board use is separately listed.','Binary archives, shortcuts and Office documents were not unpacked or modified; they cannot support a blanket no-reference claim.','No scripts/env/device text or library files have been changed.']}
dump('TEXT_REFERENCE_AUDIT.json',textreport)
with (OUT/'TEXT_REFERENCE_MATCHES.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['path']);w.writeheader();w.writerows(rows)

B=Path(r'D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025')
usage=B/'usage_audit'/'usage_counts.json'
u=jread(usage);boards=[]
for source in u['sources']:
 p=Path(source['source'])
 if not str(p).lower().startswith(str(Path(r'D:\001DIY\005lib\01brdlib')).lower()+'\\'):continue
 evidence=[]
 for rel,expected in source['evidence'].items():
  ep=B/rel;actualsha=sha(ep)
  if actualsha!=expected:raise RuntimeError('native evidence changed '+str(ep))
  evidence.append({'path':str(ep),'sha256':actualsha})
 actualsha=sha(p)
 if actualsha!=source['sha256']:raise RuntimeError('board snapshot stale '+str(p))
 declared=[{'name':n,'count':c,'canonical_hint':byname[n]['canonical_candidate'],'family':byname[n]['family']} for n,c in source['counts']['declared_psm'].items() if n in byname]
 placed=[{'name':n,'count':c,'canonical_hint':byname[n]['canonical_candidate'],'family':byname[n]['family']} for n,c in source['counts']['psm'].items() if n in byname]
 boards.append({'source':str(p),'sha256':actualsha,'native_snapshot_id':source['id'],'native_status':source['native_status'],'units':source['units'],'components_total':source['components'],'placed_symbols_total':source['placed_symbols'],'candidate_declared_packages':declared,'candidate_placed_symbols':placed,'evidence':evidence})
br={'status':'SHA_BOUND_REUSE_OF_NATIVE_READONLY_USAGE_EVIDENCE_NO_CAD_RUN','usage_snapshot':str(usage),'usage_snapshot_sha256':sha(usage),'public_boards':boards,'public_board_count':len(boards),'candidate_declared_total':sum(sum(x['count'] for x in s['candidate_declared_packages']) for s in boards),'candidate_placed_total':sum(sum(x['count'] for x in s['candidate_placed_symbols']) for s in boards),'limits':['Only seven public01brdlib source boards are included; old recent_lga1700_v2 source12 is intentionally excluded.','Actual placed symdefs and logical component declared packages are distinct; both must be considered for future updates.','Embedded symbols make a board self contained for display, but removing its external old library name affects later update workflows.','No board, active project, public library, script or env was modified.','Candidate names are reference inventory, not automatic authorization to remap functional special packages.']}
dump('PUBLIC_BRD_REFERENCE_AUDIT.json',br)
summary={k:textreport[k] for k in ('status','candidate_names','scanned_files','matched_files','matches','classification_counts','potentially_active_external_files')}
summary.update({'public_board_count':len(boards),'candidate_declared_total':br['candidate_declared_total'],'candidate_placed_total':br['candidate_placed_total'],'unreviewed_binary_container_files':[x['path'] for x in excluded if x['reason']=='BINARY_OR_UNREVIEWED_CONTAINER_NO_NO_REFERENCE_CLAIM']})
dump('SUMMARY.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k!='unreviewed_binary_container_files'},ensure_ascii=False,indent=2))
