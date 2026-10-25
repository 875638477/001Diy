# 第14课：符号—封装关联与库更新传播

学习日期：2026-10-19，Asia/Shanghai。软件与原生数据库：Cadence Capture 17.2；课程依据本机官方用户指南、Tcl 扩展手册和随附示例。本课核心验收已完成：真实 OLB 修改后，经受控原生替换更新已有 DSN，保存关闭，在另一个原生进程中核对编号、图形、属性、来源及网络。GUI 菜单操作和 UpdateCache／ReplaceCache 参数映射没有计入已验证范围。

## 可打开的实际产物

| 文件 | 用途与状态 |
| --- | --- |
| [c14_ready.dsn](../examples/lesson14_capture/final/c14_ready.dsn) | 推荐后续衔接的练习。U1401／U1402 都关联真实 QMI8610 足迹；已由独立原生进程重开验证。 |
| [c14_replace_properties.dsn](../examples/lesson14_capture/final/c14_replace_properties.dsn) | 属性替换分支，与 ready 的内容相同。 |
| [c14_update_preserve.dsn](../examples/lesson14_capture/final/c14_update_preserve.dsn) | 保留显式实例覆盖的分支；U1402 保留足迹测试标记，不用于 PCB 导入。 |
| [c14_relocated_preserve.dsn](../examples/lesson14_capture/final/c14_relocated_preserve.dsn) | 新库来源并保留覆盖的对照；本轮实际成功方法与上一分支相同，不能把文件名理解为 UpdateCache API 已通过。 |
| [c14_qmi8610_v2.olb](../examples/lesson14_capture/final/library/c14_qmi8610_v2.olb) | 最终原生 OLB，器件 QMI8610_C12；单单元 designator 为空，Value／MPN／LIB_REV 为 V2。 |
| [library](../examples/lesson14_capture/final/library) | OLB、PAD、DRA、PSM 完整依赖。 |
| [c14_baseline.dsn](../examples/lesson14_capture/run04/c14_baseline.dsn) | 保留更新前 V1 缓存、两个实例和两条信号网的原生基线。 |
| [validation.json](../logs/lesson14_capture_20261019/validation.json) | 最终独立读回比较：81 项检查通过，errors 为空。 |

这些是连接与库管理练习，尚未完成真实应用电路的所有连接、ERC 和板级导入；`ready` 表示本课库关联结果已整理好。没有修改公共元件库或用户 Cadence 环境设置。

## 需要掌握的库关系

OLB 保存符号及封装属性，DSN 中的 Design Cache 保存已放置器件的本地副本。保存 OLB 不会自动使已有实例采用新图形和新属性。实例又可以覆盖 Value、MPN、PCB Footprint 等属性，因此必须分别核查源库、缓存和实例，不能只检查库路径或一个属性。

`PCB Footprint` 是足迹名称，不含 `.psm` 扩展名。本例使用 `qmi8610_lga16_3d3_p0d5`。Capture 的物理脚号必须和 Allegro 封装一致：这里是 1—16，没有中心 EP17；器件资料及电气类型的逐脚依据见第12课。SymbolPin 的内部 position 是 0—15，真实物理编号来自 Device.GetPinNumber；不能将迭代顺序当作脚号。

库路径变化、库内容更新、已有实例属性更新是三件需要分别验收的事。ReplaceSourceLibName 只改变来源字符串，不能代替内容更新。更新后也不能继续使用旧对象或旧 FlatNet 指针作为保存后的连接证据。

## 本轮原生实做

