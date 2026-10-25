# 快速清理脚本：扩大四类文本和数据清理，保留网表

日期：2026-10-19。维护源：[eda_cleanup_payload.ps1](../scripts/eda_cleanup_payload.ps1)；入口生成器：[modernize_cleanup_scripts.py](../scripts/modernize_cleanup_scripts.py)。

用户本轮提出：“除了原理图生成的网表，其他的还是需要全部删除；01AIEDA 里面的 txt 文本也排除。”进一步明确选择 **B：扩大 TXT/XML/CSV/DAT 四类删除，其他类型沿用上一版规则**。本记录以 B 为最终要求，取代本轮讨论中“恢复原 82 项全部删除”的 A 假设；A 方案及其测试不得作为最终交付依据。

## 本轮变更与适用范围

25 个入口统一新增默认清理当前 `.txt/.xml/.csv/.dat` 四类文件，原理图网表、受保护目录除外。四类规则不再因“可能是资料或当前数据”而一律保留，也不要求先识别工程或位于编译输出目录。`,数字` 历史副本没有纳入本轮无条件规则，仍按上一版对应主文件条件判断。具体实现以维护源及最终入口清单为准。

**其他规则沿用上一版默认加强清理**：[cleanup_aggressive_20261019.md](cleanup_aggressive_20261019.md)。其日志、会话、编译输出、备份和 OPJ 判定继续有效；其中“当前 TXT/XML/CSV/DAT 默认保留”的条目由本记录替换。更早的 [cleanup_file_policy_20261019.md](cleanup_file_policy_20261019.md) 保留为历史参考。

这次没有恢复原脚本 82 种通配模式的无条件删除。配置、模型和工程设置不因曾出现在原清单里就全部删除；备份、OPJ 和编译产物也没有取消上一版条件。工作区中的原始清点证据仍可查阅 [family_inventory.json](../staging/cleanup_review_20261019/family_inventory.json)。

## 最终删除与保留判定

| 文件类别 | 最终行为 |
| --- | --- |
| 当前 TXT、XML、CSV、DAT | 默认清理，已识别原理图网表和受保护目录除外；逗号数字历史副本继续按上一版备份条件判断。 |
| `.tmp` 及逗号数字副本 | 沿用上一版，默认清理，不要求工程标记。 |
| `.log/.lst/.rpt/.dmp` 及逗号数字副本 | 沿用上一版，在已识别 Cadence、Keil/IAR 或 Altium 工程中清理。 |
| `.jrl/.iex/.drc/.tag` 及逗号数字副本 | 沿用上一版，在已识别 Cadence 工程中清理；JRL 默认开启。 |
| J-Link 日志与 Altium 预览缓存 | 沿用上一版，按识别的工程类型和原定文件名／后缀清理。 |
| 编译、链接和浏览输出 | 仍要求已识别 Keil/IAR 工程，且位于 `obj`、`obj_任意后缀`、`objects`、`list`、`listings`、`browse`、`debug`、`build` 指定构建目录中；仅删上一版列出的产物，不清空整个目录。 |
| `.bak/.dbk/.obk/.sav`、指定设计 ZIP 和其他原有版本副本 | 仍按对应主文件存在、普通非链接、非空、唯一且不早于备份的条件处理；孤立、较新或不能确认冗余的备份保留。TXT/XML/CSV/DAT 的逗号数字副本继续采用此条件，不按当前四类文件直接删除。 |
| `.opj` | 仍仅清理通过完整结构与引用检查的可重建纯原理图外壳；仿真、CIS、专门工具设置、损坏或未知结构的 OPJ 保留，DSN 和库不随之删除。 |
| `.cfg/.sct/.xcl/.dcf/.pro/.dml/.iml/.cnv/.ctl/.icf` 等当前配置和模型 | 沿用上一版保留；此前已允许按对应主文件条件清理的历史副本规则继续存在。不能把这组误写成本轮无条件恢复删除。 |
| `.PrjGrp/.OutJob`、当前 `.bom/.baf/.db` | 沿用上一版保留；不是这次四类扩展范围。 |
| `.edf` | 本轮没有新增 EDF 通配删除；仍沿用上一版保留。网表识别支持 EDIF 内容，用于保护发生改名或同格式输出的文件，并不意味着所有 EDF 先进入清理。 |
| DSN、PCB、库、源码和未命中后缀 | 保留；未新增 `.dsn/.brd/.dra/.psm/.pad/.olb/.PcbDoc/.SchDoc/.PcbLib/.SchLib/.c/.h/.cpp/.uvproj/.uvprojx/.ewp/.eww` 等主文件删除规则。 |

