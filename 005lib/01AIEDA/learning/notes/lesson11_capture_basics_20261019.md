# 第11课 Capture 工程、数据库接口、保存与回退

日期：2026-10-19（Asia/Shanghai）。已完成原生设计创建、两页结构、器件放置、对象查询、保存、丢弃未保存修改、文件备份恢复及独立进程重开。**Capture GUI 命令窗和 OPJ 图形打开仍未验收**：本机已验证的是官方数据库 DLL，不把它写成 GUI 内部 Tcl 已恢复。

## 最终文件

| 文件 | 用途 |
| --- | --- |
| [c11_basics.dsn](../examples/lesson11_capture/final/c11_basics.dsn) | 最终原生设计：TOP 下 PAGE1/PAGE2；PAGE1 放 U101，坐标(300,300) |
| [c11_basics.opj](../examples/lesson11_capture/final/c11_basics.opj) | 参照官方 PCB 示例语法生成的工程容器；相对路径指向本课DSN及C12正式OLB；GUI打开待验 |
| [c11_basics_baseline.dsn](../examples/lesson11_capture/final/c11_basics_baseline.dsn) | 保存关闭后复制的基线；恢复后与最终DSN字节一致 |
| [c11_saved_move_marked.dsn](../examples/lesson11_capture/final/c11_saved_move_marked.dsn) | 独立移动实验，保存重开后U101位于(500,450) |
| [创建与回退脚本](../scripts/c11_design_exercise.tcl) | 拒绝覆盖既有设计；只在learning内实作；可设置C11DefinitionsOnly只加载函数 |
| [创建批处理入口](../scripts/c11_final_create_batch.tcl) | 官方Tclsh/DLL独立会话入口 |
| [独立重开脚本](../scripts/c11_fresh_reopen.tcl) | 新进程重开最终DSN，核对2页、U101完整位号、16个物理脚和封装关联 |
| [持久移动验证](../scripts/c11_saved_move_verify.tcl) | 修改后标脏、逐页保存、关闭、重开验证 |
| [最终日志目录](../logs/capture_C_20261019/c11_final) | 01—08快照、创建和两项重开结果 |

最终器件来自第12课修正单单元suffix后的 [c12_qmi8610_single.olb](../examples/lesson12_capture/c12_qmi8610_single.olb)，Package为`QMI8610_C12_SINGLE`。Value为QMI8610，PCB Footprint为`qmi8610_lga16_3d3_p0d5`，物理编号1—16，无EP17。原始Reference和完整ReferenceDesignator均读回U101；没有多拼一个单元号1。

## 对象与文件的关系

OPJ组织工程资源、设计和输出路径，DSN保存原理图数据库。一个Design有根Schematic，本例根为TOP；一个Schematic包含多个Page，PAGE1/PAGE2属于同一层级域。OLB保存可复用符号，放进DSN后建立Design Cache；更改OLB不等于更改已放实例，第14课单独验证传播。符号脚内部position、物理PinNumber、功能PinName和实例位号分别核对，不能混用。

本课OPJ是依据安装示例`share/orcad/examples/pcbdesign/pcbdemo1/demoj.opj`及`pcbdemo2/HSD_FPGA.opj`结构生成的文本容器，ProjectType使用PCB。已核对资源相对路径存在；这项检查不等于Capture已解析并显示OPJ。DSN则确实由官方数据库API生成并重开。

## 实际执行通道

- 安装根：`C:/Program0/Cadence/spb172`。
- 解释器：随附` tcltk/bin/tclsh.exe`，Tcl8.6.0、64位。
- 原生模块：`tools/bin/orDb_Dll_Tcl64.dll`，加载名DboTclWriteBasic，实测版本`17.2.2016045 (3731280)`。
- `DboTclHelper_sCreateSession`返回非NULL会话；公开Dbo命令4068个。独立进程里UI Menu命令数为0。
- 当前系统Python的Tk Tcl9不能替代此8.6 ABI，不能把“有Tcl”推定为能加载Cadence数据库。

核心调用顺序：CreateDesign → GetRootSchematic → NewPage → 从源库获取Package/Device/Cell/LibPart → NewPlacedInst → SetReference → SavePage（每页）→ SaveDesign → RemoveDesign → GetDesignAndSchematics → 查询。CString/CPoint等参数通过DboTclHelper构造。

GetDesignAndSchematics是本课已验证的磁盘重开入口。GetOpenDesign查询已打开对象，不能用它替代磁盘加载。每次取得对象后先检查DboState及非NULL，再调用方法；RemoveDesign/RemoveLib后旧指针和迭代器不再使用。

