
hiNodeDefinitions=nil
procedure(hiPointOnLine(pt ends)
 let((a b dx dy cross eps)
  a=car(ends) b=cadr(ends) eps=0.00002
  dx=car(b)-car(a) dy=cadr(b)-cadr(a)
  cross=(car(pt)-car(a))*dy-(cadr(pt)-cadr(a))*dx
  abs(cross)<=eps*max(1.0 sqrt(dx*dx+dy*dy)) &&
   car(pt)>=min(car(a) car(b))-eps && car(pt)<=max(car(a) car(b))+eps &&
   cadr(pt)>=min(cadr(a) cadr(b))-eps && cadr(pt)<=max(cadr(a) cadr(b))+eps))
procedure(hiResolvePoint(net layer xy kind)
 let((found obj result)
  found=nil result=nil
  foreach(c axlDBGetDesign()->components
   foreach(p c->symbol->pins
    when(p->net && equal(p->net->name net) && equal(p->xy xy) && !equal(kind "via") result=p)))
  unless(result
   foreach(obj axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
    when(equal(obj->objType "via") && equal(obj->xy xy) && obj->net && equal(obj->net->name net) result=obj)))
  unless(result || equal(kind "via")
   foreach(obj axlExtractMap("C:/Program0/Cadence/SPB172/share/pcb/text/views/fgeo_bv.txt" nil)
    when(equal(obj->objType "line") && equal(obj->layer strcat("ETCH/" layer)) && obj->net && equal(obj->net->name net) && hiPointOnLine(xy obj->startEnd)
     when(equal(obj->parent->objType "path") result=obj->parent))))
  unless(result error("Actual endpoint copper not found net=%s layer=%s xy=%L type=%s\n" net layer xy kind))
  result))
procedure(hiResolve(key)
 let((parts row obj def generated)
  parts=parseString(key ".")
  if(length(parts)==2 then
   obj=gPin(car(parts) cadr(parts))
  else
   def=assoc(key hiNodeDefinitions)
   if(def then
    obj=hiResolvePoint(cadr(def) caddr(def) cadddr(def) nth(4 def))
   else
    row=assoc(key hiRegistry)
    unless(row error("Unknown endpoint %s\n" key))
    obj=caddr(row)
    when(listp(obj) obj=car(obj))
    when(equal(obj->objType "shape") && obj->shapeIsBoundary
     generated=setof(s axlDBGetShapes("ETCH") equal(s->shapeBoundary obj))
     unless(generated error("Dynamic boundary has no real generated ETCH copper\n"))
     obj=car(generated))))
  obj))
procedure(hiShape(f id net layer points dynamic voids)
 let((shape ret boundary path)
  if(equal(points "ROUTE_KEEPIN") then
   shape=car(axlDBCreateShape(car(axlPolyFromDB(axlDBGetDesign()->keepinRoute)) t strcat("ETCH/" layer) net))
  else
   shape=axlDBCreateOpenShape(hiClosedPath(points) t strcat("ETCH/" layer) net)
   unless(shape error("Cannot create actual shape\n"))
   foreach(v voids unless(axlDBCreateVoid(shape hiClosedPath(v)) error("Cannot add permanent shape void\n")))
   ret=axlDBCreateCloseShape(shape t)
   unless(ret error("Cannot close actual shape\n"))
   shape=car(ret))
  unless(shape error("Cannot create actual filled ETCH shape\n"))
  when(dynamic
   boundary=axlShapeChangeDynamicType(shape t t)
   unless(boundary error("Cannot convert actual shape to dynamic\n"))
   shape=boundary
   unless(equal(axlShapeDynamicUpdate(shape t) 0) error("Dynamic shape has no current actual fill\n")))
  fprintf(f "HI_SHAPE id=%L net=%L layer=%L dynamic=%L object=%L\n" id net layer dynamic shape->??)
  hiReg(id "shape" shape)
  shape))
procedure(hiVoid(f shapeId points)
 let((row shape ret)
  row=assoc(shapeId hiRegistry)
  unless(row error("Void requires known shape id %s\n" shapeId))
  shape=caddr(row)
  unless(axlDBOpenShape(shape) error("Cannot open known shape for void\n"))
  unless(axlDBCreateVoid(shape hiClosedPath(points)) error("Cannot create permanent void\n"))
  ret=axlDBCreateCloseShape(shape t)
  unless(ret error("Cannot close shape after permanent void\n"))
  fprintf(f "HI_PERMANENT_VOID shapeId=%L actual=%L\n" shapeId car(ret)->??)
  t))
