from pathlib import Path
import csv,json,re,hashlib,collections
C=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
R=C/'review'
checks=[]
evidence={}
def sha(p):
 p=Path(p); v=hashlib.sha256(p.read_bytes()).hexdigest().upper()
 evidence[str(p)]={'sha256':v,'bytes':p.stat().st_size}
 return v
def text(p):
 p=Path(p);sha(p);return p.read_text(encoding='utf-8-sig',errors='replace')
def table(p):return [r for r in csv.DictReader(text(p).splitlines(),delimiter='\t',quoting=csv.QUOTE_NONE) if all(v is not None for v in r.values())]
def check(n,ok,details=None):checks.append({'check':n,'pass':bool(ok),'detail':details})
def eq(n,a,b):check(n,a==b,{'actual':a,'expected':b})
def q(s):return s[1:-1] if s.startswith('"') and s.endswith('"') else s
# Independent reader: a small SKILL value parser, not the implementation's parsed JSON.
def values(s):
 ts=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s);i=0
 def one():
  nonlocal i
  t=ts[i];i+=1
  if t=="'":return one()
  if t=="'(":
   a=[]
   while ts[i]!=')':a.append(one())
   i+=1;return a
  if t=='(':
   a=[]
   while ts[i]!=')':a.append(one())
   i+=1;return a
  if t.startswith("'") and len(t)>1:
   # tokenizer keeps quote prefix of a symbol; quote of a list is separate.
   t=t[1:]
  if t.startswith('"'):return json.loads(t)
  if t=='nil':return None
  if t=='t':return True
  try:return int(t)
  except ValueError:
   try:return float(t)
   except ValueError:return t
 out=[]
 while i<len(ts):out.append(one())
 return out
def value(s):return values(s)[0]
def prop(s):
 a=value(s);return dict(zip(a[::2],a[1::2]))
def calls(s):
 result=[];start=0
 while True:
  m=re.search(r'axlFilmCreate\s*\(',s[start:])
  if not m:break
  p=start+m.end()-1;i=p;depth=0;quoted=False;esc=False
  while i<len(s):
   ch=s[i]
   if quoted:
    if esc:esc=False
    elif ch=='\\':esc=True
    elif ch=='"':quoted=False
   elif ch=='"':quoted=True
   elif ch=='(':depth+=1
   elif ch==')':
    depth-=1
    if depth==0:break
   i+=1
  a=value(s[p:i+1]);name=a[0];opts=dict(zip(a[1::2],a[2::2]))
  result.append((name,{k.lstrip('?'):v for k,v in opts.items()}))
  start=i+1
 return result
def norm(s):return re.sub(r'dbid:[0-9A-Fa-f]+','DBID',s)
def rows_eq(label,a,b):
 # Compare every exported field; ignore process-specific DBIDs and row ordering.
 canon=lambda rr:sorted(json.dumps({k:norm(v) for k,v in r.items()},sort_keys=True) for r in rr)
 eq(label,canon(a),canon(b))
manifest=json.loads(text(C/'input_manifest.json'))
for entry in manifest:
 eq('Immutable source SHA '+entry['source'],sha(entry['source']),entry['sha256'])
 eq('Backup exact SHA '+entry['backup'],sha(entry['backup']),entry['sha256'])
expected={}
for n in (2,4):
 films=calls(text(C/'source'/f'drill{n}.txt'));expected[n]=dict(films)
 eq(f'Original {n}L film count',len(films),15 if n==2 else 17)
 eq(f'Original {n}L first/last film identities',[films[0][0],films[-1][0]],['TOP','DisAll'])
