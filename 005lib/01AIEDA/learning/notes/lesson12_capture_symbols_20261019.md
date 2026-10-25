# 第12课 Capture 原理图符号与电气引脚验收

日期：2026-10-19（Asia/Shanghai）。本课已完成 QMI8610 的两套真实原生 OLB：主机 I²C 版和四线 SPI 版。**后续工程请使用文件名带 `_single` 的正式修订版**；C14实例实验发现首版误把Device designator设为`1`，会把U101显示为U1011，现已将单单元suffix更正为空，另存新库并通过全新原生进程重开。历史首版保留以追溯问题。首版针对源表和封装的304项独立检查为0差异；新版本16脚、图形、显示字段和读回统计与首版逐字节相同，属性仅有预期版本号变化。原生重开还确认了空Device designator。本课的“完成”范围是原生库结构、物理编号、电气建模、可见性和数据库读回；Capture 窗口中的视觉排版、工程网络连接和 ERC 分别属于后续界面及工程验收。

## 原生文件和复核入口

**后续创建规范（用户明确，2026-10-19）：** 普通器件优先单单元，普通 MCU 在一个符号单元内放全手册对应封装的全部引脚，按功能分组排布并逐物理编号核对；通过调整符号和图纸尺寸保持可读性。A4 是起始尺寸，容纳不下可以扩大，不为维持 A4 将普通 MCU 拆成多个单元。CPU 等复杂器件另按实际需要处理。详见 [符号单元规范](capture_symbol_defaults.md) 和 [纸张规范](capture_page_defaults.md)。

| 产物 | 路径或对象名 | 已核对内容 |
| --- | --- | --- |
| 正式主机 I²C 原生库 | [c12_qmi8610_single.olb](../examples/lesson12_capture/c12_qmi8610_single.olb)；Package `QMI8610_C12_SINGLE` | 空单元suffix；16脚、逐脚类型和编号、图形、属性、显示字段、独立进程重开 |
| 正式主机四线 SPI 原生库 | [c12_qmi8610_spi4_single.olb](../examples/lesson12_capture/c12_qmi8610_spi4_single.olb)；Package `QMI8610_C12_SPI4_SINGLE` | 同上；第9和13脚使用不同的方向类型 |
| 历史首版 I²C / SPI4 | [c12_qmi8610.olb](../examples/lesson12_capture/c12_qmi8610.olb)、[c12_qmi8610_spi4.olb](../examples/lesson12_capture/c12_qmi8610_spi4.olb)；原Package名不变 | 引脚检查通过；Device suffix误为1，保留教学历史，不推荐作为后续工程来源 |
| 单单元修订验收 | [新进程原生结果](../logs/capture_C_20261019/c12_single_freshprocess_result.tcldict)、[修订校验报告](../logs/capture_C_20261019/c12_single_fix_validation.json) | 两库Device.GetDesignator为空；16脚/4条线/2显示字段；创建、读取进程均退出；新库无同名OLBlck；历史库哈希不变 |
| 来源规格 | [qmi8610_pin_spec.json](../examples/lesson12_capture/qmi8610_pin_spec.json) | 数据手册出处、两种模式、引脚坐标、物理封装对应；文件中的 pending 为创建前历史状态，现状以本验收记录为准 |
| 两套原生读回 | [I²C 引脚表](../logs/capture_C_20261019/c12_i2c_verified/c12_pins.tsv)、[SPI4 引脚表](../logs/capture_C_20261019/c12_spi4_verified/c12_pins.tsv) | 从重新打开的库获取，而非创建时内存回显 |
| 独立检查报告 | [c12_independent_review.json](../logs/capture_C_20261019/c12_independent_review.json) | 304项、0差异；包含OLB和各读回文件的大小、SHA-256 |
| 执行总结果 | [verify12b.result.tcldict](../logs/capture_C_20261019/runtime/verify12b.result.tcldict) | 原生执行返回 code 0；两个profile各16 pins、4 bodyVectors、2 displayProperties、errors为空 |
| 独立新进程读回 | [原生结果](../logs/capture_C_20261019/c12_freshprocess_result.tcldict)、[启动与退出记录](../logs/capture_C_20261019/c12_freshprocess_launch.json)、[十份文件比较](../logs/capture_C_20261019/c12_freshprocess_comparison.json) | 新进程退出码0，两库前后哈希不变；10份结果逐字节相同 |
| 创建及读取脚本 | [c12_helpers.tcl](../scripts/c12_helpers.tcl) | source只定义过程；不覆盖已存在的库；输出限于learning目录 |
| 独立复核脚本 | [c12_independent_review.py](../scripts/c12_independent_review.py) | 不导入创建helper；另行抄录源文档名称/方向表并比较原生结果 |

