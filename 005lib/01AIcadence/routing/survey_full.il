; visibility-independent full survey via selectAll + coord filter (read only)
procedure( AIB_nn(o)
    if( o->net then o->net->name else "NONET" )
)
AIB_x1 = -1010.0
AIB_y1 = -845.0
AIB_x2 = 810.0
AIB_y2 = -90.0
procedure( AIB_inbox(bb)
    !( (xCoord cadr(bb)) < AIB_x1 || (xCoord car(bb)) > AIB_x2
       || (yCoord cadr(bb)) < AIB_y1 || (yCoord car(bb)) > AIB_y2 )
)
axlClearSelSet()
axlSetFindFilter(?enabled list("noall" "clines" "vias" "pins" "shapes")
                 ?onButtons list("noall" "clines" "vias" "pins" "shapes"))
axlAddSelectAll()
AIB_objs = axlGetSelSet()
printf("selected total: %d\n" length(AIB_objs))
AIB_skipped = 0
foreach(o AIB_objs
    when( o->bBox && AIB_inbox(o->bBox)
        when( !errset(
        cond(
            (o->objType == "via"
                printf("V|%s|%f|%f|%f\n" AIB_nn(o) (xCoord o->xy) (yCoord o->xy)
                    ((xCoord cadr(o->bBox)) - (xCoord car(o->bBox))) / 2.0))
            (o->objType == "pin"
                cond(
                    (o->isThrough
                        printf("PA|%s|%f|%f|%f|%f\n" AIB_nn(o)
                            (xCoord car(o->bBox)) (yCoord car(o->bBox))
                            (xCoord cadr(o->bBox)) (yCoord cadr(o->bBox))))
                    (member("ETCH/TOP" o->startEnd)
                        printf("PT|%s|%f|%f|%f|%f\n" AIB_nn(o)
                            (xCoord car(o->bBox)) (yCoord car(o->bBox))
                            (xCoord cadr(o->bBox)) (yCoord cadr(o->bBox))))
                    (member("ETCH/BOTTOM" o->startEnd)
                        printf("PB|%s|%f|%f|%f|%f\n" AIB_nn(o)
                            (xCoord car(o->bBox)) (yCoord car(o->bBox))
                            (xCoord cadr(o->bBox)) (yCoord cadr(o->bBox))))
                ))
            (o->objType == "path"
                let( (tag)
                    tag = cond(
                        (o->layer == "ETCH/TOP" "ST")
                        (o->layer == "ETCH/BOTTOM" "SB")
                        (o->layer == "ETCH/L8" "S8")
                        (o->layer == "ETCH/L3" "S3")
                        (t nil)
                    )
                    when( tag
                        foreach(s o->segments
                            printf("%s|%s|%f|%f|%f|%f|%f\n" tag AIB_nn(o)
                                (xCoord car(s->startEnd)) (yCoord car(s->startEnd))
                                (xCoord cadr(s->startEnd)) (yCoord cadr(s->startEnd))
                                s->width)))
                ))
            (o->objType == "shape"
                let( (tag)
                    tag = cond(
                        (o->layer == "ETCH/L8" "B8")
                        (o->layer == "ETCH/L3" "B3")
                        (t nil)
                    )
                    when( tag
                        foreach(s o->segments
                            printf("%s|%s|%f|%f|%f|%f\n" tag AIB_nn(o)
                                (xCoord car(s->startEnd)) (yCoord car(s->startEnd))
                                (xCoord cadr(s->startEnd)) (yCoord cadr(s->startEnd)))))
                ))
        )
        t)
            AIB_skipped = AIB_skipped + 1
        )
    )
)
printf("skipped due to errors: %d\n" AIB_skipped)
axlClearSelSet()
printf("done\n")
