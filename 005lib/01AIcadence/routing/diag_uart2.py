# diagnose blockage for UART2 routing region
import importlib.util, math
spec = importlib.util.spec_from_file_location("r2", "D:/001DIY/005lib/01AIcadence/routing/route_uart2.py")
# avoid running the routes on import: read file and exec only the setup part
src = open("D:/001DIY/005lib/01AIcadence/routing/route_uart2.py").read()
src = src.split("rx = route(")[0]
ns = {}
exec(src, ns)
make_blocked = ns["make_blocked"]
XMIN, XMAX, YMIN, YMAX = ns["XMIN"], ns["XMAX"], ns["YMIN"], ns["YMAX"]

for net, start, end in [
    ("UART2_RX_M1/3V3", (143.0, -315.0), (-912.366, -204.675)),
    ("UART2_TX_M1/3V3", (200.787, -271.654), (-914.0, -183.0)),
]:
    blocked = make_blocked(net, [])
    print(net, "start blocked:", blocked(*start), " end blocked:", blocked(*end))
    # column scan: count free cells per x
    chokes = []
    x = XMIN
    while x <= XMAX:
        free = 0
        y = YMIN
        while y <= YMAX:
            if not blocked(x, y):
                free += 1
            y += 2
        if free == 0:
            chokes.append(x)
        x += 10
    print("  fully blocked columns at x:", chokes if chokes else "none")
