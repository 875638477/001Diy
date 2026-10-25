# 第13课：多单元符号、电源脚与网络作用域

日期：2026-10-19（Asia/Shanghai）。本课已完成 **Capture 17.2 原生数据库实做与独立进程读回验收**；验收17项全部通过。执行环境为安装目录所附 Tclsh 8.6.0 和 `orDb_Dll_Tcl64.dll` 17.2.2016045，不把这一结果写成 Capture GUI 菜单或 Tcl 命令窗已通过。

最终原生工程：[c13_scope_v8.dsn](../examples/lesson13_capture/c13_scope_v8.dsn)。最终判据与逐项证据：[c13_acceptance.json](../logs/capture_C_20261019/c13_acceptance.json)。本课是网络规则练习；存在刻意不接线的引脚，不作为可投板电路发布。

## 学习与实做范围

**多单元的适用范围（用户明确，2026-10-19）：** 普通器件尤其普通 MCU 优先采用包含全部引脚的单单元符号；CPU 等复杂器件可按功能需要分单元。拆分后仍属于同一个物理器件、同一基础位号及同一 PCB 封装，完整核对物理引脚映射，不得遗漏或错误重复。本课 74HC00 多门练习用于学习已有多单元结构和作用域，不将其做法推广为普通 MCU 默认。电路模块分页面与器件符号分单元分别判断。详见 [长期符号规范](capture_symbol_defaults.md)。

| 项目 | 实做与结论 | 证据 |
| --- | --- | --- |
| 多单元器件 | 74HC00同一封装4个功能单元；A/B/C/D分别放置为U1A/U1B/U1C/U1D | 原生OLB引脚读回20行，合并后14个物理编号 |
| 隐藏电源脚 | GND7和VCC14在4个单元重复出现；不是新增8个物理焊盘 | FlatNet里4个GND7共享一个网，4个VCC14共享一个网 |
| 同页别名 | TOP1两段不接触的SAME_PAGE导线合并 | 两段wire的flat_id相同 |
| 跨页同名别名 | TOP2的SAME_PAGE与TOP1分离 | TOP2原生解析名SAME_PAGE_73，与TOP1的SAME_PAGE为不同flat_id |
| 跨页连接器 | TOP1/TOP2的CROSS_PAGE用off-page connector连接 | 两页wire位于同一FlatNet |
| 层次局部网 | CHILD_A和CHILD_B均有LOCAL别名 | HA/LOCAL与HB/LOCAL的flat_id不同 |
| 层次端口 | 顶层HA/HB块均有H_SIG引脚，子页有同名hierarchical port | PARENT_SIG_HA与HA/H_SIG相同flat_id；HB对应同理；两分支分离 |
| 全局电源 | VCC跨顶层及HA/HB子层次 | VCC、HA/VCC、HB/VCC同一global FlatNet |
| 可见POWER明确接线 | 子层次各放置一个第12课QMI8610，将VDDa2接LOCAL_PWR_A/B | 两脚type=7、visible=1、raw_global=1，但所属实际FlatNet不同且global=0 |
| 总线 | DATA[0..1]经bus entry接DATA0、DATA1 | 共同bus几何出现于两个成员的网络关系中，DATA0与DATA1保持两个FlatNet |
| 实际引脚连接 | U1A两输入接NAND_IN_A/B，输出接NAND_OUT_A | 原生物理编号1/2/3，电气类型Input/Input/Output |
| 交换规则 | 读取4单元全部20个device-pin swap id，均为-1 | 未凭逻辑等价或homogeneous属性擅自允许自动交换 |

验收读回共26条net occurrence、24条wire成员关系、21条pin成员关系。成员关系不是唯一几何对象数量：一条总线几何可出现在DATA0、DATA1两个成员关系里。

## 多单元与物理编号

| 单元 | 输入A | 输入B | 输出Y | 共用GND | 共用VCC |
| --- | --- | --- | --- | --- | --- |
| A | 1 | 2 | 3 | 7 | 14 |
| B | 4 | 5 | 6 | 7 | 14 |
| C | 9 | 10 | 8 | 7 | 14 |
| D | 12 | 13 | 11 | 7 | 14 |

