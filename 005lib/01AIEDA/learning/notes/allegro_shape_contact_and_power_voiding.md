# Allegro 铜皮全连接、电源避让与实际铜验收

整理日期：2026-10-24。适用接口以 Cadence 17.2 本机官方帮助及独立副本实测为准。本文只记录通用方法；输入、位号、层功能、数量、配置、日志、失败试验和验收结果随实际工程保存，不作为任何课程或整板已通过的证明。

## 1. 先固定修复范围与来源

保留原板及来源 SHA256，在工程内建立候选副本。明确要改变的是同网 via 的连接形式、电源分区避让，还是某个确实断开的供电端点；不要把它们合并成一次无范围的重铺铜。

读取实际层序、层功能、正负片类型、网络、动态边界、静态铜、生成铜、人工 void、固定属性及当前填铜模式。层名不代表电源或地的功能；沿用工程已确认的层叠，不根据名称改层型。未知 Cadence 进程属于用户现场，原生写入统一调度，避免并行操作同一设计。

## 2. via 全连接有三层覆盖

动态 Shape 的设置优先级为：**对象级 > Shape 实例级 > 全局**。只改全局不能证明既有 via 全部采用新设置。

| 设置层次 | via 全连接的接口或属性 | 注意事项 |
| --- | --- | --- |
| 动态全局参数 | `axlGetParam("shapeDynamic")` 的 `viaThermalType="Full contact"`，再 `axlSetParam` | 字符串带空格；修改后动态铜会标为待更新 |
| 动态实例覆盖 | 对边界的 `dynamicGroup` 设置 `VIA_THERM_CONN="FULL_CONTACT"` | 这是原生写入、保存后读回验证过的属性枚举；重新打开仍须核对 |
| via 对象覆盖 | `DYN_THERMAL_CON_TYPE`，枚举 `FULL_CONTACT` | 可按层设置；核对现有对象及定义继承，不能被局部旧值悄悄覆盖 |
| 静态全局参数 | `axlGetParam("shapeStatic")` 的 `viaThermalType="Full contact"`，再 `axlSetParam` | 仅影响下一次静态重新避让，不立即改变既有静态铜 |

全局与属性接口的字符串不同，不用显示名称猜底层枚举。实例属性写入示意：

```lisp
; 仅对已定位的候选板动态边界执行；调用后检查返回值和实际属性。
axlDBAddProp(boundary->dynamicGroup
  list(list("VIA_THERM_CONN" "FULL_CONTACT")))
```

通孔器件引脚另有 `THRU_THERM_CONN`，SMD 引脚另有 `SMD_THERM_CONN`；动态全局对应 `pinThermalType`、`smdThermalType`。请求 via 全连接不意味着要把所有器件引脚都改成直连。修改前后分别导出三层参数，避免误扩范围。

Full contact 对同网铜不产生热焊盘隔离，最小热连接数量在该模式下不适用。它不允许异网铜互连，也不保证铜皮外、void 内或孤岛上的 via 已接入目标平面；仍须核对实际各层焊盘和整条电气路径。

## 3. 电源优先级不能代替分区设计

先从原工程的网络、边界、保存铜和实际端点确定各电源分区的用途，再决定哪些动态电源区应优先于大面积地铜。对合法动态边界：

```lisp
axlShapeRaisePriority(boundary)
```

该接口把此边界升为本层最高优先级，其他重叠动态铜向它避让。返回正数为新优先级，`-1` 表示已最高，`nil` 表示对象不适用。优先级是相对值，软件可能重排，不直接硬写固定数字。

电源区之间也要单独查异网重叠，不能按调用顺序随意吞掉某个电源岛。原设计的小地岛可能供给真实地引脚、保护或局部返回，不能因为面积小就删除。记录岛上的源端点和可达铜，优先用局部避让、保留合法地通道或经授权的短接续线解决；每次修复后证明没有丢失原有合法供电与接地关系。