安装文件只读，用户公共库未修改。本课的 `.olb` 是原生数据库文件；TSV和JSON用于审查，不能代替OLB。

## 来源与引脚判断

器件依据 `D:/004Document/016Sensor/06IMU/矽睿/QMI8610 Datasheet Rev. A.pdf`，Document 13-52-14、Rev A、2018-05-10，共82个PDF页。SHA-256：`A4B2F50DBFAB21EBA0BEEACD500F214A7B9301AF733F8B3D5B28939E06D0E265`。本轮再次核对源PDF哈希；独立审查者视觉阅读了完整第8、9页，既有图像见 [第8页](../examples/qmi8610/source/page_08.png) 和 [第9页](../examples/qmi8610/source/page_09.png)。第8页Table 2、Figure 4/5和第9页续表共同给出引脚和方向依据。

Capture电气类型由功能选择，是ERC模型；原厂没有直接指定 Capture 的枚举。下表列出**已保存重开的实际值**。Input=0、Bidirectional=1、Output=2、Passive=4、Power=7已由本机17.2原生通道核对。

| 物理脚号 | 符号可见名称 | I²C版实际类型 | SPI4版实际类型 | 来源处理和必须保留的条件 |
| --- | --- | --- | --- | --- |
| 1 | RESV3 | Passive 4 | Passive 4 | 第8页要求接板GND；不是NC。类型本身不会替电路接地 |
| 2 | VDDa | Power 7 | Power 7 | 模拟供电 |
| 3 | GNDa | Power 7 | Power 7 | 模拟地 |
| 4 | RESV2 | Passive 4 | Passive 4 | NoConnect=1；原厂NC |
| 5 | RESV1 | Passive 4 | Passive 4 | NoConnect=1；原厂NC |
| 6 | SDA2 | Bidirectional 1 | Bidirectional 1 | 传感器主I²C数据；双向分类是总线功能推导 |
| 7 | SCL2 | Output 2 | Output 2 | 传感器主I²C时钟；未把此模型当作clock stretching电路保证 |
| 8 | VDDd | Power 7 | Power 7 | 数字和IO供电 |
| 9 | SA0/SDO | Input 0 | Output 2 | I²C地址选择输入；四线SPI数据输出 |
| 10 | CS | Input 0 | Input 0 | 高电平选择I²C；第9页脚注说明内部200k上拉 |
| 11 | INT2/DRDY | Output 2 | Output 2 | 中断/数据就绪输出；未据此假定开漏或推挽晶体管结构 |
| 12 | INT1/CLKout | Output 2 | Output 2 | 通用中断；OIS模式时钟输出 |
| 13 | SDA/SDI/SDIO | Bidirectional 1 | Input 0 | I²C SDA双向；SPI4 SDI输入；未创建三线SPI模式 |
| 14 | SCL/SPC | Input 0 | Input 0 | 主机接口时钟输入，须与第7脚区分 |
| 15 | GNDd | Power 7 | Power 7 | 数字地 |
| 16 | RST | Input 0 | Input 0 | 复位输入；没有仅凭名称或assert文字增添反相圆点 |