编译输出的既有后缀为 `.obj/.o/.d/.dep/.crf/.lnp/.lst/.pbi/.pbd/.browse/.linf/.pbw/.plg/.__i/.axf/.omf/.map/.htm`。源工程识别和这些输出目录条件仍有实际作用。`Release` 与独立库目录受到下文目录保护，不应声称它们已经纳入编译清理。

## 原理图网表例外

内容命中清理规则后，再识别网表并排除；实际删除前会再次检查，避免扫描后被替换为网表的文件遭删除。以下描述以当前维护源的识别逻辑为准。

| 格式 | 保护条件与已知边界 |
| --- | --- |
| Capture PCB Editor 固定交接文件名 | 精确保留 `pstchip.dat`、`pstxnet.dat`、`pstxprt.dat`、`pstdmlmodels.dat`，大小写不敏感。第四个是可选随附模型。此规则不要求内容非空或三件套同时存在；`tmp_pstchip.dat`、`pstchip.dat,1` 等不是固定名称例外。 |
| PST 内容 | 在 `.dat/.txt/.xml/.csv/.edf/.edif/.net` 非空文件开头最多 65,536 个字符中，识别行首的 `FILE_TYPE = LIBRARY_PARTS;`、`EXPANDEDNETLIST;` 或 `EXPANDEDPARTLIST;`。允许空白和大小写变化，因而改名但保留内容格式的网表仍可保护。 |
| EDIF 网表 | 文件除前置空白外以 `(edif` 开始，流式扫描到 `(viewType NETLIST)` 时保留；短标记跨读取块通过重叠尾部识别。不会完整验证 EDIF 语法和来源，也不会排除另有 SCHEMATIC 视图的混合文件。 |
| PADS 网表 | 开头读取区具有独立行 `*PADS-PCB*`，随后流式扫描同时发现 `*PART*` 与 `*NET*` 或 `*SIGNAL*` 时保留。没有自动覆盖所有 PADS 版本的不同头标识。 |
| Telesis 网表 | 开头读取区具有独立行 `$PACKAGES`，流式扫描发现独立行 `$NETS` 时保留。 |
| XML 网表 | 解析后根元素本地名称为 `netlist` 或 `export`，并同时存在 `components` 和 `nets` 元素时保留。禁用外部 XML 解析器且禁止 DTD；一般配置 XML、Capture 图形/XML 库输出不因后缀是 XML 自动保留。结构识别不证明电气连接正确。 |

除四个固定 DAT 名称外，内容识别仅应用于上述七类扩展名，不扫描任意二进制后缀。普通说明文件仅出现“网表”或 `netlist` 字样，不足以获得例外。无法读取、无法完成检查的 I/O 异常按脚本错误处理保留；损坏 XML 的 XML 解析异常表示未识别为 XML 网表，不能据此获得网表例外。

`compView.dat`、`netView.dat`、`pinView.dat`、`funcView.dat` 属 PCB 回传内容；`pxlBA.txt`、`last_import_time.txt` 属伴随记录。它们不因位于 `allegro/netlist/feedback` 目录自动保留，命中新增 TXT/DAT 规则时仍清理，所在目录受保护的情况除外。

网表的逗号数字旧副本不自动作为当前固定交接文件名保留；内容识别检查的七类扩展名也不含 `,数字`，因此这些旧副本继续采用对应主文件的冗余备份条件。不能只因名字中含 `pst`、`net` 或 `netlist` 就认定安全。

核对证据：

- [学习工程网表目录](../examples/de_15_26_20261019/native_flow_final/baseline/netlist/) 有真实 PST 三件套，分别带有上述三种 `FILE_TYPE`。
- `D:\001DIY\023USB\07usb_com\004usbtoTTL\01sch\allegro` 和 `D:\001DIY\023USB\08UsbIPDapLink\01sch\allegro` 除三件套外均有 `pstdmlmodels.dat`，包含 `PackagedDevice`、`ESpice`、`PinConnections` 模型内容。
- 本机 Cadence 17.2 文档 `C:\Program0\Cadence\spb172\doc\cap_ug\PCB_Editor_netlist_files.html` 列出 PST 三件套；同目录下的 EDIF、PADS PCB、Telesis netlist format 文档给出各格式示例。
- `C:\Program0\Cadence\spb172\doc\cap_ref\dialog_box_descriptions_e.html` 说明 EDF 也可保存 graphical EDIF，后缀不能代替网表内容识别。

