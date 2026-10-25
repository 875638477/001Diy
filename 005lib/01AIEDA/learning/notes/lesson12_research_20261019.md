# 第12课研究准备：Capture 符号、电气引脚与原生读回

日期：2026-10-19（Asia/Shanghai）。已先读 `01AIEDA/课程索引.md`、`EDA.md` 和 `learning/notes/record_location_rules.md`。本笔记记录来源研究、辅助脚本准备和首轮原生数据库读回判据更正；实际原生运行由根代理统一控制。首轮结果见末节，**不据此声称GUI通道或最终网络作用域已经验证**。

## 器件与依赖选择

沿用第8课指定的 **QMI8610 Datasheet Rev. A**，Document 13-52-14、2018-05-10、82个PDF页，SHA-256 为 `A4B2F50DBFAB21EBA0BEEACD500F214A7B9301AF733F8B3D5B28939E06D0E265`。本次重新核对源 PDF 哈希，并视觉阅读既有渲染第8、9、14、15页。

符号固定为16个外围引脚，没有 EP17。第8页中心虽然画出 NC 区域，但同时明确不可焊接，不能把图中的中心区另造为可连接的第17脚。

- 拟建 package/cell：`QMI8610_C12`；Normal part：`QMI8610_C12.Normal`；device designator：`1`。
- 拟建 OLB：[c12_qmi8610.olb](../examples/lesson12_capture/c12_qmi8610.olb)，这里只是预定输出路径，存在性及有效性须由实际运行确认。
- PCB Footprint：`qmi8610_lga16_3d3_p0d5`；PAD：`qmi8610_smd061x032_m05_p100`。
- 当前直接依赖 `[learning/examples/qmi8610/library](../examples/qmi8610/library)` 的已验原生 PAD/DRA/PSM。本次三个学习副本的 SHA 均与第8课发布清单一致。

**当前状态与历史记录不同：** 第8课 publication.json 记录的 `01Psm_lib`／`01Pad_lib` 三个公共目标，本轮检查均未找到；不否认第8课的历史发布记录，也不把历史发布当作本轮仍存在的证据。这里不恢复、复制或修改公共库，第14课应显式使用现有学习副本路径。

## 来源引脚与电气类型

默认符号使用 `HOST_I2C` 模式；helper 也可显式创建 `HOST_SPI4` 变体。不能在模式变更后沿用有矛盾的电气类型。Table 2 给出功能描述，下面的 Capture 类型是基于功能的 ERC 建模选择，不是数据手册直接规定的 Capture 枚举，也不代表完整模拟电路模型。

| 脚号 | 可见名称 | 默认 HOST_I2C 类型 | 原厂依据与处理 |
| --- | --- | --- | --- |
| 1 | RESV3 | Passive | 第8页要求接板GND；保留独立可见脚，不能设为NC |
| 2 | VDDa | Power | 模拟供电 |
| 3 | GNDa | Power | 模拟地 |
| 4 | RESV2 | Passive + NoConnect | 第8页明确NC |
| 5 | RESV1 | Passive + NoConnect | 第8页明确NC |
| 6 | SDA2 | Bidirectional | 主I²C数据；方向分类由总线功能推导 |
| 7 | SCL2 | Output | 主I²C时钟；这是主时钟建模选择，尚未确认 clock stretch 细节 |
| 8 | VDDd | Power | 数字与IO供电 |
| 9 | SA0/SDO | Input | I²C下为地址选择；SPI4变体需改为Output |
| 10 | CS | Input | 第9页说明高电平为I²C模式；注明内部200k上拉 |
| 11 | INT2/DRDY | Output | 数据就绪/FIFO中断；没有据此假定OC或推挽结构 |
| 12 | INT1/CLKout | Output | 通用中断，OIS模式可作时钟输出 |
| 13 | SDA/SDI/SDIO | Bidirectional | I²C下为SDA；SPI4下SDI应为Input；3线SPI不属于当前两个profile |
| 14 | SCL/SPC | Input | 主机接口时钟输入，不能与第7脚主I²C时钟混淆 |
| 15 | GNDd | Power | 数字地 |
| 16 | RST | Input | 第9页复位输入；没有仅凭名称或“assert”文字添加反相圆点 |

所有16脚都应显示名称、编号和引脚。首轮保存重开实际表明：POWER脚2/3/8/15的可见性为1，库级 `GetIsGlobal` 原始字段为1；其余12脚为0。这里不把该原始位等同于“隐藏脚”或最终网络作用域，详见末节更正。Pin4/5 的 `IsNoConnect=1` 是符号引脚标志，不能把它和原理图中已有NC标记、实际未连网络等不同层次的证据混为一谈。Pin1必须接地的要求需要电路审查，Passive 类型本身不会自动实现连接。

