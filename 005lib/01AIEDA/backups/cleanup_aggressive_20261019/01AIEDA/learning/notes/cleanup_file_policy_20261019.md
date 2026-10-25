# OrCAD Allegro Altium Keil IAR 文件保留与清理规范

日期：2026-10-19。适用范围：`D:\001DIY\005lib` 内的 21 个快速清理 BAT 入口，以及在另外四个项目中找到的同名主入口，共 **25 个已修订入口**；以后复制到其他工程使用时同样按本规范执行。

清理依据是“已确认的文件用途、所在目录、软件是否关闭”，不能仅凭扩展名判断。原理图、PCB、元件库、工程配置、约束、模型、模板、交付文件和恢复备份默认保留。日常快速清理只处理精确名单内的普通日志和 Altium 预览缓存；会话记录和编译中间文件通过独立开关按需处理。

本轮修改清理规则及入口文件，检查用户目录时只运行预览，不实际清理用户项目。脚本运行方式、白名单和测试结果以本文后续实现记录为准。

## 原清理脚本存在的问题

主入口 `0000Ad_Keil_Cadence_dat_iar_txt.bat` 原有 85 条生效删除命令，包括重复规则。19 个同族入口加上 `0KEIL.bat`、`04keil_lib/KEIL.bat`，共审查 21 个清理入口。19 个同族入口的独立通配模式共 82 种；不能因为文件名相近就假设各个版本完全相同。原始逐行规则、SHA256 和命中清单保存在 [原规则清点](../staging/cleanup_review_20261019/family_inventory.json) 和 [范围汇总](../staging/cleanup_review_20261019/family_summary.json)。这些是修订前的历史快照，不代表修订后的运行行为。

原规则有以下具体问题：

- 主脚本虽然注释了 `*.dat`，多个库目录里的同族副本仍会删除全部 DAT；AST2400 的两个 OrcadCaptureXML 副本保留了 XML，不能用旧主脚本覆盖后重新引入 XML 删除。
- `*.txt` 会命中出图脚本、BOM 模板、Extract 命令、软件说明和学习证据；`*.csv` 会命中物料表；`*.xml` 可以是元件库源文件或工程数据。
- `*.sct`、`*.xcl`、`*.cfg`、`*.dcf`、`*.dml`、`*.iml`、`*.cnv`、`*.map`、`*.OutJob` 等可能是用户编写的关键配置或模型，不是普通垃圾。
- `*.opj`、`*.PrjGrp` 是工程管理文件；`*.dbk`、`*.OBK`、`*.sav`、压缩副本包含恢复价值；`*.axf` 可能是必须交付或调试的固件产物。
- 原脚本的 `del /s` 从调用时的工作目录递归，未固定到 BAT 所在目录；双击、命令行或其他程序调用时，范围可能不同。
- “带复制”版本先删全部 TXT，再复制固定路径下的模板。在工作区根运行时，模板源目录 `01env` 本身也会被删除规则命中。复制不应覆盖现有定制文件。
- “带解压”及个别“带复制”副本会启动固定安装位置的 WinRAR，并用 `-y` 自动覆盖 `01env` 内容。快速清理不应附带环境覆盖操作。
- `*.log,1` 等历史副本同样可能属于验收证据；逗号编号不能单独证明可删。重复的 `*.dml,1` 规则、孤立的 `*.dml,` 规则也不能构成可靠分类。

## 已确认的误删命中实例

以下是审查时现有文件的用途。表示“旧规则会命中”，不表示已经发生删除。

