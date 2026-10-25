# 快速清理脚本：XML／CSV／DAT 保留，按原名单清理其他类型

日期：2026-10-19。维护源：[eda_cleanup_payload.ps1](../scripts/eda_cleanup_payload.ps1)；入口生成器：[modernize_cleanup_scripts.py](../scripts/modernize_cleanup_scripts.py)。

用户最终明确：“XML、CSV、DAT 这些全部保留不删，其余都删除，只是 01AIEDA 里面 TXT 不删。”本记录覆盖此前 A/B 讨论及 [cleanup_aggressive_20261019.md](cleanup_aggressive_20261019.md)、[cleanup_file_policy_20261019.md](cleanup_file_policy_20261019.md) 的运行规则。此前版本和原始清点仅作历史证据，不能用其保留条件或测试成绩代表最终版本。

## 最终判定顺序

1. **全局保留 XML、CSV、DAT**，包括当前文件及以 `,数字` 结尾的历史副本。与文件内容、是否网表、是否能重新生成无关。
2. **保留任一祖先目录完整名称为 `01AIEDA` 的 TXT 及 TXT 数字历史副本**，目录名和扩展名均不区分大小写。保护使用完整绝对路径，BAT 即使直接放在 `01AIEDA` 内启动，也不会误删其中 TXT。
3. 对其他文件，恢复各入口原脚本实际启用的删除模式；所有入口统一增加当前 `*.txt` 清理。命中名单、且未受本文其他例外保护时删除。
4. 继续跳过明确的运行环境／备份／归档目录和链接；保留已识别的其他格式原理图网表。

“其余都删除”落实为**原脚本清理名单加 TXT**，没有扩大成目录内所有文件全删，也没有启用原来注释的 DSN／PCB／库文件删除语句。

各入口从保存的原始 BAT 读取有效 `del` 命令，注释不算启用规则。Keil 专用入口仍只使用其原 Keil 项并增加 TXT，不套用 Cadence 的整套清单。XML／CSV／DAT 的全局保留优先于模式，即使某入口的原始模式中仍出现这些类型，也不会执行删除。最终每入口模式见 [migration_manifest.json](../staging/cleanup_review_20261019/migration_manifest.json) 的 `cleanup_patterns`。

## 明确保留清单

| 范围 | 最终行为 |
| --- | --- |
| `*.xml`、`*.csv`、`*.dat` | 全部保留，不只保留识别成功的网表。空文件、普通数据、配置 XML、表格 CSV、PCB 回传 DAT 也保留。 |
| `.xml/.csv/.dat` 的 `,数字` 副本 | 全部保留，例如 `settings.xml,1`、`bom.csv,7`、`pstxnet.dat,99`，不要求对应当前文件存在或较新。 |
| 绝对路径任一祖先为 `01AIEDA` 的 `*.txt`、`*.txt,数字` | 全部保留，包含学习记录、测试 TXT 和日志型 TXT；不是只按文件用途判断。 |
| 原设计主文件与未列后缀 | `.dsn/.brd/.dra/.psm/.pad/.olb`、`.PcbDoc/.SchDoc/.PcbLib/.SchLib`、`.c/.h/.cpp`、`.uvproj/.uvprojx/.ewp/.eww` 等不在原启用删除名单内，因此没有新增删除。 |
| 明确受保护目录 | 下节所列目录及全部后代保留；这部分是目录例外。 |
| 其他格式的已识别网表 | 作为额外例外保留，格式边界见后文。 |

XML／CSV／DAT 不再依赖网表识别，因此 `compView.dat`、`netView.dat`、`pinView.dat`、`funcView.dat`、一般非网表 DAT 也全部保留。固定网表 `pstchip.dat`、`pstxnet.dat`、`pstxprt.dat`、`pstdmlmodels.dat` 自然包含在全局 DAT 保留范围内。

