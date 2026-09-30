# 3D (TOP+BOTTOM) closed-loop autorouter with via jumps and DRC verdict
import heapq, math, os, time

EXCH = r"D:\001DIY\005lib\01AIcadence\ai_bridge\exchange"
REGION = r"D:\001DIY\005lib\01AIcadence\routing\full_region.txt"
XMIN, XMAX = -1000, 800
YMIN, YMAX = -835, -100
W = XMAX - XMIN + 1
H = YMAX - YMIN + 1
NPL = W * H
LINE_HALF = 2.25
CLEARANCE = 3.0
VIA_R = 7.874
VIA_COST = 40.0
BASE_DRC = None  # determined at runtime

def allegro(skill):
    rf = os.path.join(EXCH, "result.flag")
    if os.path.exists(rf):
        os.remove(rf)
    with open(os.path.join(EXCH, "command.il"), "w", encoding="ascii") as f:
        f.write(skill)
    with open(os.path.join(EXCH, "command.flag"), "w") as f:
        f.write("go")
    for _ in range(1800):
        time.sleep(0.1)
        if os.path.exists(rf):
            break
    else:
        raise RuntimeError("allegro timeout")
    time.sleep(0.2)
    with open(os.path.join(EXCH, "result.txt"), encoding="ascii", errors="replace") as f:
        return f.read()

# ---------- parse survey (single visibility-independent dump) ----------
L8_SHAPES_AS_WALLS = True
vias, pinsT, pinsB, pinsA, segsT, segsB = [], [], [], [], [], []
segsL3, wallsL3, segsL8, wallsL8 = [], [], [], []
for line in open(REGION, encoding="ascii", errors="replace"):
    f = line.strip().split("|")
    tag = f[0]
    if tag == "V":
        vias.append((f[1], float(f[2]), float(f[3]), float(f[4])))
    elif tag == "PA":
        pinsA.append((f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5])))
    elif tag == "PT":
        pinsT.append((f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5])))
    elif tag == "PB":
        pinsB.append((f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5])))
    elif tag in ("ST", "SB", "S3", "S8"):
        seg = (f[1], (float(f[2]), float(f[3])), (float(f[4]), float(f[5])), float(f[6]))
        {"ST": segsT, "SB": segsB, "S3": segsL3, "S8": segsL8}[tag].append(seg)
    elif tag in ("B3", "B8"):
        wall = (f[1], (float(f[2]), float(f[3])), (float(f[4]), float(f[5])), 0.0)
        {"B3": wallsL3, "B8": wallsL8}[tag].append(wall)

def mark_disk(grid, cx, cy, r):
    x0 = max(int(math.floor(cx - r)), XMIN)
    x1 = min(int(math.ceil(cx + r)), XMAX)
    y0 = max(int(math.floor(cy - r)), YMIN)
    y1 = min(int(math.ceil(cy + r)), YMAX)
    r2 = r * r
    for gy in range(y0, y1 + 1):
        dy2 = (gy - cy) ** 2
        base = (gy - YMIN) * W
        for gx in range(x0, x1 + 1):
            if (gx - cx) ** 2 + dy2 <= r2:
                grid[base + gx - XMIN] = 1

def mark_rect(grid, x0, y0, x1, y1, m):
    gx0 = max(int(math.floor(x0 - m)), XMIN)
    gx1 = min(int(math.ceil(x1 + m)), XMAX)
    gy0 = max(int(math.floor(y0 - m)), YMIN)
    gy1 = min(int(math.ceil(y1 + m)), YMAX)
    for gy in range(gy0, gy1 + 1):
        base = (gy - YMIN) * W
        for gx in range(gx0, gx1 + 1):
            grid[base + gx - XMIN] = 1

def mark_capsule(grid, a, b, r):
    d = math.hypot(b[0]-a[0], b[1]-a[1])
    steps = max(int(d / max(r * 0.7, 1.0)), 1)
    for i in range(steps + 1):
        mark_disk(grid, a[0] + (b[0]-a[0]) * i / steps,
                  a[1] + (b[1]-a[1]) * i / steps, r)

