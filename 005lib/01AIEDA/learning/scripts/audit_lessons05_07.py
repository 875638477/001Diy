"""Final archive audit; does not start EDA software."""
import pathlib,json,hashlib,re,csv,datetime
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA')
def read(p):return p.read_text(encoding='utf-8-sig')
def J(p):return json.loads(read(p))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
index=read(R/'课程索引.md');eda=read(R/'EDA.md')
ids=[int(n) for n in re.findall(r'^\|\s*(\d+)\s*\|',index,re.M)]
assert ids==list(range(1,61))
assert '我刚刚在另外一个窗口设计pcb' in eda,'User-added top text lost'
for t in ['TOP-BOTTOM','TOP-L2-L3-BOTTOM','TOP-L2-L3-L4-L5-BOTTOM']:assert t in eda and t in index
l5=J(R/'learning/examples/lesson05_instances/validation.json')
l5r=J(R/'learning/examples/lesson05_instances/repeat/validation.json')
l6=J(R/'learning/examples/lesson06_operations/validation.json')
l7=J(R/'learning/examples/lesson07_padstacks/validation.json')
assert l5['pass'] and l5['total_checks']==13088 and not l5['failures']
assert l5r['status']=='PASS' and not l5r['qtAssertionReproduced']
assert l6['status']=='PASS_NATIVE_SUBSET' and not l6['course6FullyComplete']
assert l7['allChecksPass'] and l7['checkCount']>=650 and not l7['failures']
defaults=R/'learning/examples/lesson07_padstacks/logs/reopen_defaults'
assert J(defaults/'launch.json')['readonlyHashUnchanged']
assert 'PACKAGE_HEIGHT_MAX "1 MM"' in read(defaults/'defaults.txt')
with (defaults/'required_texts.tsv').open(encoding='utf-8-sig',newline='') as f:ts=list(csv.DictReader(f,delimiter='\t'))
assert len(ts)==3 and all(float(t['x'])==0 and float(t['y'])==0 for t in ts)
stack=R/'learning/examples/lesson07_padstacks/logs/reopen_board/stackup.tsv'
with stack.open(encoding='utf-8-sig',newline='') as f:st=list(csv.DictReader(f,delimiter='\t'))
assert [r['name'].strip('"') for r in st if r['conductor']=='t']==['TOP','L2','L3','BOTTOM']
inventory=J(R/'learning/logs/layer_template_inventory_20261018.json')
for f in inventory['files']:assert sha(pathlib.Path(f['path']))==f['sha256'],'Template changed: '+f['path']
public=J(R/'learning/examples/qmi8610/final_validation.json')['publicArtifacts']
for file,info in public.items():assert sha(pathlib.Path(file))==info['sha256'],'Public QMI library changed'
notes=[R/'EDA.md',R/'课程索引.md',R/'lib文本索引.md']+[R/'learning/notes'/n for n in ['lesson05_instances_20261018.md','lesson06_operations_20261018.md','lesson07_padstacks_20261018.md','pcb_layer_naming.md','extracta_readback_20261018.md']]
for p in notes:
 assert p.is_file() and p.stat().st_size>500
 # Check relative Markdown file targets where used.
 for target in re.findall(r'\]\(([^)]+)\)',read(p)):
  if target.startswith(('http','C:','D:','/','#')):continue
  dest=(p.parent/target.split('#')[0])
  assert dest.exists(),'Missing note link: '+str(p)+' -> '+target
summary={'date':'2026-10-18','timezone':'Asia/Shanghai','lesson05':{'status':'Completed declared native scope','checks':l5['total_checks'],'repeat':'PASS, exit0 create/reopen, 12 native TSV files identical','originalQtException':'Retained; cause unresolved, not reproduced in repeat'},'lesson06':{'status':'Native subset complete; full course partial','gui':'native pipe unavailable','geometryPrecision':'Half-DBU bbox/vertices difference reproduced, old cause unresolved'},'lesson07':{'status':'Basic hole geometry and persisted four-layer mapping complete','checks':l7['checkCount'],'notValidated':l7['notValidated'],'boardDRC':'stored0/state nil; no complete board DRC pass claim'},'fixedCopperLayerRule':{'2':['TOP','BOTTOM'],'4':['TOP','L2','L3','BOTTOM'],'6':['TOP','L2','L3','L4','L5','BOTTOM'],'extend':'TOP, L2 through L(N-1), BOTTOM'},'templateAudit':{'count':len(inventory['files']),'inputsUnchanged':True,'exception':'drill12.txt contains TOP,L2..L12,BOTTOM (13 copper films), expected 12 ending L11'},'publicQmiLibraryUnchanged':True,'userPcbNotModified':True,'notes':[{ 'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in notes],'resumption':'Read EDA.md, course index, pcb_layer_naming.md, relevant lesson notes and validation data before continuing; copy whole 01AIEDA when moving computers.'}
out=R/'learning/logs/lessons05_07_result_20261018.json'
out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'archiveAudit':'PASS','lessons':[summary['lesson05']['status'],summary['lesson06']['status'],summary['lesson07']['status']],'notes':len(notes),'curriculumRows':len(ids),'unchangedTemplates':len(inventory['files']),'summary':str(out)},ensure_ascii=False,indent=2))

