"""Independent comparison of persisted Allegro readback against teaching spec.
No CAD modifications. Ring NPTH is not a bare or plated hole.
"""
import csv,json,pathlib,re,sys,hashlib,math
root=pathlib.Path(__file__).resolve().parents[1]
spec=json.loads((root/"lesson07_spec_v4.json").read_text(encoding="utf-8-sig"))
problems=[]
checks=[]
def check(ok,msg):
    checks.append({"ok":bool(ok),"check":msg})
    if not ok: problems.append(msg)
def rows(p):
    with p.open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def num(v):
    if v in ("nil","",None):return None
    return float(v)
def norm(v):return re.sub("[^a-z0-9]","",str(v).lower())
def near(a,b):return a is not None and math.isclose(float(a),float(b),abs_tol=1e-6,rel_tol=0)
def dim(kind,p):
    return p[{"REGULAR":"regular","ANTI":"anti","THERMAL":"thermal","KEEPOUT":"keepout"}[kind]]
def case_for(row):
    for c in spec["cases"]:
        p=spec["padstacks"][c["pad"]]
        if row["padstack"].lower()==p["name"] and near(num(row["x"]),c["xy"][0]) and near(num(row["y"]),c["xy"][1]):
            return c,p
    return None,None
def expected_figure(figure,xy):
    if xy is None:return figure in ("nil","NULL","",None)
    return figure not in ("nil","NULL","",None)
