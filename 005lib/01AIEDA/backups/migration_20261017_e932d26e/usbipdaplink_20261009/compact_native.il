procedure(AI_inside(bb area)
  bb && area &&
  car(car(bb)) >= car(car(area))-0.0001 &&
  cadr(car(bb)) >= cadr(car(area))-0.0001 &&
  car(cadr(bb)) <= car(cadr(area))+0.0001 &&
  cadr(cadr(bb)) <= cadr(cadr(area))+0.0001
)

procedure(AI_groupMove(name refs area delta angle origin)
  let((d objs n b o q s result before)
    d=axlDBGetDesign()
    objs=nil
    foreach(s d->symbols
      when(member(s->refdes refs) objs=cons(s objs))
    )
    unless(length(objs)==length(refs)
      error("Missing symbol in module %s" name)
    )
    when(area
      foreach(n d->nets
        foreach(b n->branches
          foreach(o b->children
            when(member(o->objType list("path" "via" "shape"))
              q=o
              when(o->objType=="shape"
                when(o->symbolEtch q=nil)
                when(q && o->shapeBoundary q=o->shapeBoundary)
              )
              when(q && AI_inside(q->bBox area) && !member(q objs)
                objs=cons(q objs)
              )
            )
          )
        )
      )
      foreach(b axlDBGetLonelyBranches()
        foreach(o b->children
          when(member(o->objType list("path" "via" "shape")) && AI_inside(o->bBox area) && !member(o objs)
            objs=cons(o objs)
          )
        )
      )
      foreach(o axlDBGetShapes("BOUNDARY")
        when(AI_inside(o->bBox area) && !member(o objs) objs=cons(o objs))
      )
    )
    fprintf(AI_log "MODULE %s COUNT %d DELTA %L ANGLE %L ORIGIN %L\n" name length(objs) delta angle origin)
    foreach(o objs
      fprintf(AI_log "BEFORE %s %L %L\n" o->objType o->layer o->bBox)
    )
    if(angle==0 then
      result=axlTransformObject(objs ?move delta ?allOrNone t)
    else
      result=axlTransformObject(objs ?move delta ?angle angle ?origin origin ?allOrNone t)
    )
    unless(result error("Transform failed in module %s" name))
    foreach(o result
      when(o->objType
        fprintf(AI_log "AFTER %s %L %L\n" o->objType o->layer o->bBox)
      )
    )
    fprintf(AI_log "RESULT %s COUNT %d\n" name length(result))
    result
  )
)

AI_log=outfile("D:/001DIY/023USB/08UsbIPDapLink/02pcb/compact_layout/compact_move_log.txt")
AI_mark=axlDBTransactionStart()
AI_ok=errset(load("D:/001DIY/005lib/01AIcadence/usbipdaplink_20261009/compact_moves.il") t)
if(AI_ok then
  axlDBTransactionCommit(AI_mark)
  fprintf(AI_log "SHAPE_UPDATE %L\n" axlShapeDynamicUpdate(nil t))
  fprintf(AI_log "SAVED %L\n" axlSaveDesign(?design "D:/001DIY/023USB/08UsbIPDapLink/02pcb/compact_layout/compact_stage1.brd" ?noConfirm t))
else
  axlDBTransactionRollback(AI_mark)
  fprintf(AI_log "FAILED_ROLLED_BACK\n")
)
close(AI_log)
