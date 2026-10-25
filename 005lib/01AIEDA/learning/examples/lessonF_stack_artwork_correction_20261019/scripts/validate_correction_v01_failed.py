from pathlib import Path
import re,json,csv,hashlib,collections
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
checks=[];details={}
def ck(n,v,a=None):checks.append({'name':n,'pass':bool(v),'actual':a})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|[()\']|[^\s()\']+',s);i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=="'":return take()
  if v=='(':
   a=[]
   while t[i]!=')':a.append(take())
   i+=1;return a
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def rows(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def attrs(v):return dict(zip(v[::2],v[1::2]))
def norm(s):
 s=re.sub(r'(dbid|propList):[0-9A-Fa-f]+',r'\1:SESSIONID',s)
 return s
def bag(p):return collections.Counter(norm(x) for x in p.read_text().splitlines())
inputs=json.loads((R/'input_manifest.json').read_text())
for item in inputs:
 ck('Input source stable '+item['key'],sha(Path(item['source']))==item['sha256'])
 ck('Backup exact '+item['key'],sha(Path(item['backup']))==item['sha256'])
for item in inputs:
 if item['kind']!='board':continue
 k=item['key'];n=item['layerCount'];before=R/f'logs/baseline_{k}';after=R/f'logs/reopen_{k}'
 d={'workingBoard':item['working'],'SHA256':sha(Path(item['working'])),'sourceSHA256':item['sha256'],'layerCount':n}
 for stage in ['baseline','fix','reopen','outline']:
  folder=R/f'logs/{stage}_{k}';launch=json.loads((folder/'launch.json').read_text())
  ck(k+' '+stage+' native exit0',launch['completed'] and launch['exitCode']==0)
  ck(k+' '+stage+' no SKILL error','*Error*' not in (folder/'stdout.txt').read_text(errors='replace'))
  if stage!='fix':ck(k+' '+stage+' SHA unchanged',launch['beforeSHA256']==launch['afterSHA256'])
  marker={'baseline':'FCOR_READ_COMPLETE','reopen':'FCOR_READ_COMPLETE','fix':'FCOR_FIX_COMPLETE','outline':'FCOR_OUTLINE_COMPLETE'}[stage]
  f={'baseline':'structure.txt','reopen':'structure.txt','fix':'fix.txt','outline':'outline_exact.tsv'}[stage]
  ck(k+' '+stage+' semantic COMPLETE',marker in (folder/f).read_text())
 fix=(R/f'logs/fix_{k}/fix.txt').read_text()
 ck(k+' native save DRC0 current','DRC=0 COUNT=0 STATE=t' in fix)
 struct=(after/'structure.txt').read_text()
 ck(k+' mm4 saved', 'units=("millimeters" 4)' in struct)
 copper=['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']
 ck(k+' rawETCH exact copper sequence',sx(re.search(r'etch_group=(.*)',struct)[1])==copper)
 ck(k+' routing exact uppercase sequence',sx(re.search(r'\nroute=(.*)',struct)[1])==copper)
 rawxs=[attrs(sx(x.split('\t',1)[1])) for x in struct.splitlines() if x.startswith('XS_RAW\t')]
 ck(k+' rawXSection conductor exact uppercase',[x['name'] for x in rawxs if x['conductor']]==copper)
 ck(k+' no physical MASK',not any(x['layerType']=='MASK' or x['maskLayer'] for x in rawxs))
 oldstack=rows(before/'stackup_full.tsv');newstack=rows(after/'stackup_full.tsv')
 def stableStack(xs):return [{key:v for key,v in x.items() if key!='position'} for x in xs if sx(x['type'])!='MASK']
 ck(k+' all retained copper/dielectric properties unchanged',stableStack(oldstack)==stableStack(newstack))
 d['copperDielectricThicknessMM']=sum(float(x['thickness']) for x in newstack)
 d['actualCopperNames']=copper
 # Complete full-template replay and saved effective membership/options.
 template=json.loads((R/f'source/drill{n}_parsed.json').read_text())
 films={sx(x['name']):attrs(sx(x['attributes'])) for x in rows(after/'films_full.tsv')}
 ck(k+' complete template Film name sequence',list(films)==[x['name'] for x in template['films']])
 ck(k+' no extra outline Film','F28_DESIGN_OUTLINE' not in films)
 ck(k+' exact film count',len(films)==(15 if n==2 else 17),len(films))
 presence={sx(x['layer']):sx(x['exists']) for x in rows(after/'layer_presence.tsv')}
 omissions=[];duplicates=[]
 for film in template['films']:
  name=film['name'];actual=films[name]
  ck(k+' original full call executed '+name,f'FILM_RESULT\t"{name}"\tt' in fix)
  expected=[x for x in dict.fromkeys(film['layers']) if presence.get(x)]
  got=actual['groupMembers']
  ck(k+' '+name+' complete valid layer membership',got==expected,{'expected':expected,'actual':got})
  filtered=[x for x in dict.fromkeys(film['layers']) if not presence.get(x)]
  if filtered:omissions.append({'film':name,'nativeFilteredInvalidReferences':filtered})
  dup=[x for x,count in collections.Counter(film['layers']).items() if count>1]
  if dup:duplicates.append({'film':name,'deduplicatedReferences':dup})
  call=sx(film['rawCall'][film['rawCall'].index('('):])
  opts=attrs(call[1:])
  for key,val in opts.items():
   if key=='?layers':continue
   field=key[1:]
   if field in ['xOffset','yOffset']:
    got=actual['offset'][0 if field=='xOffset' else 1]
   else:got=actual[field]
   if field=='ipc2581' and val==[]:val=None
   ck(k+' '+name+' option '+field,got==val,{'expected':val,'actual':got})
 d['filmCount']=len(films);d['filteredInvalidTemplateReferences']=omissions;d['nativeDeduplicatedSourceReferences']=duplicates
 expectedMissing={'BOARD GEMETRY/SILKSCREEN_TOP','BOARD GEMETRY/SILKSCREEN_BOTTOM'}
 if n==2:expectedMissing|={'CONSTRAINT REGION/L2','CONSTRAINT REGION/L3'}
 ck(k+' filtered refs exactly documented historical invalid set',{v for f in omissions for v in f['nativeFilteredInvalidReferences']}==expectedMissing)
 # Exact geometry, original logical connectivity and saved constraints are preserved.
 for fn in ['components.tsv','component_pins.tsv','nets.tsv','net_rules.tsv','group_members.tsv','physical_csets.tsv','spacing_csets.tsv','electrical_csets.tsv','placed_pins.tsv','placed_pads.tsv','padstacks.tsv','mechanical_direct.tsv','direct_geometry.tsv','route_geometry.tsv','vias.tsv','physical_pad_layers.tsv']:
  ck(k+' preserved '+fn,bag(before/fn)==bag(after/fn),{'beforeRows':len(rows(before/fn)),'afterRows':len(rows(after/fn))})
 ck(k+' constraint inheritance modes/properties unchanged',bag(before/'constraint_summary.txt')==bag(after/'constraint_summary.txt'))
 a=(before/'specific_proof.tsv').read_text();b=(after/'specific_proof.tsv').read_text()
 ck(k+' via count/classclass preserved',norm(a)==norm(b))
 mask=[x for x in rows(after/'physical_pad_layers.tsv') if 'MASK_' in x['layer']]
 ck(k+' actual pin/via mask aperture observations retained',len(mask)==(92 if n==4 else 88),len(mask))
 for cls in ['BOARD GEOMETRY','PACKAGE GEOMETRY','PIN','VIA CLASS']:
  for side in ['TOP','BOTTOM']:
   ck(k+' mask opening subclass retained '+cls+'/'+side,presence[cls+'/SOLDERMASK_'+side] is True)
 outline=rows(R/f'logs/outline_{k}/outline_exact.tsv')[:-1]
 ck(k+' root and legacy outline exactly2 shapes',len(outline)==2,len(outline))
 by={sx(x['role']):x for x in outline}
 root=by['AUTHORITATIVE_ROOT'];copy=by['NON_ROOT_COPY']
 ck(k+' authoritative root remains DESIGN_OUTLINE',sx(root['layer'])=='BOARD GEOMETRY/DESIGN_OUTLINE')
 ck(k+' only legacy copy OUTLINE',sx(copy['layer'])=='BOARD GEOMETRY/OUTLINE')
 ck(k+' exact8vertices+bbox legacy copy',[root[x] for x in ['bbox','filled','vertices']]==[copy[x] for x in ['bbox','filled','vertices']] and len(sx(root['vertices']))==8)
 ck(k+' source mechanical root exact same',root['vertices']==next(x['vertices'] for x in rows(before/'direct_geometry.tsv') if x['role']=='DESIGN_OUTLINE'))
 summary=(after/'native_summary.txt').read_text()
 ck(k+' logical/placed counts and current DRC0','components=80\nnets=69\nsymbols=5\ndrcs=0\ndrcState=t' in summary)
 ck(k+' logical272 pin assignments',len(rows(after/'component_pins.tsv'))==272)
 ck(k+'22 actual placed pins',len(rows(after/'placed_pins.tsv'))==22)
 if n==4:ck(k+'1 unique real through via','UNIQUE_VIA_COUNT\t1\n' in b)
 details[k]=d
F=R/'logs/reopen_F29'
ck('F29 27 domain classes and207 net memberships',len(rows(F/'group_members.tsv'))==213 and len({x['group'] for x in rows(F/'group_members.tsv') if sx(x['groupType'])=='NETCLASS'})==27)
ck('F29 69 inherited net rules',len(rows(F/'net_rules.tsv'))==69)
ck('F29 all10physical+7spacing+1ECsets',len(rows(F/'physical_csets.tsv'))==40 and len(rows(F/'spacing_csets.tsv'))==28 and len(rows(F/'electrical_csets.tsv'))==1)
export=json.loads((R/'exports/export_result.json').read_text())
ck('New v4 TCF official export+compare',all(x['exitCode']==0 and x['boardBefore']==x['boardAfter'] for x in export['records']))
ck('New v4 TCF exact native compare no updates','No objects were updated.' in (R/'exports/techfile_run/compare_techfile.log').read_text())
ck('New v4 TCF no physical MASK','SOLDERMASK_TOP' not in (R/'exports/F29_RULES_v4.tcf').read_text())
fail=[x for x in checks if not x['pass']]
out={'status':'PASS_NATIVE_USER_LAYER_ARTWORK_CORRECTION' if not fail else 'FAIL','allChecksPass':not fail,'checkCount':len(checks),'checks':checks,'failures':fail,'boards':details,'scope':'Original physical MASK layers removed; copper names/order preserved; complete immutable drill2/4 Film definitions replayed and every valid member plus every explicit option read back. Native filtering of template historical invalid refs is explicitly reported; no fake class/extra copper introduced. Apertures, geometry, connectivity, constraints preserved. No CAM fabrication content, complete board routing, SI/PI simulation, or production release certification.'}
(R/'validation.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps({'status':out['status'],'checks':len(checks),'failures':fail},indent=2))