来源为TI SN74HC00 / SN54HC00资料SCLS181H（2021-08修订），PDF第3页的14脚封装图与Table 5-1。该页同时列出20脚FK封装，当前练习只使用其14脚列，不能混用编号。已视觉复核[第3页图像](../staging/capture_C_20261019/ti_sn74hc00_pdf003.png)。[本地原厂PDF](../staging/capture_C_20261019/ti_sn74hc00_scls181h.pdf) SHA-256：`E53F9214ECB928B870DA41E540821FC182559BDAD2611FE7047CC9D9693A4C75`。

实做库使用安装目录`library/pspice/74hc.olb`的学习副本[hc_source.olb](../examples/lesson13_capture/hc_source.olb)，读取package `74HC00`、part `74HC00.Normal`。原生结果是package size=4、homogeneous=1。这里沿用库的多单元结构，不声称手工从零绘制了该原厂库图形，也不把符号当成经过本课电气仿真验收的PSpice模型。

物理脚号必须从`DboDevice.GetPinNumber(position)`取得。`DboSymbolPin.GetPinPosition`是单元内位置索引，不是封装编号；只看符号名称A/B/Y不足以确认实际引脚。原生表见[c13_hc00_pins.tsv](../logs/capture_C_20261019/c13_hc00_pins.tsv)。

**同一个物理封装还必须共享基位号。** 最终v8四个74HC00实例的raw Reference全部为`U1`，device designator分别A/B/C/D；转成`DboPlacedInst`后读取的完整ReferenceDesignator精确为U1A/U1B/U1C/U1D。不能把DboPartInst基类的GetReferenceDesignator结果当成完整位号，它在本机仍只返回基位号。验收已新增这一项；[完整位号读回](../logs/capture_C_20261019/c13_fullrefs_v8.tsv)保留raw/full/device三列。

QMI8610最终改用第12课正式[c12_qmi8610_single.olb](../examples/lesson12_capture/c12_qmi8610_single.olb)，package为QMI8610_C12_SINGLE、device suffix为空。U2/U3的raw和完整位号均分别为U2/U3。早期v7曾把HC实例raw设为U1A/U1B/U1C/U1D，实际上得到U1AA/U1BB/U1CC/U1DD，且旧QMI库会得到U21/U31；因此v7不能作为同物理封装的最终验收产物。问题经placed类的独立读回发现后，另建v8修正，没有覆盖v7历史文件。

## 电源脚的三个不同问题

1. **是否可见：** 决定编辑器是否画出/显示该pin。
2. **库里raw IsGlobal字段：** 17.2把POWER脚保存、重开后保留为1，不能只凭这一位判断每次实际接线归属。
3. **实际展开后的FlatNet：** 本课用保存后独立进程重开及网络展开读取，直接核对最终作用域和物理引脚成员。

74HC00隐藏的GND/VCC自动按全局电源网连接。本课第12课QMI8610的VDDa则为可见POWER脚：HA/U2.VDDa2明确接LOCAL_PWR_A，HB/U3.VDDa2明确接LOCAL_PWR_B。两脚raw_global均为1，实际网络分别为LOCAL_PWR_A、LOCAL_PWR_B，两个FlatNet不同，global均为0。

反例也保存了：没有明确接线的QMI VDDd/GNDd/GNDa在本实验中按名称成为VDDD/GNDD/GNDA全局网络。因此“把电源脚显示出来”本身不能保证局部作用域；应明确接线，并复核展开后的网络。原厂Capture帮助`Making_power_pins_visible.html`和`Creating_a_Part_Body.html`对可见电源脚与接线的说明，与本课实测相符。

这不是完整供电接法示例：QMI8610保留脚、供电去耦、NC等实际设计要求仍按第12课资料执行；当前仅测作用域。

## 网络命名与层次

同页net alias可以合并同名导线；跨页连接应使用off-page connector。本课故意把相同的SAME_PAGE文字放在TOP1/TOP2，用原生网络证明它们分离。原生解析名可能附加对象编号用于消歧，不应把这种临时名字作为外部稳定接口。

顶层两个drawn hierarchical block分别引用CHILD_A、CHILD_B，ContentsViewType=SCHEMATIC_VIEW_TYPE，IsPrimitive=NOT_PRIMITIVE。每个块的H_SIG引脚只与所引用子页的同名hierarchical port绑定；它们不是全局信号。HA/LOCAL与HB/LOCAL仍然不同。VCC则作为global跨越这两个层次。