当前保留正则识别 `.xml/.csv/.dat` 及其 `,数字` 结尾；`file.dat.bak` 的最终后缀为 BAK，仍可能按该入口的 `*.bak` 清理。`file.xml.old` 等其他命名不因为中间有 `.xml` 就自动获得全局保留，是否清理由实际模式决定。

## 默认删除清单

原同族清点包含 82 种去重模式，见 [family_inventory.json](../staging/cleanup_review_20261019/family_inventory.json)。全局 XML／CSV／DAT 规则从执行层覆盖相应模式；其余仍按**每入口自己的原名单**恢复。以下是所有入口合并后的类型说明，不表示每份 Keil 脚本都有全部规则。

| 类型 | 恢复的原清理模式 |
| --- | --- |
| TXT | 所有入口统一增加 `*.txt`；原有的 `*.txt,1`、`JLinkLog.txt` 等仍存在。`01AIEDA` 内所有 TXT 数字副本受保护；其他位置的 TXT 数字副本仅在原模式命中时清理，不新增任意 `*.txt,数字` 通配。 |
| 日志、报告和临时文件 | `*.log`、`*.log,1`、`*.log,2`、`*.log,3`、`*.lst`、`*.rpt`、`*.tmp`、`*.dmp`、`*.iex`、`*.DRC`、`*.tag` |
| 会话记录 | `*.jrl`、`*.jrl,1`、`*.jrl,2`、`*.jrl,3` |
| 编译、链接和浏览相关文件 | `*.__i`、`*.axf`、`*.browse`、`*.crf`、`*.d`、`*.dep`、`*.linf`、`*.lnp`、`*.map`、`*.o`、`*.obj`、`*.omf`、`*.pbd`、`*.pbi`、`*.pbw`、`*.plg` |
| 备份和指定设计压缩副本 | `*.bak`、`*.dbk`、`*.OBK`、`*.sav`、`*.PcbDoc.Zip`、`*.PcbLib.Zip`、`*.PrjPCB.Zip` |
| 工程外壳、工程组和输出设置 | `*.opj`、`*.PrjGrp`、`*.OutJob` |
| 配置、约束、模型和转换输入 | `*.cfg`、`*.cfg,1`、`*.cnv`、`*.cnv,1`、`*.ctl`、`*.dcf`、`*.dml`、`*.dml,`、`*.dml,1`、`*.dml,2`、`*.iml`、`*.iml,1`、`*.pro`、`*.sct`、`*.xcl` |
| 其他交换／数据／文档 | `*.baf`、`*.BOM`、`*.db`、`*.edf`、`*.htm`；识别成功的其他格式网表例外见后文。 |
| Altium 预览与结构缓存 | `*.$$$Preview`、`*.pcbdoc_viewstate`、`*.PCBDOCPreview`、`*.PCBPreview`、`*.PrjPCBStructure`、`*.SchDocPreview`、`*.SchPreview` |
| 其他原有模式 | `*.ddk`、`*.edk`、`*.mpf`、`*.mpj`、`*.tra` |

原清单中的 `*.xml`、`*.csv`、`*.dat`、`*.dat,1`、`*.dat,2`、`*.dat,3` **不删除**；这一优先规则不能被原命令清点表反向覆盖。

恢复原名单后，以下上一版条件已取消：

- 无需先识别 Cadence／Altium／Keil 工程。目录里单独存在命中模式的文件也可清理。
- 编译产物不再限定必须位于 `obj/objects/debug/build` 等输出目录。`lib/library/release` 也不再整体跳过。
- 备份不再要求存在对应主文件，不再比较主文件是否非空、唯一或时间较新。孤立备份和较新备份若命中原名单也会删除。
- `.opj` 不再判断是否纯原理图外壳。该入口原名单有 `*.opj` 时，含仿真、CIS 或专门设置的 OPJ 也会删除；DSN 不随之删除，但不能承诺工程设置保留。
- 当前 SCT／XCL／CFG／DCF／DML／IML／CNV／CTL／PRO／MAP／OutJob／PrjGrp 等配置或模型不再享有上一版全局保留。命中所属入口名单就清理，受保护目录除外。