def build_grids(net, extra_disks):
    gT = bytearray(NPL)
    gL = bytearray(NPL)   # L3
    g8 = bytearray(NPL)   # L8
    gB = bytearray(NPL)
    gV = bytearray(NPL)   # 1 = via NOT allowed
    infl = CLEARANCE + LINE_HALF
    vinfl = CLEARANCE + VIA_R
    for n, x, y, r in vias:
        if n != net:
            mark_disk(gT, x, y, r + infl)
            mark_disk(gL, x, y, r + infl)
            mark_disk(g8, x, y, r + infl)
            mark_disk(gB, x, y, r + infl)
            mark_disk(gV, x, y, r + vinfl)
    for n, x0, y0, x1, y1 in pinsA:
        if n != net:
            mark_rect(gT, x0, y0, x1, y1, infl)
            mark_rect(gL, x0, y0, x1, y1, infl)
            mark_rect(g8, x0, y0, x1, y1, infl)
            mark_rect(gB, x0, y0, x1, y1, infl)
            mark_rect(gV, x0, y0, x1, y1, vinfl)
    for n, x0, y0, x1, y1 in pinsT:
        if n != net:
            mark_rect(gT, x0, y0, x1, y1, infl)
            mark_rect(gV, x0, y0, x1, y1, vinfl)
    for n, x0, y0, x1, y1 in pinsB:
        if n != net:
            mark_rect(gB, x0, y0, x1, y1, infl)
            mark_rect(gV, x0, y0, x1, y1, vinfl)
    for n, a, b, w in segsT:
        if n != net:
            mark_capsule(gT, a, b, w/2 + infl)
            mark_capsule(gV, a, b, w/2 + vinfl)
    for n, a, b, w in segsB:
        if n != net:
            mark_capsule(gB, a, b, w/2 + infl)
            mark_capsule(gV, a, b, w/2 + vinfl)
    for n, a, b, w in segsL3:
        if n != net:
            mark_capsule(gL, a, b, w/2 + infl)
            mark_capsule(gV, a, b, w/2 + vinfl)
    for n, a, b, w in wallsL3:
        # plane boundary: wall on L3 routing and via placement
        mark_capsule(gL, a, b, infl)
        mark_capsule(gV, a, b, vinfl)
    for n, a, b, w in segsL8:
        if n != net:
            mark_capsule(g8, a, b, w/2 + infl)
            mark_capsule(gV, a, b, w/2 + vinfl)
    if L8_SHAPES_AS_WALLS:
        for n, a, b, w in wallsL8:
            mark_capsule(g8, a, b, infl)
    for cx, cy, r in extra_disks:
        mark_disk(gT, cx, cy, r)
        mark_disk(gL, cx, cy, r)
        mark_disk(g8, cx, cy, r)
        mark_disk(gB, cx, cy, r)
        mark_disk(gV, cx, cy, r)
    return gT, gL, g8, gB, gV

def idx(x, y):
    return (y - YMIN) * W + (x - XMIN)

def inb(x, y):
    return XMIN <= x <= XMAX and YMIN <= y <= YMAX

def astar3d(grids, gV, start, goal):
    nlay = len(grids)
    s = (round(start[0]), round(start[1]))
    g = (round(goal[0]), round(goal[1]))
    moves = [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),
             (1,1,1.4142),(1,-1,1.4142),(-1,1,1.4142),(-1,-1,1.4142)]
    gsc = {}
    came = {}
    openq = []
    for L in range(nlay):
        if grids[L][idx(*s)] == 0:
            st = (s[0], s[1], L)
            gsc[st] = 0.0
            heapq.heappush(openq, (0.0, st))
    while openq:
        _, cur = heapq.heappop(openq)
        x, y, L = cur
        if abs(x-g[0]) <= 1 and abs(y-g[1]) <= 1:
            path = [(g[0], g[1], L), cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)
            return path[::-1]
        for dx, dy, c in moves:
            nx, ny = x+dx, y+dy
            if not inb(nx, ny) or grids[L][idx(nx, ny)]:
                continue
            nst = (nx, ny, L)
            ng = gsc[cur] + c
            if ng < gsc.get(nst, 1e18):
                gsc[nst] = ng
                came[nst] = cur
                heapq.heappush(openq, (ng + math.hypot(g[0]-nx, g[1]-ny), nst))
        # layer change via through-hole via (clear spot required on all layers)
        if gV[idx(x, y)] == 0:
            for oL in range(nlay):
                if oL == L or grids[oL][idx(x, y)]:
                    continue
                nst = (x, y, oL)
                ng = gsc[cur] + VIA_COST
                if ng < gsc.get(nst, 1e18):
                    gsc[nst] = ng
                    came[nst] = cur
                    heapq.heappush(openq, (ng + math.hypot(g[0]-x, g[1]-y), nst))
    return None

