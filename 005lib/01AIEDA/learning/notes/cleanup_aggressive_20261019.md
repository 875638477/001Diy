# 快速清理脚本：默认加强清理记录

> **这是前版历史记录，不再代表当前默认行为。** 用户最终明确XML/CSV/DAT全部保留，TXT排除01AIEDA内文件，其余恢复各入口原删除名单；配置、模型、备份和OPJ的前版保留条件已被覆盖。当前以 [最新清理规范](cleanup_user_rules_20261019.md) 为准，本文217项测试仅证明当时版本。

日期：2026-10-19。适用：`0000Ad_Keil_Cadence_dat_iar_txt.bat` 及同族清理入口；本轮同步范围为既有 25 个入口。

## 用户要求与本轮调整

用户明确要求：“保持原来的删除选项尽量删除垃圾。”本轮据此扩大默认清理范围：日志、报告、会话记录、临时文件、预览缓存，以及已识别 Keil/IAR 工程构建目录中的指定编译输出，直接纳入默认清理。`/history`、`/build` 保留兼容，二者现在默认开启。

原脚本的 82 种独立通配模式仍作为逐项审查依据。恢复清理力度不等于恢复对全部 TXT、XML、DAT、配置和模型的无差别删除；这些文件中已有实际设计输入、模板和元件库数据。本记录取代此前“默认仅清具体名称日志”的运行说明。历史版本和原始命令清点仍保留，不能拿历史清点数量当作本次实际删除数量。

维护源：[eda_cleanup_payload.ps1](../scripts/eda_cleanup_payload.ps1)。以下名单以该脚本的实际判定为准，后缀比较不区分大小写。

## 默认清理名单

| 后缀／文件名 | 默认清理条件 |
| --- | --- |
| `.tmp`、`.tmp,数字` | 在清理范围内、且不在受保护目录或链接中，即进入候选；不要求先识别 EDA 工程。 |
| `.log`、`.lst`、`.rpt`、`.dmp`，以及这些后缀的 `,数字` 副本 | 当前目录或祖先目录识别到 Cadence、Keil/IAR 或 Altium 工程／设计。现在包含自定义名称日志，不限此前点名的少数日志。 |
| `.iex`、`.drc`、`.tag`，以及 `,数字` 副本 | 已识别 Cadence 设计／工程。 |
| `.jrl`、`.jrl,数字` | 已识别 Cadence 设计／工程；会话记录默认清理，无需再加 `/history`。 |
| `JLinkLog.txt`、`JLinkARM.log` | 已识别 Keil/IAR 工程。`JLinkLog.txt` 是当前 TXT 保留规则中的明确例外。 |
| `.pcbdoc_viewstate`、`.pcbdocpreview`、`.schdocpreview`、`.pcbpreview`、`.schpreview`、`.prjpcbstructure`、`.$$$preview` | 已识别 Altium 工程／设计。 |
| `.obj`、`.o`、`.d`、`.dep`、`.crf`、`.lnp`、`.lst`、`.pbi`、`.pbd`、`.browse`、`.linf`、`.pbw`、`.plg`、`.__i`、`.axf`、`.omf`、`.map`、`.htm` | 已识别 Keil/IAR 工程，并且文件位于下表指定的构建目录中。无需再加 `/build`。只删这些文件，不删整个目录。 |

构建目录名为 `obj`、`obj_任意后缀`、`objects`、`list`、`listings`、`browse`、`debug`、`build`，匹配任意一层目录名。其后代文件也受相同条件约束。`Release`、`lib`、`library` 等受保护目录仍跳过；不能把它们误写成已纳入清理的构建目录。

工程识别依据：Cadence 为 `.dsn/.brd/.dra/.pad/.psm/.olb/.opj`；Keil/IAR 为 `.uvproj/.uvprojx/.uv2/.ewp/.eww`；Altium 为 `.PcbDoc/.SchDoc/.PcbLib/.SchLib/.PrjPCB`。识别状态向已扫描目录的子目录继承。

## 默认按条件清理：备份、历史副本与 OPJ

### 冗余备份及版本副本

只有找到**唯一对应、非空、普通且非链接的主文件**，并且主文件修改时间不早于备份时，才删除备份。主文件缺失、为空、对应关系不唯一，或备份比主文件更新，均保留。删除前会重新检查对应主文件是否仍满足条件。

| 候选备份模式 | 对应主文件判定 |
| --- | --- |
| `.dbk` | 同名 `.dsn`；同时识别 Capture 常见的 `_数字` 备份后缀。 |
| `.obk` | 同名 `.olb`；同时识别 `_数字` 备份后缀。 |
| `.sav` | 同名 `.brd/.dra/.pad`；同时识别 `_数字` 备份后缀。 |
| `.bak` | 优先考虑去掉 `.bak` 后的完整原文件名，再考虑同名 `.dsn/.olb/.brd/.dra/.pad/.opj/.cfg/.c/.h/.cpp/.sct/.xcl/.icf`；也识别 `_数字` 备份后缀。最终必须恰好有一个对应主文件。 |
| `.PcbDoc.Zip`、`.PcbLib.Zip`、`.PrjPCB.Zip` | 去掉 `.Zip` 后的对应设计／工程文件。其他 ZIP 不按此规则处理。 |
| `.dsn/.brd/.dra/.pad/.psm/.olb/.opj/.dat/.txt/.cfg/.cnv/.iml/.dml/.ctl/.dcf/.xml/.csv/.bom/.log/.jrl` 的 `,数字` 副本 | 去掉最后 `,数字` 后的同名当前文件。当前主文件仍保留；日志和 JRL 副本若已命中前面的默认日志／会话规则，则按前面的规则清理。 |