| 文件 | 实际用途 | 原规则风险 |
| --- | --- | --- |
| `01env/BOM.txt` | BOM 表头和属性组合模板 | `*.txt` 会破坏模板源 |
| `01env/reports.txt`、`reports_value.txt` | ExtractUI 生成的组件属性抽取命令文件 | `*.txt` 会删除可重用报告配置 |
| `01env/drill2.txt`、`drill2REF.txt`、`drill2VAL.txt`、`drill4.txt`、`drill6.txt`、`drill8.txt` 等 | 内容为 `axlFilmCreate` 的出图设置脚本 | 文件后缀是 TXT，实质是设计工作流配置 |
| `01AIEDA/learning/examples/de_15_26_20261019/BOM_baseline.csv`、`BOM_eco.csv` | 基线及 ECO 后的物料清单 | `*.csv` 会删除采购、审查及对比产物 |
| `01AIEDA/learning/examples/de_15_26_20261019/native_flow_final/baseline/netlist/pstchip.dat`、`pstxnet.dat`、`pstxprt.dat` | 原理图到 PCB 的真实导出网表 | 部分同族入口会删除 `*.dat` |
| `01AIEDA/learning/examples/de_15_26_20261019/native_flow_final/feedback/compView.dat`、`pinView.dat`、`netView.dat`、`funcView.dat` | PCB 回传信息及 ECO 一致性核对输入 | 删除后会丢失本次验收对应的证据 |
| `01AIEDA/learning/staging/a4_review_20261019/packaging/allegro.cfg` | Capture 导出组件、网络等属性的配置 | `*.cfg` 会改变后续导出行为 |
| `01AIEDA/learning/staging/a4_review_20261019/packaging/devices.dml` | 包装流程生成的模型容器；该次文件内容很少 | 这个文件很小不能推导其他 DML 可删，模型库扩展名应保留 |
| `AUTOlib/ul_AST2400/OrcadCaptureXML` 及 `AUTOlib/ast2400lib/01_成品库_ul_AST2400/OrcadCaptureXML` 中的源 XML | 供应商 Capture 符号导入源 | 旧主脚本的 XML 规则不适用于该目录 |
| `01AIEDA/learning/logs`、`examples`、`staging` 内的日志、JRL、备份和文本 | 学习记录、失败定位、读回验证、历史对比 | 即使格式通常可再生成，这次历史证据仍需保留 |

原始清点时，`*.txt` 命中 490 个文件，其中 `01AIEDA` 之外的 16 个全部位于 `01env`。同期清点到 DAT 58 个、CFG 21 个、OPJ 7 个、DML 12 个、CSV 2 个、JRL 92 个、LOG 122 个、LST 7 个、DBK 22 个、OBK 5 个。这些是修订前清点结果，不应作为长期不变的文件数量或实际删除数量。

## 原规则逐类处理清单

本表覆盖清点到的 82 种独立通配模式。大小写在 Windows 文件名比较中不区分；重复删除命令合并解释。原脚本中已经注释的 DSN、BRD、库文件等也继续保护。