1. 从第12课已验收 OLB 建立隔离 V1 库，设置 Value=QMI8610_V1、MPN=QMI8610_MPN_V1、LIB_REV=C14_V1。单单元 device designator 从 `1` 改为空，避免完整位号变成 U14011／U14021。
2. 创建真实 DSN 的 TOP／PAGE1，放置 U1401 和 U1402，位置分别为 (500,500)、(1000,500)。两个物理14脚分别连接 C14_SCL_1、C14_SCL_2。
3. U1402 显式覆盖 Value、MPN、自定义属性和 PCB Footprint；足迹覆盖值是 `C14_PROP_SENTINEL_NOT_FOR_PCB`。覆盖清单写在脚本中，不通过“与库当前值是否相同”来猜测覆盖。
4. 源库 V2 增加一条对角线，原生图形由4条线变成5条线；Value、MPN、LIB_REV 和库默认自定义值改成 V2。16个脚号、电气类型、脚热点与外框坐标保持不变。
5. UpdateCache／ReplaceCache 的初次调用没有达到传播判据，保留其日志。随后使用已确认有效的原生 `DboPage.ReplaceInst` 替换既有实例，再明确恢复位号及所选覆盖。A、B 两个保留分支本次走同一受控替换路径；C 分支采用库的 V2 属性。
6. 每页 MarkModified／SavePage，实例修改后 MarkModified，再 SaveDesign、RemoveDesign。另起原生 Tclsh 进程重新打开 DSN，从已完整加载的单页原理图生成新的 occurrence／FlatNet 读回连接；不重复强制 Expand。
7. 复制原有 B8 学习目录中的实际 PAD／DRA／PSM；逐文件 SHA-256 与原文件一致。最终 ready 又作为独立 DSN 重开核查。

保存返回成功并不足以验收；必须确认关闭重开仍有页面、实例、更新后的图形及属性。直接 NewPlacedInst 可以从源 part／device 建立缓存；本轮先 CopyPackageAllToCache 后取设备的尝试返回了 NULL，失败中间文件保留，未作为有效基线。

## 结果对照

| 检查项 | V1 基线 | 保留覆盖 A／B | 替换属性 C／ready |
| --- | --- | --- | --- |
| 实例位号 | U1401、U1402 | 均保持 | 均保持 |
| 缓存图形 | 4条线 | V2，5条线 | V2，5条线 |
| 缓存 LIB_REV | C14_V1 | C14_V2 | C14_V2 |
| U1401 Value／MPN | V1 | V2 | V2 |
| U1402 Value／MPN | INSTANCE_* 覆盖 | 保留 INSTANCE_* | 采用 V2 |
| U1402 自定义覆盖 | INSTANCE_CUSTOM_OVERRIDE | 保留 | LIB_DEFAULT_V2 |
| U1402 PCB Footprint | 测试标记 | 保留测试标记 | qmi8610_lga16_3d3_p0d5 |
| 活跃实例源库 | run04 的 V1 来源 | final/library 的 V2 OLB | final/library 的 V2 OLB |
| 物理编号／脚名／类型／热点／位置 | 基线 | 逐项不变 | 逐项不变 |
| 原生连接集合 | 基线 | 完全一致 | 完全一致 |

最终独立连接读回每份文件有10行成员记录、10个唯一的 `(flat_net, reference, pin_number, pin_name, page)` 元组：四组电源各接两个器件，共8个成员，加两个各自独立的 SCL14 成员。两个信号网各自只包含对应器件的14脚，没有合并成同一网。对比使用全部10个成员，更新前后完全一致。

最终 OLB 与已放缓存均显示物理脚号。实验中曾将源 pin4 的单独 `numberVisible` 改成0，但 ReplaceInst 后缓存读回为1，不能声称该单独显示标志已传播；最终交付库已明确恢复为1，并再次原生重开核对。此现象与第12课的 POWER raw-global 位同样说明：原始标志、实际图形及实际连接需要分别判断。

## 自动 API 的边界与失败记录

