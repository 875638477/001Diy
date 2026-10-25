import os,json,pathlib,math,hashlib,datetime,re,shutil
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu")
G=R.parent
os.environ["TMP"]=os.environ["TEMP"]=str(R/"runtime")
def load(p):
    b=p.read_bytes()
    return json.loads(b.decode("utf-8-sig")),hashlib.sha256(b).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def transform(point,xy,a):
    ca,sa=math.cos(math.radians(a)),math.sin(math.radians(a))
    return [xy[0]+ca*point[0]-sa*point[1],xy[1]+sa*point[0]+ca*point[1]]
def transformbox(box,local,xy,a):
    pts=[transform([x+local[0],y+local[1]],xy,a) for x in (box[0][0],box[1][0]) for y in (box[0][1],box[1][1])]
    return [[min(p[k] for p in pts) for k in (0,1)],[max(p[k] for p in pts) for k in (0,1)]]
def samebox(a,b,t=.00025):return max(abs(a[i][j]-b[i][j]) for i in (0,1) for j in (0,1))<t
inv,invsha=load(G/"inventory/inventory_4L.json")
plan,plansha=load(G/"plans/placement_plan.json")
prop,propsha=load(R/"placement_mcu.json")
ep={c["ref"]:c for c in inv["components"]}
want={c["ref"]:c for c in plan["placements"]}
ours={c["ref"]:c for c in prop["placements"]}
refs=list(ours)
snapshots={}
for variant in ("4L","2L"):
    f=R/f"native_snapshot_{variant}_reconcile02.json"
    if not f.exists():
        snapshots[variant]={"status":"AWAITING_READBACK"};continue
    n,nsha=load(f)
    native={c["ref"]:c for c in n["placements"]}
    findings=[];items=[];pinCount=0
    for ref in refs:
        a=native.get(ref);w=want[ref];e=ep[ref]
        checks=[];errors=[]
        if not a:
            findings.append({"ref":ref,"error":"missing actual placed component"});continue
        if math.dist(a["xy"],[w["x"],w["y"]])>.0002 or abs((a["rotation"]-w["rotation"]+180)%360-180)>.0002:errors.append("native pose differs from current common plan")
        if a["package"].upper()!=e["package"].upper():errors.append("package changed")
        if not samebox(a["bodyExtent"],w["extent"]):errors.append("actual body bbox differs from common transformed package bbox")
        pins={p["number"]:p for p in a["pins"] if p["number"]}
        if set(pins)!=set(p["number"] for p in e["logicalPins"]):errors.append("logical pin set changed")
        for p in e["logicalPins"]:
            aa=pins.get(p["number"])
            if not aa:continue
            pinCount+=1
            expectedXY=transform(p["localXY"],a["xy"],a["rotation"])
            expectedBBox=transformbox(p["regularPadBBox"],p["localXY"],a["xy"],a["rotation"])
            goodNet=aa["net"]==p["net"]
            goodXY=math.dist(aa["xy"],expectedXY)<.00025
            goodBBox=samebox(aa["padBBox"],expectedBBox)
            checks.append({"pin":p["number"],"net":aa["net"],"actualXY":aa["xy"],"sameNet":goodNet,"sameXY":goodXY,"sameCopperBBox":goodBBox})
            if not(goodNet and goodXY and goodBBox):errors.append("pin "+p["number"]+" net/anchor/copper mismatch")
        items.append({"ref":ref,"nativeXY":a["xy"],"rotation":a["rotation"],"logicalPins":len(pins),"errors":errors,"pins":checks})
        if errors:findings.append({"ref":ref,"errors":errors})
    ndir=pathlib.Path(n["readbackDirectory"])
    drcfile=ndir/"g_drc_details.txt"
    drctext=drcfile.read_text(encoding="utf-8-sig") if drcfile.exists() else ""
    m=re.search(r"DRC_STATUS\s+G_SNAPSHOT\s+(\d+)\s+(\w+)",drctext)
    drcCurrentZero=bool(m and m.group(1)=="0" and m.group(2)=="t" and "G_SNAPSHOT_COMPLETE" in drctext)
    c18=next(p for p in native["C18"]["pins"] if p["number"]=="1")
    topPads=[p for p in native["U1"]["pins"] if abs(p["xy"][1]-31.25)<.0001]
    topEdge=max(p["padBBox"][1][1] for p in topPads)
    c21=next(p for p in native["C21"]["pins"] if p["number"]=="1")
    y=32.20;half=.1
    snapshots[variant]={"status":"PASS_MCU_PLACEMENT_PIN_MAPPING_SCOPE" if not findings else "REQUIRES_CORRECTION","snapshot":str(f),"snapshotSHA256":nsha,"readbackDirectory":str(ndir),"nativeDRCReportSHA256":sha(drcfile) if drcfile.exists() else None,"nativeDRCZeroCurrent":drcCurrentZero,"componentsReviewed":len(items),"logicalPinsCompared":pinCount,"findings":findings,"items":items,"actualRouteCount":len(n["routes"]),"actualViaCount":len(n["vias"]),"actualPlaneCount":len(n["planes"]),"adcPostEscapeCorridor":{"ADCcenterY":y,"assumedTraceWidth":.20,"C18pad1MinY":c18["padBBox"][0][1],"MCUNorthPadsMaxY":topEdge,"C18edgeClearance":round(c18["padBBox"][0][1]-y-half,6),"MCUpadEdgeClearance":round(y-topEdge-half,6),"C21edgeClearance":round(c21["padBBox"][0][1]-y-half,6),"status":"POST_FINE_PITCH_ESCAPE_GEOMETRIC_RESERVATION_ONLY_NOT_ROUTED","finePitchRestriction":"ADC0/U1.10 beside VDDA/U1.9 still needs explicit power spacing resolution; .30 class spacing can govern this adjacent pair."}}