## 目录保护

继续按完整目录名、不区分大小写跳过以下目录及全部后代：

| 用途 | 受保护目录名 |
| --- | --- |
| 学习记录 | `01AIEDA` |
| 工作流运行模板 | `01env` |
| 版本与运行环境 | `.git`、`.svn`、`.hg`、`node_modules`、`.venv`、`venv` |
| 备份、归档、历史、原件和发布 | `backup`、`backups`、`archive`、`archives`、`rar`、`zip`、`history`、`original`、`originals`、`release`、`releases` |
| 独立库目录 | `lib`、`libs`、`library`、`libraries` |

`01AIEDA` 采用**整目录保护**，从而同时满足其中 TXT 排除和完整学习记录持续保存；其他后缀也保留。`01env` 同样额外保留，因为包含 BOM、Extract、钻孔和报告等实际运行 TXT 模板。这些不是网表例外，而是明确的目录例外。

`005lib`、`01Psm_lib` 不等于完整名称 `lib`；`backup_work` 不等于 `backup`。如果 BAT 自身或其任一祖先目录命中受保护名称，拒绝执行清理。普通目录里的 TXT 说明、XML 源资料、CSV 表格和 DAT 数据不会因为有使用价值而自动获得目录例外。

同一轮候选中，仍按条件识别的旧备份先于当前四类文本和数据处理，避免对应主文本先被删除后，再核对旧副本时将其错误视为缺少主文件。较新、孤立或空主文件对应的旧副本继续保留。

## TXT 模板补回

原“带复制”入口在清理后继续按各自原配置，从受保护的 `01env` 补回缺失的 `BOM.txt`、`reports.txt`、`drill4noet.txt` 中对应几项；并非所有入口都复制全部三份。来源优先从 BAT 所在目录向祖先查找 `01env`，其次使用既有 `D:\001DIY\005lib\01env`。

**工程根目录同名自定义 TXT 可能先被新增 TXT 规则删除，再由 `01env` 模板补回。** 因此不能再沿用“工程里的所有同名自定义 TXT 都始终保留”的上一版结论。复制阶段只补当时缺失项，不覆盖仍存在的文件、目录或链接；模板源缺失或不是普通文件则输出原因并跳过。

原“带解压”入口仍只清理，不自动展开归档或覆盖环境。此次四类范围调整没有恢复隐式解压。

## 运行方式与验证范围

```bat
0000Ad_Keil_Cadence_dat_iar_txt.bat /preview
0000Ad_Keil_Cadence_dat_iar_txt.bat
```

`/preview` 仅列清理候选和补模板意图，不修改文件。双击或无参数运行会实际清理；目标始终为 BAT 所在目录及允许扫描的子目录。`/history`、`/build` 沿用上一版默认开启且保留兼容；`/help` 可查用法，未知参数报错。

BAT 继续保存为 UTF-8 无 BOM、CRLF，执行 `chcp 65001`，从自身按 UTF-8 读取嵌入 PowerShell，无需依赖外置 PS1。拒绝盘符根和指定系统／用户根目录；跳过链接、联接及其他重解析点；逐文件验证完整绝对路径，再用 `Remove-Item -LiteralPath` 删除；不递归删除整个目录。扫描后大小或修改时间变化会保留。检测到对应 Capture、Allegro、Padstack、Altium、Keil/IAR 进程时，实际清理拒绝执行，预览可继续。

本轮同步目标为既有 25 个入口：工作区 21 个及已授权的外部项目 4 个。本轮修改前快照位于 [cleanup_user_rules_20261019](../../backups/cleanup_user_rules_20261019/)，原始脚本备份仍保留。最终入口配置以 [migration_manifest.json](../staging/cleanup_review_20261019/migration_manifest.json) 为准。

**真实工程本轮只执行预览，不执行清理。** 实际删除验证仅操作 `01AIEDA` 内隔离测试样本，并由测试限定范围；生产脚本仍保持目录保护。最终同步与验证证据写入 `01AIEDA/learning/staging/cleanup_review_20261019/user_rules/final_verification.json`；本记录建立时不预报最终通过次数，也不沿用 A 方案或上一版的测试成绩。