def numbers(v):return [float(x) for x in re.findall(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?",v)]
summary={}
for run in ["reopen_package","reopen_board"]:
    d=root/"logs"/run
    text=(d/"verify.txt").read_text()
    check("L07_READ COMPLETE" in text,run+" completed")
    check('units=("millimeters" 3)' in text,run+" mm accuracy 3")
    pinrows=rows(d/"pins.tsv")
    padrows=rows(d/"pads.tsv")
    psrows=rows(d/"padstacks.tsv")
    stack=rows(d/"stackup.tsv")
    polyrows=rows(d/"polygons.tsv")
    check(len(pinrows)==6,run+" six pins")
    check(len(psrows)==3,run+" three accepted padstacks")
    seen=set()
    for row in pinrows:
        c,p=case_for(row)
        check(c is not None,run+" expected pin position/name "+str(row))
        if c is None:continue
        seen.add(c["id"])
        check(near(num(row["rotation"]),c["rotation"]),run+" "+c["id"]+" rotation")
        check((row["mechanical"]=="t")==c["mechanical"],run+" "+c["id"]+" mechanical status")
        check(row["through"]=="t",run+" "+c["id"]+" geometric through span")
        check(norm(row["plating"])==("plated" if p["plating"]=="Y" else "nonplated"),run+" "+c["id"]+" plating")
        check(norm(row["hole_type"])==("circledrill" if p["hole"]=="CIRCLE" else "ovalslot"),run+" "+c["id"]+" hole type")
        if p["hole"]=="CIRCLE":
            check(near(num(row["drill_diameter"]),p["drill"][0]),run+" "+c["id"]+" round diameter")
        else:
            check(near(num(row["drill_x"]),p["drill"][0]) and near(num(row["drill_y"]),p["drill"][1]),run+" "+c["id"]+" padstack-local slot X/Y")
        if c["number"] is not None:check(row["number"]==c["number"],run+" "+c["id"]+" pin number")
    check(seen=={c["id"] for c in spec["cases"]},run+" all cases seen")
    etch=["ETCH/TOP","ETCH/BOTTOM"] if run=="reopen_package" else ["ETCH/TOP","ETCH/L2","ETCH/L3","ETCH/BOTTOM"]
    check(len(padrows)==6*(len(etch)*4+4),run+" all pad layer/type queries recorded")
    for row in padrows:
        c,p=case_for(row)
        if c is None:check(False,run+" unknown pad row");continue
        layer=row["layer"]
        xy=p["mask"] if "SOLDERMASK" in layer else None if "PASTEMASK" in layer else dim(row["kind"],p)
        check(expected_figure(row["figure"],xy),run+" "+c["id"]+" "+layer+" "+row["kind"]+" presence")
        if xy is None:
            check(num(row["width"]) in (None,0) and num(row["height"]) in (None,0),run+" "+c["id"]+" "+layer+" absent geometry")
        else:
            expected=list(reversed(xy)) if c["rotation"]%180==90 else xy
            check(near(num(row["width"]),expected[0]) and near(num(row["height"]),expected[1]),run+" "+c["id"]+" "+layer+" "+row["kind"]+" rotated extents")
    for row in psrows:
        p=next((p for p in spec["padstacks"] if p["name"]==row["padstack"].lower()),None)
        check(p is not None,run+" known persisted padstack")
        if p is None:continue
        check(norm(row["plating_api"])==("plated" if p["plating"]=="Y" else "nonplated"),run+" "+p["name"]+" plating API agrees")
        check(numbers(row["drill_offset"])==[0,0],run+" "+p["name"]+" drill offset")
        expected_usage={"THRU_PIN":"throughpin","MECH_HOLE":"mechanicalhole","SLOT":"slot"}[p["usage"]]
        check(norm(row["usage"])==expected_usage,run+" "+p["name"]+" persisted usage")
        if p["hole"]=="OVAL_SLOT":check(near(num(row["drill_x"]),p["drill"][0]) and near(num(row["drill_y"]),p["drill"][1]),run+" "+p["name"]+" persisted slot axes")
        else:check(near(num(row["drill_diameter"]),p["drill"][0]),run+" "+p["name"]+" persisted round diameter")
    defaults=set()
    pattern=re.compile(r'DEFAULT_INTERNAL padstack="([^"]+)" kind="([^"]+)" figure=(nil|"[^"]*") bbox=(.*)')
    for line in text.splitlines():
        m=pattern.fullmatch(line)
        if not m:continue
        name,kind,figure,box=m.groups()
        p=next(p for p in spec["padstacks"] if p["name"]==name.lower())
        xy=dim(kind,p)
        defaults.add((name.lower(),kind))
        n=numbers(box)
        if xy is None:
            check(figure in ("nil",'"NULL"'),run+" "+name+" default "+kind+" absent")
        else:
            check(len(n)==4 and near(n[2]-n[0],xy[0]) and near(n[3]-n[1],xy[1]),run+" "+name+" default "+kind+" extents")
    check(len(defaults)==12,run+" default internal all 3x4 kinds")
    for row in polyrows:
        c,p=case_for(row)
        if c is None:check(False,run+" unexpected polygon");continue
        n=numbers(row["bbox"])
        xy=list(reversed(p["regular"])) if c["rotation"]%180==90 else p["regular"]
        check(len(n)==4 and near(n[2]-n[0],xy[0]) and near(n[3]-n[1],xy[1]),run+" "+c["id"]+" world polygon extents "+row["layer"])
        if len(n)==4:check(near((n[2]+n[0])/2,c["xy"][0]) and near((n[3]+n[1])/2,c["xy"][1]),run+" "+c["id"]+" world polygon center")
    check(len(polyrows)==6*len(etch),run+" one regular polygon per pin per copper layer")
    if run=="reopen_board":
        conductors=[r["name"] for r in stack if r["name"] in ("TOP","L2","L3","BOTTOM")]
        check(conductors==spec["boardConductorLayers"],run+" TOP-L2-L3-BOTTOM order")
    launch=json.loads((d/"launch.json").read_text())
    check(launch["completed"] and launch["exitCode"]==0,run+" native normal exit")
    check(launch["readonlyHashUnchanged"] is True,run+" readonly hash unchanged")
    summary[run]={"pins":len(pinrows),"padRows":len(padrows),"polygons":len(polyrows),"stackRows":len(stack)}
for name in [p["name"] for p in spec["padstacks"]]:
    log=root/"logs"/("import_"+name)
    import_text=(log/"import.log").read_text()
    check(not re.search(r"\b(?:Warning|Error)-",import_text,re.I),name+" accepted import log has no warnings/errors")
result={
    "lesson":7,"date":"2026-10-18","status":"completed_geometry_and_layer_mapping" if not problems else "partial",
    "allChecksPass":not problems,"checkCount":len(checks),"failures":problems,"summary":summary,
    "scope":"Three accepted educational padstacks and persisted 0/90 degree package/4-layer mapping, not production qualification.",
    "failedVariants":["eda_l07_npth_200","eda_l07_npth_200_ko","eda_l07_npth_200_spot"],
    "notValidated":["Pure no-copper NPTH unattended clean import","Dynamic shape voiding and board-level keepout effect","Negative-plane spoked thermal flash/artwork","Manufacturing drill copper subtraction/output and solderability"],
    "ringMeaning":"Non-plated barrel with nominal copper rings. No plated barrel or interlayer electrical connection inferred.",
    "checks":checks}
(root/"validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},ensure_ascii=False,indent=2))
if problems:sys.exit(1)