changes=[]
for ref in refs:
    p=ours[ref];w=want[ref]
    if math.dist(p["xy"],[w["x"],w["y"]])>.0001 or abs((p["rotation"]-w["rotation"]+180)%360-180)>.0001:
        changes.append({"ref":ref,"ourRetainedCandidate":{"xy":p["xy"],"rotation":p["rotation"]},"rootCommonPlan":{"xy":[w["x"],w["y"]],"rotation":w["rotation"]},"reason":{"C18":"root raised by .20mm to reserve ADC post-escape corridor","R29":"root moved BOOT1 static pull-down clear LDO/SPI","R32":"root moved ADC series resistor clear NSS resistor bank"}.get(ref,"root global placement reconciliation")})
lim=[
{"id":"G31","status":"THREE_LOOPS_UNROUTED_AT_PLACEMENT_CHECKPOINT","rule":"V3V3/GND normal .60mm, neck .25mm maximum1mm; verify real connected cap/pin/via/filled plane later"},
{"id":"G33_HSE","status":"PLACED_WITH_PATH_GUIDES_ONLY","rule":"No digital fanout through oscillator/load-cap/guard zone; U1.2/.3/.4 cannot simply escape north across OSC_IN. Route elsewhere/layer with continuous return and current rules; inner non-GND signal routing presently disallowed, changing permission needs explicit plan update."},
{"id":"G33_HSE_GROUND","status":"AN2867_LOCAL_COPPER_NOT_IMPLEMENTED","rule":"L2 full-board GND does not prove isolated local oscillator reference/guard/cap return. Y1.2/.4 case-ground return must be distinguished from load-cap quiet return; no floating island or digital trace across isolation slot."},
{"id":"G33_ADC","status":"RC_TOPOLOGY_AND_C18_CHANNEL_REVIEWED_NOT_ROUTED","rule":"J10.1->R32.1->R32.2(ADC0)->C24.1/U1.10; C24.2 returns close VSSA8. Post-escape corridor reserved; VDDA/NRST interaction and narrow pin spacing remain native routing review."},
{"id":"G33_RESET_BOOT","status":"PLACED_STATIC_CONTROL_PATHS","rule":"C21 remains at NRST MCU side; J7/J9 service branches must not share oscillator quiet return. R29 static bias needs source integrity and correct net, not arbitrary high-speed length cap."},
{"id":"G35_36","status":"REFERENCE_PLANE_EXPERIMENT_SEPARATE","rule":"Checkpoint has no plane or demo tracks. Experimental GND copper 4L L2/2L BOTTOM is separately verified; no full routed PCB/USB90ohm/EMI/manufacturing/GUI claim"}]
out={"date":datetime.datetime.now().astimezone().isoformat(),"status":"PASS_MCU_LAYOUT_NATIVE_SCOPE_WITH_ROUTING_OPEN_ITEMS" if all(s.get("status","").startswith("PASS") and s["nativeDRCZeroCurrent"] for s in snapshots.values()) else "REQUIRES_FOLLOWUP","sourceInventorySHA256":invsha,"commonPlanSHA256":plansha,"retainedProposalSHA256":propsha,"reviewScope":"Independent read-only recomputation of selected 24 MCU/decoupling/clock/reset/ADC components; native pin anchors and top copper bbox compared with original native package-local geometry. Root owns full80-component/board review.","nativeSnapshots":snapshots,"rootOverridesAgainstRetainedCandidate":changes,"routingOpenItems":lim,"previewInspected":str(G/"review_figures/mcu_decoupling_clock.png"),"previewSHA256":sha(G/"review_figures/mcu_decoupling_clock.png")}
(R/"native_mcu_placement_review.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
api=R/"api_sources";api.mkdir(exist_ok=True)
src=pathlib.Path(r"C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS")
sources=[]
for name in ("axlRegionCreate.txt","axlRegionAdd.txt","axlCNSCreate.txt","axlCNSSetSpacing.txt","axlCnsClassTableCreate.txt","axlCnsClassTableSeek.txt","axlCnsClassTableFind.txt","axlLayerGet.txt","axlLayerCreateNonConductor.txt"):
    p=src/name;q=api/name;shutil.copyfile(p,q)
    sources.append({"source":str(p),"copied":str(q),"SHA256":sha(q)})
html=[
(r"C:\Program0\Cadence\SPB172\doc\constraintcore\chap1.html","#1071088","Region-Class-Class > Region-Class > Region; nested innermost, overlap most conservative; arbitrary per-pin spacing overrides not supported"),
(r"C:\Program0\Cadence\SPB172\doc\cmref\objects.html","#region","Region can have multiple shapes, layer can be by-layer; actual native subclass identity must be inspected"),
(r"C:\Program0\Cadence\SPB172\doc\propref\properties.html","#852968","PIN_ESCAPE controls automatic router escape placement, does not waive spacing"),
(r"C:\Program0\Cadence\SPB172\doc\cmug\02objects.html","#region","Region shapes and Region-Class constraint scope")]
apis={"status":"READ_ONLY_OFFICIAL_API_RESEARCH_UNEXECUTED_DRAFT","copiedPrimaryReferences":sources,"localManualSections":[{"path":p,"anchor":a,"SHA256":sha(pathlib.Path(p)),"finding":f} for p,a,f in html],"recommendedScope":"Copy S_POWER_030 into new CSet; change only smdpin_line and line_line to .20mm on actual TOP applicability; bind region-class NC_POWER_LV_S to three small disconnected shapes covering only three VDD/VSS pin necks/transition; preserve normal .60/neck.25/max1mm and all via/hole constraints. Native must verify inside/outside region and reopen. Do not change global default/power class.","licenseCondition":"Regions unavailable PCB L or below; API success/current native DRC and inside/outside challenge mandatory.","notAWorkingResult":"No region created by this review; pin_escape_region_draft.il unexecuted and requires caller-supplied real layer/subclass and reviewed boxes."}
(R/"pin_escape_api_review.json").write_text(json.dumps(apis,ensure_ascii=False,indent=2),encoding="utf-8")
note=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\notes\lessonG_mcu_20261020.md")
text=note.read_text(encoding="utf-8-sig")
marker="## 8. 统一布局原生快照专项复核（2026-10-20）"
if marker in text:text=text[:text.index(marker)].rstrip()+"\n"
addition=r"""
## 8. 统一布局原生快照专项复核（2026-10-20）

已按统一plans/placement_plan.json复核原生两板reconcile_4L_02 / reconcile_2L_02读回的U1、C13—24、R26—32、Y1、J7/J8/J10共24件。每板96个真实逻辑pin，分别核原理图网络、原生pad锚点、由原生local几何独立旋转得到的铜bbox；24件角度/原点/PlaceBound也与当前计划相符。两板本次原生DRC均为0且当前。证据、输入hash与逐pin结果保存在[MCU专项原生复核JSON](../examples/lessonG_30_37_20261020/engineering_mcu/native_mcu_placement_review.json)。这是第30/31/33课的**布局与pin几何范围通过**；三回路真实铜另存实验，不能把未布线空气线、原点距离或DRC=0解释成信号/电源完整性验收。

原24件候选JSON保留原稿身份，不随根全局覆盖。统一计划对本组3项修正：C18由(37,32.8984)90°上移0.20mm到(37,33.0984)90°；R29从(31,27.5)0°改为pin1(31.4,23)的180°摆位（真实原点31.5016,23）；R32从(31,33)0°上移到(31,35)0°。C8/C9由电源组/根调整，全板80件核对由根专项报告负责，不能把旧候选与新原生不同代误当软件旋转错误。

C18.1现为(37,33.2)，铜下边y32.73。以ADC0脱出细脚后的0.20mm水平线中心y32.20估算，对C18铜边净距0.43mm，对MCU北排铜边0.25mm，对C21.1下铜边0.23mm；分别给0.30mm电源侧及0.20mm普通侧留下几何余量。原位置两铜边间仅0.68mm，低于0.20线+0.30/0.20两侧间距所需0.70mm，因此已实际修改并读回。**这不证明U1.10细脚处的ADC/VDDA/NRST本层脱出已经完成**：ADC0旁VDDA9同样受电源0.30mm间距影响，仍要正式细脚区域规则/实际路径验证。R32.1朝输入，R32.2/C24.1/U1.10属于同一ADC0，MCU侧RC拓扑正确。

HSE的B3路径和Y1真实pad方向已在原生预览中目视；仍只是布局与走廊预审。U1.2/.3/.4向北的PC13/14/15若直走会穿OSC_IN横向通道及振荡局部地预留，后续必须向区外逃线或使用被允许且返回连续的层；当前4层非GND信号的内部布线权限仍禁止，不能凭建议直接把L3当可走线层。2层若改走BOTTOM更需避免割断振荡器下方/负载电容返回。ABM3B壳地2/4与负载cap回流的物理区别、AN2867局部专用地/护环仍未实现，连续L2整板地不能代替这些验收。

三对VDD演示后续需验证：0.60mm普通电源/地线，0.25mm短颈最大1mm，两个GND过孔到实际填充GND铜的导电图及重开读回。原生S_POWER_030的smdpin_line/line_line/via_line为0.30mm，而MCU相邻pin铜间仅0.20mm；不能用全板放宽或全线0.25mm掩盖细脚逃线条件。已只读核17.2官方axlRegionCreate/Add、axlCnsClassTableCreate与优先级，整理[最小区域例外API依据](../examples/lessonG_30_37_20261020/engineering_mcu/pin_escape_api_review.json)及[未运行SKILL草案](../examples/lessonG_30_37_20261020/engineering_mcu/pin_escape_region_draft.il)。Region-Class可只针对本地3段电源脚末端把smdpin_line/line_line改0.20mm，其他via/孔/普通宽度仍保留；实际层作用域、许可、区域内外DRC挑战与重开成功才算生效。PIN_ESCAPE属性仅控制自动路由逃线生成，**不是间距豁免**。

此快照每板已有1颗继承教学GND过孔，但无局部示范走线、无实际GND平面。三回路/4L L2与2L BOTTOM地铜试验另存，后续追加导电图与最小scope区域规则验证，不把本阶段冻结板宣称为完整布线、90Ω、EMI或制造放行结果。
"""
note.write_text(text.rstrip()+"\n"+addition,encoding="utf-8")
print(json.dumps({"status":out["status"],"variants":{k:{"status":v["status"],"pins":v.get("logicalPinsCompared"),"DRC0current":v.get("nativeDRCZeroCurrent"),"findings":v.get("findings")} for k,v in snapshots.items()},"rootChangedMCURefs":[x["ref"] for x in changes]},ensure_ascii=True))