文件可能有人工编辑价值不再构成自动保留理由。例如 TXT 说明、SCT 内存布局、DCF 约束或 DML 模型都可能被原清理模式命中；当前记录必须如实反映这一点，不能继续声称关键配置全部保留。

## 01AIEDA 与其他目录

`01AIEDA` **已取消整目录保护，只精确排除 TXT 及 TXT 数字历史副本**。其中 XML／CSV／DAT 及数字副本依靠全局规则保留；LOG／JRL／OPJ／DBK／配置等仍可能按原清单删除。MD／JSON／PS1／PY／BAT 等未命中清单的记录和维护源保留，但不能据此承诺全部学习产物都不清理。

继续整体保护以下完整目录名及所有后代，大小写不敏感：

| 用途 | 完整目录名 |
| --- | --- |
| 实际运行模板 | `01env` |
| 版本和运行环境 | `.git`、`.svn`、`.hg`、`node_modules`、`.venv`、`venv` |
| 备份、归档、历史和原件 | `backup`、`backups`、`archive`、`archives`、`rar`、`zip`、`history`、`original`、`originals` |

`01env` 含 BOM、Extract、钻孔、报告等运行 TXT 模板，属于明确的额外目录例外，不属于网表例外。普通 `lib/libs/library/libraries/release/releases` 不在当前整体保护表中；这些目录内符合原模式的文件可清理。

目录名完整匹配：`005lib` 不等于 `lib`，`backup_work` 不等于 `backup`，`01AIEDA_old` 不等于 `01AIEDA`。根目录或任一祖先命中整体受保护目录名时，脚本拒绝清理；`01AIEDA` 本身不再触发整根拒绝，只触发其中 TXT 的精确保护。

## 其他网表格式例外

XML／CSV／DAT 及数字副本已经全局保留，不需要识别内容。为兼顾先前“原理图生成网表保留”的要求，脚本还保留其他扩展名中可识别的网表；这属于额外例外，不能简化成“网表以外所有 TXT 都删除”。

- 对 `.dat/.txt/.xml/.csv/.edf/.edif/.net` 非空文件，开头最多 65,536 字符内，行首出现 `FILE_TYPE = LIBRARY_PARTS;`、`EXPANDEDNETLIST;` 或 `EXPANDEDPARTLIST;` 时识别为 PST。允许空白和大小写变化。
- EDIF 文件除前置空白外以 `(edif` 开始，流式扫描发现 `(viewType NETLIST)` 时保留；不完整验证 EDIF 语法或来源，也不排除同文件另有 SCHEMATIC 视图。
- PADS 文件开头读取区有独立行 `*PADS-PCB*`，流式扫描同时发现 `*PART*` 与 `*NET*` 或 `*SIGNAL*` 时保留；未覆盖所有 PADS 历史版本的不同头标识。
- Telesis 文件开头读取区有独立行 `$PACKAGES`，流式扫描发现独立行 `$NETS` 时保留。
- XML 内容识别仍支持根元素本地名 `netlist/export` 且同时有 `components/nets` 的格式；禁止 DTD 和外部解析器。但 XML 当前是否清理已经由全局保留决定，不依赖这个结构检查成功。

普通文本仅提到“网表”或 `netlist` 不足以获得内容例外；四个精确 PST DAT 文件名保留规则也不意味着任意名称含 `pst` 就保留。I/O 异常导致不能检查时，本次保留并输出原因；XML 解析异常表示没有通过结构识别，不能据此取得额外格式例外。网表内容识别不适用于 `,数字` 扩展名，但 XML／CSV／DAT 数字副本仍已受全局保留。

`.edf` 在原清理模式中，可能是图形 EDIF 或网表；只有通过当前内容识别的网表获得该项额外保护。`.net/.edif` 通常不在原清理名单中，本来也不删除。参考本机 Cadence 17.2 文档 `C:\Program0\Cadence\spb172\doc\cap_ug\PCB_Editor_netlist_files.html` 及同目录 EDIF、PADS PCB、Telesis 格式说明；`cap_ref\dialog_box_descriptions_e.html` 说明 EDF 也可保存 graphical EDIF，后缀本身不能证明是网表。

