; Reusable, read-only Allegro17.2 polygon guard. No design setters or saves.
; Units are the active drawing units: caller must pass margin explicitly.
; Return list(nativeGuardPolygons methodSymbol), or error. An empty expand
; NEVER means "no intersection". Query AND of the returned guard with all
; relevant other-net actual copper before accepting a geometry change.
procedure(aiPolygonOp(a b op)
 let((r e)
  cond((null(a) if(equal(op 'OR) then b else nil))
       (null(b) if(equal(op 'AND) then nil else a))
       (t r=axlPolyOperation(a b op) e=axlPolyErrorGet()
        when(e error("Native polygon operation error %L\n" e))
        unless(r error("Native operation returned bareNIL, not empty placeholder\n"))
        remove(nil r)))))
procedure(aiPolygonMarginGuard(poly margin)
 let((guard e bb path rb x0 y0 x1 y1 method)
  unless(poly && poly->area>0.0 && length(poly->vertices)>=3 && margin>0.0
   error("Expected positive native polygon and explicit positive margin\n"))
  e=axlPolyErrorGet() when(e error("Unconsumed polygon error before guard %L\n" e))
  guard=axlPolyExpand(list(poly) margin 'ACU_BLUNT)
  e=axlPolyErrorGet() when(e error("Native margin expansion error %L\n" e))
  unless(guard error("Margin expansion returned bareNIL\n"))
  guard=remove(nil guard) method='nativeExpand
  unless(guard
   ; Three times the requested margin allows at most one margin of native
   ; quantization. The actual bbox below must STILL retain two margins.
   ; If drawing precision is too coarse, reject instead of silently passing.
   bb=poly->bBox unless(bb error("Missing native polygon bbox\n"))
   x0=caar(bb)-3.0*margin y0=cadar(bb)-3.0*margin
   x1=caadr(bb)+3.0*margin y1=cadadr(bb)+3.0*margin
   path=axlPathStart(list(x0:y0 x1:y0 x1:y1 x0:y1 x0:y0) 0.0)
   unless(path error("Guard rectangle path creation failed\n"))
   guard=axlPolyFromDB(path)
   e=axlPolyErrorGet() when(e error("Guard rectangle conversion error %L\n" e))
   guard=remove(nil guard)
   unless(length(guard)==1 error("Guard rectangle missing/fragmented\n"))
   rb=car(guard)->bBox
   unless(caar(rb)<=caar(bb)-2.0*margin && cadar(rb)<=cadar(bb)-2.0*margin && caadr(rb)>=caadr(bb)+2.0*margin && cadadr(rb)>=cadadr(bb)+2.0*margin
    error("Guard rectangle native rounding lost conservative margin\n"))
   method='conservativeBbox)
  when(aiPolygonOp(list(poly) guard 'ANDNOT)
   error("Guard fails exact native containment of original polygon\n"))
  list(guard method)))