源工具的 Polygon、Region、Fill 可能被归并成目标的同一 Shape 类别。把不同间距取保守最大值会改变重铺后的狭窄通道，甚至隔断原连接；应回到源逐对象规则核查，而非用不满足最小线宽的细桥补救。动态参数只有 DRC／Thermal-anti 选择和附加 Oversize，未找到可直接对单个动态 Shape 设置绝对 via 间距的文档化字段；负 Oversize 也不受支持。约束 Region 是空间作用域，会影响其中符合条件的所有对象，不能当作动态／静态类型过滤器。若用局部 Region 恢复源要求，须先证明范围内及边缘不会放宽其他源类别，克隆当前对象实际活动的 CSet 只改目标项，逐层逐字段证明其他值保持。不能因名称为 DEFAULT 就选它作基线；还要核原生有效继承和范围内外反测。

完全嵌套的两个异网 Shape 也不能仅凭“内层优先”接受真重叠。若高优先级更新后仍相交，核查当前对象身份、正负片、有效间距及 `DYN_DO_NOT_VOID` 等覆盖，保留为未解决问题；未找到官方例外时不自造解释。

## 4. 更新、静态重避让与转换边界

动态更新作用于 `shapeIsBoundary=t` 的母边界：

```lisp
axlShapeDynamicUpdate(boundary t) ; 强制更新该边界，即使并非 OOD
axlShapeDynamicUpdate(nil nil)   ; 更新全部 OOD 动态边界
axlDBDynamicShapes(nil)          ; 只查询 OOD 数量
```

动态更新包含自动避让、平滑和热连接生成，会改变实际铜。单边界更新返回 `0` 为成功、`1` 为失败、`nil` 为错误；全体更新的数值是失败数量。`axlDBDynamicShapes(t)` 的返回数是更新前 OOD 数量，不能误读成更新后剩余数量。强制更新会忽略当前动态填铜开关；“禁止自动填铜保存”不能阻止这一显式调用。

静态铜使用 `axlShapeAutoVoid(staticShape options)`，不适用于动态边界、动态生成铜或负片平面内部避让。其默认行为会重建热连接，并可能将一个 Shape 分成多个对象；必须接收返回对象、重新枚举并核验。`noRipThermals` 保留旧热连接，不应未经核验就用于要求改变连接形式的任务。

不要为方便而批量来回转换静态／动态。`axlShapeChangeDynamicType(staticShape t t)` 会删除原静态 void；动态转静态则可能丢失原母边界、参数及人工 void 的意图。先保存原边界和人工开口并逐项分类，确认能够恢复之后才在副本尝试。

人工永久开口可用 `axlDBCreateVoid` 配合 `axlDBOpenShape`／`axlDBCreateCloseShape`。动态人工 void 必须加在 BOUNDARY 上，不能改生成的 ETCH 子铜。它是长期保留的设计意图，不能随意替代按异网间距计算的自动避让，也不能为显示连续而全删 void。

## 5. 母边界重叠不等于实铜短路

动态母边界用于描述铺铜范围；实际导电图形是其生成的 ETCH 铜。`boundary->shapeAuto` 给出生成铜，`child->shapeBoundary` 指向母边界，`boundary->dynamicGroup` 保存实例覆盖。不要直接移动、加属性或删除自动生成子铜。

逐物理层导出实际 Shape、孔洞、via 与 pin 的 **regular pad** 及 cline 铜宽；不能只取外接框、中心点或库里的名义圆。`axlPolyFromDB(shape ?holes t)` 保留 void，via／pin 用实际层参数读取。弧、多边形、孔洞的离线重建须对照原生面积、bbox 和单位，并记录离散化误差；解析失败不能当作无铜。

对同层异网的实际铜求交，同时检查小于有效间距的情况。原生 `axlPolyOperation(polysA polysB 'AND)` 中，`(nil)` 是空交集，`nil` 是运算失败，后者需读取 `axlPolyErrorGet()`，不能都记成零重叠。零面积接触仍可能短路；正面积相交与违反间距分别记录。若使用离线几何引擎，独立核对 void、弧和误差，不把近似结果冒充原生 DRC。

