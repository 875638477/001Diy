# Rasterized A* router for UART2_RX / UART2_TX on ETCH/BOTTOM (units: mils)
import heapq, math

REGION = "D:/001DIY/005lib/01AIcadence/routing/big_region3.txt"
XMIN, XMAX = -1000, 300
YMIN, YMAX = -835, -100
W = XMAX - XMIN + 1
H = YMAX - YMIN + 1
LINE_HALF = 2.25
CLEARANCE = 4.0

# survey big_region3 already contains all committed bottom traces (incl. UART4)
done_routes = []

vias, pins, segs = [], [], []
for line in open(REGION, encoding="ascii", errors="replace"):
    f = line.strip().split("|")
    if f[0] == "V":
        vias.append((f[1], float(f[2]), float(f[3]), float(f[4])))
    elif f[0] == "P":
        pins.append((f[1], float(f[2]), float(f[3]), float(f[4]), float(f[5])))
    elif f[0] == "S":
        segs.append((f[1], (float(f[2]), float(f[3])), (float(f[4]), float(f[5])), float(f[6])))
for net, w, pts in done_routes:
    for i in range(len(pts)-1):
        segs.append((net, pts[i], pts[i+1], w))

def build_grid(net):
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
    for n, a, b, w in segs:
        if n != net:
            r = w / 2 + CLEARANCE + LINE_HALF
            d = math.hypot(b[0]-a[0], b[1]-a[1])
            steps = max(int(d / (r * 0.8)), 1)
            for i in range(steps + 1):
                mark_disk(a[0] + (b[0]-a[0]) * i / steps,
                          a[1] + (b[1]-a[1]) * i / steps, r)
    return grid

def free(grid, x, y):
    if not (XMIN <= x <= XMAX and YMIN <= y <= YMAX):
        return False
    return grid[(int(y) - YMIN) * W + int(x) - XMIN] == 0

def seg_clear(grid, x1, y1, x2, y2):
    d = math.hypot(x2-x1, y2-y1)
    n = max(int(d / 0.5), 1)
    for i in range(n + 1):
        x = x1 + (x2-x1) * i / n
        y = y1 + (y2-y1) * i / n
        if not free(grid, round(x), round(y)):
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

def route(net, start, end, extra):
    grid = build_grid(net)
    for n, a, b, w in extra:
        pass  # extras already included via segs append below
    # unblock immediate start/end neighborhoods (own escape vias already excluded by net)
    p = astar(grid, start, end)
    if not p:
        print(f"{net}: NO PATH")
        return None
    pts = simplify(grid, p, start, end)
    ok = all(seg_clear(grid, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])
             for i in range(len(pts)-1))
    print(f"{net}: {len(pts)} vertices, check={'CLEAR' if ok else 'VIOLATION'}")
    for x, y in pts:
        print(f"    list({x:.3f} {y:.3f})")
    return pts

rx = route("UART2_RX_M1/3V3", (143.0, -315.0), (-912.366, -204.675), [])
if rx:
    for i in range(len(rx)-1):
        segs.append(("UART2_RX_M1/3V3", rx[i], rx[i+1], 4.5))
tx = route("UART2_TX_M1/3V3", (200.787, -271.654), (-914.0, -183.0), [])
if tx:
    for i in range(len(tx)-1):
        segs.append(("UART2_TX_M1/3V3", tx[i], tx[i+1], 4.5))
wf = route("WIFI_BT_RSTN/1V8", (-224.113, -248.327), (-172.602, -814.631), [])