def seg_clear(grid, x1, y1, x2, y2):
    d = math.hypot(x2-x1, y2-y1)
    n = max(int(d / 0.5), 1)
    for i in range(n + 1):
        x = round(x1 + (x2-x1)*i/n)
        y = round(y1 + (y2-y1)*i/n)
        if not inb(x, y) or grid[idx(x, y)]:
            return False
    return True

def simplify_run(grid, pts):
    out = [pts[0]]
    i = 0
    while i < len(pts)-1:
        j = len(pts)-1
        while j > i+1:
            if seg_clear(grid, out[-1][0], out[-1][1], pts[j][0], pts[j][1]):
                break
            j -= 1
        out.append(pts[j])
        i = j
    return out

LAYER_NAMES = ("ETCH/TOP", "ETCH/L3", "ETCH/L8", "ETCH/BOTTOM")

def plan(net, start, end, extra):
    gT, gL, g8, gB, gV = build_grids(net, extra)
    grids = (gT, gL, g8, gB)
    p3 = astar3d(grids, gV, start, end)
    if not p3:
        return None
    # split into per-layer runs; record via locations at layer changes
    runs = []  # (layer, [pts])
    cur_layer = p3[0][2]
    cur_pts = [(float(p3[0][0]), float(p3[0][1]))]
    via_pts = []
    for q in p3[1:]:
        if q[2] != cur_layer:
            via_pts.append((float(q[0]), float(q[1])))
            runs.append((cur_layer, cur_pts))
            cur_layer = q[2]
            cur_pts = [(float(q[0]), float(q[1]))]
        else:
            cur_pts.append((float(q[0]), float(q[1])))
    runs.append((cur_layer, cur_pts))
    # endpoints exact
    runs[0] = (runs[0][0], [start] + runs[0][1][1:])
    runs[-1] = (runs[-1][0], runs[-1][1][:-1] + [end])
    out_runs = []
    for L, pts in runs:
        grid = grids[L]
        if len(pts) >= 2:
            out_runs.append((L, simplify_run(grid, pts)))
    return out_runs, via_pts

SKILL_HEAD = """; 3d attempt for {net}
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
AIB_net = nil
foreach(x axlDBGetDesign()->nets
    when( x->name == "{net}" AIB_net = x )
)
AIB_drc0 = AIB_countDrc()
AIB_objs = nil
AIB_fail = nil
"""

SKILL_TAIL = """
axlShell("drc update")
AIB_drc1 = AIB_countDrc()
printf("DRC0=%d DRC1=%d fail=%L\\n" AIB_drc0 AIB_drc1 AIB_fail)
if( AIB_fail || AIB_drc1 > AIB_drc0 then
    axlClearSelSet()
    axlSetFindFilter(?enabled list("noall" "drcs") ?onButtons list("noall" "drcs"))
    axlAddSelectAll()
    foreach(m axlGetSelSet()
        printf("D|%f|%f\\n"
            ((xCoord car(m->bBox)) + (xCoord cadr(m->bBox))) / 2.0
            ((yCoord car(m->bBox)) + (yCoord cadr(m->bBox))) / 2.0)
    )
    axlClearSelSet()
    foreach(o AIB_objs errset(axlDeleteObject(o) nil))
    axlShell("drc update")
    printf("VERDICT REJECTED\\n")
else
    printf("VERDICT ACCEPTED\\n")
)
printf("done\\n")
"""

