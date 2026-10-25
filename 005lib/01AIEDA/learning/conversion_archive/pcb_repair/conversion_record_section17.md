
## 十七 2026-10-23：以原 AD 为基准修复原理图和 PCB 转换损失

用户后续要求：“理论上 按照ad的工程是原版 更改cadence的原理图 或者修复 allegro的pcb”。本轮以原 AD 原理图和原 AD PCB 分别为权威基线，修复两种派生格式已证实的转换损失；保留原资料 Sch/PCB 之间已有的设计差异。此前“先保留这些差异”的要求继续适用于安装孔、USB 引脚等源设计差异。

### 当前交付入口

新目录：[04AD_original_repair_20261023](./04AD_original_repair_20261023)。

- [Capture 工程](./04AD_original_repair_20261023/sch/LGA1700_AD_REF.opj)
- [原理图 LGA1700.DSN](./04AD_original_repair_20261023/sch/LGA1700.DSN)
- [修复后的 Allegro PCB](./04AD_original_repair_20261023/pcb/LGA1700_AD_PCB_repaired.brd)
- [使用说明](./04AD_original_repair_20261023/使用说明.md)
- [完整工程 ZIP](./LGA1700_AD_original_repaired_20261023.zip)

目录内包含 OPJ、DSN、OLB、BRD、PST 网表、1067 个 PSM、1067 个 DRA、138 个 PAD、器件定义、本项目库环境和验证报告。原 AD 文件、`01sch`、`02pcb` 及公共库均未覆盖。`03repair_review_20261023` 保留为上一阶段历史快照。

### 原理图：以 Altium 原生编译连接为准

在本机 Altium 18.0.7 中通过官方脚本接口，对原 AD 工程的独立 39 文件副本进行编译，导出扁平网络与活动物理引脚。35 页共 6608 个活动引脚；1871 个原生网络对象中有 4 个空网络，物理连接比较采用 1867 个非空分区，即 1085 个多引脚分区、782 个单引脚分区。没有把同名的局部网络强行视为同一网络。

最终修复包括：

1. 按源 AD 的真实电气端点恢复 1147 个 Off-page connector，其中 576 个在 Port 原点、571 个在其右端。没有仅按文字位置放置连接。
2. 校正 496 个接地符号热点；原 343 个 VCC 类符号热点保持。按原 AD 编译的 GNDA 八脚同网关系补一个原生 GNDA 全局接点，最终 840 个全局电源对象。
3. 按原 AD 线段几何恢复 493 条导线端点；包括 USB 后置页面误延长到数据线的接地线，消除 USB_PN6/GND 误连。负半数坐标按 Tcl round 的 AwayFromZero 规则处理。
4. 用 16 段一个文档单位的短线恢复 DIMMA1 DQS 源零长度连线的真实引脚连接，保存重开与 PST 中均存在。
5. 为 17 个源局部分区的 19 个 Alias 使用带作用域名称，避免与同名跨页 Port/电源误合并；原名、源网络及修改原因保留在所属导线上。GNDA 结论以实际原生编译结果为准，替代上一节尚待确认的判断。
6. 保留此前 Q39 的封装名修复和 Device 冲突修复。外部 OLB 的 215 个 part 清理 Device→AD_DEVICE，其他库属性、184 packages、4221 pin mappings、2056 vectors 均无非预期变化。Q39 使用的库 part 由 27 个位号共用，因此外部库默认封装未全局更改，正确值保留在 Q39 实例中。

原生 SDK 直接保存新短线后曾发生 B0 页封装元数据异常：虽然文件有 6608 个引脚，但 PST 缺少该页部分元件并报错，故未交付。最终采用 Cadence 原生 XMATIC 的 DSN→XML→DSN 重建数据库对象 ID，再重新执行完整检查。XML 导入记录中的旧 PortOccurrence 引用提示已保留在 staging，未据此忽略最终验证。采用的文件已通过下述独立检查。

最终工程中 35 页、1131 个实例、6608 个引脚完整；元件值、封装、位置、旋转/镜像，引脚身份/名称/位置/NC，以及 AD 来源追溯属性均核对通过。XML 将 USB_PN6 的两条相邻共线段合法合并为与原 AD 对应的一条，最终 8628 个 wire 对象；其余变化均已逐项核准。

**从实际交付路径 DSN 原生导出 PST 返回 0、错误 0。对最终 PST 与原 AD 编译结果逐脚比较：6608 个引脚无缺失、无额外；1867 个非空分区完全一致；源网络拆分 0、目标误合并 0、引脚归属差异 0；2,145,791 对同网引脚关系全部保持。** 自动网络名及局部限定名有差异，仅网络文字不同不等于连接错误。