额外注意第15页实际供电域：VDDa推荐2.7/3.3/3.47V，VDDd推荐1.62/1.80/1.98V；第14页VDDd绝对最大2.05V。不能因为模拟电源典型3.3V就把数字IO电源也连3.3V。本课只记录来源条件，不进行硬件上电验收。

完整逐引脚来源、两种profile、物理编号对应及当前依赖哈希见 [qmi8610_pin_spec.json](../examples/lesson12_capture/qmi8610_pin_spec.json)。显示名称将主要功能和别名合并，物理映射依靠编号而不是字符串完全相等；例如第13脚旧物理规格名使用 `SDA/SDI/SDO`，本符号的 `SDIO` 来自第9页功能描述，不构成新增物理引脚。

## 已定位的本机官方 API 与实例

以下路径均在 `C:/Program0/Cadence/spb172/` 下，只读访问，未改安装文件。

| 来源 | 精确位置与用途 |
| --- | --- |
| 完整原生创建示例 | `tools/capture/tclscripts/capPSpiceModelApp/PWL/Digital/Gates/OR/tcl/PwlORSymbolCreate.tcl`：创建库、package、cell、part、图形、引脚、Device物理脚号，保存并移除库 |
| 接口PDF | `tools/capture/tclscripts/OrCAD_Capture_TclTk_Extensions.pdf`，922页；第178页CreateLib/SaveLib，第215页NewPart，第334页NewSymbolPinScalar，第592页part可见性，第603—604/608—609页pin getter/setter，第724/726页物理脚号API |
| 读取库引脚示例 | `doc/orctclcap/Getting_Pin_Names_from_a_Library_Part.html`：Package→Device→Cell→LibPart→NewLPinsIter |
| 改名与改编号示例 | `doc/orctclcap/Change_pin_name_or_pin_number__in_a_library.html`：Pin.SetPinName 与 Device.NewPinNumber 是不同对象层次 |
| 数据模型 | `doc/capinfomodel/dboimnew.html`：Package、Device、Cell、LibPart、SymbolPin对象关系 |
| 数据库示例 | `doc/orctclsample/TCL_Programming_with_OrCAD_Capture_Database.html` 与 `Basic_OrCAD_TCL_Sample_Snippets.html` |
| 几何与矢量读回 | `tools/capture/tclscripts/cdnTclEncrypted/orPrmDboStreamer.tcl` 的streamDboVectors/streamDboLine；同目录orPrmDboGeom.tcl的CPoint/CRect转换 |

接口PDF的178、334、726页已渲染并视觉核对签名，其余相关页已抽取并另渲染供继续查阅；相关PNG、全文抽取位于 `learning/staging/capture_C_20261019/`。本次未把“渲染过”写成所有页都已逐页视觉阅读。

关键调用顺序：

```tcl
set session $::DboSession_s_pDboSession
DboSession -this $session
set status [DboState]
set lib [$session CreateLib $pathCString $status]
set package [$lib NewPackage $packageCString $status]
set cell [$lib NewCell $cellCString $status]
set part [$lib NewPart $normalNameCString $status]
$cell AddPart $part
$part SetCellPtr $cell
$part SetPackagePtr $package
set pin [$part NewSymbolPinScalar $status $nameCString $type $start $hotPoint 1 $position]
set device [$package NewDevice $designatorCString 0 $cell $status]
$device NewPinNumber $numberCString $positionIntPointer 0 -1
$lib SavePackageAll $package
$session SaveLib $lib
$session RemoveLib $lib
```

`position` 是符号内部索引，不是物理脚号。当前明确以position 0～15映射number 1～16；读回必须先取SymbolPin.GetPinPosition，再由Device.GetPinNumber得到物理编号。仅列出16个SymbolPin不能证明物理编号正确。

setter可能返回DboState，也可能为void，必须根据官方签名或示例分别处理。CString、CPoint、int&使用DboTclHelper构造；不能直接把Tcl字符串和整数代替所有C++引用参数。示例中会调用exit，本helper改为error返回，由根代理控制进程，不自行退出Capture。

## 可执行 helper 与检查边界

[c12_helpers.tcl](../scripts/c12_helpers.tcl) 被source时只定义过程，不自动创建或打开库。主要入口：

```tcl
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c12_helpers.tcl}
::C12::CreateQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610.olb} QMI8610_C12 HOST_I2C
::C12::ReadQmi8610 {D:/001DIY/005lib/01AIEDA/learning/examples/lesson12_capture/c12_qmi8610.olb} QMI8610_C12 {D:/001DIY/005lib/01AIEDA/learning/logs/c12_reopen_20261019} HOST_I2C
```

这些入口仅由根代理在Capture内部统一执行。创建过程拒绝覆盖现有目标，输出路径限制在learning内部；不会发布公共库。创建后SavePackageAll/SaveLib并RemoveLib，返回路径和名称，避免继续使用关闭后的对象指针。读回过程默认结束后RemoveLib，不删除任何库文件。

