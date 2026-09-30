# A* router for UART4_RX and UART4_TX on ETCH/BOTTOM (units: mils)
import heapq, math

REGION = "D:/001DIY/005lib/01AIcadence/routing/uart4_region.txt"
XMIN, XMAX = -704.0, -184.0
YMIN, YMAX = -787.0, -232.0
LINE_HALF = 2.25
CLEARANCE = 6.0

# already-routed WIFI_BT_RSTN bottom trace (manually added obstacle, w=4.5)
WIFI_SEGS = []
_wifi_pts = [(-224.113,-248.327),(-193,-257),(-187,-262),(-184,-270),(-187,-298),
             (-225,-336),(-245,-363),(-247,-372),(-232,-406),(-231,-436),
             (-240,-557),(-243,-696),(-207,-770),(-172.602,-814.631)]
for i in range(len(_wifi_pts)-1):
    WIFI_SEGS.append((_wifi_pts[i], _wifi_pts[i+1], 4.5, "WIFI_BT_RSTN/1V8"))

vias, pins, segs = [], [], list(WIFI_SEGS)
for line in open(REGION, encoding="ascii", errors="replace"):
    f = line.strip().split("|")
    if f[0] == "V":
        vias.append((f[1], float(f[2]), float(f[3]), float(f[4])))
    elif f[0] == "P":
        pins.append((f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5])))
    elif f[0] == "S":
        segs.append(((float(f[2]), float(f[3])), (float(f[4]), float(f[5])), float(f[6]), f[1]))

def pt_seg_dist2(px, py, a, b):
    ax, ay = a; bx, by = b
    dx, dy = bx-ax, by-ay
    L2 = dx*dx + dy*dy
    if L2 == 0:
        return (px-ax)**2 + (py-ay)**2
    t = max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy) / L2))
    cx, cy = ax + t*dx, ay + t*dy
    return (px-cx)**2 + (py-cy)**2

def make_blocked(net, extra_segs):
    """return blocked(x,y) for routing given net; same-net obstacles excluded"""
    vs = [(x, y, r) for n, x, y, r in vias if n != net]
    ps = [(x1, y1, x2, y2) for n, x1, y1, x2, y2 in pins if n != net]
    ss = [(a, b, w) for a, b, w, n in segs + extra_segs if n != net]
    def blocked(x, y):
        for vx, vy, r in vs:
            need = r + CLEARANCE + LINE_HALF
            if (x-vx)**2 + (y-vy)**2 < need*need:
                return True
        m = CLEARANCE + LINE_HALF
        for x1, y1, x2, y2 in ps:
            if x1-m <= x <= x2+m and y1-m <= y <= y2+m:
                return True
        for a, b, w in ss:
            need = w/2 + CLEARANCE + LINE_HALF
            if pt_seg_dist2(x, y, a, b) < need*need:
                return True
        return False
    return blocked

def seg_clear(blocked, x1, y1, x2, y2):
    d = math.hypot(x2-x1, y2-y1)
    n = max(int(d/0.5), 1)
    for i in range(n+1):
        x = x1 + (x2-x1)*i/n
        y = y1 + (y2-y1)*i/n
        if blocked(x, y) or not (XMIN <= x <= XMAX and YMIN <= y <= YMAX):
            return False
    return True

def astar(blocked, start, goal):
    s = (round(start[0]), round(start[1]))
    g = (round(goal[0]), round(goal[1]))
    moves = [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),
             (1,1,1.4142),(1,-1,1.4142),(-1,1,1.4142),(-1,-1,1.4142)]
    openq = [(0, s)]
    gsc = {s: 0}
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
            if not (XMIN <= nx <= XMAX and YMIN <= ny <= YMAX):
                continue
            if blocked(nx, ny):
                continue
            ng = gsc[cur] + c
            if ng < gsc.get((nx, ny), 1e18):
                gsc[(nx, ny)] = ng
                came[(nx, ny)] = cur
                heapq.heappush(openq, (ng + math.hypot(g[0]-nx, g[1]-ny), (nx, ny)))
    return None

def simplify(blocked, path, start, end):
    pts = [start] + [(float(x), float(y)) for x, y in path[1:-1]] + [end]
    out = [pts[0]]
    i = 0
    while i < len(pts)-1:
        j = len(pts)-1
        while j > i+1:
            if seg_clear(blocked, pts[i][0], pts[i][1], pts[j][0], pts[j][1]):
                break
            j -= 1
        out.append(pts[j])
        i = j
    return out

def route(net, start, end, extra_segs):
    blocked = make_blocked(net, extra_segs)
    p = astar(blocked, start, end)
    if not p:
        print(f"{net}: NO PATH")
        return None
    pts = simplify(blocked, p, start, end)
    ok = all(seg_clear(blocked, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])
             for i in range(len(pts)-1))
    print(f"{net}: {len(pts)} vertices, check={'CLEAR' if ok else 'VIOLATION'}")
    for x, y in pts:
        print(f"    list({x:.3f} {y:.3f})")
    return pts

rx = route("UART4_RX_M1/1V8", (-287.0, -297.0), (-628.306, -745.306), [])
extra = []
if rx:
    for i in range(len(rx)-1):
        extra.append((rx[i], rx[i+1], 4.5, "UART4_RX_M1/1V8"))
tx = route("UART4_TX_M1/1V8", (-224.113, -271.95), (-664.441, -747.441), extra)