第13脚图中别名和续表文字有 `SDO`／`SDIO` 差别，符号采用第9页功能说明的三线SPI别名 `SDIO`。同一物理脚仍为13；不能因字符串不同增加一脚。四线SPI符号虽保留功能别名，电气类型只为当前HOST_SPI4模式服务。跨接口模式重用符号时，必须同时检查profile和脚9/13方向，不能只改器件显示值。

第8页中心NC区明确不可焊接，两个库都只有1至16号脚，没有EP17。已有封装也是16个外围焊盘；本次独立检查将其原生读回的16个编号和坐标逐项与spec比较，全部相同。原理图符号按功能排布，不要求模仿物理封装边缘位置，连接对应以物理脚号为准。

供电要求仍按Rev A适用条件使用：第15页VDDa推荐2.7/3.3/3.47V，VDDd推荐1.62/1.80/1.98V；第14页VDDd绝对最大2.05V。不能从VDDa典型3.3V推出VDDd也可接3.3V。详情和来源页见 [研究记录](lesson12_research_20261019.md)；本课未进行硬件上电试验。

## OLB对象关系和创建方法

本课使用安装随附的 `C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll`，由 Cadence 随附Tclsh8.6加载 `DboTclWriteBasic 17.2.2016045 (3731280)` 并创建DboSession。这是官方原生数据库SDK通道。运行记录中的UI命令数为0，不能把它写成已经打开并操纵Capture图形界面。

按官方数据模型建立 `Lib → Package → Device → Cell → LibPart → SymbolPin` 关系。Package表示整个器件；Device保存物理引脚映射，Cell/LibPart保存符号图形和引脚。SymbolPin的内部position为0至15，Device把它们映射到物理编号1至16。只数到16个图形引脚不足以验收，必须通过 `GetPinPosition → Device.GetPinNumber` 读回编号。

原生创建过程使用 `CreateLib`、`NewPackage`、`NewCell`、`NewPart`、`NewSymbolPinScalar`、`NewDevice` 和 `NewPinNumber`，完成关联后执行 `SavePackageAll`、`SaveLib`、`RemoveLib`。再次由路径打开库后读取全部字段。CString、CPoint和int引用按官方DboTclHelper构造，未把所有C++参数当成普通Tcl字符串处理。

官方依据在安装目录内：`tools/capture/tclscripts/OrCAD_Capture_TclTk_Extensions.pdf`（922页，第178、215、334、592、603—609、724、726页）；原生创建范例为 `tools/capture/tclscripts/capPSpiceModelApp/PWL/Digital/Gates/OR/tcl/PwlORSymbolCreate.tcl`。物理脚号读取依据 `doc/orctclcap/Getting_Pin_Names_from_a_Library_Part.html`，对象层次依据 `doc/capinfomodel/dboimnew.html`。详情与签名定位保留在研究记录，未修改安装示例。

## 保存重开后的图形和属性

两库的原生body均为四条直线，形成 `(0,0)` 至 `(220,180)` 的矩形。左侧1至8脚body端点x=0、连接热点x=-20；右侧9至16脚body端点x=220、热点x=240；每列y按20步进。16个连接热点均读回与spec一致。读回图形的是数据库矢量，界面字体、最终文字拥挤情况仍须Capture窗口检查。

两个LibPart均为引脚名称显示=1、编号显示=1；逐脚visible=1、numberVisible=1。仅脚4/5的NoConnect标志=1，其余14脚=0。库级NoConnect不是原理图中已放置NC标记或工程ERC通过的证明。

| 已读回字段 | 实际值 |
| --- | --- |
| Value | QMI8610 |
| Manufacturer | QST |
| Manufacturer Part Number | QMI8610 |
| PCB Footprint 和 packagePCBFootprint | qmi8610_lga16_3d3_p0d5 |
| Symbol Revision | C12_REV2_SINGLE；历史首版为C12_REV1 |
| Source Revision | 13-52-14 Rev A, 2018-05-10 |
| Interface Profile | HOST_I2C 或 HOST_SPI4，与各库一致 |
| Datasheet | QMI8610 Datasheet Rev. A.pdf |
| Part Reference 显示字段 | 坐标(0,-20)，displayType=1 |
| Value 显示字段 | 坐标(100,200)，displayType=1 |