check('No review code launches Cadence',True,'Review uses saved readonly text exports and SHA256 only.')
film_details={}
for entry in [r for r in manifest if r['kind']=='board']:
 key=entry['key'];n=entry['layerCount'];before=C/'logs'/('baseline_'+key);after=C/'logs'/('reopen_'+key)
 fix=C/'logs'/('fix_'+key)
 lp=json.loads(text(after/'launch.json'));frec=json.loads(text(fix/'launch.json'))
 check(key+' fresh readonly completed exit0',lp['completed'] and lp['exitCode']==0 and lp['readonly'])
 eq(key+' readonly unchanged on disk',lp['beforeSHA256'],lp['afterSHA256'])
 eq(key+' current native SHA',sha(entry['working']),lp['afterSHA256'])
 check(key+' native correction completed exit0',frec['completed'] and frec['exitCode']==0)
 for folder in (before,after):
  s=text(folder/'structure.txt')
  check(str(folder.name)+' raw reader completed','FCOR_READ_COMPLETE' in s)
 st=text(after/'structure.txt')
 eq(key+' metric precision supports .0025',value(re.search(r'^units=(.*)$',st,re.M)[1]),['millimeters',4])
 copper=['TOP','BOTTOM'] if n==2 else ['TOP','L2','L3','BOTTOM']
 eq(key+' raw ETCH group uppercase exact order',value(re.search(r'^etch_group=(.*)$',st,re.M)[1]),copper)
 eq(key+' raw routable uppercase exact order',value(re.search(r'^route=(.*)$',st,re.M)[1]),copper)
 legacy=value(re.search(r'^legacy_xsection=(.*)$',st,re.M)[1])
 eq(key+' old API also returns uppercase conductor names',[x[0] for x in legacy if x[1]=='CONDUCTOR'],copper)
 stacks=table(after/'stackup_full.tsv');oldstacks=table(before/'stackup_full.tsv')
 eq(key+' new physical xsection conductors',[q(x['name']) for x in stacks if x['conductor']=='t'],copper)
 eq(key+' no physical MASK rows',sum(q(x['type'])=='MASK' or x['function']=='"MASK"' for x in stacks),0)
 eq(key+' exactly two old physical MASK rows',sum(q(x['type'])=='MASK' for x in oldstacks),2)
 fields=[f for f in stacks[0] if f!='position']
 strip=lambda rr:sorted(json.dumps({k:r[k] for k in fields},sort_keys=True) for r in rr if q(r['type'])!='MASK')
 eq(key+' every other xsection scalar preserved',strip(stacks),strip(oldstacks))
 # Double-check raw new API, avoiding display-title casing or lossy table-only evidence.
 raw=[prop(line.split('\t',1)[1]) for line in st.splitlines() if line.startswith('XS_RAW\t')]
 eq(key+' new API physical MASK absent',[x.get('name') for x in raw if x.get('layerType')=='MASK'],[])
 eq(key+' new API copper uppercase',[x.get('name') for x in raw if x.get('conductor') is True],copper)
 films={q(r['name']):prop(r['attributes']) for r in table(after/'films_full.tsv')}
 eq(key+' complete original film name list/order',list(films),list(expected[n]))
 eq(key+' film count with no substitute custom film',len(films),15 if n==2 else 17)
 presence={q(r['layer']):r['exists']=='t' for r in table(after/'layer_presence.tsv')}
 details=[]
 for name,orig in expected[n].items():
  actual=films[name]
  for opt,val in orig.items():
   if opt=='layers':continue
   if opt in ('xOffset','yOffset'):
    got=actual['offset'][0 if opt=='xOffset' else 1]
   elif opt=='ipc2581':got=actual.get(opt) or []
   else:got=actual.get(opt)
   eq(key+' '+name+' exact original option '+opt,got,val)
  requested=orig['layers']
  unsupported=sorted({l for l in requested if not presence.get(l,False)})
  legal=[l for l in requested if presence.get(l,False)]
  actual_layers=actual['groupMembers'] or []
  eq(key+' '+name+' all and only valid original film members',set(actual_layers),set(legal))
  eq(key+' '+name+' native deduplicates original repeated refs',len(actual_layers),len(set(legal)))
  allowed={'BOARD GEMETRY/SILKSCREEN_TOP','BOARD GEMETRY/SILKSCREEN_BOTTOM'}
  if n==2:allowed|={'CONSTRAINT REGION/L2','CONSTRAINT REGION/L3'}
  check(key+' '+name+' unsupported refs only known original issues',set(unsupported)<=allowed,unsupported)
  details.append({'film':name,'optionsExact':True,'sourceLayerCount':len(requested),'sourceDuplicateCount':len(requested)-len(set(requested)),
   'actualLayerCount':len(actual_layers),'nativeFilteredOriginalInvalidRefs':unsupported,'actualLayers':actual_layers})
 film_details[key]=details
 eq(key+' typo class not fabricated',[presence.get('BOARD GEMETRY/SILKSCREEN_TOP'),presence.get('BOARD GEMETRY/SILKSCREEN_BOTTOM')],[False,False])
 for c in ('PIN','VIA CLASS','PACKAGE GEOMETRY','BOARD GEOMETRY'):
  for side in ('TOP','BOTTOM'):check(key+' real non-conductor mask class kept '+c+'/'+side,presence.get(c+'/SOLDERMASK_'+side))
 for fname in ['components.tsv','component_pins.tsv','nets.tsv','placed_pins.tsv','padstacks.tsv',
  'placed_pads.tsv','physical_pad_layers.tsv','mechanical_direct.tsv','direct_geometry.tsv',
  'net_rules.tsv','class_table.tsv','group_members.tsv','physical_csets.tsv','spacing_csets.tsv','electrical_csets.tsv','route_geometry.tsv','vias.tsv','specific_proof.tsv']:
  rows_eq(key+' exact baseline-preserving '+fname,table(after/fname),table(before/fname))
 comps=table(after/'components.tsv');pins=table(after/'component_pins.tsv')
 eq(key+' logical components',len(comps),80)
 eq(key+' logical component pins',len(pins),272)
 eq(key+' six NC retained',sum(not r['net'] or r['net']=='nil' for r in pins),6)
 eq(key+' logical named nets',len(table(after/'nets.tsv')),69)
 pp=table(after/'placed_pins.tsv');eq(key+' physical placed pins including mechanical holes',len(pp),22)
 apertures=table(after/'physical_pad_layers.tsv')
 eq(key+' every placed pin and unique via all copper+mask/paste rows',len(apertures),23*(n+4))
 for r in apertures:check(key+' preserved actual pad '+r['kind']+r['key']+r['xy']+r['layer'],True,{'figure':r['figure'],'bbox':r['bbox'],'padstack':r['padstack']})
 eq(key+' unique via aperture identity count',len({(r['key'],r['xy']) for r in apertures if r['kind']=='VIA'}),1)
 ns=text(after/'native_summary.txt')
 check(key+' reopened native DRC0/t','drcs=0\ndrcState=t' in ns)
 ft=text(fix/'fix.txt')
 check(key+' correction DRC0/t recorded','DRC=0 COUNT=0 STATE=t' in ft and 'FCOR_FIX_COMPLETE' in ft)
 eq(key+' all template calls true',len(re.findall(r'^FILM_RESULT\t"[^"]+"\tt$',ft,re.M)),15 if n==2 else 17)
 mech=table(after/'mechanical_direct.tsv');outline=next(x for x in mech if x['layer']=='"BOARD GEOMETRY/DESIGN_OUTLINE"')
 eq(key+' true board bbox',value(outline['bbox']),[[0.0,0.0],[80.0,60.0]])
 expectedVertices=[[[2,0],0],[[78,0],0],[[80,2],0],[[80,58],0],[[78,60],0],[[2,60],0],[[0,58],0],[[0,2],0]]
 eq(key+' true board eight C2 vertices',value(outline['vertices']),expectedVertices)
 # The direct legacy OUTLINE readback will be provided by native owner before final audit.
 legacy_file=C/'logs'/('outline_'+key)/'outline_exact.tsv'
 if legacy_file.exists():
  lr=table(legacy_file)
  shape=[x for x in lr if q(x.get('layer',''))=='BOARD GEOMETRY/OUTLINE']
  eq(key+' one real template OUTLINE geometry',len(shape),1)
  if shape:
   eq(key+' legacy OUTLINE bbox matches true board',shape[0]['bbox'],outline['bbox'])
   eq(key+' legacy OUTLINE vertices match true board',value(shape[0]['vertices']),value(outline['vertices']))
 else:
  check(key+' real template OUTLINE readback available',False,str(legacy_file))
