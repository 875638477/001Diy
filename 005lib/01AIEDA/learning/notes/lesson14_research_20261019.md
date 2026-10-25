# 第14课 Capture 库更新传播研究与实验方案

日期：2026-10-19，Asia/Shanghai。课程按根目录60课索引的 C 阶段执行。研究对象是本机 `C:/Program0/Cadence/SPB172` 官方 Capture 文档与随附 Tcl；本文件记录已读资料、待原生验证的接口和实验判据。Capture 运行由根 agent 独占，本研究没有启动 GUI、编辑用户工程或修改公共库。

## 已确认的设计缓存模型

首次放置库器件后，设计内保存 LibPart、Package 等本地副本，实例通常引用这个缓存，并保留原始库来源。原始 OLB 保存成功不代表已经放置的实例更新。

官方 `capinfomodel/dboimnew.html` 说明：UpdateCache 用于让既有实例符合缓存中的器件版本；CacheIsOutOfDate 比较源器件与缓存时间戳，源器件较新时判过期。ReplaceCache 可用于移动库路径或切换表示。更新后要重新取得数据库对象；修改设计后，FlatNet 需要重新计算，它不是磁盘持久化的实体，不能继续用更新前的 FlatNet 指针当连接证据。信息模型称重算函数为 UpdateFlatNets，但本次在随附 Tcl 方法目录没有找到该名称，不能把 C++ 描述直接当作已确认的 Tcl 调用。可在保存关闭后用新会话重开设计，再通过官方 NewFlatNetsIter 路线重新生成读回证据。

`cap_ug` 两篇更新帮助在表格中给出的行为如下。正文中关于同名检查的语句容易被读成“同名一定不更新”，本课以时间戳说明与实际保存、重开读回共同判断。

| 检查对象 | Update Cache | Replace 保留原理图属性 | Replace 替换属性并保留 RefDes |
| --- | --- | --- | --- |
| 符号图形与引脚 | 更新 | 更新 | 更新 |
| 库级属性值 | 未在实例改过则更新，改过则保留 | 同前 | 更新 |
| 原理图实例／occurrence 属性值 | 保留 | 保留 | 更新 |
| 位号 | 保留 | 保留 | 保留 |
| 引脚属性值 | 未在实例改过则更新，改过则保留 | 同前 | 更新 |
| Package 级属性，如 PCB Footprint | 保留 | 保留 | 更新 |
| 引脚属性的显示位置／坐标 | 更新 | 更新 | 更新 |
| 器件属性的显示位置／坐标 | 保留 | 保留 | 更新 |

替换属性而不保留 RefDes 是第四种模式，官方表格注明位号也会更新；本课主实验明确保留位号。Replace 可以改 part 名称、库及路径并强制重载；Update 继续使用原有链接。保留属性的 Replace 与 Update 在属性处理上相同，但来源选择能力不同。

尤其要分别读取缓存 Package 的 PCB Footprint 和已放实例的 PCB Footprint。官方 `capUtils/capSyncPropPCBFootprint.tcl` 专门比较这两个值，再显式调用实例 SetPCBFootprint；不能仅看到缓存更新就认为实例足迹已同步。

## 原生接口与读回方法

接口来自随附 `OrCAD_Capture_TclTk_Extensions.pdf`，尚需在当前 Capture 对象上验证实际调用和标志含义。

