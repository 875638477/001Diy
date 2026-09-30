# flood fill on rasterized big-region grid
from collections import deque
src = open("D:/001DIY/005lib/01AIcadence/routing/route_uart2b.py").read()
src = src.split("rx = route(")[0]
ns = {}
exec(src, ns)
build_grid, free = ns["build_grid"], ns["free"]
XMIN, XMAX, YMIN, YMAX = ns["XMIN"], ns["XMAX"], ns["YMIN"], ns["YMAX"]

net, start, end = "UART2_RX_M1/3V3", (143, -315), (-912, -205)
grid = ns["build_grid"](net)
print("start free:", free(grid, *start), " end free:", free(grid, *end))
s = start
seen = {s}
q = deque([s])
minx = maxx = s[0]
miny = maxy = s[1]
while q:
    x, y = q.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if (nx, ny) in seen or not free(grid, nx, ny):
            continue
        seen.add((nx, ny))
        q.append((nx, ny))
        minx = min(minx, nx); maxx = max(maxx, nx)
        miny = min(miny, ny); maxy = max(maxy, ny)
print("reachable:", len(seen), "x:", minx, "..", maxx, "y:", miny, "..", maxy)

# where is the western frontier? sample boundary cells at min x band
frontier = sorted([p for p in seen if p[0] <= minx + 3])[:20]
print("western frontier cells:", frontier)
