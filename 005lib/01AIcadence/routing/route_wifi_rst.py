# A* router for net WIFI_BT_RSTN/1V8 on ETCH/BOTTOM (units: mils)
# Obstacles: through vias inside surveyed corridor box (-274,-864)..(-122,-198)
import heapq, math

START = (-224.113, -248.327)
END   = (-172.602, -814.631)

# (x, y, pad_radius) from Allegro survey run #15, endpoints excluded
VIAS = [
    (-153.81, -841.91, 9.845), (-188.0, -869.68, 7.874), (-129.0, -835.0, 7.874),
    (-177.165, -248.031, 7.874), (-248.0, -410.0, 7.874), (-223.0, -546.0, 7.874),
    (-248.327, -200.491, 7.874), (-144.39, -816.32, 9.845), (-169.73, -368.203, 7.874),
    (-204.28, -372.65, 7.874), (-185.006, -389.113, 7.874), (-183.0, -415.0, 7.874),
    (-211.836, -346.526, 7.874), (-130.217, -201.083, 7.874), (-230.0, -370.0, 7.874),
    (-224.705, -224.705, 7.874), (-198.0, -580.0, 7.874), (-203.605, -529.498, 7.874),
    (-258.0, -391.0, 7.874), (-163.508, -345.0, 7.874), (-153.839, -271.95, 7.874),
    (-153.839, -224.705, 7.874), (-248.327, -271.358, 7.874), (-200.491, -271.95, 7.874),
    (-248.327, -224.705, 7.874), (-200.491, -201.083, 7.874), (-153.839, -248.327, 7.874),
    (-176.869, -224.705, 7.874), (-138.304, -441.988, 7.874), (-137.454, -466.124, 7.874),
    (-192.018, -737.982, 7.874), (-193.0, -761.0, 7.874), (-198.526, -706.474, 7.874),
    (-226.67, -691.52, 7.874), (-145.205, -783.205, 7.874), (-125.955, -631.492, 7.874),
    (-137.955, -682.492, 7.874), (-174.0, -716.0, 7.874), (-270.0, -440.0, 7.874),
    (-200.0, -819.0, 7.874), (-224.113, -271.95, 7.874), (-177.165, -200.787, 7.874),
    (-167.01, -514.26, 7.874), (-141.225, -533.375, 7.874), (-201.51, -668.3, 7.874),
    (-115.33, -438.38, 7.874), (-127.43, -418.91, 7.874), (-166.0, -440.0, 7.874),
    (-153.939, -420.061, 7.874),
]

LINE_HALF = 2.25      # 4.5 mil line width / 2
CLEARANCE = 6.0       # spacing margin
GRID = 1.0
# stay inside surveyed corridor (shrunk 10 mil)
XMIN, XMAX = -264.0, -132.0
YMIN, YMAX = -855.0, -208.0

def blocked(x, y):
    for vx, vy, r in VIAS:
        need = r + CLEARANCE + LINE_HALF
        if (x - vx) ** 2 + (y - vy) ** 2 < need * need:
            return True
    return False

def seg_clear(x1, y1, x2, y2):
    d = math.hypot(x2 - x1, y2 - y1)
    n = max(int(d / 0.5), 1)
    for i in range(n + 1):
        x = x1 + (x2 - x1) * i / n
        y = y1 + (y2 - y1) * i / n
        if blocked(x, y) or not (XMIN <= x <= XMAX and YMIN <= y <= YMAX):
            return False
    return True

def snap(p):
    return (round(p[0]), round(p[1]))

def astar(start, goal):
    s, g = snap(start), snap(goal)
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
                h = math.hypot(g[0]-nx, g[1]-ny)
                heapq.heappush(openq, (ng + h, (nx, ny)))
    return None

def simplify(path):
    # line-of-sight smoothing
    pts = [START] + [(float(x), float(y)) for x, y in path[1:-1]] + [END]
    out = [pts[0]]
    i = 0
    while i < len(pts) - 1:
        j = len(pts) - 1
        while j > i + 1:
            if seg_clear(pts[i][0], pts[i][1], pts[j][0], pts[j][1]):
                break
            j -= 1
        out.append(pts[j])
        i = j
    return out

path = astar(START, END)
if not path:
    print("NO PATH FOUND")
else:
    pts = simplify(path)
    print("vertices:", len(pts))
    for p in pts:
        print(f"  ({p[0]:.3f} {p[1]:.3f})")
    # verify each final segment
    ok = all(seg_clear(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])
             for i in range(len(pts)-1))
    print("final check:", "CLEAR" if ok else "VIOLATION")