| 原规则模式 | 修订后的类别和处理 |
| --- | --- |
| `*.bak`、`*.dbk`、`*.OBK`、`*.sav` | 恢复备份，默认保留。DBK 是 Capture 设计备份，OBK 是库备份；SAV 还可能是错误时保存的布局数据库。不能归入日常清理或编译清理。 |
| `*.opj`、`*.PrjGrp` | 工程管理配置，默认保留。纯原理图 OPJ 可在满足下文条件时人工删除，不纳入批量默认规则。 |
| `*.cfg`、`*.cfg,1`、`*.sct`、`*.xcl`、`*.dcf`、`*.pro` | 配置、内存布局、约束或命令文件，保留。CFG 历史副本也可能是唯一旧版设置。 |
| `*.dml`、`*.dml,`、`*.dml,1`、`*.dml,2`、`*.iml`、`*.iml,1` | SI 器件模型、互连模型及其历史版本，保留。生成的空工作库也不通过扩展名全盘删除。 |
| `*.cnv`、`*.cnv,1`、`*.map` | 转换和层映射配置，保留。本次 `/build` 也不清理 MAP，避免将用户编写的层映射误当链接报告。 |
| `*.baf`、`*.edf`、`*.ctl`、`*.dat`、`*.dat,1`、`*.dat,2`、`*.dat,3`、`*.db` | 反标、图形 EDIF、绘图控制、网表和数据库，默认保留。可由工具重新输出不等于当前版本的文件没有交付和追溯价值。 |
| `*.BOM`、`*.csv`、`*.xml`、`*.txt`、`*.txt,1`、`*.htm` | BOM、源数据、文档、模板或报告，默认保留。不使用这些宽泛后缀进行日常递归删除。 |
| `*.OutJob` | Altium 制造、装配、文档、校验等输出设置，保留；它不是已经生成的临时输出。 |
| `*.PcbLib.Zip`、`*.PcbDoc.Zip`、`*.PrjPCB.Zip` | 备份或归档，保留。其他 ZIP、RAR 同样不自动删除、不自动展开。 |
| `*.log`、`*.log,1`、`*.log,2`、`*.log,3`、`JLinkLog.txt` | 不再按扩展名处理；只有精确常规日志白名单内的文件才可进入默认候选。与故障分析、已发布验收相关的日志应先移入保留目录。 |
| `*.jrl`、`*.jrl,1`、`*.jrl,2`、`*.jrl,3` | 操作会话记录。默认保留，仅 `/history` 按精确程序会话文件名处理，且相关软件已关闭、不需要这段操作历史。 |
| `*.pcbdoc_viewstate`、`*.PCBDOCPreview`、`*.SchDocPreview`、`*.PrjPCBStructure`、`*.$$$Preview`、`*.PCBPreview`、`*.SchPreview` | Altium 显示状态、预览或编译结构缓存，在当前目录或祖先识别到 Altium 工程/设计后进入候选；仅按这些已知缓存后缀处理，不能扩大成任意 ZIP、DAT 或 XML 清理。 |
| `*.obj`、`*.o`、`*.d`、`*.dep`、`*.crf`、`*.__i`、`*.lst`、`*.lnp`、`*.plg` | 通常含对象文件、依赖、浏览/预处理信息及构建日志；默认保留，只在已经识别到 Keil/IAR 工程且位于指定构建目录内时，按 `/build` 的实际白名单选择处理。供应商预编译对象或源目录中的同名文件保留。 |
| `*.pbi`、`*.pbd`、`*.browse`、`*.linf`、`*.pbw` | 部分版本的源浏览、构建信息或工具状态文件；不同版本不能混用解释。只对确认是已识别工程构建目录中的可再生成成员开放 `/build`；不能对工程根及供应商库递归清理。 |
| `*.tmp`、`*.rpt`、`*.tra` | 可能是临时数据、报告、跟踪或未保存的恢复数据；本次默认和 `/build` 均保留，不凭这些扩展名清理。 |
| `*.axf`、`*.omf` | AXF 是带符号可执行映像，OMF 可能是对象模块或构建结果；默认保留。新 `/build` 不删除 AXF、HEX、BIN 等最终固件文件，也不扩大删除未知 OMF。 |
| `*.ddk`、`*.edk`、`*.mpf`、`*.mpj` | 老工具链或其他程序可能使用的项目、状态或数据，不能作为全局垃圾；默认保留。没有足够依据将 MPJ 等一律认定为可再生成缓存。 |
| `*.iex`、`*.dmp`、`*.DRC`、`*.tag` | 用途依工具、流程和目录而变，默认保留。DRC 可能是设计审查报告，DMP 可能用于定位崩溃，未经精确识别不进入默认白名单。 |

## OPJ 与备份的具体规则

Capture 的 `.dsn` 保存原理图数据库；`.opj` 保存对设计、库及其他资源的引用，还可能保存工具对话框和输出相关信息。它是正常工程文件。