## 6. 从实际铜建立连通分区和孤岛 BFS

逻辑网名相同并不代表物理相通。按以下层次建立可追溯的物理图：

1. 每层以实际 Shape 铜、pin/via regular pad 和带宽度的 cline 铜为节点，保存网络、层、几何及来源。只在真实导电接触处建边，不把同网对象自动相连。
2. via／镀通孔按真实层跨、钻孔和焊盘定义连接其各层导体；非镀孔不产生跨层导通。中心在铜内不等于焊盘接触，跨层 span 也不能凭名称推断。
3. 从已确认的供电／公共地锚点做 BFS 或并查集，列出每个 pin、via、铜片的可达分区。另输出没有物理终端的铜岛、含必需端点但未到锚点的岛，以及断开的 cline 分支。
4. 同时读取原生物理连通分区或 `axlDBGetConnect(obj t)`。其可能返回 path 父对象，须遍历 segments；空枚举、缺少焊盘层或未解析对象必须记为未验证。
5. 用“完整物理位号＋脚号＋网络＋世界坐标”比较源与候选的端点集合和分区，不跨会话比较 dbid／分区编号。逐项列出缺脚、新脚、合法连接拆分和分区合并，并追踪每个 via 的可达性。

源板若已有异网短接，不能要求候选保留那个错误合并的分区。先按网络和源意图区分应保留的合法关系，再验证修复消除异网铜接触且未断开任何所需端点。无孤岛、全部同网端点可达仍不等于回流、铜颈、承流或制造已合格。

## 7. canonical line／path 差分保留真实改动

原生重开或保存可能反向表达线段、重组 path。将显式 cline 展开成段，以网络、物理层、线宽、端点和图形种类建立稳定键；直线端点方向可规范化，弧还须保留圆心、半径、起止和扫向，并只合并已证明等价的反向表达。

使用保留重复次数的多重集合，而非去重 set。path 的父对象编号、段顺序或分组变化与铜变化分开报告；不能用随意舍入、只比长度或无条件合并共线段掩盖支点、短支线和真实铜差异。手工线、自动热连接、生成铜和母边界分别比较。

修复预期会改变填铜时，把批准的边界／参数／新增接续线列为明确差分合同。器件、焊盘、非目标手工线和原有合法端点关系保持；生成铜的改变按避让和连通结果验收。不要一边要求重铺铜，一边用“全板几何哈希相同”作为唯一成功条件。

CFX 保存重开也可能只改变 `Gate/object/children Kind="Pin"` 中有名 Pin 子对象的排列。先用独立解析器证明每个完整子树、Name／AltName 等全部属性及重复次数保持，且 Gate 对象顺序与其他内容未变，才允许仅对此容器按完整子树排序。不能全局排序 XML 子节点，尤其不能打乱层叠或其他有序序列。保留原始字节 SHA、未归一时的失败报告和归一后的语义比较；补最小反测：只排列应相等，改 Pin 名称、属性或重复次数必须不等。受控顺序归一不是忽略内容，也不能把未保存或未执行的检查改写为通过。

## 8. fresh DRC 与许可边界

保存时 DRC marker 为零不等于当前设计无错。分别记录读取到的存量结果和本轮显式更新：

```lisp
axlCNSDesignModeGet('all)
axlCNSPhysicalModeGet('all)
axlCNSSpacingModeGet('all)
axlCNSSameNetModeGet('all)
axlCNSEcsetModeGet('all)
axlCNSAssemblyModeGet('all)
axlDRCUpdate(t)
```

先保存 master DRC、各域实际模式、动态填铜状态和产品／选项。`ModeGet(nil)` 可列当前支持项；`off` 与当前产品不支持是不同状态，不为得到“全检查”而擅自打开源设计已关闭的规则。普通 `SHAPE_TO_SHAPE_SPACING` 与高级制造 `DFF_CS_SHP_TO_SHP` 不是同一项。