这些规则处理冗余版本，不判断当前主文件是否已通过软件打开或电气检查；主文件存在且时间较新不能代替设计验收。备份、归档目录始终受目录保护，不会因为目录内另有主文件就被扫描删除。

### 纯原理图 `.opj`

`.opj` 属于工程管理文件。本轮允许默认删除符合保守结构判定的纯原理图工程外壳；`.dsn` 和 `.olb` 不随之删除。具体条件包括：

- 文件非空且不超过脚本设定的大小上限，具有合法 `ExpressProject` 表达式，工程类型是 `PCB` 或 `Schematic`。
- 括号、字符串和节点通过完整结构检查；存在未知节点、损坏内容或多段根表达式时保留。
- File 引用仅包含 `.dsn/.olb`，其中恰好一份 `.dsn`；引用文件都必须存在、非空，位于本次清理范围内，且不经过文件／目录链接。
- 出现 PSpice、Simulation、CIS、DataSource、ToolSettings、Constraint、DBC 等仿真、数据库或专门设置特征时保留。
- 删除前再次检查引用和结构。不能确认是可重建纯原理图外壳的 OPJ 继续保留。

普通窗口位置等已知状态节点可以通过结构检查，但不是所有历史 Capture 版本的 OPJ 节点都在允许表中；未知格式会保留。删除 OPJ 后，再次打开 DSN 可能重新生成工程文件，原工程窗口和路径设置可能需要重建。

## 默认保留名单

| 类别 | 保留后缀／内容 | 例外与说明 |
| --- | --- | --- |
| 原理图、PCB、元件库 | `.dsn .brd .dra .pad .psm .olb .PcbDoc .SchDoc .PcbLib .SchLib .IntLib` | 当前设计和库保留；冗余 `,数字` 备份按上面的对应主文件规则处理。 |
| 正式工程与输出设置 | `.PrjPCB .PrjGrp .OutJob .uvproj .uvprojx .uv2 .uvopt .uvoptx .opt .ewp .eww` | OPJ 只有满足上面的严格条件才清理；仿真/CIS/专门设置工程保留。 |
| 当前数据、网表与 BOM | `.dat .txt .xml .csv .bom .edf .baf .db` | 当前 DAT 包括 `pstchip.dat/pstxnet.dat/pstxprt.dat` 全部保留。TXT 中明确的 `JLinkLog.txt` 例外；部分 `,数字` 历史副本按冗余版本规则处理。 |
| 配置、约束、模型与链接输入 | `.cfg .sct .xcl .dcf .pro .dml .iml .cnv .ctl .icf` | 当前文件保留。SCT/XCL 是链接配置输入，不能因原清理脚本曾列出就恢复删除。部分 `,数字` 副本可按冗余版本条件清理；`.dml,` 这样的孤立逗号模式不恢复。 |
| 源码、脚本、模板 | `.c .h .cpp .s .asm .inc .bat .ps1 .py .tcl .il` 等，以及 `BOM.txt/reports.txt/reports_value.txt/drill*.txt` 等工作流模板 | 当前 TXT 通配保留，避免删除 BOM 属性模板、Extract 命令、出图设置和说明资料。 |
| 固件与预编译库 | `.hex .bin .elf .out .lib .a` | 本轮仍保留；`.axf/.omf` 仅在已识别工程的指定构建目录中默认清理。 |
| 未明确确认用途的原模式 | `.ddk .edk .mpf .mpj .tra` | 未恢复为默认删除规则，不把未知工程／数据文件直接当垃圾。 |
| 不满足清理条件的备份和压缩包 | 孤立或更新的 `.bak .dbk .obk .sav`、普通 `.zip .rar` 及其他归档 | 只有明确列出的冗余设计 ZIP 才可能按主文件条件清理。 |
| 其他未列入清理规则的文件 | 包括不在指定嵌入式构建目录中的 `.map/.htm/.obj/.o/.axf/.omf` | 按未命中规则保留；`.htm` 文档不会全盘通配删除。 |

上述分组覆盖原脚本的独立通配模式：生成日志／临时／检查文件、JRL 及数字副本、Altium 预览、编译输出、OPJ、恢复备份、设计 ZIP、当前网表／报告数据、配置模型、TXT/XML/CSV，以及 DDK/EDK/MPF/MPJ/TRA 等未确认模式。原清点见 [family_inventory.json](../staging/cleanup_review_20261019/family_inventory.json)。

