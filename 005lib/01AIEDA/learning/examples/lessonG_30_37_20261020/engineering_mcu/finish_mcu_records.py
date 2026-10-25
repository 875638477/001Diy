import os,json,pathlib,hashlib,math,re,itertools
ROOT=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_mcu")
os.environ["TMP"]=os.environ["TEMP"]=str(ROOT/"runtime")
note=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\notes\lessonG_mcu_20261020.md")
p=json.loads((ROOT/"placement_mcu.json").read_text(encoding="utf-8"))
a=json.loads((ROOT/"placement_mcu_candidateA.json").read_text(encoding="utf-8"))
def lookup(d,ref,n): return next(v["xy"] for c in d["placements"] if c["ref"]==ref for v in c["pins"] if v["number"]==str(n))
def man(x,y):return sum(abs(a-b) for a,b in zip(x,y))
def measure(d):
    return {"input_endpoint_manhattan":man(lookup(d,"U1",5),lookup(d,"Y1",1)),
            "out_to_R31_manhattan":man(lookup(d,"U1",6),lookup(d,"R31",1)),
            "R31_to_crystal_manhattan":man(lookup(d,"R31",2),lookup(d,"Y1",3))}
ma,mb=measure(a),measure(p)
paths=[
 dict(net="OSC_IN",points=[lookup(p,"U1",5),[40.75,32.30],[43.0,32.30],lookup(p,"Y1",1)],role="main input path preview"),
 dict(net="OSC_OUT",points=[lookup(p,"U1",6),[40.25,32.15],lookup(p,"R31",1)],role="MCU to series position"),
 dict(net="XTAL_OUT",points=[lookup(p,"R31",2),[40.2,37.7],lookup(p,"Y1",3)],role="main output after series position"),
 dict(net="OSC_IN",points=[lookup(p,"Y1",1),lookup(p,"C22",1)],role="load capacitor branch"),
 dict(net="XTAL_OUT",points=[[40.2,37.7],lookup(p,"C23",1)],role="load capacitor branch")]
for v in paths:v["geometric_preview_length_mm"]=sum(math.dist(x,y) for x,y in zip(v["points"],v["points"][1:]))
gaps=[]
for x,y in itertools.combinations(p["placements"],2):
    aa,bb=x["bodyBound"],y["bodyBound"]
    dx=max(0,aa[0][0]-bb[1][0],bb[0][0]-aa[1][0])
    dy=max(0,aa[0][1]-bb[1][1],bb[0][1]-aa[1][1])
    gaps.append((math.hypot(dx,dy),x["ref"],y["ref"]))
