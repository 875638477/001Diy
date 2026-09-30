# Negotiated routing for the last nets: rip AI routes, re-survey, retry orders
import importlib, itertools, os, shutil, sys, time

sys.path.insert(0, r"D:\001DIY\005lib\01AIcadence\routing")
import autoroute3d as ar

FULL = r"D:\001DIY\005lib\01AIcadence\routing\full_region.txt"
EXCH = ar.EXCH

# original (user-made) vias per net -- never delete these
ORIG_VIAS = {
    "UART4_TX_M1/1V8": [(-664.441, -747.441), (-224.113, -271.95)],
    "UART4_RX_M1/1V8": [(-628.306, -745.306), (-287.0, -297.0)],
    "WIFI_BT_RSTN/1V8": [(-172.602, -814.631), (-224.113, -248.327)],
}
ENDPOINTS = {
    "UART4_RX_M1/1V8": ((-287.0, -297.0), (-628.306, -745.306)),
    "UART4_TX_M1/1V8": ((-224.113, -271.95), (-664.441, -747.441)),
    "WIFI_BT_RSTN/1V8": ((-224.113, -248.327), (-172.602, -814.631)),
}

RIP_TMPL = """; rip AI-routed objects of {net} (keep escapes + original vias)
axlClearSelSet()
axlSetFindFilter(?enabled list("noall" "clines" "vias") ?onButtons list("noall" "clines" "vias"))
axlAddSelectAll()
AIB_del = nil
foreach(o axlGetSelSet()
    when( o->net && o->net->name == "{net}"
        cond(
            (o->objType == "path"
                let( (bb w h)
                    bb = o->bBox
                    w = (xCoord cadr(bb)) - (xCoord car(bb))
                    h = (yCoord cadr(bb)) - (yCoord car(bb))
                    when( w + h > 50.0
                        AIB_del = cons(o AIB_del)
                    )
                ))
            (o->objType == "via"
                let( (x y keep)
                    x = xCoord(o->xy)
                    y = yCoord(o->xy)
                    keep = nil
{keeps}
                    when( !keep
                        AIB_del = cons(o AIB_del)
                    )
                ))
        )
    )
)
axlClearSelSet()
printf("RIP {net}: deleting %d objs\\n" length(AIB_del))
when( AIB_del errset(axlDeleteObject(AIB_del) nil) )
axlShell("drc update")
printf("done\\n")
"""

def rip(net):
    keeps = ""
    for x, y in ORIG_VIAS[net]:
        keeps += (f'                    when( abs(x - ({x:.3f})) < 1.0 && '
                  f'abs(y - ({y:.3f})) < 1.0 keep = t )\n')
    out = ar.allegro(RIP_TMPL.format(net=net, keeps=keeps))
    for ln in out.splitlines():
        if ln.startswith("RIP"):
            print(ln)

SURVEY = open(r"D:\001DIY\005lib\01AIcadence\routing\survey_full.il", encoding="ascii").read()

def survey():
    ar.allegro(SURVEY)
    shutil.copy(os.path.join(EXCH, "result.txt"), FULL)
    importlib.reload(ar)
    print("survey refreshed:", sum(1 for _ in open(FULL)))

def try_order(order):
    results = {}
    for net in order:
        s, e = ENDPOINTS[net]
        results[net] = ar.route_net(net, s, e, max_tries=4)
    return results

if __name__ == "__main__":
    orders = [
        ["UART4_RX_M1/1V8", "WIFI_BT_RSTN/1V8", "UART4_TX_M1/1V8"],
        ["WIFI_BT_RSTN/1V8", "UART4_RX_M1/1V8", "UART4_TX_M1/1V8"],
        ["UART4_TX_M1/1V8", "UART4_RX_M1/1V8", "WIFI_BT_RSTN/1V8"],
    ]
    for i, order in enumerate(orders):
        print(f"=== ROUND {i+1}: rip all 3, re-survey, order: {order} ===")
        for net in ORIG_VIAS:
            rip(net)
        survey()
        results = try_order(order)
        print("round result:", results)
        if all(results.values()):
            print("ALL ROUTED")
            break
    print(ar.allegro('axlShell("rats all")\nprintf("rats refreshed\\n")\n'))