## 目录保护与删除边界

默认跳过 `01AIEDA`、`01env`、`.git/.svn/.hg`、`node_modules`、`.venv/venv`、`backup/backups`、`archive/archives`、`RAR/ZIP`、`history`、`original/originals`、`release/releases`、`lib/libs/library/libraries`。名称比较不区分大小写。这些目录本身及其后代均受保护；BAT 自己位于受保护目录内时也拒绝清理。

BAT 固定清理自身所在目录及符合条件的子目录。逐个文件核对完整绝对路径，使用 PowerShell `Remove-Item -LiteralPath`，不通过拼接 CMD 删除命令操作。拒绝盘符根目录和指定系统／用户根目录，跳过重解析点、目录联接、文件链接；扫描后大小或修改时间变化的文件会保留。

实际清理前需关闭 Capture、Allegro、Padstack、Altium、Keil/IAR 等脚本识别的设计／构建软件。检测到相关进程时只允许预览，防止删除软件还在使用的会话和中间文件。

## 调用方式与编码

```bat
0000Ad_Keil_Cadence_dat_iar_txt.bat /preview
0000Ad_Keil_Cadence_dat_iar_txt.bat
0000Ad_Keil_Cadence_dat_iar_txt.bat /help
```

第一条仅预览，第二条执行默认加强清理。旧调用中的 `/history`、`/build` 仍接受，不再扩大默认范围，因为对应功能默认已开启。未知参数会在删除前报错。

“带复制”入口继续按原入口指定清单补齐缺失模板，不覆盖已有定制文件；“带解压”入口不自动覆盖解压环境。所有入口保持自包含：BAT 中嵌入同一份 PowerShell 逻辑，单独复制 BAT 即可使用。

入口编码要求为 **UTF-8 无 BOM、CRLF 换行**。ASCII 启动段设置代码页 65001，PowerShell 显式以 UTF-8 读取嵌入内容，避免 Windows PowerShell 5.1 默认解码行为影响中文和脚本运行。原始历史备份保持原字节，不为统一编码改写历史证据。

## 备份、同步与验证记录

本轮修改前快照保存在 [cleanup_aggressive_20261019](../../backups/cleanup_aggressive_20261019)，包括本轮前的脚本版本和相关验证材料。更早的最原始脚本仍在 [cleanup_scripts_20261019](../../backups/cleanup_scripts_20261019) 及 [cleanup_scripts_20261019_external](../../backups/cleanup_scripts_20261019_external)。

已同步既有 25 个清理入口：工作区内 21 个，以及此前已授权处理的其他项目中 4 个同名脚本。外部更新只按精确文件名单替换 BAT，核对修改前、备份和新版本的 SHA256；不执行项目清理。工作区清单见 [migration_manifest.json](../staging/cleanup_review_20261019/migration_manifest.json)，外部同步见 [external_sync_result.json](../staging/cleanup_review_20261019/aggressive/external_sync_result.json)。

新版通过 **217 项隔离行为测试，0 失败**，报告中的生产载荷哈希与部署版本一致。测试脚本是 [test_eda_cleanup_aggressive.ps1](../scripts/test_eda_cleanup_aggressive.ps1)，结果见 [results.json](../staging/cleanup_review_20261019/aggressive/tests/run_20261019_090949_859861cd/results.json)。覆盖默认删除/保留、普通GUI纯原理图OPJ、仿真/CIS/未知OPJ保留、旧/更新/孤立备份、扫描后主文件变化复查、预览不变、路径边界和实际目录联接。文件符号链接样例因创建权限不足跳过，未声称该项已实测通过。

实际 BAT 入口由 [verify_cleanup_entrypoints.py](../scripts/verify_cleanup_entrypoints.py) 和 [finalize_cleanup_review.py](../scripts/finalize_cleanup_review.py) 仅运行 `/preview` 检查：**25个入口的CMD预览全部通过，57份关键设计/模板文件哈希未变**，25份BAT均为UTF-8无BOM及CRLF，记录中的本地链接无失效。汇总见 [final_verification.json](../staging/cleanup_review_20261019/aggressive/final_verification.json)。用户实际工程未执行删除；删除分支仅处理 `01AIEDA` 内自建隔离样例。此前83项结果只代表旧保守策略。

## 官方依据

- [Keil 文件类型](https://www.keil.com/support/man/docs/uv4cl/uv4cl_b_filetypes.htm)：区分构建输出、源码、工程配置和链接控制；XML 也可能是供应商设备描述，SCT 属于链接控制输入。
- [Keil Clean Target 范围](https://www.keil.com/support/man/docs/uv4cl/uv4cl_ui_project.htm)：官方清理按 Object/Listing 输出目录区分中间产物，本轮借鉴目录条件。该官方命令的全部删除范围与本脚本并不相同。
- 本机 Cadence 17.2 官方文档依据沿用 [初次文件分类记录](cleanup_file_policy_20261019.md) 中的逐项来源；旧文档的默认删除策略由本记录更新，原始用途说明和历史审查证据仍保留。
