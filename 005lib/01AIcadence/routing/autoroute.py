# Closed-loop autorouter: A* candidate -> place in Allegro -> DRC verdict -> retry
import heapq, math, os, time

EXCH = r"D:\001DIY\005lib\01AIcadence\ai_bridge\exchange"
REGION = r"D:\001DIY\005lib\01AIcadence\routing\big_region5.txt"
LAYER = "ETCH/BOTTOM"
XMIN, XMAX = -1000, 800
YMIN, YMAX = -835, -100
W = XMAX - XMIN + 1
H = YMAX - YMIN + 1
LINE_HALF = 2.25
CLEARANCE = 4.0

# ---------- allegro bridge ----------
def allegro(skill):
    rf = os.path.join(EXCH, "result.flag")
    if os.path.exists(rf):
        os.remove(rf)
    with open(os.path.join(EXCH, "command.il"), "w", encoding="ascii") as f:
        f.write(skill)
    with open(os.path.join(EXCH, "command.flag"), "w") as f:
        f.write("go")
    for _ in range(120):
        time.sleep(1)
        if os.path.exists(rf):
            break
    else:
        raise RuntimeError("allegro timeout")
    time.sleep(0.3)
    with open(os.path.join(EXCH, "result.txt"), encoding="ascii", errors="replace") as f:
        return f.read()

# ---------- obstacle model ----------
vias, pins, segs, walls = [], [], [], []
for line in open(REGION, encoding="ascii", errors="replace"):
    f = line.strip().split("|")
    if f[0] == "V":
        vias.append((f[1], float(f[2]), float(f[3]), float(f[4])))
    elif f[0] == "P":
        pins.append((f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5])))
    elif f[0] == "S":
        segs.append((f[1], (float(f[2]), float(f[3])), (float(f[4]), float(f[5])), float(f[6])))

def build_grid(net, extra_disks):
    grid = bytearray(W * H)
    def mark_disk(cx, cy, r):
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
    def mark_rect(x0, y0, x1, y1, m):
        gx0 = max(int(math.floor(x0 - m)), XMIN)
        gx1 = min(int(math.ceil(x1 + m)), XMAX)
        gy0 = max(int(math.floor(y0 - m)), YMIN)
        gy1 = min(int(math.ceil(y1 + m)), YMAX)
        for gy in range(gy0, gy1 + 1):
            base = (gy - YMIN) * W
            for gx in range(gx0, gx1 + 1):
                grid[base + gx - XMIN] = 1
    for n, x, y, r in vias:
        if n != net:
            mark_disk(x, y, r + CLEARANCE + LINE_HALF)
    for n, x0, y0, x1, y1 in pins:
        if n != net:
            mark_rect(x0, y0, x1, y1, CLEARANCE + LINE_HALF)
    for n, a, b, w in segs + walls:
        if n != net:
            r = w / 2 + CLEARANCE + LINE_HALF
            d = math.hypot(b[0]-a[0], b[1]-a[1])
            steps = max(int(d / max(r * 0.7, 1.0)), 1)
            for i in range(steps + 1):
                mark_disk(a[0] + (b[0]-a[0]) * i / steps,
                          a[1] + (b[1]-a[1]) * i / steps, r)
    for cx, cy, r in extra_disks:
        mark_disk(cx, cy, r)
    return grid

def free(grid, x, y):
    if not (XMIN <= x <= XMAX and YMIN <= y <= YMAX):
        return False
    return grid[(int(y) - YMIN) * W + int(x) - XMIN] == 0

def seg_clear(grid, x1, y1, x2, y2):
    d = math.hypot(x2-x1, y2-y1)
    n = max(int(d / 0.5), 1)
    for i in range(n + 1):
        if not free(grid, round(x1 + (x2-x1)*i/n), round(y1 + (y2-y1)*i/n)):
            return False
    return True

