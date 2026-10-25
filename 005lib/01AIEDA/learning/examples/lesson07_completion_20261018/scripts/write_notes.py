from pathlib import Path
import json,hashlib,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_completion_20261018')
V=json.loads((R/'validation.json').read_text())
assert V['status']=='PASS_CAD_LESSON07_COMPLETION' and V['allChecksPass']
sha=lambda f:hashlib.sha256((R/f).read_bytes()).hexdigest().upper()
notes='''# 第7课补齐：纯无铜 NPTH、真正 thermal flash、keepout 与实际铜

日期：2026-10-18，Asia/Shanghai。实机：Cadence Allegro / Padstack Editor 17.2 S045 Windows 64-bit。

**完成结论：本课规定的孔/各层焊盘/反焊盘/热焊盘定义、纯 NULL 非镀铜孔、机械 keepout、实际四层映射及保存重开，均已在原生 CAD 中实操并独立验收。** 本次补齐前次第7课遗留的纯无铜孔、有效避铜和真实四辐条 FLASH。完成状态为 `PASS_CAD_LESSON07_COMPLETION`，157 项独立检查全部通过。原始第7课的 PTH/带铜环 NPTH/槽孔与0°、90°几何记录保留，见 [原课笔记](lesson07_padstacks_20261018.md)。

所有源码、PXML、练习库、试错、JSON、日志和预览均在 `D:\\001DIY\\005lib\\01AIEDA` 内。未修改公共库、用户打开的 Allegro PID 9136、全局 HOME、01env 模板或快捷方式。

## 1. 最终入口与规格

练习根目录：[lesson07_completion_20261018](../examples/lesson07_completion_20261018)。这是隔离软件教学 coupon，没有真实器件或板厂认可尺寸。

- [最终 spec_v2.json](../examples/lesson07_completion_20261018/spec_v2.json)
- [最终原生 SKILL](../examples/lesson07_completion_20261018/scripts/lesson07c_v2.il)
- [最终独立验收](../examples/lesson07_completion_20261018/validation.json)
- [独立 Python 验收源码](../examples/lesson07_completion_20261018/scripts/validate.py)
- [最终四层 BRD](../examples/lesson07_completion_20261018/library/eda_l07c_clearance_4layer_v2.brd)
- [封装 DRA](../examples/lesson07_completion_20261018/library/eda_l07c_null_npth_coupon.dra) / [PSM](../examples/lesson07_completion_20261018/library/eda_l07c_null_npth_coupon.psm)
- [纯 NULL 孔 PAD](../examples/lesson07_completion_20261018/library/eda_l07c_npth_200_null.pad) / [PXML](../examples/lesson07_completion_20261018/library/eda_l07c_npth_200_null.pxml)
- [正常 checked 创建的 PTH PAD](../examples/lesson07_completion_20261018/library/eda_l07c_pth_080_c160_th4.pad)
- [可用四辐条 FLASH 源 DRA](../examples/lesson07_completion_20261018/library/eda_l07c_th4_200_160_w30_d80.dra) / [FSM](../examples/lesson07_completion_20261018/library/eda_l07c_th4_200_160_w30_d80.fsm)
- [只读原始数据](../examples/lesson07_completion_20261018/logs/reopen_board02/readback.txt)
- [预览](../examples/lesson07_completion_20261018/preview.svg)：由原生读回数值绘制，非 Cadence 界面截图。

统一 mm，drawing accuracy=3。四层实际铜层名和顺序 **TOP-L2-L3-BOTTOM**；TOP/L2/BOTTOM 为动态正片铜，L3 为负片层的静态 GND 铜。层名代表位置，功能通过 net 和说明表达。DEFAULT_INTERNAL 是 padstack 模板定义，不用作物理层名。

| 项目 | 教学数值与意义 |
| --- | --- |
| NPTH | Ø2.000，NON_PLATED，Mechanical_hole，电气编号为空，封装原点(0,0)，板上(20,20) |
| NPTH 各层铜 | REGULAR/THERMAL/ANTI/KEEPOUT 全部 NULL/空，未伪造铜环或电气 thermal |
| 独立机械 keepout | 封装 ROUTE KEEPOUT/ALL，3×3 mm；板上(18.5,18.5)至(21.5,21.5) |
| PTH | Ø0.800，PLATED，各层 REGULAR Ø1.600，ANTI Ø2.000，mask 输入 Ø1.800 |
| PTH 1 / 2 | 封装(-5,0)/0°、(5,0)/90°；板上(15,20)/GND、(25,20)/OTHER |
| 负片 FSM | 外径2.0、内径1.6、四个保留铜辐条宽0.3；中央Ø0.8为钻除中心点 |
| 文字与高度 | REF DES/SILKSCREEN_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP，三文字锚点均(0,0)；填充 PLACE_BOUND 的 PACKAGE_HEIGHT_MAX="1 MM" |

## 2. 纯无铜孔不能用带铜环 NPTH 替代

孔壁是否镀铜与各层是否存在铜 pad 是两件事。前次的 `_npth_200_ring` 属于带铜环但孔壁不镀铜的另一种结构，不能作为本次纯无铜孔的替代。

本次 PXML 使用 MECH_HOLE、CIRCLE、plating=N；BEGIN_LAYER/DEFAULT_INTERNAL/END_LAYER 的 REGULAR_PAD 均 figure=NONE、width/height=0。保留双面Ø2.2 mask 输入；不加入 ANTI、THERMAL 或 padstack KEEPOUT。通过原生 `axlLoadPadstack` 后实际读回 Mechanical_hole、NON_PLATED、drillDiameter=2.0，实例 isMech=t，各铜层 pad 为 NULL/空。

同层 padstack KEEPOUT 在没有有效 Regular/Thermal/Anti 时可能被移除，不能只填尺寸后认为有效。因此本次避铜使用封装独立 filled ROUTE KEEPOUT/ALL shape；它属于机械约束，不添加铜。

## 3. 必须保留的警告与导入状态

官方 `padstack_editor.exe -x` 已写出纯 NULL `.pad`，随后报 **No default internal pads are defined** 并停在警告界面。该警告在全部内部铜为 NULL 的机械孔用途下可解释；仍必须由独立 keepout/孔到铜规则和实际铜几何保障安全。

[import_null/launch.json](../examples/lesson07_completion_20261018/logs/import_null/launch.json) 如实记录 completed=false、terminated=true、exitCode=1：15秒后仅终止本次启动的 importer PID 18660。没有称它正常无警告退出；没有关闭检查。`.pad` 可用性由后续原生加载、封装保存/编译、四层实例重开及无铜实测证明。

直接 SKILL 创建 NULL 孔时正常检查会报 Hole larger than pad size 并返回 nil，不能使用 `g_nocheck=t` 为了让结果看起来通过。本次使用官方 PXML 保留真实定义与用途性警告。

## 4. 原生 API 实操所得

本机 `axlDBCreatePadStack.txt` 将 drill 构造器写成 make_axlPadStackPad；官方 `dbcreate/pad.il` 示例及实机表明正确的是 **make_axlPadStackDrill**。误用 Pad 构造器出现 ?usage、?holeType 字段不存在。PXML usage=MECH_HOLE 与 native usage=Mechanical_hole 属不同接口枚举，不能照抄；Through_pin 是 native PTH 用法。

本次保留 create_package 至 create_package06 的失败源码/日志：构造器笔误、usage 拼写、非法 drill figure、NULL 孔通用检查，以及四扇区 FLASH 的 origin 检查。Allegro `.scr` 使用 errset 时，函数失败仍可能 exitCode=0；必须同时有 COMPLETE、预期文件和独立重开验收。

首次四扇区 FSM 编译成功，但 PTH 正常 checked 创建报 Padstack origin outside pad boundary。按官方 thermal 示例支持的 center dot 方式，新增**与Ø0.8孔相同、最终被钻除的中心点**，四个避铜扇区和0.3宽辐条保持不变；新名称 `_th4_200_160_w30_d80` 保存为独立版本，正常检查通过。旧四扇区 FSM保留，不冒充最终可用版本。

可用 FSM 有4个环形扇区和1个中央圆。独立解析实机 polygon：各扇区面积0.222676 mm²，解析几何目标0.222458406 mm²；差异来自0.001mm网格量化，容差0.002 mm²。中心圆面积0.5026548 mm²，匹配 π×0.4²。

## 5. 动态边界的网络参数陷阱及 v2 修正

第一次板上用 `axlDBCreateRectangle(... "BOUNDARY/TOP" "GND")` 创建动态边界。官方说明该函数 net 参数仅对 ETCH 有意义，BOUNDARY 实际忽略它。v1 正片铜因此是 dummy net，GND 引脚也被完整避铜；这不是合格的 GND 平面。**v1 BRD、原始 readback、validation_v1.json 均保留作为失败/局部证据，不作为最终版本。** v1 验收仅证明机械避铜，不能证明 GND 热连接。

v2 创建 boundary 后显式调用：

    axlDBAssignNet(boundaryDbid "GND" t)
    axlShapeDynamicUpdate(nil t)

随后独立读回三个 BOUNDARY/TOP、L2、BOTTOM 的 net=GND，四层实际 ETCH 铜均 net=GND；引脚1=GND、引脚2=OTHER 分别核对。证明不能只依赖创建调用的输入字符串。

为给物理引脚分配网络，还需用本课隔离两针 device TXT 经 axlDBCreateComponent 建立逻辑 coupon，再放置 U1。纯非逻辑 `axlDBCreateSymbol(list(package "PACKAGE"))` 的未分配引脚不能可靠改 net，首轮因此停止；保留 create_board/failed_source.il。这里没有制作 Capture .olb。

## 6. 真正的铜避让和受控挑战

最终正片 TOP/L2/BOTTOM 的 NPTH 自动 void bbox 为 **(18.498,18.498)至(21.502,21.502)**，实际边界比3mm keepout每侧再外扩0.002mm，孔边到最近铜≥0.502mm。L3 负片静态铜使用明确3×3 mm void，孔边到铜≥0.500mm。四层半径1.49mm探针与真实铜 polygon 的 AND 交集面积均0；周围铜面积>150mm²，排除空板导致的伪通过。

在事务内故意增加宽0.2mm、(19,20)至(21,20)的导线穿过孔/keepout，原生全量 DRC实测2项：

- Mechanical Drill Hole to Line Spacing：expected 0.203 MM，actual 0 MM。
- Line to Route Keepout Spacing：actual 0 MM，实际碰入 keepout。

记录见 [create_board03/create.txt](../examples/lesson07_completion_20261018/logs/create_board03/create.txt)。随后事务 rollback，重新获取对象/更新全部动态铜并全量 DRC，最终 drc_update=0、state=t；独立重开 stored_drcs=0、drc_state=t。没有把侵入线留在最终板。0 DRC只是辅助证据，实际铜、安全区和受控失败才证明规则有效。

## 7. 正片实际 thermal 与负片 FLASH 的区别

v2 引脚1在 TOP、L2、BOTTOM 各生成4条原生 thermal cline，共12条；实际宽度 **0.127mm**，中心线从(15,20)延伸到距中心0.98mm，越过半径0.929mm的铜 void并连到同属GND的实际铜。每条 thermal 的 polygon 面积0.140589 mm²，宽与端点、正面积、引脚/铜/路径 net=GND 均独立核对；OTHER引脚无这些 GND thermal。

**0.127mm来自本次正片动态铜默认连接参数；0.3mm来自单独构造的负片 FSM，两者是不同来源，不能认为 Padstack THERMAL 尺寸自动控制所有正片热连接。** 默认0.127mm不是电源/地焊盘的通用推荐。实际项目需结合电流、铜厚、压降/回路、焊接与装配要求设置辐条宽度、数量、直连或热连接，并重新观察实际铜。课内测试只证明软件定义和连接方法已掌握，未把默认值认证为实际产品规则。

## 8. 验收、试错与可复现记录

最终 [validation.json](../examples/lesson07_completion_20261018/validation.json) 包含157项检查、allChecksPass=true、failures=[]、status=PASS_CAD_LESSON07_COMPLETION。

核心检查包括真实 process exitCode/COMPLETE、DRA/BRD只读哈希不变、孔径/镀铜/机械属性/实例坐标与0°/90°、各层 REGULAR/ANTI/FSM映射、三项文字原点/1mm高度、四层顺序与L3负片属性、独立keepout持久化、实际NPTH void/铜交集、受控DRC及rollback、boundary/生成铜的GND归属、12条实际thermal与铜多边形。

最终成功过程目录：create_flash02、create_package07、create_board03、reopen_flash、reopen_package02、reopen_board02。每个有独立 launch.json、stdout/stderr 和原生报告。重复读回首轮不小心查询 PACKAGE 中不存在的 L2/L3，出现 No match subclass；后改为先读 Cross Section 再查询实际层，reopen_package02 不再产生这些查询警告。PACKAGE 默认内部定义由输入/四层板实际映射分别检查，不能虚构包内已有L2/L3。

第一次加强验收把板中变成大写的 FSM 名当作错误；Cadence/Windows库名大小写不敏感，改用 casefold 比较，原始失败结果保留 logs/validation_fsm_case_failed.json。没有修改几何来迎合验收。

SPMHUT-48 Scaled value has been rounded off 仍保留；没有隐藏或声称全流程无警告。关键孔/铜/辐条数值以实际保存重开数据为准。

原生重读使用 learning/scripts/launch_cadence17.py 的 readonly 模式，选新日志目录，输入最终BRD和 scripts/reopen_board02.scr；不要覆盖已有 launch.json。创建教学目标前须用新隔离目录/名字并更新绝对路径；不要把历史失败 prepare/finalize 中转程序当作通用重放入口。最终 validate.py 可独立重跑，以现存只读数据核验，并刷新产物清单。

## 9. 本课完成边界

本课完成的是焊盘/物理封装及与实际铜相互作用的 CAD 实操，已覆盖原来未验收项。Gerber/NC制造输出、钢网、加工公差、实际板厂接收/实物焊接认证不在本次软件第7课验收内，不能称已通过。原始槽孔方向和镀铜验收仍以原第7课数据为据；本次没有为消除纯无铜孔警告而重新定义为带铜环结构。后续实际项目的 SI/PI/EMI 仍要在真实网络、回流与制造规则下审查，不能从本教学 coupon 的0DRC外推。

最终清单见 [artifact_manifest.json](../examples/lesson07_completion_20261018/artifact_manifest.json)，包含源脚本、失败证据、原生工程、日志和SHA256。
'''
notes+='\n最终关键SHA256：\n\n'
for f in ['library/eda_l07c_null_npth_coupon.dra','library/eda_l07c_null_npth_coupon.psm','library/eda_l07c_npth_200_null.pad','library/eda_l07c_pth_080_c160_th4.pad','library/eda_l07c_th4_200_160_w30_d80.fsm','library/eda_l07c_clearance_4layer_v2.brd']:
 notes+=f'- `{f}`：`{sha(f)}`\n'