拟验收的原生字段：

- 16个唯一物理编号、名称、profile电气类型、position、visible/numberVisible/global/noConnect，以及每个引脚start/hotPoint。
- part级名称/编号可见性；package PCB Footprint；厂商、料号、来源、profile和版本属性。
- body真实四条线的端点；REF/Value显示属性名称、坐标和显示类型。
- 保存关闭后重读，而不是仅以内存中创建返回值作为成功证据。

读回输出为 `c12_pins.tsv`、`c12_properties.tsv`、`c12_vectors.tsv`、`c12_display_properties.tsv` 和 `c12_readback_result.tcldict`。需要保留实际日志；预定文件名不等于已经运行产生文件。

本子任务只在普通无GUI Tcl解释器中加载helper，检查语法、两profile各16行、引脚绘图坐标、路径保护和非Capture执行拒绝，没有自行调用Dbo API；检查结果在 [c12_plain_tcl_checks.json](../staging/capture_C_20261019/c12_plain_tcl_checks.json)。根代理的后续原生结果与边界见末节。

## 下一步与接续接口

根代理统一试跑、保存原始错误并调整有证据支持的API调用；C14继续使用同一part和footprint做库版本传播。若API返回成功但读回字段不一致，仍记为失败。C13的多单元与隐藏电源／网络作用域应另建受控实例，不能把本符号的可见且非global电源脚当作已学会隐藏电源。

本阶段只新增learning下文件，未改课程索引、EDA总日志、总进度或任何公共库。

## 首轮原生数据库结果与 POWER 原始标志更正

根代理通过 Tclsh8.6 加载官方 `orDb_Dll_Tcl64.dll / DboTclWriteBasic17.2.2016045`，建立原生数据库Session。这是官方数据库DLL通道，本项证据不代表GUI Capture脚本入口已建立。INPUT/IO/OUTPUT/PASSIVE/POWER的枚举0/1/2/4/7已由该通道确认。

首轮 `CreateQmi8610` 已实际保存OLB；读回取得16脚、4条body线、2项显示属性及部件属性。初版判据却将“visible/numberVisible”和“raw global”合并，并错误要求所有脚global=0，导致四个POWER脚报错。原始 [c12_pins.tsv](../logs/capture_C_20261019/c12_reopen/c12_pins.tsv) 实际为：

| 脚组 | type | visible | numberVisible | raw GetIsGlobal |
| --- | ---: | ---: | ---: | ---: |
| 2、3、8、15 | 7 POWER | 1 | 1 | 1 |
| 其余12脚 | 保留各自类型 | 1 | 1 | 0 |

因此不是发现四个隐藏脚。初版 [create12a.result.tcldict](../logs/capture_C_20261019/runtime/create12a.result.tcldict) 与失败读回记录保留不变，不因更新判据就改写成当时通过。

官方依据新增：

- `doc/cap_ug/Making_power_pins_visible.html` 说明默认电源全局连接可由“使电源脚可见并实际连接wire或其他connectivity对象”覆盖；仅显示隐藏脚不改变其全局性质。
- `doc/cap_ug/Creating_a_Part_Body.html` 的Visibility段要求可见POWER脚接wire，隔离网络的判断不能只看显示。
- 安装脚本 `orPrmDboStreamer.tcl` 有 `LONG_VISIBLE_GLOBAL,POWER` 组合；`capAssociatePSpiceModel.tcl` 用“POWER且GetIsVisible=0”识别隐藏电源脚，也没有以GetIsGlobal单项代替隐藏性。

修复方式是保留四个POWER电气类型、严格核visible=1和numberVisible=1，另行记录本机原生重开看到的POWER rawGlobal=1；**不通过把POWER降为Passive来消除报错**。最终网络隔离是否成立，必须在第13课放置实例、接wire／port后读实际网络，不能从库原始位推出。

helper已修改上述分离判据，并新增 `::C12::ProbePowerFlags`：在新的隔离OLB中测试四种setter顺序，记录每一步及保存重开后的type/visible/rawGlobal，供根代理区分setter即时作用与保存归一化。该探针由本子任务准备但未自行执行。

建议探针新路径 `learning/staging/capture_C_20261019/c12_power_flags_probe.olb`；如另建正式修订，使用 `learning/examples/lesson12_capture/c12_qmi8610_visible_v2.olb`，不覆盖初版。初版helper、pin_spec及哈希清单备份在同一staging目录的 `c12_*_before_power_review.*` 和 `c12_power_review_backup_manifest.json`。当前pin_spec把global字段明确标为raw库元数据，最终作用域仍待实测。精确诊断见 [c12_power_flag_review.json](../staging/capture_C_20261019/c12_power_flag_review.json)。