`axlDRCUpdate(t)` 检查当前开启的在线和 batch 项，并会启用 Online DRC，但仍受模式、产品能力与外部检查器限制。保存调用返回值、完整 batch 日志及更新后状态。`design->drcState` 为 `t` 表示最新、`nil` 表示过期、`batch` 表示 batch 过期；日志写“完成”但状态仍非最新时，记录两项事实和未查明的原因，不改写为整板通过。

`design->drcs` 和 `design->waived` 分别保留；DRC 的 `name/type/source/actual/expected/xy/violations` 用于分类和定位。原生 DRC 对象会变化，不能跨会话比较 dbid。原板与候选在相同模式、相同产品条件下分别 fresh 检查，按规则名、域、层、坐标、实际值、要求值做保重复的多重集合比较，列出既有、增加、消除和变值记录。总数不变不表示没有回归；标记坐标变化也不能未经对象证据就认定新增实体错误。目标区域检查同时保留窗口定义与全板结果。

若软件提示某些设计能力因产品／选项不匹配而禁用，保存模式为 ON 或约束能重开，只能证明数据存储，不能证明该检查执行过。`Update to Tier` 的官方描述是匹配当前产品／选项的设计能力，不能无证据承诺它只改显示或必然删除规则；先在副本比较，再决定是否使用。不以消除警告、隐藏／豁免 marker 或降低规则换取通过。

## 9. 完整新进程重开后再交付

关闭候选板及执行进程，使用项目私有环境在完整新进程中打开实际交付路径。重新解析对象，读回连接参数、边界／优先级、层序、CSet、生成铜、OOD、via/pad/cline 分区、孤岛及 DRC 状态；源板 SHA256 保持不变。

配置保存、填铜完成、实际几何、必需端点连通、fresh DRC、许可范围与人工视觉各自列结论。任一解析、求解或重新打开未完成，都保留具体待办。只读复核不应重保存源件；交付时包含可复现的工程私有参数、必要脚本、输入身份、日志和差异说明，学习库只保留本文这类方法。

## 本机官方资料入口

以下均相对 `<Cadence根>`；先核实际安装版本，不把旧机器路径写进通用脚本：

- `share/pcb/examples/skill/DOC/QIR/NEW/axlParamShapeDoc.txt`：动态／静态参数、`Full contact` 和静态下一次重避让的边界。
- `doc/algroshapes/algroshapes.html`：`1035538` 参数层级、`1035487` 优先级、`1039225` 转换限制。
- `doc/propref/properties.html`：`931032` VIA_THERM_CONN、`854493` THRU_THERM_CONN、`915361` DYN_THERMAL_CON_TYPE、`851398` DYN_DO_NOT_VOID。
- `doc/algroskill/02dbdesc.html`：动态边界／生成铜／dynamicGroup、设计和 DRC 对象属性。
- `share/pcb/examples/skill/DOC/FUNCS/` 下的 `axlShapeDynamicUpdate.txt`、`axlShapeRaisePriority.txt`、`axlShapeAutoVoid.txt`、`axlShapeChangeDynamicType.txt`、`axlDBCreateVoid.txt`、`axlDBGetConnect.txt`、`axlPolyFromDB.txt`、`axlPolyOperation.txt`、`axlDRCUpdate.txt` 及各域 `ModeGet` 说明。
- `share/pcb/consmgr/cmdict.l`：FULL_CONTACT 对象枚举、普通 Shape 间距和验证模式；`doc/fcoms/fchap.html` 的 `1109031` 为 Update to Tier 描述。

相关入口：[通用转换流程](ad_to_cadence_conversion_workflow.md)、[规则迁移方法](ad_to_allegro_constraint_migration.md)、[层名与层功能](pcb_layer_naming.md)。