def make_skill(net, runs, via_pts):
    parts = [SKILL_HEAD.format(net=net)]
    for x, y in via_pts:
        parts.append(
            f'AIB_v = errset(axlDBCreateVia("0402" list({x:.3f} {y:.3f}) AIB_net) nil)\n'
            f'printf("VIA ret=%L err=%L\\n" AIB_v errset.errset)\n'
            f'if( AIB_v && car(AIB_v) && caar(AIB_v) then\n'
            f'    AIB_objs = cons(caar(AIB_v) AIB_objs)\n'
            f'else\n'
            f'    AIB_fail = t\n'
            f')\n')
    for L, pts in runs:
        layer = LAYER_NAMES[L]
        parts.append(f'AIB_pp = axlPathStart(list(list({pts[0][0]:.3f} {pts[0][1]:.3f})) 4.5)\n')
        for x, y in pts[1:]:
            parts.append(f'AIB_pp = axlPathLine(AIB_pp 4.5 list({x:.3f} {y:.3f}))\n')
        parts.append(
            f'AIB_ret = errset(axlDBCreatePath(AIB_pp "{layer}") nil)\n'
            f'if( AIB_ret && caar(AIB_ret) then\n'
            f'    printf("PATH {layer} nSegs=%L net=%L\\n" caar(car(AIB_ret))->nSegs caar(car(AIB_ret))->net->name)\n'
            f'    AIB_objs = cons(caar(car(AIB_ret)) AIB_objs)\n'
            f'else\n'
            f'    printf("PATH {layer} FAILED err=%L\\n" errset.errset)\n'
            f'    AIB_fail = t\n'
            f')\n')
    parts.append(SKILL_TAIL)
    return "".join(parts)

def route_net(net, start, end, max_tries=6):
    extra = []
    for attempt in range(1, max_tries + 1):
        t0 = time.time()
        planned = plan(net, start, end, extra)
        if not planned:
            print(f"[{net}] attempt {attempt}: NO PATH (extra={len(extra)})")
            return False
        runs, via_pts = planned
        nseg = sum(len(p)-1 for _, p in runs)
        print(f"[{net}] attempt {attempt}: {len(runs)} runs, {len(via_pts)} new vias, "
              f"{nseg} segs (plan {time.time()-t0:.0f}s)")
        out = allegro(make_skill(net, runs, via_pts))
        if "VERDICT ACCEPTED" in out:
            print(f"[{net}] ACCEPTED on attempt {attempt}")
            for L, pts in runs:
                tgt = (segsT, segsL3, segsL8, segsB)[L]
                for i in range(len(pts)-1):
                    tgt.append((net, pts[i], pts[i+1], 4.5))
            for x, y in via_pts:
                vias.append((net, x, y, VIA_R))
            return True
        markers = []
        for ln in out.splitlines():
            if ln.startswith("D|"):
                _, mx, my = ln.split("|")
                markers.append((float(mx), float(my), 15.0))
        keylines = [l for l in out.splitlines()
                    if l.startswith(("VIA ", "PATH ", "DRC0", "VERDICT"))]
        print(f"[{net}] rejected: {len(markers)} markers; " + " // ".join(keylines[:6]))
        if not markers:
            return False
        extra.extend(markers)
    print(f"[{net}] gave up after {max_tries} tries")
    return False

def register_committed(net, runs_layers):
    """add already-committed routes (from previous session) as obstacles"""
    for L, pts, w in runs_layers:
        tgt = (segsT, segsL3, segsL8, segsB)[L]
        for i in range(len(pts)-1):
            tgt.append((net, pts[i], pts[i+1], w))

if __name__ == "__main__":
    results = {}
    results["UART4_RX"] = route_net("UART4_RX_M1/1V8", (-287.0, -297.0), (-628.306, -745.306))
    results["WIFI_RST"] = route_net("WIFI_BT_RSTN/1V8", (-224.113, -248.327), (-172.602, -814.631))
    results["UART2_TX"] = route_net("UART2_TX_M1/3V3", (200.787, -271.654), (-914.0, -183.0))
    print("SUMMARY:", results)
    print(allegro('axlShell("rats all")\nprintf("rats refreshed\\n")\n'))