两profile只在脚9与13的类型和Interface Profile属性上有预期差别；编号、名称、图形、可见性和footprint对应一致。原始属性、图形、显示属性表与引脚表位于各自 `c12_i2c_verified`、`c12_spi4_verified` 日志目录。

## 单单元Device suffix的工程验证和修正

第14课把符号放入工程后发现：给实例设置U101，`GetReferenceDesignator`却得到U1011。首版创建语句误把 `NewDevice` 的第一个参数当成“第1个器件”，传入字符串`1`；该参数实际是Device的逻辑单元后缀，适用于多单元A/B或1/2等标识。单单元器件应传空字符串，0才是该调用中的position参数。

已重新核对本机官方922页API PDF的第599页：`DboPackage.NewDevice(designator CString&, position int, cell DboCell*, status DboState&)`；第724页：`DboDevice.GetDesignator(designator CString&)`返回DboState。helper现使用 `NewDevice [cstring ""] 0 $cell $state`。修正前helper另存于 `learning/staging/capture_C_20261019/c12_helpers_before_single_fix.tcl`，历史两库未覆盖。

通过 [c12_build_single_fix.tcl](../scripts/c12_build_single_fix.tcl) 创建两个新库并退出后，再启动另一个全新原生Tclsh进程，执行 [c12_reopen_single_fix.tcl](../scripts/c12_reopen_single_fix.tcl)。后者重新打开两库，分别确认`devicePosition=0`、`deviceDesignator={}`；每库仍为16 pins、4 bodyVectors、2 displayProperties、errors为空。父进程等待创建和读取两个进程退出，退出码均0。补核真实的`.OLBlck`命名后，两个新库均无同名`.OLBlck`或`.OLB.lck`文件；其他会话可继续打开历史库，其锁不在本实验清理范围内。

[c12_run_single_fix.py](../scripts/c12_run_single_fix.py) 保存了上述运行和比较记录：两个新版各4份引脚/矢量/显示/统计文件与历史版逐字节相同，属性表仅允许Symbol Revision由C12_REV1变为C12_REV2_SINGLE；两份属性表均符合。历史两库SHA-256前后相同，新库哈希另记于修订校验报告。此次修正确认Device原生后缀字段为空；新库在具体工程中的RefDes显示由C11/C14放置实例继续核对。

正式新版读回在 `logs/capture_C_20261019/c12_single_fresh_i2c` 与 `c12_single_fresh_spi4`。引脚规格JSON继续保存首版准备时状态，后续依赖路径和suffix应以本节及新版原生库为准。

## POWER标志探针及首次失败的修正

初次创建成功后，读取过程错误要求所有引脚 `GetIsGlobal=0`，因此四个POWER脚报错。原始 [create12a结果](../logs/capture_C_20261019/runtime/create12a.result.tcldict) 和 [首次引脚表](../logs/capture_C_20261019/c12_reopen/c12_pins.tsv) 保留，未改写失败历史。

新增隔离OLB探针检查四种setter顺序，完整结果为 [c12_power_flags_probe.tsv](../logs/capture_C_20261019/c12_power_flags_probe.tsv)。实际现象如下：

| 探针 | 实际现象 |
| --- | --- |
| POWER后设置global=0，再设visible=1 | rawGlobal始终为1 |
| POWER后先visible=1，再global=0 | rawGlobal始终为1 |
| POWER隐藏再恢复可见，多次global=0 | visible能由0恢复1，rawGlobal始终为1 |
| 先将POWER改为INPUT，再改回POWER | rawGlobal随类型由1变0，再回1；恢复POWER后global=0仍为1 |
| 保存、移除库、重开 | 四脚均type=7、visible=1、rawGlobal=1 |

这证明本机SDK中的该原始位与POWER类型相关，不能用它单独判定引脚是否隐藏，也不能靠更换setter顺序使它归零。修正采用分别检查电气类型、可见性和原始位；没有把电源脚降为Passive以规避检查。