| 用途 | 接口或官方实现 | 依据 |
| --- | --- | --- |
| 同来源更新 | `DboLib.UpdateCache(sourceLibName, sourceObjName, nObjType, bUpdate=1)` | PDF 205–206页 |
| 更换来源／替换 | `DboLib.ReplaceCache(oldName, oldLib, newName, newLib, bUpdateCache=0, bPreserverefDes=0)` | PDF 206页 |
| 缓存来源及对象 | `GetSourceLibName`、`GetCachedPackage`、`NewCachesIter` | PDF 198–199页；官方 ReplacePath 脚本 |
| 缓存导出 OLB | `NewCachesIter`→PACKAGE→`CopyPackageAll`→`SaveLib` | `capDB/capExportDesignCache.tcl` |
| 库符号脚名与图形脚位 | Package→Device→Cell→LibPart→`NewLPinsIter`→SymbolPin | `orctclcap/Getting_Pin_Names_from_a_Library_Part.html` |
| 物理脚号 | `Device.GetPinNumber(pinPosition, CString)` | PDF 724–726页 |
| 实例脚号、可见性与网络 | PortInst 的 `GetPinNumber`、`GetPinName`、`GetPinType`、`GetIsVisible`、`GetIsNumberVisible`、`GetIsNoConnect`、`GetHotSpot`、`GetNet` | PDF 542–545页 |
| 库脚图形属性 | SymbolPin 的位置、起点／热点、可见性、脚号可见性、NoConnect | PDF 602–605页 |
| 实例与缓存足迹 | 实例 `GetPCBFootprint`；`GetPackage` 后再读 package `GetPCBFootprint` | 官方足迹同步脚本 |
| 原生 XML | `XMATIC_ExportDesignInXML $design $CString` | `capDesignDifference/tcl/OrHandlerDesignDifference.tcl` |

物理编号不能从 SymbolPin 的数组顺序或 GetPinPosition 直接推导；必须通过 Device 映射。实例读回则可以直接取 PortInst 编号。原生 XML 示例的第二参数接收字符串，并非输出文件路径，保存文件时应另行写入学习目录。

`ReplaceSourceLibName` 只改缓存来源路径，随附 ReplacePath 工具还会核对新库对象。这一步不能代替 UpdateCache／ReplaceCache 的内容传播验证。

`Tools – Export Properties` 可以导出设计／库器件及引脚的 EXP，支持实例与 occurrence 模式；不能选中 Design Cache 作为导出对象。EXP 的 ID、Net Name、Net ID 等有规定格式，更新过程中只把它作为只读证据，不跨设计变化重新导入旧 EXP。直接 Tcl 读回和 XML 导出更适合作为本课前后快照。

## 与 C12 和 B8 的样例衔接

C12 协作样例约定为 package/cell `QMI8610_C12`、normal part `QMI8610_C12.Normal`、device designator `1`，计划由根 agent 生成练习库 `learning/examples/lesson12_capture/c12_qmi8610.olb`。本课实验应从其最终验收副本再复制，不能用尚未生成的文件充当完成证据。

Footprint 取 B8 已验收的 `qmi8610_lga16_3d3_p0d5`，物理编号必须仍为 1–16，无 EP17。C12 的 HOST_I2C 引脚电气定义和数据手册核验归 C12 记录，本课不另造真实器件脚表。

C12 协作本轮清点发现：历史 B8 发布所列公共 `01Psm_lib`／`01Pad_lib` 位置目前没有 QMI 文件；不能由历史记录推断当前仍存在。当前依赖采用 `learning/examples/qmi8610/library` 内原有 DRA／PSM／PAD，分别为 71560／14224／3656 字节。公共位置只登记现状，不在本课补发公共库；实验副本及结果均放本课隔离目录。

## 最小实验设计

实验尚未原生执行。建议目录 `learning/examples/lesson14_capture`，运行日志使用新的 `learning/logs/lesson14_capture_20261019/runNN`，禁止覆盖既有练习或公共库。