(R.parent.parent/'notes/lesson07_completion_20261018.md').write_text(notes,encoding='utf-8')
# Preview constructed from native readback values; no fake screenshot or inferred completed route.
text=(R/'logs/reopen_board02/readback.txt').read_text()
assert 'BOUNDARY_NET\t"BOUNDARY/TOP"' in text and 'THERMAL_CLINE\t"1"\t"ETCH/TOP"\t0.127' in text
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="600" viewBox="0 0 1100 600"><rect width="1100" height="600" fill="#151d2a"/><style>text{font-family:Segoe UI,Arial,sans-serif;fill:#edf3fa}.muted{fill:#b0c0d4}</style><text x="40" y="45" font-size="24">Lesson 7: native TOP copper readback, final v2</text><text x="40" y="75" font-size="15" class="muted">Derived geometry preview, not a Cadence screenshot. mm; teaching coupon only.</text>']
# Map board x11..29/y15..25 to pixel; scale40.
def xy(x,y):return (100+(x-11)*40,510-(y-15)*40)
def rect(lo,hi,color):
 x,y=xy(lo[0],hi[1]);w=(hi[0]-lo[0])*40;h=(hi[1]-lo[1])*40
 svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}"/>')
def circle(x,y,r,fill,stroke='none'):
 x,y=xy(x,y);svg.append(f'<circle cx="{x}" cy="{y}" r="{r*40}" fill="{fill}" stroke="{stroke}"/>')