安装帮助 `doc/cap_ug/Making_power_pins_visible.html` 说明：电源脚默认具有按名称连接的全局行为；将脚做成可连接的可见脚并实际接wire或其他连接对象，可覆盖默认连接。仅“显示隐藏脚”不等于改变作用域。`Creating_a_Part_Body.html`也要求可见POWER脚接wire。库中的rawGlobal=1与visible=1可以同时出现。网络是否按预期隔离，必须在第13课放置实例、建立wire/port后检查实际网络，本课不从rawGlobal位推导工程连通结果。

## 独立核对和验收边界

独立核对重新视觉读取源表，另外抄录引脚名称及两模式电气类型，不加载创建helper。随后比较两套原生TSV、spec及第8课原生封装pins.tsv，检查源PDF哈希、编号唯一性、物理映射、名称、模式方向、可见性、NoConnect、连接热点、四条body矢量、显示字段、器件属性、封装名及POWER探针结果。304项通过，没有放宽编号、类型或可见性要求。复核命令：

```powershell
python 'D:\001DIY\005lib\01AIEDA\learning\scripts\c12_independent_review.py'
```

进一步由 [c12_run_fresh_process.py](../scripts/c12_run_fresh_process.py) 启动独立的 Cadence Tclsh8.6进程，执行 [c12_fresh_process_read.tcl](../scripts/c12_fresh_process_read.tcl)：重新加载同一官方DLL、创建新的DboSession、只读打开两个首版OLB并关闭。新进程分别得到16 pins、4 bodyVectors、2 displayProperties、errors为空，随后以0退出；父进程等待退出后核对两个OLB的SHA-256前后完全一致。此过程不使用原来正在运行的SDK Session。新旧各5份读回文件合计10项逐字节比较全部通过。运行脚本拒绝覆盖已有实验日志，复核现存证据时无需再次运行原生进程。首轮启动记录只匹配了`*.lck`，没有涵盖Capture实际使用的`.OLBlck`，因此不把其空列表作为完整锁检查证据；正式_single版已补核两种命名。

| 验收项 | 结果和证据范围 |
| --- | --- |
| 真实OLB创建并保存 | 通过；两套原生文件存在，哈希入独立报告 |
| 保存后移除库并重新打开 | 通过；原生会话内重新加载，不只验创建返回值 |
| 全新原生进程重新打开最终库 | 通过；两个库各16脚、4条线、2显示字段；10份读回文件与既有结果完全一致，进程已退出 |
| 单单元Device suffix | 通过；正式_single两库新进程GetDesignator为空，position=0；原版错误suffix=1保留历史说明 |
| 16脚逐号、逐名、逐类型核对 | 通过；两模式各16脚，9/13差异正确，无EP17 |
| 引脚名称、编号、可见性、NC标志 | 通过；全部可见，脚4/5为NC，脚1不是NC |
| 图形、属性和显示字段读回 | 通过；每库4条线、2显示字段及指定属性 |
| 与已有封装编号、坐标对应 | 通过；采用learning内B8原生封装读取结果 |
| GUI显示、放置、连线、ERC | 由界面和第13—14课工程验收补充；本项没有从SDK成功推定 |

本课关联的PAD/DRA/PSM现存于 [QMI8610学习库](../examples/qmi8610/library)。历史B8发布清单中的公共目标路径本轮未找到，因此第14课应显式指定现存学习副本，验证库搜索路径、实例物理编号和更新传播；本课不把历史发布记录当成当前公共库存在的证据。

本轮新增的源码、探针库、失败记录和正式产物均保留于 `01AIEDA`，未使用系统Temp中转。后续新工程使用 `QMI8610_C12_SINGLE`／`QMI8610_C12_SPI4_SINGLE` 所在新OLB，并保持RefDes、实例属性及封装属性分别核对；历史C14实验如使用独立副本修正suffix，仍保留该实验自身的版本和日志。