对于只画原理图、没有仿真配置和特殊工程设置的项目，如果已关闭 Capture、保留了 `.dsn` 及所需库，并接受重新设置工程引用和输出，可以人工删除 `.opj`。以后直接打开 `.dsn`，软件可能重建工程文件。这个有条件的人工操作，不应变成所有目录都执行的 `del *.opj /s`。纯原理图也可能自定义过工程配置，所以清理器默认保留 OPJ。

DBK、OBK、SAV、BAK 以及压缩归档保留。需要减少备份数量时，应先确认主文件可以正常打开、目标版本已独立备份，再由用户选择具体历史版本处理；本快速清理器不承担备份淘汰功能。锁文件不自动清理，避免干扰当前打开的设计或他人的会话。

## 新入口的运行方式

| 运行方式 | 用途 |
| --- | --- |
| 双击 BAT 或不传参数运行 | 在 BAT 所在目录的授权范围内，只清理精确白名单内的常规日志及满足条件的 Altium 预览缓存；保留工程、配置、模型、源码、输出、备份和学习记录。 |
| `/preview` | 只预览候选及统计，不删除；“带复制”入口也只说明将补齐的模板，不写入用户项目。 |
| `/history` | 在默认候选之外，允许处理名单内的会话 JRL；只适用于相关 EDA 软件已关闭且不需要该操作历史的情况。 |
| `/build` | 在默认候选之外，只处理识别到 Keil/IAR 工程的 Obj、Objects、Listings 等指定构建目录内的白名单中间文件；不删除整个目录，不删源码、链接配置或最终固件。 |

`/preview` 可以与 `/history`、`/build` 组合，用来先检查额外候选。例如先运行 `0000Ad_Keil_Cadence_dat_iar_txt.bat /preview /history`，或 `0000Ad_Keil_Cadence_dat_iar_txt.bat /preview /build`。实际支持的参数组合、工程识别与目录名单以部署脚本为准。

所有入口固定从自身位置解析目标目录，对绝对路径做范围检查；拒绝不适合清理的系统范围，不穿越符号链接、目录联接等重解析点。保护目录包括 `01AIEDA`、`01env`、备份和归档目录，不能靠把日志放在这些目录下再递归删掉来破坏记录。`RAR`、ZIP、RAR 包不展开、不修改。

需要保留某次普通日志用于调试时，应先复制到项目的明确保留目录或 `01AIEDA`；“工具下次可以再生成日志”不能恢复某次故障发生时的原始内容。

## 带复制与带解压入口

“带复制”入口保留补齐模板的用途，但只按该入口原来使用的具体名单补缺失的 `BOM.txt`、`reports.txt`，部分入口另含 `drill4noet.txt`。已有文件一律不覆盖。模板源目录 `01env` 永久排除于清理；找不到源文件时说明缺失，不通过自动解压或删除现有文件来补救。

“带解压”入口停止自动启动 WinRAR、停止 `-y` 覆盖环境。名称暂时兼容旧用法，但不再附带解压动作。环境包如需恢复，应由用户明确选择包和目标后单独操作。

为便于单独复制 BAT 使用，入口采用自包含方式：BAT 中嵌入 Windows PowerShell 载荷，PowerShell 从 BAT 自身按 UTF-8 读取脚本内容。全部修订 BAT 使用 UTF-8 无 BOM、CRLF；不依赖命令提示符的当前代码页解释中文载荷，也不依赖额外复制一个 PS1 文件。

## 同步修订的 21 个清理入口

这些文件用途均为快速清理；供应商目录内的少数同族清理副本也纳入修订。含生成封装、焊盘及调用 Allegro 的 BAT，不因其中出现 `del` 就一起替换。

