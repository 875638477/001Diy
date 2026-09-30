# bidirectional flood fill for UART2_RX with full bottom data
from collections import deque
src = open("D:/001DIY/005lib/01AIcadence/routing/route_all3.py").read()
src = src.split("rx = route(")[0]
ns = {}
exec(src, ns)
free = ns["free"]
XMIN, XMAX, YMIN, YMAX = ns["XMIN"], ns["XMAX"], ns["YMIN"], ns["YMAX"]

def flood(grid, seed):
    seen = {seed}
    q = deque([seed])
    ext = [seed[0], seed[0], seed[1], seed[1]]
    while q:
        x, y = q.popleft()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            n = (x+dx, y+dy)
            if n in seen or not free(grid, n[0], n[1]):
                continue
            seen.add(n)
            q.append(n)
            ext[0] = min(ext[0], n[0]); ext[1] = max(ext[1], n[0])
            ext[2] = min(ext[2], n[1]); ext[3] = max(ext[3], n[1])
    return seen, ext

grid = ns["build_grid"]("UART2_RX_M1/3V3")
a, ea = flood(grid, (143, -315))
b, eb = flood(grid, (-912, -205))
print("east pocket:", len(a), "x", ea[0], "..", ea[1], "y", ea[2], "..", ea[3])
print("west pocket:", len(b), "x", eb[0], "..", eb[1], "y", eb[2], "..", eb[3])
# closest approach between pockets
best = None
bs = sorted(b)
import math
bset = b
for (x, y) in list(a)[::7]:
    for (u, v) in list(b)[::23]:
        d = (x-u)**2 + (y-v)**2
        if best is None or d < best[0]:
            best = (d, (x, y), (u, v))
print("closest approach ~:", math.sqrt(best[0]), best[1], best[2])