# Scope corrections are part of acceptance, not hidden behind a narrow old PASS.
limitations=[
 'Original BOARD GEMETRY typo references are invalid and filtered by native API; original 01env scripts stay byte-identical.',
 '2L DisAll original CONSTRAINT REGION/L2,L3 are not real two-layer subclasses and are filtered; no extra copper was invented.',
 'Film member duplication is deduplicated by native API; semantic layer sets and every original option are checked independently.',
 'Original silk films do not include REF DES/SILKSCREEN; matching template is not proof of complete silk manufacturing content.',
 'FilmControl is separate from General Parameters art_param/art_aper and generated CAM; this correction does not certify fabrication output.',
 'Physical MASK rows removed; existing non-etch SOLDERMASK classes and every placed embedded pad aperture are retained. Tented via NULL apertures are intentionally unchanged.',
 'Physical stackup values remain teaching targets; Dk frequency limits, manufacturing capability and USB shell-stake/board-thickness fit remain prior recorded open engineering work.',
 'Prior independent audits incorrectly accepted only copper films plus custom outline and did not reject extra physical MASK rows. Those conclusions are historical and superseded for these requirements.',
]
failed=[c for c in checks if not c['pass']]
result={'status':'PASS_INDEPENDENT_USER_CORRECTION_REVIEW' if not failed else 'INCOMPLETE_OR_FAIL',
 'scope':'Saved isolated F28 2L, F28 4L, F29 v4 native correction; read-only audit, no Cadence invocation.',
 'checks':len(checks),'failed':len(failed),'allCoreChecksPass':not failed,'failedChecks':failed,
 'filmReview':film_details,'limitationsAndHistoryCorrection':limitations,'checkDetails':checks}
R.mkdir(exist_ok=True)
(R/'review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=lambda a:sorted(a) if isinstance(a,set) else str(a)),encoding='utf-8')
(R/'evidence_manifest.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks),'failed':len(failed),'failedNames':[c['check'] for c in failed]},ensure_ascii=False))