1. `0000Ad_Keil_Cadence_dat_iar_txt.bat`
2. `0000Ad_Keil_Cadence_dat_iar_txt带复制.bat`
3. `0000Ad_Keil_Cadence_dat_iar_txt带解压.bat`
4. `keilkill.bat`
5. `01brdlib/0000Ad_Keil_Cadence_iar_txt带复制.bat`
6. `01Psm_lib/0000Ad_Keil_Cadence.bat`
7. `01Psm_lib/0000Ad_Keil_Cadence_iar_txt带复制.bat`
8. `04keil_lib/keilkill.bat`
9. `AUTOlib/0000Ad_Keil_Cadence_iar_txt带复制.bat`
10. `AUTOlib/ast2400lib/01_成品库_ul_AST2400/OrcadCaptureXML/0000Ad_Keil_Cadence_iar_txt.bat`
11. `AUTOlib/BGA256/0000Ad_Keil_Cadence_iar_txt带复制.bat`
12. `AUTOlib/QFN30/0000Ad_Keil_Cadence_iar_txt.bat`
13. `AUTOlib/rg45x4/0000Ad_Keil_Cadence_iar_txt带复制.bat`
14. `AUTOlib/STM32F769AG_UFBGA176/0000Ad_Keil_Cadence_iar_txt带复制.bat`
15. `AUTOlib/ul_AST2400/OrcadCaptureXML/0000Ad_Keil_Cadence_iar_txt.bat`
16. `AUTOlib/USB-C-TH_TYPE-C-31-M-43/0000Ad_Keil_Cadence_iar_txt带复制.bat`
17. `PCB_pads_LIB/0000Ad_Keil_Cadence.bat`
18. `PCB_pads_LIB/000Ad_Keil_Cadence.bat`
19. `PCB_pads_LIB/删除ad keil cadence垃圾 .bat`
20. `0KEIL.bat`
21. `04keil_lib/KEIL.bat`

明确排除的例子：`01script_file/TMC6460/TQFN38_5X7.bat`、`01script_file/AST2400/LFBGA408_19X19.bat`、`01captureLib` 与供应商 `AllegroV17_2/backup` 中的封装生成 BAT，以及 `01env/env.bat`、`copyrom.bat` 等环境工具。压缩包里可能还存在旧清理脚本，包内内容本次保留；以后从旧包取出清理入口，应使用本次修订后的入口替换后再运行。

## 官方依据

本地来源为本机 Cadence 17.2 安装目录。下表以文件名和相关段落说明定位，行号仅反映当前本地文档版本。

| 来源 | 支持的事实 |
| --- | --- |
| `C:/Program0/Cadence/spb172/doc/cap_ug/Creating_a_Project.html`，约第 89 行 | OPJ 是设计容器，保存 DSN、引用资源、输出报告和工具信息。 |
| `C:/Program0/Cadence/spb172/doc/cap_ug/Saving_a_project__design__or_library.html`，约第 205—218 行 | DBK/OBK 是备份；DSN 与 OPJ 配套保存。 |
| `C:/Program0/Cadence/spb172/doc/conref/confiles.html`，约第 138 行 | DCF 含设计对象的约束和属性，17.2 流程中使用二进制数据库。 |
| `C:/Program0/Cadence/spb172/doc/sqdml/chapter1.html`，约第 213 行 | DML 保存 SI 器件模型。 |
| `C:/Program0/Cadence/spb172/doc/squg/03_models.html`，约第 713 行 | IML 保存互连模型。 |
| `C:/Program0/Cadence/spb172/doc/algrologic/chap2.html`，约第 325 行 | BAF 包含位号、门/引脚交换等反标信息。 |
| `C:/Program0/Cadence/spb172/doc/dcoms/dchap.html`，约第 35977 行；`doc/discrete_to_ads/discrete_to_ads.html`，约第 601 行 | CNV/MAP 可以是可编辑的层转换映射配置。 |
| `C:/Program0/Cadence/spb172/doc/algroman/chap5.html`，约第 645—650 行 | CTL 是绘图控制文件，允许编辑。 |
| `C:/Program0/Cadence/spb172/doc/cap_ref/dialog_box_descriptions_e.html`，约第 888 行 | EDF 可以保存图形 EDIF 设计，并不一定只是网表。 |
| `C:/Program0/Cadence/spb172/doc/algroidf/chap1.html`，约第 405 行；`doc/icoms/ichap.html`，约第 1638 行 | PRO 可为 Pro/ENGINEER 配置或 Extract 命令文件。 |
| `C:/Program0/Cadence/spb172/doc/cap_ug/Property_Flow_from_Capture_to_PCB_Editor.html`，约第 91—109 行 | Allegro CFG 控制 Capture 到 PCB Editor 的属性传递。 |
| `C:/Program0/Cadence/spb172/doc/algrostart/chap1.html`，约第 3453、3463、5049 行 | DBDoctor 日志用于诊断；SAV 可用于错误后的数据库恢复；JRL 是会话事件记录。 |
| `C:/Program0/Cadence/spb172/doc/algrologic/chap1.html`，约第 305 行 | `netrev.lst` 记录导入是否成功及警告、错误。 |
| `C:/Program0/Cadence/spb172/doc/algrolibdev/chap5.html`，约第 1193 行 | `dev_check.log` 保存器件与封装检查结果。 |
| `C:/Program0/Cadence/spb172/doc/algroskill/22extrct.html`，约第 226 行 | `extract.log` 可用于分析抽取失败原因。 |

