# flood fill reachability diagnosis (2 mil grid)
from collections import deque
src = open("D:/001DIY/005lib/01AIcadence/routing/route_uart2.py").read()
src = src.split("rx = route(")[0]
ns = {}
exec(src, ns)
make_blocked = ns["make_blocked"]
XMIN, XMAX, YMIN, YMAX = ns["XMIN"], ns["XMAX"], ns["YMIN"], ns["YMAX"]

net, start, end = "UART2_RX_M1/3V3", (143.0, -315.0), (-912.366, -204.675)
blocked = make_blocked(net, [])
STEP = 2
def snap(p):
    return (round(p[0]/STEP)*STEP, round(p[1]/STEP)*STEP)
s, g = snap(start), snap(end)
seen = {s}
q = deque([s])
minx = maxx = s[0]
while q:
    x, y = q.popleft()
    for dx, dy in ((STEP,0),(-STEP,0),(0,STEP),(0,-STEP)):
        nx, ny = x+dx, y+dy
        if (nx, ny) in seen or not (XMIN <= nx <= XMAX and YMIN <= ny <= YMAX):
            continue
        if blocked(nx, ny):
            continue
        seen.add((nx, ny))
        q.append((nx, ny))
        minx = min(minx, nx)
        maxx = max(maxx, nx)
print("reachable cells:", len(seen))
print("x extent of reachable region:", minx, "..", maxx)
print("goal reached:", g in seen, " goal:", g)