最终交付 DSN SHA256：`81924DF03109CC8D2222B3558CE0C6B18EF56CBDB078CE522F36632D113BE268`。XML 重建后初始副本的哈希为 BC541…AC38F；原生 PST 打包更新了交付 DSN 的元数据，最终又以实际交付文件重新进行对象读回与逐脚网络验收。

### PCB：恢复 F_USB3，全部源焊盘逐一验证

重新按全部 symbol 的 pin 实体核查：原 AD PCB 与转换板均有 **6521 个实际焊盘**。此前 6485 是已关联逻辑元件的 pin 统计口径，另有 27 个机械 pin 和 9 个孤立 F_USB3 pin；不能据此认定丢了 36 个焊盘。

确认所有焊盘实体已存在后，仅将 F_USB3 的现有孤立封装重新关联逻辑元件，并恢复原 AD PCB 的 8 个有网焊盘；脚 9 原本无网继续无网，未新增供电脚 2。没有重放、移动或替换封装，没有增删焊盘，没有从待修复 Capture 网表向整板写入网络。

保存后重新以 Allegro 原生只读方式打开，结果为 1066 components、1066 symbols、6521 pads、1103 nets。原 AD 的 5745 个有网焊盘和 776 个无网焊盘身份/网络全部一致；0 缺失/额外，0 源网络拆分，0 误合并。82408 条显式几何与动态铜皮用户边界记录保持一致。

恢复网络时 Allegro 正常重新计算了部分动态填铜，26 条旧生成几何消失、10 条新生成几何出现；另将 F_USB3 assembly 位号文字从 `.DESIGNATOR` 改为 `F_USB3`。这些变化已单列，没有声称所有派生填铜逐字不变。原有 8 个过期动态 shape 仍为 8 个，未擅自进行全板更新。

最终 PCB SHA256：`1D0760CFCE9CDA2A2AADC6891A4D434E5703424FF4F4C841383BC78586866D25`。

### 实际导入检查与尚存差异

直接使用本次交付的 PST、BRD 和独立 libraries/pcbenv 再次执行严格原生 `netrev -e -y 2`。没有启用走线拆除或忽略 FIXED；输入输出为不同文件。缺失封装 `SPMHNI-194` 为 **0**，说明本项目库路径与封装名称问题已解决。

原 Sch/PCB 引脚定义差异仍导致 16 组 device/symbol 检查错误，加停止项共 17 errors，返回 2，没有生成 ECO 结果板。详细日志在 `verification/library_import_test/netrev.lst`。这不是原理图导出失败，也不应靠忽略错误或改写 PST 解决。

保留的差异包括：31 个原理图独有电阻、6 个安装孔的 16 脚/4 焊盘定义、F_USB1/F_USB3 的脚 2/脚 9、CN/DIMM/PCH/PCIe 的重复或额外 NC 脚，以及源 Sch 局部网络和 PCB 网络归并的差异。后续整板同步需要明确设计意图后再修改源定义。此次完成的是两种转换结果各自忠实于原 AD，不代表源 Sch 与源 PCB 本来已经一致。

Altium 原生编译还有 12003 条未分类诊断，本次未将其认定为全部致命错误，也未宣称原工程 ERC 清洁；PCB 未作全板 DRC/生产签核。当前交付用于继续设计与复核。

### 主要证据

- `verification/final_pst_export.json`：实际交付 DSN 的原生导出状态及哈希。
- `verification/ad_native_partition/`：最终逐脚网络分区与 AD 原生 gold 比较。
- `verification/ad_native_gold/`：AD 原生扁平网络、引脚和原文件哈希基线。
- `verification/source_manifest/`：源对象、导线修复、Alias 追溯等独立验收。
- `verification/xml_roundtrip/`：对象重建前后差异及允许归一化的完整验证。
- `verification/pcb/`：6521 个焊盘逐一对照及 PCB 保存重开验证。
- `verification/library/`：外部 OLB 属性清理和原生重开审计。
- `verification/library_import_test/`：交付库路径的严格导入试验与保留的脚号差异。
- `verification/original_files_unchanged.json`、`文件校验.csv`：原输入不变与交付文件完整性。

全部原生脚本、日志、源语义调查、失败试验和 XML 中间文件仍保留在 `D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023`。大型 XML/Tcl 临时文件及失败候选没有混入交付工程。