补充的官方网络来源：

- [Keil Arm Linker 设置](https://www.keil.com/support/man/docs/uv4/uv4_dg_adsld.asp)：SCT 指定映像各内存区域和段的组织、放置。
- [IAR 创建应用工程](https://updates.iar.com/FileStore/STANDARD/001/000/590/ew/doc/infocenter/GettingStarted/CreatingAnApplicationProject/CreatingAnApplProj.ENU.html)：XCL 是 XLINK 的链接配置，可作为项目自定义内存布局输入。
- [IAR 文件类型](https://docs.iar.com/ewrx/5.2x/en/ide-project-management-and-building/product-files/file-types.html)：列出对象模块、依赖、PBI/PBD 浏览信息、项目、工作区、ICF 和 XCL 等文件用途；该版本说明不应直接套用所有历史工具版本。
- [Altium 使用 Output Jobs 准备制造数据](https://www.altium.com/documentation/altium-designer/preparing-for-manufacture/output-jobs)：OutJob 保存输出集合与输出设置，可跨项目复用并纳入工程。

## 本轮验证与交付

本轮用户工程只运行了 `/preview`，没有执行实际清理。删除分支只在 `01AIEDA` 内自建的隔离样例中测试；测试通过导入函数及限定到该样例的根目录检查执行，不改变生产入口对 `01AIEDA` 的保护。

### 最终运行名单

- Cadence：在当前目录或祖先识别到 `.dsn/.brd/.dra/.pad/.psm/.olb/.opj` 时，默认只清 `allegro.log`、`padstack.log`、`padstack_editor.log`、`netlist.log`、`netrev.lst`、`dev_check.log`、`genfeed.log`、`swp.log`、`extract.log`、`dbdoctor.log`、`batch_drc.log`，及这些精确名称的逗号数字副本。删除会失去对应诊断历史，仍需保留的日志应归档。
- Altium：识别到 `.PcbDoc/.SchDoc/.PcbLib/.SchLib/.PrjPCB` 后，清理上表列出的预览/显示状态/编译结构缓存。
- J-Link：识别到 Keil/IAR 工程后，只清 `JLinkLog.txt`、`JLinkARM.log`。
- `/history` 额外加入 `allegro.jrl`、`padstack_editor.jrl` 和逗号数字副本。它们含会话回放信息，默认保留。
- `/build` 额外加入 `obj/objects/list/listings/browse` 构建目录中的 `.obj/.o/.d/.dep/.crf/.lnp/.lst/.pbi/.pbd/.browse/.linf/.pbw/.plg`。必须同时识别到 `.uvproj/.uvprojx/.uv2/.ewp/.eww` 工程，且这些文件可从源码重新生成；不清整个文件夹、不删 `.axf/.elf/.out/.hex/.bin/.lib/.a` 或链接配置。

清理范围固定为 BAT 所在目录。跳过 `01AIEDA`、`01env`、备份/归档/历史/原件/发布目录、RAR/ZIP 归档目录、版本管理目录和目录联接；不因 `v1/version1/17.2` 等目录名就把实际工作工程排除，其源码和配置仍保留。若 BAT 自己位于受保护目录中也拒绝清理。删除逐文件使用 PowerShell `Remove-Item -LiteralPath`，检查绝对路径边界、文件修改时间、大小和重解析点，不再使用无区别 `del /s`。

实际清理要求先关闭 Capture、Allegro、Padstack、Altium、Keil/IAR；检测到这些软件的已知主进程运行时只允许预览。带复制的入口只补缺失模板，保留已经存在的定制文件；带解压及暗含解压的三个旧入口已取消自动解压覆盖。

### 验证结果

- **83 项隔离行为测试通过，0 失败**。覆盖中文和空格/`!&()`/单引号路径、预览内容不变、未知参数拒绝、配置/固件/数据保护、项目识别与构建目录双条件、可选历史清理、模板不覆盖、扫描后文件改变拒绝，以及实际 junction 目标不受影响。文件 symlink/悬空 symlink 因当前环境权限或平台行为限制跳过，未把跳过项算作通过。[测试脚本](../scripts/test_eda_cleanup.ps1)、[最终验证汇总](../staging/cleanup_review_20261019/final_verification.json)。
- **21 个工作区 BAT 实际 CMD 预览入口通过**，均从无关工作目录调用，确认目标仍为 BAT 所在目录、`removed=0`、正确退出码；57 个重点设计/模板/工程/BOM 文件哈希未变化。另验证含中文、空格和 `!&()` 的 BAT 路径能调用。[入口验证报告](../staging/cleanup_review_20261019/entrypoint_verification.json)。
- **另外 4 个项目同名副本已同步并通过实际 CMD 预览**，均使用与已验证主入口相同的内容。位置分别为 `D:/001DIY/000driver/18Brushless/01SCH`、`D:/001DIY/023USB/07usb_com/004usbtoTTL/01sch`、`D:/001DIY/023USB/08UsbIPDapLink/01sch` 和同项目 `02pcb`。只替换 BAT，没有清理这些工程。[同步记录](../staging/cleanup_review_20261019/external_sync_result.json)、[外部入口预览](../staging/cleanup_review_20261019/external_preview_verification.json)。
- **25 个入口均为 UTF-8 无 BOM、CRLF**。无 BOM 避免 CMD 将首行 BOM 识别为命令；ASCII 启动段设定代码页65001，嵌入载荷由 PowerShell 显式按 UTF-8 读取。中文路径的实际调用已验证，不依赖 PowerShell 5.1 对无 BOM 文件的隐式编码判断。原始备份保持原字节和原编码，以便可靠回退。

原始脚本备份在 `01AIEDA/backups/cleanup_scripts_20261019`；四个其他项目副本的原件在 `01AIEDA/backups/cleanup_scripts_20261019_external`。原件哈希、改后哈希和各入口原复制功能见 [迁移清单](../staging/cleanup_review_20261019/migration_manifest.json)。这些备份是历史版本，不应作为当前清理入口使用。

统一维护源为 [PowerShell 清理逻辑](../scripts/eda_cleanup_payload.ps1)，[生成器](../scripts/modernize_cleanup_scripts.py)负责将同一逻辑嵌入工作区21个入口。生成器先备份原件，不执行清理；外部四个副本的同步另有记录。以后复制任意修订后的 BAT 到工程即可独立运行，不需要另外复制 PS1。
