"""Evidence-based validation for lesson06 and lesson05 independent repeat. Stdlib only."""
import pathlib,json,csv,hashlib,re
ROOT=pathlib.Path(r'D:\001DIY\005lib\01AIEDA')
B=ROOT/'learning/examples/lesson06_operations'
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return [{k:v.strip('"') for k,v in r.items()} for r in csv.DictReader(f,delimiter='\t')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
want={'INITIAL':[5,5,7,7],'MOVED':[7,4,9,6],'ROTATED':[5,4,7,6],'OOPS':[7,4,9,6],'ROLLBACK':[5,5,7,7],'COMMIT':[4,7,6,9],'AFTER_SAVE':[4,7,6,9],'REOPEN':[4,7,6,9]}
states=rows(B/'logs/create03/states.tsv')+rows(B/'logs/reopen/states.tsv')
assert len(states)==8
for r in states:assert all(abs(float(r[k])-v)<1e-9 for k,v in zip(['minx','miny','maxx','maxy'],want[r['state']]))
op=(B/'logs/create03/operations.txt').read_text(encoding='utf-8-sig')
for flag in ['visibility_restored=t','filter_enabled_restored=t','filter_buttons_restored=t','grid_restored=t','selection_result=t count=1 types=("shape")','LESSON06 COMPLETE_NATIVE_SUBSET']:
 assert flag in op,flag
assert 'probe_t=("SHAPES")' in op
assert 'filter_probe_nil=("BONDSMART" "DYNTHEMALS" "SHAPES" "TEXT")' in op
geometry=B/'logs/create03/geometry.tsv'
assert geometry.read_bytes()==(B/'logs/create03/geometry_after_save.tsv').read_bytes()==(B/'logs/reopen/geometry.tsv').read_bytes()
g=rows(geometry);assert len(g)==1
assert abs(float(g[0]['width'])-.101)<1e-9
q=rows(B/'logs/create03/quantization.tsv');assert len(q)==9
for r in q:
 r.update({k:float(v) for k,v in r.items()})
 assert abs(r['actual_x']/.001-round(r['actual_x']/.001))<1e-8
 assert abs(r['actual_y']+8)<1e-9
 r['delta_x_mm']=r['actual_x']-r['input_x']
launches={}
for part in ['create03','reopen']:
 j=json.loads((B/'logs'/part/'launch.json').read_text(encoding='utf-8-sig'))
 assert j['completed'] and j['exitCode']==0
 assert '*Error*' not in (B/'logs'/part/'stdout.txt').read_text(errors='replace')
 assert 'ASSERT failure' not in (B/'logs'/part/'stderr.txt').read_text(errors='replace')
 launches[part]=j
assert launches['reopen']['readonlyHashUnchanged']
result={'status':'PASS_NATIVE_SUBSET','course6FullyComplete':False,'pending':['Interactive viewport/menu/mouse/undo practice pending native desktop connection','Old mil/0 half-unit discrepancy cause remains unresolved'],'transactionStates':states,'settingsRestored':True,'filterSemanticsObserved':'nil=enabled, t=onButtons; automatic BONDSMART/DYNTHEMALS added','filterInitialState':'nil/nil in fresh process; known initialized baseline established for restoration test','quantizationObserved':q,'oddDbuLineGeometry':g[0],'geometryPersistent':True,'boardSHA256':sha(B/'lesson06_operations.brd'),'exitCodes':{k:v['exitCode'] for k,v in launches.items()},'interpretation':'Grid differs from database resolution. 0.101 mm line poly bbox includes half-DBU values while vertices fall on 0.001 mm grid. Observed differences retained, no general rounding rule or old-bug root cause inferred.'}
(B/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
L5=ROOT/'learning/examples/lesson05_instances';repeat=L5/'repeat';matches=[]
for stage in ['before','after','after_save']:
 for name in ['symbols.tsv','pins.tsv','children.tsv']:
  rel=pathlib.Path('logs/create02')/stage/name
  assert (L5/rel).read_bytes()==(repeat/rel).read_bytes(),str(rel)
  matches.append(str(rel))
for name in ['symbols.tsv','pins.tsv','children.tsv']:
 rel=pathlib.Path('logs/reopen')/name
 assert (L5/rel).read_bytes()==(repeat/rel).read_bytes(),str(rel)
 matches.append(str(rel))
for stage in ['create02','reopen']:
 j=json.loads((repeat/'logs'/stage/'launch.json').read_text(encoding='utf-8'))
 assert j['completed'] and j['exitCode']==0
 assert 'ASSERT failure' not in (repeat/'logs'/stage/'stderr.txt').read_text(errors='replace')
 if stage=='reopen':assert j['readonlyHashUnchanged']
r5={'status':'PASS','matchedNativeTsvFiles':matches,'repeatCreateExitCode':0,'repeatReopenExitCode':0,'qtAssertionReproduced':False,'originalQtAssertionRetained':True,'rootCause':'Not established','repeatBoardSHA256':sha(repeat/'lesson05_instances.brd')}
(repeat/'validation.json').write_text(json.dumps(r5,indent=2),encoding='utf-8')
env=pathlib.Path(r'D:\001DIY\005lib\01env');audit=[]
for p in sorted(env.glob('drill*.txt')):
 text=p.read_text(encoding='utf-8-sig',errors='replace');films=[]
 for block in re.split(r'(?=axlFilmCreate\s*\()',text):
  m=re.search(r'axlFilmCreate\s*\(\s*"([^"]+)"',block)
  if m and re.fullmatch(r'TOP|BOTTOM|L\d+',m[1]):
   films.append({'name':m[1],'etch':re.findall(r'"ETCH/([^"]+)"',block)})
 count=int(re.search(r'drill(\d+)',p.name)[1])
 expected=['TOP']+['L'+str(n) for n in range(2,count)]+['BOTTOM']
 names=[f['name'] for f in films]
 audit.append({'path':str(p),'sha256':sha(p),'expectedCopperLayers':expected,'copperFilmNamesInFileOrder':names,'filmLayerReferences':films,'nameOrderMatchesUserRule':names==expected,'note':'Film sequence is an artwork parameter; physical stack order must be verified from board cross-section.'})
out=ROOT/'learning/logs/layer_template_inventory_20261018.json'
out.write_text(json.dumps({'source':'User instruction and read-only inventory of 01env drill*.txt; scripts not executed or changed','files':audit},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'lesson06':result['status'],'lesson05Repeat':r5['status'],'templateFiles':len(audit),'templateExceptions':[p['path'] for p in audit if not p['nameOrderMatchesUserRule']]},ensure_ascii=False,indent=2))