## 复制变体、运行与验证

原“带复制”入口在清理后，按各自原配置从受保护的 `01env` 补回缺失的 `BOM.txt`、`reports.txt`、`drill4noet.txt` 中对应几项；并非所有入口复制全部三份。来源优先向 BAT 所在目录的祖先查找 `01env`，其次使用既有 `D:\001DIY\005lib\01env`。

工程根目录同名自定义 TXT 可先被删除，再由 `01env` 模板补回；不能声称所有同名自定义 TXT 都始终保留。复制阶段只补当时缺失项，不覆盖仍存在的文件／目录／链接；缺失或非普通源模板会跳过并说明原因。`01AIEDA` 中 TXT 已受保护，不因这轮清理而删后重建。

原“带解压”入口不自动展开压缩包或覆盖环境；恢复删除名单没有恢复隐式解压。

```bat
0000Ad_Keil_Cadence_dat_iar_txt.bat /preview
0000Ad_Keil_Cadence_dat_iar_txt.bat
```

`/preview` 只显示候选与补模板意图，不修改文件。无参数／双击会实际清理；目标固定为 BAT 自身所在目录和允许扫描的子目录。`/history`、`/build` 仅兼容旧用法，不再决定原模式是否生效；`/help` 可查用法，未知参数报错。

BAT 保存为 UTF-8 无 BOM、CRLF，执行 `chcp 65001`，从自身按 UTF-8 读取嵌入 PowerShell，不依赖外置 PS1。继续拒绝盘符根及指定系统／用户根；跳过文件链接、目录联接和重解析点；逐文件核对绝对路径，再用 `Remove-Item -LiteralPath` 删除，不递归删除整个目录。扫描后大小或修改时间变化则保留。识别到 Capture／Allegro／Padstack／Altium／Keil/IAR 等对应进程时，只允许预览。

已同步既有 25 个入口：工作区 21 个及已授权外部项目 4 个。最终更正前的快照存于 [cleanup_user_final_20261019](../../backups/cleanup_user_final_20261019/)，更早的本轮前快照在 [cleanup_user_rules_20261019](../../backups/cleanup_user_rules_20261019/)，原始 BAT 备份继续保留。每入口模式、编码、哈希与模板配置以最终 [migration_manifest.json](../staging/cleanup_review_20261019/migration_manifest.json) 为准；外部同步见 [external_sync_result.json](../staging/cleanup_review_20261019/user_rules/external_sync_result.json)。

最终规则通过 **418 项隔离行为检查，0 失败**。仅采用明确标记 `final_preserve_XML_CSV_DAT_and_AIEDA_TXT_original_other_masks` 且生产载荷哈希一致的 [最终结果](../staging/cleanup_review_20261019/user_rules/tests/run_20261019_093257_0c8b300a/results.json)；[测试脚本](../scripts/test_eda_cleanup_user_rules.ps1)覆盖全局数据文件保留、AIEDA作为根及嵌套目录的TXT保护、各入口原名单、配置/备份/OPJ直接清理、大文件网表、删除前复核和实际目录联接。文件符号链接样例受系统创建权限限制跳过，不声称已实测通过。此前A/B成绩与首次测试自身路径正则笔误的失败报告仅作历史，不计入最终验证。

**真实工程本轮仅预览，未实际清理。** 实际删除验证仅使用 `01AIEDA` 中隔离样本，测试对外层学习容器路径的模拟只允许发生在自己创建的样本边界内，不改变生产判断。**25个实际BAT入口的CMD预览全部通过，全部为UTF-8无BOM及CRLF，57份关键设计/模板文件哈希未变，记录链接无失效。** 汇总见 [final_verification.json](../staging/cleanup_review_20261019/user_rules/final_verification.json)。