1. 固定基线。复制 C12 最终 OLB 和必要依赖到本课目录，以同一 OLB 路径保存 v1；保留 v1 文件、SHA、实际库对象来源及保存时间。建立练习 DSN，放两个实例 U1401／U1402，保存并重开。
2. 建立可判定的覆盖。设置不同的 `C14_INST_OVERRIDE`，一个实例保留继承的 Value／MPN，另一个明确编辑它们；另加 `C14_PIN_OVERRIDE` 用于区分库脚属性和实例覆盖。给若干信号脚连接具名网络，记录 `(RefDes,物理脚号)→net`，并记录脚热点、图形、可见性与足迹。
3. 创建 v2。在同一隔离 OLB 原路径保存新版本；改 `LIB_REV` 与一个未覆盖的库属性，增加非电气的图形标记 `C14_REV_V2`，改变未连接 NC 脚的显示状态。物理编号、引脚热点及真实电气类型保持不变。保存并关闭／重新取得库，使缓存时间戳判断能看到已落盘的新版本。
4. 为三个分支分别复制同一个已保存 v1 DSN。A 做 Update Cache；B 做 Replace 并保留原理图属性；C 做 Replace 替换原理图属性但显式保留 RefDes。每个分支均保存更新前、调用结果、即时读回、保存后的 DSN、关闭重开读回和导出缓存 OLB。
5. 单独验证来源变化。另存同 package 名的 v2 库到新路径。A 仍使用旧来源，B/C 显式 Replace 到新来源，读回缓存原始库路径，验证改来源不是只改字符串。
6. 分别验收图形／脚号／网络／属性。16个物理编号保持完整且唯一，热点与 `(RefDes,脚号)→net` 不意外变化；v2 图形标记和选定的显示变更出现；实例覆盖与库属性按各分支模式处理；RefDes 始终 U1401/U1402。
7. 验证足迹差异时，可在隔离属性实验副本给 U1402 一个明确标为 `C14_PROP_SENTINEL_NOT_FOR_PCB` 的实例足迹。Update／保留模式应保留该值，替换属性模式应回到库中真实足迹。这只是瞬时属性覆盖实验；最终继续 PCB 流程的练习副本必须显式恢复 B8 的真实足迹，并检查实际16脚对应与 PAD/DRA/PSM 依赖。
8. 保存最终练习文件，再用新的原生会话重开核对。比较学习源依赖文件的前后 SHA；公共位置若基线缺失，验收仍应为缺失且未被本课补写；若存在其他公共文件，核其未被改动。失败调用、错误标志、未变化的分支也保留，不把进程 exit0、保存成功或库路径字符串一致单独视为传播成功。

上面的 A/B/C 是 UI 行为模式。原生 `ReplaceCache` 的 `bUpdateCache` 只有名称和类型文档，本研究未确认 0／1 与 UI 属性模式如何映射，不能先认定“1就是保留”。根 agent 应先在可丢弃副本上两值对照，再把已测映射写入验收。最后参数 `bPreserverefDes` 明确传 1，避免依赖默认0。

## 已提供辅助脚本与当前验证状态

[c14_helpers.tcl](../scripts/c14_helpers.tcl) 只定义函数，source 时不执行 CAD 编辑。已用无 GUI 的 Tcl 解释器检查定义可解析；这仅是 Tcl 语法检查，不是 Capture 内部 API 验证。

- `probeSignatures`：列出相关原生命令是否存在以及无参数调用返回的签名。
- `snapshotPackage`：导出 device-position 到物理脚号、库脚属性、可见性、热点与图形范围。
- `snapshotPlacedInstance`：导出 RefDes、实例／缓存足迹、属性覆盖与逐脚网络。
- `snapshotCache`：导出缓存名称、类型和来源库。
- `updateCache`／`replaceCache`：仅接受 learning 内路径，设计名必须为隔离 DSN；替换需显式保留 RefDes。实际运行参数与返回 DboState 需原生日志补验。

读回报告为 UTF-8 Tcl list/dict，标明 `C14_TCL_REPORT_1`。单个字段若显示 `ERROR:`，是读回失败，不是空属性或验收通过。旧对象指针、迭代器或更新前 FlatNet 不应跨更新继续用。

当前状态：官方资料已读，最小实验及脚本已准备；OLB→DSN 更新、保存重开和连接保持均待根 agent 原生实测，尚未标记第14课完成。

## 来源与证据

- [官方帮助提取稿](../staging/capture_C_20261019/c14_official_sources.txt) 与 [来源 SHA](../staging/capture_C_20261019/c14_official_source_manifest.json)。
- [capinfomodel 正文](../staging/capture_C_20261019/c14_capinfomodel_body.txt) 与 [PDF／官方脚本 SHA](../staging/capture_C_20261019/c14_extra_source_manifest.json)。
- [当前学习源依赖快照](../staging/capture_C_20261019/c14_dependency_snapshot.json)：DRA／PSM／PAD 的实际路径、大小及 SHA。
- [研究提取脚本](../staging/capture_C_20261019/c14_read_docs.py) 与 [Tcl 定义解析结果](../staging/capture_C_20261019/c14_helper_parse.json)。

研究产物与所有中转均在 `01AIEDA/learning` 内。本文件没有更新课程索引、EDA.md 或总日志。