clock=dict(status="UNROUTED_GEOMETRIC_PREVIEW_NOT_NATIVE_DRC",candidate="B3",candidateA=ma,candidateB3=mb,totalA=sum(ma.values()),totalB3=sum(mb.values()),relativeReduction=(sum(ma.values())-sum(mb.values()))/sum(ma.values()),metric="Manhattan between actual pad centers; excludes resistor interior, is not a completed route length",previewPaths=paths,clearanceNotes=["proposed .20mm line horizontal y32.30","MCU upper pad edge31.85: centerline clearance.45 minus halfwidth.10 = .35mm","Y1.4 GND lower copper edge32.80: centerline clearance.50 minus halfwidth.10 = .40mm","all other pin/trace/region rules including near pin neck require native DRC; no full clearance PASS"],minimumOwnBodyGap=dict(mm=min(gaps)[0],refs=list(min(gaps)[1:])))
(ROOT/"clock_path_precheck.json").write_text(json.dumps(clock,ensure_ascii=False,indent=2),encoding="utf-8")
text=note.read_text(encoding="utf-8")
old="本首稿Y1@(43,37.5)180°，其1=(45,38.7)、3=(41,36.3)；R31.1=(41.6,33)、.2=(41.6,34.5748)，C22.1=(47.4,38.7)、C23.1=(38.6,36.3)。它服从现有大0603/PlaceBound的空间约束，尚需优化OSC_IN绕过壳地焊盘的真实路径，不能声称已经最短或布线通过。优先保持源→晶体→负载电容的拓扑明确，禁止为缩中心距把电容放在封装边界重叠处。"
new="初稿A的Y1@(43,37.5)180°虽然包络不重叠，IN端点曼哈顿长11.7mm，OUT两段合计5.4252mm，明显失衡，因此没有当作合格收敛方案。已保留[候选A](../examples/lessonG_30_37_20261020/engineering_mcu/placement_mcu_candidateA.json)并改为当前B3：Y1@(43.2,35.7)90°，其1=(44.4,33.7)、3=(42.0,37.7)；R31.1=(40.2,33.2)、.2=(40.2,34.7748)，C22.1=(46.2,34.0)、C23.1=(39.8,37.7)。C21左移到(38.6,32.8984)90°，C18移到(37.0,32.8984)90°，C17移到(46.1,32.4)0°，为真正通道让出空间。\\n\\nB3的IN端点曼哈顿6.1mm、OUT两段合计6.5252mm，总和比A减少约26.3%，两臂更均衡。这是实际pad中心间的可比较预算，排除了电阻内部，不是已布线的线长。输入路径预判U1.5→(40.75,32.30)→(43.0,32.30)→Y1.1，横线位于MCU上侧pad边31.85与Y1.4地pad下边32.80之间；以0.20mm线估，两侧边到边余量分别约0.35/0.40mm。输出R31.2沿x40.2向上到y37.7再接Y1.3，途中与C23.1同节点。ADC/VDDA/NRST/OSC_OUT/OSC_IN的源脚与外部扇出次序保持，主枝无需交叉。\\n\\n[路径预审](../examples/lessonG_30_37_20261020/engineering_mcu/clock_path_precheck.json)保存比较、折线和几何长度。当前24件最小PlaceBound间隙约0.2284mm，仅对本组成立；全部电源/相邻pin/间距/neck还要正式原生核验。没有为缩中心距把器件边界重叠，也没有据预判声称最优、启动或布线通过。"
assert old in text
text=text.replace(old,new.replace("\\n","\n"))
text=text.replace("24件坐标首稿与无交叠局部包络预审","24件坐标B3候选、时钟两臂比较与无交叠局部包络预审")
note.write_text(text,encoding="utf-8")
source=ROOT/"source"
sourceReview=dict(status="PRIMARY_DOCUMENTS_REVIEWED_NOT_HARDWARE_VERIFIED",DS5319_current_matches_inherited=hashlib.sha256((source/"DS5319_current_download.pdf").read_bytes()).hexdigest()==hashlib.sha256((source/"DS5319_inherited.pdf").read_bytes()).hexdigest(),docRevisions={"DS5319":"Rev20 July2025 114PDFpages","AN2586":"Rev8 Dec2022","AN2867":"Rev24 Feb2026","AN2834":"Rev10 Oct2024","ABM3B":"RevU Aug2024"},visualPagesReviewed={"DS5319":[26,36],"AN2586":[22],"AN2867":[45,46,47],"AN2834":[37,38,39],"ABM3B":[3]},materialBoundaries=["AN2867 local oscillator plane/guard separate requirement, not fulfilled merely by global L2 ground intention","ABM3B2/4 GND case physical return distinguished from load-cap quiet return","AN2834 separated grounds/star recommendations preserved with context; this board shared GND is explicit engineering choice","no uniform numerical distance thresholds asserted","no fabrication/90ohm/GUI/EMI/startup/ADC accuracy guarantee"],candidateB3MinBodyGap=min(gaps)[0])
(ROOT/"source_review.json").write_text(json.dumps(sourceReview,ensure_ascii=False,indent=2),encoding="utf-8")
links=[]
for label,target in re.findall(r"\[([^\]]*)\]\(([^)]+)\)",text):
    if target.startswith(("http://","https://","#")):continue
    resolved=(note.parent/target.split("#")[0]).resolve()
    links.append(dict(target=target,exists=resolved.exists()))
assert all(x["exists"] for x in links)
(ROOT/"note_links_check.json").write_text(json.dumps({"links":links,"pass":True},ensure_ascii=False,indent=2),encoding="utf-8")
manifest={"scope":"engineering_mcu own files and own course note only","status":"COMPLETE_ENGINEERING_PROPOSAL_NOT_NATIVE_LAYOUT","files":[]}
for f in sorted(ROOT.rglob("*")):
    if f.is_file() and f.name!="artifact_manifest.json":manifest["files"].append(dict(path=str(f),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
manifest["files"].append(dict(path=str(note),bytes=note.stat().st_size,sha256=hashlib.sha256(note.read_bytes()).hexdigest()))
(ROOT/"artifact_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"clock":clock,"noteLocalLinks":len(links),"manifestFiles":len(manifest["files"]),"noteSHA256":hashlib.sha256(note.read_bytes()).hexdigest()},ensure_ascii=True,indent=2))
