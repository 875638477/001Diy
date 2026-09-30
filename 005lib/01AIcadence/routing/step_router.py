# Incremental router: plan on L8 only, commit one short piece at a time,
# DRC-check each piece, keep good pieces, retry only the failed piece.
import math, sys, time

sys.path.insert(0, r"D:\001DIY\005lib\01AIcadence\routing")
import autoroute3d as ar

L8 = 2                  # layer index of ETCH/L8 in ar.LAYER_NAMES
CHUNK = 150.0           # max length of one committed piece (mils)
MAX_REPLANS = 12

PIECE_TMPL = """; incremental piece for {net}
procedure( AIB_countDrc()
    let( (n)
        axlClearSelSet()
        axlSetFindFilter(?enabled list("noall" "drcs") ?onButtons list("noall" "drcs"))
        axlAddSelectAll()
        n = length(axlGetSelSet())
        axlClearSelSet()
        n
    )
)
AIB_drc0 = AIB_countDrc()
AIB_pp = axlPathStart(list(list({x1:.3f} {y1:.3f})) 4.5)
AIB_pp = axlPathLine(AIB_pp 4.5 list({x2:.3f} {y2:.3f}))
AIB_ret = errset(axlDBCreatePath(AIB_pp "ETCH/L8") nil)
AIB_obj = nil
when( AIB_ret && car(AIB_ret) AIB_obj = caar(car(AIB_ret)) )
if( !AIB_obj then
    printf("PIECE CREATE-FAILED err=%L\\n" errset.errset)
else
    axlShell("drc update")
    AIB_drc1 = AIB_countDrc()
    AIB_netName = if( AIB_obj->net then AIB_obj->net->name else "NONET" )
    printf("PIECE drc0=%d drc1=%d net=%s\\n" AIB_drc0 AIB_drc1 AIB_netName)
    if( AIB_drc1 > AIB_drc0 then
        axlClearSelSet()
        axlSetFindFilter(?enabled list("noall" "drcs") ?onButtons list("noall" "drcs"))
        axlAddSelectAll()
        foreach(m axlGetSelSet()
            printf("D|%f|%f\\n"
                ((xCoord car(m->bBox)) + (xCoord cadr(m->bBox))) / 2.0
                ((yCoord car(m->bBox)) + (yCoord cadr(m->bBox))) / 2.0)
        )
        axlClearSelSet()
        errset(axlDeleteObject(AIB_obj) nil)
        axlShell("drc update")
        printf("PIECE REJECTED\\n")
    else
        printf("PIECE OK\\n")
    )
)
printf("done\\n")
"""

def chop(pts):
    """split polyline into pieces no longer than CHUNK"""
    pieces = []
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i+1]
        d = math.hypot(x2-x1, y2-y1)
        n = max(int(math.ceil(d / CHUNK)), 1)
        for k in range(n):
            a = (x1 + (x2-x1)*k/n,     y1 + (y2-y1)*k/n)
            b = (x1 + (x2-x1)*(k+1)/n, y1 + (y2-y1)*(k+1)/n)
            pieces.append((a, b))
    return pieces

def plan_l8(net, start, end, extra):
    """single-layer A* on L8 only (via grid fully blocked -> no layer changes)"""
    grids = ar.build_grids(net, extra)
    g8 = grids[2]
    p3 = ar.astar3d((g8,), bytearray(b"\x01") * ar.NPL, start, end)
    if not p3:
        return None
    pts = [(float(x), float(y)) for x, y, _ in p3]
    out = [pts[0]]
    i = 0
    while i < len(pts)-1:
        j = len(pts)-1
        while j > i+1:
            if ar.seg_clear(g8, out[-1][0], out[-1][1], pts[j][0], pts[j][1]):
                break
            j -= 1
        out.append(pts[j])
        i = j
    return out

def route_incremental(net, start, end):
    extra = []
    committed = start
    replans = 0
    while replans < MAX_REPLANS:
        pts = plan_l8(net, committed, end, extra)
        if not pts:
            print(f"[{net}] NO PATH from {committed} (extra={len(extra)})")
            return False
        pieces = chop(pts)
        print(f"[{net}] plan from {committed}: {len(pieces)} pieces")
        ok_all = True
        for (a, b) in pieces:
            out = ar.allegro(PIECE_TMPL.format(net=net, x1=a[0], y1=a[1], x2=b[0], y2=b[1]))
            if "PIECE OK" in out:
                committed = b
                ar.segsL8.append((net, a, b, 4.5))
                continue
            # rejected or failed: mark obstacles, replan from last good point
            markers = [ln for ln in out.splitlines() if ln.startswith("D|")]
            for ln in markers:
                _, mx, my = ln.split("|")
                extra.append((float(mx), float(my), 12.0))
            print(f"[{net}] piece {a}->{b} rejected ({len(markers)} markers), replanning")
            replans += 1
            ok_all = False
            break
        if ok_all:
            print(f"[{net}] COMPLETE at {committed}")
            return True
    print(f"[{net}] gave up after {MAX_REPLANS} replans")
    return False

if __name__ == "__main__":
    print("step_router ready; call route_incremental(net, start, end)")