- 初次 UpdateCache 返回 success，缓存仍是 V1；它不符合图形／属性传播验收。ReplaceCache 一支返回 Failed。之后的诊断出现无效／NULL 原生对象，已停止探测并禁用相关诊断入口；不再对 NULL 调用方法。
- 本机原生 ReplaceInst 的保留位号参数没有得到预期结果，直接读回一度为 `U?`。成功方法明确保存原 reference、替换后 SetReference、MarkModified，并以独立重开结果证明保持了 U1401／U1402。
- ReplaceInst 保留了旧的未使用缓存条目。最终同时记录旧、新两个来源；验收检查每个**活跃实例**的 GetSourceLibName 指向 V2，而没有要求整个缓存表仅剩新来源。旧缓存未被冒然清除。
- 实例 GetBoundingBox 在此 SDK 路径读回为 (0,0,0,0)，不作为图形正确的证据；图形验证采用 LibPart 的逐条原生 vector 端点、外框、引脚热点和实例位置。
- 早先强制 Expand 已完整加载的单页原理图，读回出现20行与额外生成的 SCL 名称。第13课最终证据确认此操作会重复内部容器；本课已在新进程中取消强制 Expand，重新读取基线、三个分支与 ready，均得到正确的10个唯一成员。此前 expanded 快照与 `validation_expanded.json` 只作为历史，不用于最终连接验收。
- 原始快照中未定义的可选属性显示 `ERROR:DbStateFailed:GetEffectivePropStringValue`，表示该读取没有对应属性；必检的 Value、MPN、LIB_REV、足迹、编号和图形字段均有明确有效值。初次失败验收保留为 [validation_initial.json](../logs/lesson14_capture_20261019/validation_initial.json)。

上述成功流程是受控原生替换及明确的属性策略，不能等同于已经操作并通过 Capture GUI 的 Update／Replace Cache 对话框。后续可在界面通道可用时单独补做 GUI 属性模式与标志映射；本课已有工程更新与持久化的核心结果无需依赖该映射。

## 后续继续的方法

继续练习请从 `c14_ready.dsn` 开始。Capture 放置库添加 `final/library/c14_qmi8610_v2.olb`；Allegro 在学习用工程的 User Preferences → Paths → Library 中，把下面同一个目录添加到 `psmpath` 和 `padpath`：

`D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/final/library`

本次只写出配置说明，没有修改用户 env。psmpath 用于查找 PSM 等符号，padpath 用于查找 PAD；DRA 是可编辑源，PSM 是用于放置的编译封装。导入前核对 Capture 中两个实例的 `PCB Footprint=qmi8610_lga16_3d3_p0d5`、物理脚号1—16及 B8 封装定义。

| 依赖 | 字节数 | SHA-256（完整值见 validation.json） |
| --- | --- | --- |
| qmi8610_lga16_3d3_p0d5.dra | 71560 | 706d2be58e091644… |
| qmi8610_lga16_3d3_p0d5.psm | 14224 | d67bf02f0172ee03… |
| qmi8610_smd061x032_m05_p100.pad | 3656 | d36328465d8f50fa… |

后续更新应先保留源库和 DSN 基线，再逐项比较来源、位号、物理编号、图形、实例覆盖和网络；最终使用新的原生进程重开。保留覆盖的两个分支只用于理解传播策略，不直接用于 PCB 导入。

## 证据与复核入口

- [官方资料研究记录](lesson14_research_20261019.md)：用户指南对 Update／Replace 属性策略的表格与本机文档路径。
- [最终独立读回目录](../logs/lesson14_capture_20261019/independent_natural)：每个工程的原生 cache、package、instance、connectivity 快照，以及最终 OLB 读回。
- [进程执行日志](../logs/lesson14_capture_20261019/batch)：controlled07、normalize09、verify_natural11 均 exit0、code0；失败／超时批次分开保留。
- [最终比较程序](../scripts/c14_validate_results.py)：只比较已保存原生读回，记录81项结果与依赖 SHA。
- [受控替换脚本](../scripts/c14_controlled_update.tcl)、[独立验证脚本](../scripts/c14_independent_verify.tcl)、[原生批处理入口](../scripts/c14_native_batch.py)。创建脚本防止覆盖已有结果；不要在同一最终目录直接重复创建。

所有记录、脚本、试错文件、中转、备份和原生文件均在 `01AIEDA/learning` 内。旧失败锁文件保留在各自历史目录；最终交付目录没有本轮遗留的原生锁文件。本课未调整课程总索引，由主任务统一登记。