总线是标量信号集合，不是把全部位短路的铜线。DATA[0..1]对应DATA0和DATA1，标量别名不带方括号。bus entry提供连接图示；位的对应仍要由名字验证。原厂帮助`Bus_connectivity.html`、`Wire_connectivity.html`均明确总线与标量的名称匹配规则。

## 保存、重开与验收方法

最终DSN创建与读回分属不同私有Tclsh进程：

- [创建日志](../logs/capture_C_20261019/c13_create_v8.tcldict)：PID 29140，退出code=0。
- [网络读回日志](../logs/capture_C_20261019/c13_verify_v8.tcldict)：PID 24148，code=0。
- [页面/实例读回日志](../logs/capture_C_20261019/c13_inspect_fullrefs_v8.tcldict)：PID 29508，code=0；保存后可见TOP1、TOP2、A1、B1及各自实例与逐脚编号。

创建阶段逐页MarkModified、SavePage，逐schematic保存，再SaveDesign、RemoveDesign。不能把“内存对象已存在”当成文件已经保存。

本机独立17.2 SDK重新读取多页TOP时，初始网络容器只覆盖最后一页。对两页TOP显式调用官方`DboSchematic.Expand()`后，才取得完整图；单页CHILD_A/B不重复Expand。最初对所有schematic反复Expand曾产生重复旧容器，已修正，最终读回没有这种重复。`IsExpanded=1`也不足以替代逐页wire核对。

读取路径：`GetDesign` → TOP `Expand` → `GetRootOccurrence` → `NewFlatNetsIter` → `NewNetOccurrencesIter` → occurrence `GetNet` → **DboSchematicNet** `NewWiresIter/NewPortInstsIter`。所有返回对象在调用前检查非NULL。

逐项判据由Python独立读取原生TSV，与TI手册引脚表和网络连通关系比较，未只验证“脚本跑完”。[c13_validate.py](../scripts/c13_validate.py)可直接重跑17项验收；它不修改DSN。

详细读回：

- [网络与层次路径](../logs/capture_C_20261019/c13_flat_occurrences_v8.tsv)
- [导线和总线成员](../logs/capture_C_20261019/c13_flat_wires_v8.tsv)
- [物理引脚及显隐/电气类型](../logs/capture_C_20261019/c13_flat_pins_v8.tsv)
- [页面/实例完整清单](../logs/capture_C_20261019/c13_inspection_v8.tcldict)

## 异常记录与已停用路径

本课早期有两类原生调用失败，已保留过程日志，不把失败隐藏为成功：

- 关闭后的`GetOpenDesign`返回NULL；早期探针未先判空，对NULL执行`DboDesign -this`造成原生进程退出。该探针已停用。
- 本机17.2的**DboFlatNet.NewWiresIter**路径发生native crash，并曾出现Windows/Visual Studio即时调试器提示。没有启动VS或修改系统异常/调试器配置。后续转为独立批处理进程隔离，再改用已实际验证的**DboSchematicNet.NewWiresIter**安全路径。

用户截图中的PID 31400检查时已不存在；当时没有任何tclsh进程可再清理。未终止不明归属的Capture进程，未删除其可能使用的lock。已停用的helper/NULL探针保存在[历史文本快照](../staging/capture_C_20261019/c13_retired_history/)，不再作为可执行验证入口。v1—v7和失败日志保留供追溯，**交付与验收只引用v8**。

后续学习使用[c13_batch.tcl](../scripts/c13_batch.tcl)私有进程包装器、[c13_helpers.tcl](../scripts/c13_helpers.tcl)、[c13_run16.tcl](../scripts/c13_run16.tcl)创建入口（已有文件时拒绝覆盖），[c13_run17.tcl](../scripts/c13_run17.tcl)只读网络入口、[c13_run18.tcl](../scripts/c13_run18.tcl)只读页面入口。包装器记录owned PID并正常退出；不连接用户Capture会话。

## 本课结论与后续衔接

多单元图形、单元内pin position、物理封装编号和最终FlatNet成员必须分别核对。本课已覆盖同页/跨页/层次/全局/总线这五种作用域，给第14课提供真实的编号、显隐、电源和网络判据。

仍未声称通过的项目：Capture GUI命令窗口、交互式gate/pin swap、PSpice仿真及生产电路ERC/投板。本课没有执行交换；homogeneous=1和逻辑对称性不足以代替明确swap group、约束和回标规则。本课完成边界是独立练习DSN的原生数据库实做与读回，不修改公共元件库。