rect([11,15],[29,25],'#b8782e')
for x in [15,25]:circle(x,20,.929,'#151d2a')
rect([18.498,18.498],[21.502,21.502],'#151d2a')
for x in [15,25]:circle(x,20,.8,'#dca64b')
# Actual native 0.127mm thermal paths are radial to0.98mm. Only GND pin1 connected.
for a,b in [((15,19.02),(15,20)),((15,20),(15,20.98)),((14.02,20),(15,20)),((15,20),(15.98,20))]:
 x1,y1=xy(*a);x2,y2=xy(*b);svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#dca64b" stroke-width="{.127*40}" stroke-linecap="square"/>')
for x in [15,25]:circle(x,20,.4,'#151d2a','#91acc5')
circle(20,20,1,'#151d2a','#91acc5')
x,y=xy(18.5,21.5);svg.append(f'<rect x="{x}" y="{y}" width="120" height="120" fill="none" stroke="#69cce5" stroke-dasharray="7 5"/>')
for x,label in [(15,'1 / GND'),(20,'NPTH / no copper'),(25,'2 / OTHER')]:
 xx,yy=xy(x,18);svg.append(f'<text x="{xx}" y="{yy}" text-anchor="middle" font-size="16">{label}</text>')
svg+=['<text x="850" y="160" font-size="19">Actual checks</text><text x="850" y="195" font-size="15">157 checks PASS</text><text x="850" y="225" font-size="15">TOP/L2/BOTTOM:</text><text x="850" y="250" font-size="15">4 × 0.127mm thermal</text><text x="850" y="295" font-size="15">NPTH copper gap</text><text x="850" y="320" font-size="15">positive: ≥0.502mm</text><text x="850" y="345" font-size="15">negative L3: ≥0.500mm</text><text x="850" y="390" font-size="15">Controlled DRC: 2</text><text x="850" y="415" font-size="15">After rollback: 0</text><text x="40" y="565" font-size="15" class="muted">Positive dynamic thermal width 0.127mm is a default; negative FLASH uses0.3mm spokes. Set real design rules.</text></svg>']
(R/'preview.svg').write_text(''.join(svg),encoding='utf-8')
print(json.dumps({'note':str(R.parent.parent/'notes/lesson07_completion_20261018.md'),'preview':str(R/'preview.svg'),'status':V['status'],'checks':len(V['checks'])},ensure_ascii=False))
