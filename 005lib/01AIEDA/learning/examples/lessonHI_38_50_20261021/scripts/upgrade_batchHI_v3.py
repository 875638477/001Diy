from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/compile_batchHI_v2.py').read_text()
s=s.replace(" elif typ=='region':"," elif typ=='netClass':\n  statements.append(f'hiAssignNetClass(f {q(op[\"name\"])} \\'{op[\"domain\"]} {q(op[\"cset\"])} list('+ ' '.join(q(n) for n in op['nets'])+'))')\n elif typ=='region':")
s=s.replace(" if typ=='via':statements.append(", " if typ=='bindShape':statements.append(f'hiBindExistingShape(f {q(ident)} {q(net)} {q(op[\"layer\"])})')\n elif typ=='void':statements.append(f'hiVoid(f {q(op[\"shapeId\"])} {points(op[\"polygon\"])})')\n elif typ=='via':statements.append(")
s=s.replace("for p in data.get('proofs',[]):", "for check in data.get('postChecks',[]):\n if check['type']=='hseIsolation':statements.append(f'hiHSEIsolationChallenge({q(out.as_posix())} {pt(check[\"anchorXY\"])} {q(check[\"localLayer\"])} {pt(check[\"guardXY\"])})')\n else:raise ValueError(check['type'])\nfor p in data.get('proofs',[]):")
s=s.replace("R/'scripts/batchHI_extended.il',il", "R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',il")
(R/'scripts/compile_batchHI_v3.py').write_text(s,encoding='ascii')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text()
s=s.replace('procedure(hiHSEIsolationChallenge(out anchorXY)','procedure(hiHSEIsolationChallenge(out anchorXY localLayer guardXY)')
s=s.replace('let((f mark via beforeCount)','let((f mark via beforeCount graph quietShape guard)')
s=s.replace('beforeCount=length(axlDBGetDesign()->drcs)','axlDRCUpdate(t) axlDBRefreshId(nil)\n  beforeCount=length(axlDBGetDesign()->drcs)')
s=s.replace('  hiProof(f "C22.2" "C23.2" t)\n  hiProof(f "C22.2" "U1.47" nil)',
'''  hiProof(f "C22.2" "C23.2" t)
  graph=gConnectedObjects(gPin("C22" "2"))
  quietShape=setof(s graph equal(s->objType "shape") && equal(s->layer strcat("ETCH/" localLayer)) && s->fill)
  guard=hiResolvePoint("GND" "TOP" guardXY "point")
  fprintf(f "NEGATIVE_LOCAL_REFERENCE count=%d guardReached=%L\\n" length(quietShape) if(member(guard graph) then t else nil))
  unless(quietShape && member(guard graph) error("Local island or quiet guard disconnected in anchor-negative test\\n"))
  hiProof(f "C22.2" "U1.47" nil)''')
p.write_text(s,encoding='ascii')
apis=['axlDBOpenShape','axlDBCreateVoid','axlDBCreateOpenShape','axlDBCreateCloseShape','axlShapeDynamicUpdate','axlDBGetShapes','axlDBTransactionStart','axlDBTransactionRollback','axlNetClassCreate','axlNetClassGet','axlNetClassAdd','axlNetClassRemove','axlDBAddProp']
base=Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS')
dest=R/'source/apiHI';dest.mkdir(exist_ok=True)
import shutil,json,hashlib
e=[]
for n in apis:
 src=base/(n+'.txt');out=dest/src.name;shutil.copyfile(src,out);e.append({'api':n,'officialSource':str(src),'copy':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest().upper()})
(dest/'source_manifest.json').write_text(json.dumps(e,indent=2),encoding='utf8')
print('prepared compiler3 and '+str(len(e))+' official API copies; HSE negative helper not executed yet')