def astar(grid, start, goal):
    s = (round(start[0]), round(start[1]))
    g = (round(goal[0]), round(goal[1]))
    moves = [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),
             (1,1,1.4142),(1,-1,1.4142),(-1,1,1.4142),(-1,-1,1.4142)]
    openq = [(0.0, s)]
    gsc = {s: 0.0}
    came = {}
    while openq:
        _, cur = heapq.heappop(openq)
        if abs(cur[0]-g[0]) <= 1 and abs(cur[1]-g[1]) <= 1:
            path = [g, cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)
            return path[::-1]
        for dx, dy, c in moves:
            nx, ny = cur[0]+dx, cur[1]+dy
            if not free(grid, nx, ny):
                continue
            ng = gsc[cur] + c
            if ng < gsc.get((nx, ny), 1e18):
                gsc[(nx, ny)] = ng
                came[(nx, ny)] = cur
                heapq.heappush(openq, (ng + math.hypot(g[0]-nx, g[1]-ny), (nx, ny)))
    return None

def simplify(grid, path, start, end):
    pts = [start] + [(float(x), float(y)) for x, y in path[1:-1]] + [end]
    out = [pts[0]]
    i = 0
    while i < len(pts)-1:
        j = len(pts)-1
        while j > i+1:
            if seg_clear(grid, pts[i][0], pts[i][1], pts[j][0], pts[j][1]):
                break
            j -= 1
        out.append(pts[j])
        i = j
    return out

# ---------- skill generation ----------
SKILL_TEMPLATE = """; auto attempt for {net}
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
AIB_pp = axlPathStart(list({p0}) 4.5)
{lines}
AIB_ret = axlDBCreatePath(AIB_pp "{layer}")
AIB_obj = caar(AIB_ret)
printf("CREATED net=%L nSegs=%L\\n" AIB_obj->net->name AIB_obj->nSegs)
axlShell("drc update")
AIB_drc1 = AIB_countDrc()
printf("DRC0=%d DRC1=%d\\n" AIB_drc0 AIB_drc1)
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
    axlDeleteObject(AIB_obj)
    axlShell("drc update")
    printf("VERDICT REJECTED\\n")
else
    printf("VERDICT ACCEPTED\\n")
)
printf("done\\n")
"""

def make_skill(net, pts):
    p0 = f"list({pts[0][0]:.3f} {pts[0][1]:.3f})"
    lines = "\n".join(
        f"AIB_pp = axlPathLine(AIB_pp 4.5 list({x:.3f} {y:.3f}))" for x, y in pts[1:])
    return SKILL_TEMPLATE.format(net=net, p0=p0, lines=lines, layer=LAYER)

# ---------- main loop ----------
def route_net(net, start, end, max_tries=8):
    extra = []
    for attempt in range(1, max_tries + 1):
        grid = build_grid(net, extra)
        p = astar(grid, start, end)
        if not p:
            print(f"[{net}] attempt {attempt}: NO PATH (extra={len(extra)})")
            return False
        pts = simplify(grid, p, start, end)
        print(f"[{net}] attempt {attempt}: candidate {len(pts)} vts, sending to Allegro...")
        out = allegro(make_skill(net, pts))
        if "VERDICT ACCEPTED" in out:
            print(f"[{net}] ACCEPTED on attempt {attempt}")
            for i in range(len(pts)-1):
                segs.append((net, pts[i], pts[i+1], 4.5))
            return True
        markers = []
        for ln in out.splitlines():
            if ln.startswith("D|"):
                _, mx, my = ln.split("|")
                markers.append((float(mx), float(my), 20.0))
        if not markers:
            print(f"[{net}] rejected but no markers?! output:\n{out}")
            return False
        print(f"[{net}] rejected, {len(markers)} violation markers added")
        extra.extend(markers)
    print(f"[{net}] gave up after {max_tries} tries")
    return False

if __name__ == "__main__":
    ok1 = route_net("UART4_RX_M1/1V8", (-287.0, -297.0), (-628.306, -745.306))
    ok2 = route_net("UART4_TX_M1/1V8", (-224.113, -271.95), (-664.441, -747.441))
    ok3 = route_net("WIFI_BT_RSTN/1V8", (-224.113, -248.327), (-172.602, -814.631))
    print("summary:", ok1, ok2, ok3)
    out = allegro('axlShell("rats all")\nprintf("done\\n")\n')
    print(out)

