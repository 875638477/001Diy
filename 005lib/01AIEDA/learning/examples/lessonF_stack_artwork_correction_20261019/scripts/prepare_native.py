from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonF_stack_artwork_correction_20261019')
refs=[]
for n in [2,4]:
 d=json.loads((R/f'source/drill{n}_parsed.json').read_text())
 refs+= [v for f in d['films'] for v in f['layers']]
 p=R/f'scripts/full_template_{n}.il';s=p.read_text()
 p.write_text(f'procedure(fcorTemplate{n}(f)\n let((r)\n'+s+'\n t))\n',encoding='ascii')
ls=' '.join('"'+x+'"' for x in sorted(set(refs)))
src=r'''
procedure(fcorMaskPad(f obj kind key)
 let((p)
  foreach(l append(mapcar(lambda((x) strcat("ETCH/" x)) axlSubclassRoute()) list("PIN/SOLDERMASK_TOP" "PIN/SOLDERMASK_BOTTOM" "PIN/PASTEMASK_TOP" "PIN/PASTEMASK_BOTTOM"))
   p=axlDBGetPad(obj l "REGULAR")
   fprintf(f "%s\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" kind key obj->xy obj->name l if(p then p->figureName else nil) if(p then p->bBox else nil) obj->definition->usage))))
procedure(fcorRead(out)
 let((f ff mf vf d p s o seen xs poly)
  f29Read(out)
  f29ExtraRead(out)
  f29SpecificProof(out)
  l28More(out)
  l28Mechanical(out)
  f=outfile(strcat(out "/structure.txt"))
  ff=outfile(strcat(out "/films_full.tsv"))
  mf=outfile(strcat(out "/physical_pad_layers.tsv"))
  vf=outfile(strcat(out "/layer_presence.tsv"))
  d=axlDBGetDesign()
  fprintf(f "units=%L\nlegacy_xsection=%L\netch_group=%L\nroute=%L\n" axlDBGetDesignUnits() axlGetXSection() axlGetParam("paramLayerGroup:ETCH")->groupMembers axlSubclassRoute())
  fprintf(f "XSECTION_ALL=%L\n" axlXSectionGet(nil 'all))
  foreach(xs axlXSectionGet(nil 'all) fprintf(f "XS_RAW\t%L\n" xs->??))
  fprintf(f "BOARD_ROOT=%L\n" d->designOutline)
  fprintf(ff "name\tattributes\n")
  foreach(n axlGetParam("artwork")->groupMembers
   p=axlGetParam(strcat("artwork:" n))
   fprintf(ff "%L\t%L\n" n p->??))
  fprintf(mf "kind\tkey\txy\tpadstack\tlayer\tfigure\tbbox\tusage\n")
  foreach(s d->symbols foreach(o s->pins fcorMaskPad(mf o "PIN" list(s->name o->number))))
  seen=nil
  foreach(o axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
   when(equal(o->objType "via") && !member(o seen)
    seen=cons(o seen) fcorMaskPad(mf o "VIA" o->name)))
  fprintf(vf "layer\texists\n")
  foreach(l fcorTemplateLayers fprintf(vf "%L\t%L\n" l axlIsLayer(l)))
  foreach(l list("BOARD GEOMETRY/SOLDERMASK_TOP" "BOARD GEOMETRY/SOLDERMASK_BOTTOM" "PACKAGE GEOMETRY/SOLDERMASK_TOP" "PACKAGE GEOMETRY/SOLDERMASK_BOTTOM" "PIN/SOLDERMASK_TOP" "PIN/SOLDERMASK_BOTTOM" "VIA CLASS/SOLDERMASK_TOP" "VIA CLASS/SOLDERMASK_BOTTOM")
   fprintf(vf "%L\t%L\n" l axlIsLayer(l)))
  fprintf(f "FCOR_READ_COMPLETE\n")
  foreach(o list(f ff mf vf) close(o)) t))
procedure(fcorFix(n board out root)
 let((f xs masks result names old outline poly points existing c r)
  f=outfile(strcat(out "/fix.txt"))
  fprintf(f "START\t%L\t%L\n" axlCurrentDesign() axlDBGetDesignUnits())
  outline=axlDBGetDesign()->designOutline
  fprintf(f "ROOT_BEFORE=%L LAYER=%L\n" outline outline->layer)
  ; Increase metric storage precision only; preserve all existing coordinates.
  result=axlDBChangeDesignUnits(nil 4)
  fprintf(f "PRECISION_RESULT=%L ACTUAL=%L\n" result axlDBGetDesignUnits())
  unless(equal(axlDBGetDesignUnits() list("millimeters" 4)) error("Metric4 precision unavailable\n"))
  masks=nil
  foreach(xs axlXSectionGet(nil 'all)
   when(equal(xs->layerType "MASK")
    masks=cons(xs->position masks)
    fprintf(f "REMOVE_PHYSICAL_MASK\t%L\t%L\n" xs->name xs->position)))
  ; Highest current positions first; reacquire live id for each delete.
  masks=sort(masks 'greaterp)
  foreach(position masks
   xs=axlXSectionGet(nil position)
   unless(xs && equal(xs->layerType "MASK") error("Mask id/type mismatch\n"))
   unless(axlXSectionDelete(xs) error("Physical MASK delete failed\n")))
  names=axlSubclassRoute()
  fprintf(f "ACTUAL_COPPER=%L\n" names)
  unless(equal(names if(n==2 then list("TOP" "BOTTOM") else list("TOP" "L2" "L3" "BOTTOM"))) error("Unexpected actual copper names\n"))
  ; Create only legal missing non-conductor subclasses, never extra ETCH layers or classes.
  foreach(l fcorTemplateLayers
   unless(axlIsLayer(l)
    c=car(parseString(l "/"))
    if(member(c axlClasses()) && !member(c list("ETCH" "PIN" "VIA CLASS" "CONSTRAINT REGION" "ROUTE KEEPOUT" "VIA KEEPOUT" "BOUNDARY" "ANTI ETCH" "ROUTER PLAN" "CAVITY" "DRC ERROR CLASS")) then
     r=axlLayerCreateNonConductor(l)
     fprintf(f "MISSING_NONCONDUCTOR_CREATE\t%L\t%L\t%L\n" l r axlIsLayer(l))
    else
     fprintf(f "UNRESOLVED_TEMPLATE_REFERENCE\t%L\tclass_exists=%L\n" l member(c axlClasses())))))
  ; Original template uses legacy OUTLINE. Keep authoritative DESIGN_OUTLINE root untouched.
  existing=axlDBGetShapes("BOARD GEOMETRY/OUTLINE")
  unless(existing
   poly=car(axlPolyFromDB(outline))
   points=mapcar('car poly->vertices)
   foreach(v poly->vertices unless(equal(cadr(v) 0.0) error("Nonlinear outline needs exact arc handling\n")))
   points=append(points list(car(points)))
   result=axlDBCreateShape(axlPathStart(points 0.0) nil "BOARD GEOMETRY/OUTLINE" nil nil)
   unless(result error("Legacy outline copy failed\n"))
   fprintf(f "LEGACY_OUTLINE_CREATED=%L\n" car(result)))
  unless(equal(axlDBGetDesign()->designOutline outline) error("Authoritative board outline root changed\n"))
  ; Only film parameter records are removed. Geometry and subclasses are preserved.
  old=copy(axlGetParam("artwork")->groupMembers)
  foreach(name old
   p=axlGetParam(strcat("artwork:" name))
   unless(axlDeleteObject(p) error("Film parameter delete failed\n")))
  load(strcat(root if(n==2 then "/scripts/full_template_2.il" else "/scripts/full_template_4.il")))
  if(n==2 then fcorTemplate2(f) else fcorTemplate4(f))
  fprintf(f "FILMS_AFTER=%L\n" axlGetParam("artwork")->groupMembers)
  fprintf(f "DRC=%L COUNT=%d STATE=%L\n" axlDRCUpdate(t) length(axlDBGetDesign()->drcs) axlDBGetDesign()->drcState)
  unless(axlSaveDesign(?design board ?noMru t ?noConfirm t) error("Corrected board save failed\n"))
  fprintf(f "FCOR_FIX_COMPLETE\n") close(f) t))
'''
src='fcorTemplateLayers=list('+ls+')\n'+src
(R/'scripts/correction.il').write_text(src,encoding='ascii')
p=R.as_posix()
loads=[
'D:/001DIY/005lib/01AIEDA/learning/scripts/de_board_read.il',
'D:/001DIY/005lib/01AIEDA/learning/examples/lesson29_constraints_20261019/scripts/build29_v2.il',
'D:/001DIY/005lib/01AIEDA/learning/examples/lesson29_constraints_20261019/scripts/read29.il',
'D:/001DIY/005lib/01AIEDA/learning/examples/lesson29_constraints_20261019/scripts/extra_read29.il',
'D:/001DIY/005lib/01AIEDA/learning/examples/lesson29_constraints_20261019/scripts/specific_proof.il',
'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019/scripts/more28.il',
'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019/scripts/mechanical28.il',
p+'/scripts/correction.il']
header='set NOCONFIRM\n'+''.join('skill errset(load("'+x+'") t)\n' for x in loads)
records=json.loads((R/'input_manifest.json').read_text())
for row in records:
 if row['kind']!='board':continue
 k=row['key'];n=row['layerCount'];board=Path(row['working']).as_posix()
 for stage in ['baseline','fix','reopen']:
  tag=stage+'_'+k
  fn=f'fcorRead("{p}/logs/{tag}")' if stage!='fix' else f'fcorFix({n} "{board}" "{p}/logs/{tag}" "{p}")'
  (R/f'scripts/{tag}.scr').write_text(header+f'skill errset({fn} t)\nquit\nfillin "yes"\n',encoding='ascii')
print('NATIVE_FIX_AND_READBACK_READY')
