from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');d=json.loads((R/'engineering_power/RIGHT10_source_joint_v1.json').read_text());old=d['oscillatorReferenceRework']['source'];new=d['oscillatorReference'];Q=json.dumps
pt=lambda p:'list('+' '.join(str(float(x)) for x in p)+')';pts=lambda pp:'list('+' '.join(pt(p) for p in pp)+')'
body=r'''procedure(hiPolygonMatches(obj points)
 let((poly vertices actual n ok found)
  poly=car(axlPolyFromDB(obj))
  unless(poly return(nil))
  vertices=poly->vertices
  when(exists(v vertices abs(cadr(v))>0.0000001) return(nil))
  actual=mapcar('car vertices)
  when(length(actual)>1 && equal(car(actual) car(last(actual))) actual=reverse(cdr(reverse(actual))))
  when(length(points)>1 && equal(car(points) car(last(points))) points=reverse(cdr(reverse(points))))
  n=length(points) found=nil
  unless(length(actual)==n return(nil))
  foreach(order list(actual reverse(actual))
   for(offset 0 n-1
    ok=t
    for(k 0 n-1
     unless(abs(car(nth(mod(k+offset n) order))-car(nth(k points)))<0.00011 && abs(cadr(nth(mod(k+offset n) order))-cadr(nth(k points)))<0.00011 ok=nil))
    when(ok found=t)))
  found))
procedure(hiUniqueExactShape(net layer polygon dynamic)
 let((found)
  found=setof(s axlDBGetShapes(strcat(if(dynamic then "BOUNDARY/" else "ETCH/") layer))
    s->net && equal(s->net->name net) && if(dynamic then s->shapeIsBoundary else !s->shapeBoundary && !s->shapeIsBoundary) && hiPolygonMatches(s polygon))
  unless(length(found)==1 error("Exact polygon shape is not uniquely selected net=%L layer=%L dynamic=%L found=%L\n" net layer dynamic found))
  car(found)))
procedure(hiReplaceExactShape(f id net layer oldPolygon newPolygon dynamic voids)
 let((target)
  target=hiUniqueExactShape(net layer oldPolygon dynamic)
  fprintf(f "HI_REPLACE_EXACT_SHAPE_OLD id=%L attrs=%L polygon=%L\n" id target->?? oldPolygon)
  unless(axlDeleteObject(target) error("Cannot remove exact old reference shape\n"))
  axlDBRefreshId(nil)
  when(setof(s axlDBGetShapes(strcat(if(dynamic then "BOUNDARY/" else "ETCH/") layer)) s->net && equal(s->net->name net) && hiPolygonMatches(s oldPolygon)) error("Old polygon was not removed before replacement\n"))
  hiShape(f id net layer newPolygon dynamic voids)
  target=hiUniqueExactShape(net layer newPolygon dynamic)
  fprintf(f "HI_REPLACE_EXACT_SHAPE_NEW id=%L attrs=%L polygon=%L\n" id target->?? newPolygon)
  target))
procedure(hiUniqueBoundaryByBBox(net layer bbox)
 let((found)
  found=setof(s axlDBGetShapes(strcat("BOUNDARY/" layer)) s->net && equal(s->net->name net) && equal(s->bBox bbox))
  unless(length(found)==1 error("Application boundary not unique by net/layer/bbox\n"))
  car(found)))
procedure(hiReplaceExactVoid(f id net layer bbox oldPolygon newPolygon)
 let((boundary candidates target beforeCount otherVoids)
  boundary=hiUniqueBoundaryByBBox(net layer bbox)
  candidates=setof(v boundary->voids hiPolygonMatches(v oldPolygon))
  unless(length(candidates)==1 error("Old permanent void not unique; refuse overlay\n"))
  target=car(candidates) beforeCount=length(boundary->voids) otherVoids=setof(v boundary->voids !equal(v target))
  fprintf(f "HI_REPLACE_PERMANENT_VOID_OLD id=%L boundary=%L target=%L attrs=%L oldPolygon=%L\n" id boundary target target->?? oldPolygon)
  unless(axlDeleteObject(target) error("Cannot delete exact old permanent void\n"))
  axlDBRefreshId(nil) boundary=hiUniqueBoundaryByBBox(net layer bbox)
  unless(length(boundary->voids)==beforeCount-1 error("Permanent void removal affected unexpected count\n"))
  when(setof(v boundary->voids hiPolygonMatches(v oldPolygon)) error("Old permanent void still exists\n"))
  foreach(v otherVoids unless(member(v boundary->voids) error("Unrelated permanent void changed\n")))
  hiReg(id "shape" boundary) hiVoid(f id newPolygon)
  boundary=hiUniqueBoundaryByBBox(net layer bbox)
  unless(length(boundary->voids)==beforeCount && length(setof(v boundary->voids hiPolygonMatches(v newPolygon)))==1 error("New exact permanent void not present once\n"))
  fprintf(f "HI_REPLACE_PERMANENT_VOID_NEW id=%L oldRemoved=t newUnique=t voidCount=%d newPolygon=%L\n" id length(boundary->voids) newPolygon)
  t))
'''
p=R/'scripts/batchHI_shapes_v3.il';p.write_text(p.read_text()+'\n'+body,encoding='ascii')
tag='HSE_replacement_rollback_4L_01';out=(R/'logs'/tag).as_posix()
program='procedure(hiHSEReplacePilot()\n let((f mark before)\n f=outfile('+Q(out+'/hi_hse_replace_rollback.txt')+')\n hiRegistry=nil\n before=hiUniqueExactShape("GND" "L2" '+pts(old['islandPolygon'])+' nil)\n fprintf(f "BEFORE quietShape=%L oldStemPoint=%L newStemPoint=%L storedDRCs=%d\\n" before axlGeoPointInShape(list(45.45 29.5) before t) axlGeoPointInShape(list(46.35 30.5) before t) length(axlDBGetDesign()->drcs))\n mark=axlDBTransactionStart()\n unwindProtect(progn(axlDBControl(\'drcEnable nil)\n'
program+=' hiReplaceExactShape(f "PILOT_NEW_QUIET" "GND" "L2" '+pts(old['islandPolygon'])+' '+pts(new['islandPolygon'])+' nil nil)\n'
for layer in ['L2','L3']:program+=' hiReplaceExactVoid(f '+Q('PILOT_APP_'+layer)+' "GND" '+Q(layer)+' list(list(0.5 0.5) list(79.5 59.5)) '+pts(old['applicationGroundVoidPolygon'])+' '+pts(new['applicationGroundVoidPolygon'])+')\n'
program+=' axlShapeDynamicUpdate(nil t) axlDBRefreshId(nil)\n before=hiUniqueExactShape("GND" "L2" '+pts(new['islandPolygon'])+' nil)\n fprintf(f "REPLACED oldStemPoint=%L newStemPoint=%L noFullDRCRequested=t\\n" axlGeoPointInShape(list(45.45 29.5) before t) axlGeoPointInShape(list(46.35 30.5) before t))\n unless(!axlGeoPointInShape(list(45.45 29.5) before t) && axlGeoPointInShape(list(46.35 30.5) before t) error("New quiet stem not actually replaced\\n"))\n t) progn(unless(axlDBTransactionRollback(mark) error("Reference replacement rollback failed\\n")) axlDBControl(\'drcEnable t)))\n before=hiUniqueExactShape("GND" "L2" '+pts(old['islandPolygon'])+' nil)\n unless(member(gPin("U1" "47") gConnectedObjects(gPin("C22" "2"))) error("Original quiet bridge graph did not restore\\n"))\n fprintf(f "HSE_REFERENCE_REPLACE_ROLLBACK_COMPLETE_NO_SAVE_NO_FULL_DRC_REQUEST oldShapeRestored=%L C22toVSS47Restored=t drcEnable=%L\\n" before axlDBControl(\'drcEnable)) close(f) t))\n'
p=R/f'scripts/{tag}.il';p.write_text(program,encoding='ascii')
loads=[R/'source/placementG.il',R/'source/local_copperG_v2.il',R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',p];snap=R/'source/readback_snapshots'/tag;snap.mkdir(parents=True,exist_ok=False);h='set NOCONFIRM\n';m=[]
for i,p in enumerate(loads):
 dst=snap/(str(i).zfill(2)+'_'+p.name);shutil.copyfile(p,dst);h+='skill errset(load('+Q(dst.as_posix())+') t)\n';m.append({'source':str(p),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiHSEReplacePilot() t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(m,indent=2))