## 保存与回退的实测结果

| 步骤 | 实际读取结果 | 证据 |
| --- | --- | --- |
| 创建并保存基线 | TOP，2页，PAGE1的U101=(300,300) | 01_saved、02_reopened |
| 内存中移动，未保存 | U101=(700,500) | 03_unsaved_move |
| RemoveDesign丢弃，再从磁盘重开 | U101恢复(300,300) | 04_discard_reopened |
| 标脏并保存移动 | U101=(500,450) | 05_saved_move；独立保存移动副本08重开再次确认 |
| 关闭，复制基线覆盖隔离练习，再重开 | U101恢复(300,300) | 06_restored_reopened |
| 全新原生进程打开最终文件 | 2页；完整位号U101；16个物理脚；封装名正确 | [fresh_reopen_result](../logs/capture_C_20261019/c11_final/fresh_reopen_result.tcldict)，code0 |
| 独立移动副本保存关闭重开 | U101=(500,450)，位号不变 | [saved_move_result](../logs/capture_C_20261019/c11_final/saved_move_result.tcldict)，code0 |

坐标为Capture原理图绘图单位，不是PCB毫米坐标。PAGE2是空白练习页，整个DSN为接口与结构练习，不是完整可投板电路，也没有把空白页面或未接脚称为ERC通过。

两个必须保留的经验：

1. **保存设计不自动代替保存新建页面。** 首次尝试只调用SaveDesign，创建时内存有2页，关闭重开后却无页面。随后对每页调用Schematic.SavePage再SaveDesign，页面持久化成功。失败文件和日志保留在lesson11_capture首层、c11_design日志，不作为最终练习入口。
2. **修改已保存对象后要明确标脏。** SetLocation返回成功，内存快照坐标已变，但仅SavePage/SaveDesign重开仍是旧坐标。对实例及页面调用MarkModified，再逐页保存，重开才读到(500,450)。失败证据在[c11_design_run02](../logs/capture_C_20261019/c11_design_run02)的saved_move_failed01及08_saved_move_unmarked_failure。没有以“保存函数返回成功”代替持久性核对。

回退优先在关闭的隔离练习文件上进行：保存基线、修改、核对；需要恢复时先关闭，再复制已确认基线，重开读取。不要用此处的文件覆盖方式操作正在打开的用户工程。本课未验证GUI Undo菜单，数据库丢弃和文件恢复不能替代GUI撤销的验收。

## GUI启动与本次异常

官方`doc/capqrc/CommandLineArgs.html`支持-product、-lite、-i；`doc/cap_ug/Execute_TCL_script_in_Windows.html`给出Capture启动脚本入口。实际分别以隔离INI尝试Capture CIS和Lite启动；均未取得启动脚本完成凭据，未打开用户设计，后续停止这两个本课自建进程。因此GUI命令窗、选择、菜单、页面视觉布局及OPJ图形打开保留待验，不能写成已完成。

C13探索时，NULL对象强制转换和FlatNet.NewWiresIter曾触发原生崩溃。用户随后看到tclsh错误与Windows即时调试器窗口。本次已停止这些调用并改为安全的NetOccurrences查询路线，未主动打开Visual Studio，未修改系统异常处理或调试器配置。事件见[异常记录](../logs/capture_C_20261019/native_exception_incident_20261019.md)。后续原生批次相互隔离，对所有返回对象先检查NULL。当前无法控制桌面UI的限制也如实保留，不用其他方式模拟GUI验收。

## 来源及继续入口

本机官方`tools/capture/tclscripts/OrCAD_Capture_TclTk_Extensions.pdf`：DboSession加载/创建/保存/移除设计见175、179—180页，NewSchematic/SaveSchematic见223页，NewPage/SavePage见362页，NewPlacedInst见424—425页。官方capUtils/capSyncPropPCBFootprint.tcl也在修改实例后显式MarkModified。检索稿为[922页API提取](../staging/capture_C_20261019/capture_api_reference.txt)。这些是已读的官方API资料，不代表已逐课观看尚在下载的72讲视频。

下一次继续时先读本笔记和C阶段总结；原生文件用final子目录，run02和首层仅保留历史。恢复桌面通道后补验OPJ打开、PAGE1/PAGE2可见、U101符号排版和Capture命令窗中的只读查询；补验前第11课整体状态保留“原生操作完成、GUI待验”。
