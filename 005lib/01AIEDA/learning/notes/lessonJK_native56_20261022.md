# J/K 原生实操记录：文字/高度、制造训练输出、受控 ECO、四层功能派生

记录开始：2026-10-22；实际续作与保存：2026-10-23。目录固定在 `01AIEDA`，本次新文件集中于 `learning/examples/lessonJK_51_59_20261022`（下称 JK）。只有本任务原生执行者启动 Cadence；独立用户 GUI 与练习隔离，不输入命令、不结束其进程、不访问其工程。进程身份须同时核 PID、创建时间、可执行路径和命令行，不能把复用的 PID 当作旧进程。

本记录对应可复现的实际命令、参数文件、BRD 和输出，不代表整板毕业验收。H/I 原训练板仍有 7 个 GPIO 未完成，4 个 USB 数据/共享网的电气求解及 whole-board DRC 为 pending/null。原生保留的 stored DRC 数字不等于本轮重新完成全检查。所有 CAM 目录均标记 **TRAINING_NOT_FOR_FAB**。

## 1. 输入与隔离

原始输入只读，未覆盖：

| 输入 | SHA-256 |
| --- | --- |
| HI `HI_2L_padentry_normalized_b019_DRC_PENDING.brd` | `AA3BFC0E01B06CB1058462439C71E56BC316F1F2929859B6A224320BE1013420` |
| HI `HI_4L_padentry_normalized_b019_DRC_PENDING.brd` | `B7A32330992F49609339E33C00BE92D989D0EA0C4AF64ED2763D0678DE14B501` |

每次先复制到 JK 新 working copy，只编辑工作副本内存，SaveAs 的新输出若已存在即拒绝。没有改公共库、`01env`、原 HI BRD、用户真实工程、系统 HOME 或系统 PATH。TEMP、TMP、ALLEGRO_PCBENV、cwd、日志均在本课。官方工具路径是 `C:/Program0/Cadence/SPB172/tools/bin`，版本 17.2 S045。跨机需校验安装路径/版本并重新读回，不能仅凭这些脚本文件称新机器也已通过。

启动器子环境先 `source $TELENV` 初始化官方安装环境，然后关闭本任务 autosave，设置本课 artpath/ncdpath。只设置 CDSROOT 不足以使独立 artwork 找到 `allegro_smi_modules.txt`。PATH 仅对子进程补 tools/bin。

## 2. K56：真实 o/O 链与安全拆解

已归档 `01env/env`、drill2/4、gerber/gerber_mil 原文和 SHA，见 JK `native/source_guard.json` 与 `source/env_oO_chain`。

- `o` 与 `O` 都 replay `D:/001DIY/005lib/01script_file/gerber.scr`，单位为毫米。
- Ctrl+o/O 对应 `gerber_mil.scr`，不是普通大小写的区别。
- 原宏没有 shell 删除，但会创建 NC 图例、创建大范围 PHOTOPLOT_OUTLINE、多次 save，并执行钻孔、铣槽和光绘；因此本次不直接 replay 原宏。
- 原宏实际选全 Film 后排除 `DisAll/DisBOTTOM/DisTOP/PDFBOTTOM/PDFTOP` 五项。本次为完整训练导出全部 15/17 Film，未改变 Film 的 layers/options。
- 原模板 `BOARD GEMETRY` 拼写及两层不适用引用沿用原生既有过滤结果，没有偷偷修模板、添加内层或改快捷键。

安全流程：对私有复制板打开官方参数 form，只设置输出参数，不创建图例/新板框、不 save；随后用独立官方 `artwork.exe`、`nctape.exe -v`、`ncroute.exe -v` 串行输出。

实际参数：

| 项目 | 已保存参数 |
| --- | --- |
| Gerber | RS274X，MM，3.6，scale 1，film max 300×300 mm，leading zero suppression YES、trailing/equal NO |
| NC | Enhanced Excellon，METRIC，absolute，3.4，X/Y offset 0，leading/trailing/equal suppression NO |
| 钻孔 | plated/non-plated 分文件，按层对，自动选刀 |
| 槽 | separate routing，plated `.rou`，4 条 J2 槽使用 0.6 mm 刀径 |

重要操作发现：Allegro `-p <log>` 会使内部 cwd 指向日志目录，参数 form 生成的 `art_param.txt`、`nc_param.txt` 在该日志目录。首轮我只查 exports 而误认为没有产生参数；后已查明并归档。`-nographic` form replay 实际成功，随后隐藏图形进程重试不是必要步骤，也不是鼠标 GUI 操作已学会的证据。

实际基线输出：

- JK `exports/native_2L_TRAINING_NOT_FOR_FAB`：15 个 `.art`，独立 PTH/NPTH `.drl` 和 plated `.rou`。
- JK `exports/native_4L_TRAINING_NOT_FOR_FAB`：17 个 `.art`，独立 PTH/NPTH `.drl` 和 plated `.rou`；标记 `LEGACY_STACK_L3_GND_REVIEW_ONLY`。
- 两层铜名 `TOP-BOTTOM`，四层 `TOP-L2-L3-BOTTOM`，完整 Film 名保持原文大小写，包括 `OUTlie`、`DisTOP` 等。
- NPTH 实际命中为 J2 两个 Ø0.65 定位孔，以及四角 Ø2 安装孔。不能按 NPTH 文件刀具头中出现的所有刀具定义统计孔数，应按实际 T 工具选择与命中坐标统计。
- 4 条槽不可当圆孔钻出；nctape 明确警告交给 NC routing，ncroute 的实际 `.rou` 已产生。

`artwork` 的真实返回码是 1，日志明确“ARTWORK had warnings”：原板 DRC 状态过期，且没有 PHOTOPLOT_OUTLINE，工具使用 drawing extents。NC 两工具返回 0。没有为了清警告关闭 DRC、填假板框或伪称量产通过。原始 DESIGN_OUTLINE/legacy OUTLINE 仍由 BRD 原生几何与光绘独立比对。

## 3. J55：板级实例文字与高度整改

实际新板：

| 派生板 | SHA-256 |
| --- | --- |
| JK `native/2L/JK_2L_J55_text_height_review_NOT_RELEASED.brd` | `EAA65005B80694AB58617CBF3637815484C7510F2CC0693BF0FFC3D41BDC5FBD` |
| JK `native/4L/JK_4L_J55_text_height_review_NOT_RELEASED.brd` | `9DEC773FE106E09C9844FEF5F160E1A1B3348BFC693926579F0CAF0A6A18DCF0` |

逐个实例先解析全部 old/style selector，唯一匹配后才开启变更。REFDES 的 SILKSCREEN_TOP、ASSEMBLY_TOP 以及 COMPONENT VALUE 的 ASSEMBLY_TOP 三类文字坐标都设为器件原点；保留实际旋转、镜像、字体块与对齐方式，不把锚点位于原点误称字形包围框几何中心。删除错误 COMPONENT VALUE/SILKSCREEN_TOP，保留 7 个 PACKAGE GEOMETRY 丝印极性/引脚标记。

每板最终 240 个必需文字 + 7 个包装标记 = 247 个文字。80 个真正 PlaceBound shape 中，72 个缺少 MAX 的实例 shape 加 `PACKAGE_HEIGHT_MAX = 1 MM`，8 个原显式 MAX 和所有 MIN 保留。另 4 个同包围框的遗留 PlaceBound **path** 保留，不把它们误算为额外 shape，也不假设 path 可附高度生效。1 mm 仅默认教学占位，不代表已选 MPN 的真实高度/机械合格。

原生 API：`axlChangeLayer`、`axlDBChangeText`、完整 `make_axlTextOrientation`、`axlTransformObject`、`axlDBCreateText(... symbolInstance)`、`axlDBAddProp(list(shape), list(list(...)))`。未改库符号或公共封装。事务前后保真检查包含器件/pin/pad/阻焊锡膏、过孔/铜形、原 CSet/net/class/Film/层叠、symdef 与机械数据；固定手工线段另由实际 route_geometry/role/CAM 独立对比闭合（见下方空采样勘误）；成功后才另存。fresh 使用官方 -readonly 重开，读取实际文本/形状/规则及所有旧 endpoint 合同，未重跑已知挂起求解器。

实际脚本顺序：`prepare_j55_sources.py` → `j55_plan_static.il` → `j55_apply_core_v2.il`（官方 drain）→ `j55_outer.il` → `run_j55.py --variant ... --mode build/reopen --tag <新目录>`。每次 tag/output 都必须新建，不可直接重放覆盖。2L 成功 build_try06、4L 成功 build_try01；fresh 为 `logs/native_j55_{2L,4L}_reopen_01`。独立逐项核对共 1644 检查通过，见 `audits/j55_corrected_independent_summary.json`。

失败和改进均保留：原额外 full_geometry fingerprint 两次 AV，均未进入核心或保存；改用 H/I 已实证 branch/GetConnect 读法。初稿使用不支持的 fflush，官方语言文档确认应 drain，保留初稿另出 v2。try04 核心内存成功后，守卫因 transient propList 地址及非 ETCH pad-outline 缓存产生伪差，严格回滚未保存；改为真实字段与实际铜线比较，焊盘/开窗由逐 pin 数据独立守卫。不得把这些失败日志当成功。

## 4. 修正后 CAM 与三个伴随文字图

J55 修正后真实再次输出到 `exports/J55_corrected_{2L,4L}_TRAINING_NOT_FOR_FAB`，仍完整 15/17 Film、PTH/NPTH、槽；输入 SHA 稳定，artwork 警告真实保留。

模板盲点：原 `SKILTOP` 只有 PACKAGE GEOMETRY/SILKSCREEN_TOP（另有无效拼写引用），不包含 REF DES/SILKSCREEN_TOP。`PDFTOP` 包含 REF DES/ASSEMBLY_TOP，但不包含 COMPONENT VALUE/ASSEMBLY_TOP。照原模板完整导出，不等于用户要求的所有字层已输出。

因此另建独立 generator 副本，只含三个临时 Film，导到 `exports/supplement_{2L,4L}_THREE_TEXTS_TRAINING`：

1. `REFDES_SILK_TOP.art` → REF DES/SILKSCREEN_TOP。
2. `REFDES_ASSEMBLY_TOP.art` → REF DES/ASSEMBLY_TOP。
3. `VALUE_ASSEMBLY_TOP.art` → COMPONENT VALUE/ASSEMBLY_TOP。

三图分开避免同原点 Ref/Value 叠字，不混入原模板目录、不改变主 J55 训练板 15/17 Film。它们是补充复核图，不是自动形成可生产包。Root 已实际渲染三图和原模板前后差异；不能只看文件存在。

## 5. K58：只对未布局 DE 板重放受控 ECO

输入包 `eco/source_inputs` 有 119 项复制及原源 SHA。独立核对的期望仅 R19/R20 2.2k→3.3k 与 J13.7/8 的 PB8/PB9 对换，MCU 45/46 不变。

实际命令是官方 `netrev.exe -e -i <JK copied eco/netlist> <新 DE_BASELINE_WORKING.brd> <新 DE_ECO_REPLAY.brd>`。`-e` 的官方含义是缺封装作为错误，并非“打开 ECO”；`-n` 是新建板，本轮已有板 ECO 不加；`-d` 会禁 DRC，本轮没有使用。

实际输出 `eco/DE_REPLAY_ONLY/DE_ECO_REPLAY.brd` SHA `C1F5DF07547330977BFCE2C7296219F07691EE3793122F7BF99E475DBAB4F984`，明确 `ECO_TRAINING_UNPLACED_NOT_HI_NOT_FOR_FAB`。fresh baseline/eco 各 80 元件、272 pin、69 net、6 NC、placed0；没有对 HI/J55/新栈路由板 netrev。原 DSN/PST/BRD 与所有输入副本 SHA 不变。

VALUE 证据来自官方 `axlWriteDeviceFile(comp->compdef, directory)` 的实际 native 设备定义和 compdef 属性，按 ref 独立目录导出，避免 devices.map 覆盖；没有从 deviceType 后缀猜数值。独立审查 `review/independent_K58/review.json` 共 1453 项通过。此为受控回放，不代表两完整布线工程的第58课结课验收已完成。

## 6. 新四层默认与真实派生板（与 legacy 输出严格区分）

用户新默认：TOP 器件/信号，L2 完整公共 GND，L3 电源层，BOTTOM 信号；层名固定 `TOP-L2-L3-BOTTOM`。旧 b019/J55 板 L3=GND，只作为 `LEGACY_STACK_L3_GND_REVIEW_ONLY` 历史。停止采用 L2 信号桥候选，不能改功能文字后冒称实际铜已改。

实际已另存 `native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd`，SHA `471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9`。源是修正后的 J55 4L，正式合同 `audits/j52_53_newstack_native_contract.json`。

真实动作：唯一识别并归档旧 L2 HSE 静岛和 L2/L3 GND 母形/原 void，删除这些内层对象，创建新的全板 dynamic L2 GND、单一 dynamic L3 V3V3。静态转 dynamic 会删除原静态 void，故本新架构不把旧 HSE moat 偷偷带回；TOP 既有 quiet/阶段 void 不因本次被广删。填充后读 actual ETCH polygons、holes、net/layer 和 OOD。V5/VIN/VDDA 仍由既有外层铜供给，不假造多电源区域。

为 V3V3 单独静态复制 P_POWER_060 到 `JK_P_V3V3_L3_PLANE`，仅 L3 `allow_etch`=true，绑定 V3V3；其它所有原 CSet/spacing/neck/via/inner signal 权限不变。这是副本，不是动态 parent 继承；没有开放 L2 信号，也没有改变全局默认。新权限包含 V3V3 在 L3 的 etch，不等同允许普通信号在内层走线。

try01 append 参数错误回滚；try02 actual planes/共地/8cap 通过后，anchor 唯一筛选未过而回滚未保存；try03 填充后刷新 DBID 并用坐标精度容差定位，挑战与恢复及固定对象守卫均通过后保存。每次源 SHA 稳定，无覆盖旧板。实际 scoped GND=0、V3V3=0，仅是这两网范围；whole DRC 仍 null。自动审批曾两次超时且未执行，均拆分为先落盘可审脚本再单独运行；没有绕过审批。

新 HSE 架构预期改变：删除旧 anchor 后 C22.2/C23.2 仍经连续 L2 共地，原“必须断开”的旧测试正式退役；事务回退原 anchor 后再核全旧连接合同。不能把新架构按旧断开测试伪判 PASS。8 个既有 V3/GND 电容 C9/C11/C12/C13/C14/C15/C16/C17 的 pin1→实际 L3 V3V3、pin2→实际 L2 GND 可达已检查，但这只是电气铜图可达，不认证高频参考转换。BOTTOM 参考变为电源平面，TOP/BOTTOM 过孔处应审实际 V3-GND 去耦位置、路径/热焊盘/有效电容；单加 GND via 不等同电源/地参考转换已完成。VDDA/VBUS 电容不能冒充 V3/GND 转换电容。

新栈 fresh、单独新 CAM、全足迹与局部回路独立工程审查结果在后续补充；不能沿用旧 L3 GND 的光绘、参考截图或通过结论。

## 7. 复现与状态边界

可从 `native` 中对应 launcher、每个 `logs/native_*/launch.json/run.scr`、实际参数文件和 `source/*_official` 恢复命令、环境、输入身份与输出。工具 normal exit0 只代表命令结束，必须核输出与 fresh/独审。失败脚本和回滚日志留存，不能从最终入口删除后假称一次成功。

本轮已经实际学到并验证：完整模板制造输出、PTH/NPTH/槽区分、文本实例修正、默认高度实例属性、可逆受控 ECO、真实内层平面功能派生和原生读回。未完成项继续显式保留：鼠标 GUI 操作熟练度、7 GPIO 全板连通、USB4/whole DRC 重算、真实阻抗/材料资格、器件高度与 MPN、完整 HF 返回/EMI/硬件测量与制造释放。不能因为有 Gerber 或局部 scoped0 就把这些改成完成。


## 8. 保存后补证与空集合勘误（2026-10-23）

新栈 fresh readonly 完成于 `logs/native_newstack_4L_reopen_01`，输入 SHA 保持 `471176A9...31F3F9`。原生实际 L2 GND 为 1 块共地 fill，56 个真实 GND pin、76 个实际 GND via 共通；L3 V3V3 为 1 块 fill，32 个 V3 pin、3 个 V3 via 共通，无 GND/V3 铜图短路。build 初次填充后有未刷新缓存的 via=0 摘要，不作“全部过孔已核”证据，以 fresh 实际表/图及独立复核为准。

首个 `newstack_reference_samples.tsv` 实际 manualSegments=0/samples=0，**NOT_EVIDENCE，不是零缺失或参考已通过**。其原因是 GetConnect 图返回 path 父对象，而新补 reader 没有递归 `path->segments`。同一缺陷使外层 manual-LINE 子守卫未覆盖实际手工线段，不能沿用“全部线段指纹严格相同”的口头结论。已有原生 `route_geometry.tsv` 与 `hi_route_roles.tsv` 实际包含完整铜段，因此固定铜保真由这些非空数据及 CAM 的独立 multiset 比较闭合，不能靠原空集合判断。

原空表与首次日志原样保留。修正版 `native/native_segments_reader_v2.il` 明确读取 path/cline 的 segments，另行 readonly 导到 `logs/native_newstack_reference_segments_01`：932 个实际总段 = 750 个 manual + 182 个 generated thermal；非 GND 外层 manual 658 段、18,854 个实际中心线样点，步长不超过 0.1 mm，参考网明确 TOP→L2 GND、BOTTOM→L3 V3V3。计数必须非空并与实际 fgeo/role 表核对；中心线采样仍不等于完整线宽足迹/HF 返回通过。没有为补采样修改 BRD 或覆写第一次 fresh。

新栈完整制造训练输出已独立重导到 `exports/newstack_4L_TRAINING_NOT_FOR_FAB`：真实新 17 Film、PTH/NPTH、4 条槽。其参数沿原生已验证格式，只改新文件前缀。L2/L3 文件从新实际铜层产生，不混用旧 legacy GND/GND 文件。真实 artwork rc=1 警告与 NC rc=0 均留存。

三板的实际 VALUE 后又独立只读导到 `exports/devicevalues_J55_2L_TRAINING`、`devicevalues_J55_4L_TRAINING`、`devicevalues_newstack_4L_TRAINING`；每个 ref 的 native device 文件与 compdef 原属性均在，不从 deviceType 后缀或旧 inventory 猜值。主板文字、height、铜、层名和 Film 身份仍不变。


?????????? TOP?L2 ? 11,405 ?? 928 ??BOTTOM?L3 ? 7,449 ?? 660 ????????????? pin/via ???????????????????????/????????????????????????? PASS?????? `native/reference_sample_diagnostic.json`?HF ???????? pending?


## 9. ?????????

?????? `review/independent_newstack/review.json`?73 ????0 ?????/?? L2 GND-L3 V3V3/?????/? HSE ????????????? **OPEN**??? 103 ????????? 8 ???66 ?????????????????? HF ?????

? manual ??????????????`native/manual_copper_preservation_validation.json` ? HI?J55 ?? 772 ???? 750 ???? J55??? 750 ? manual ???? net/layer/width/?????????? missing0/added0????? native segment reader 750 manual ??? fgeo/role ?????????????????????????????????????

Root ??? CAM ? 85 ???/??? 34 ?? Film ?????????? L2/L3 ?????????? L2/L3 ??????????????????????????/EMI ?????J55 ???? 1644 ??ECO ???? 1453 ???????????

?? 7 ??????? SHA ?????? `native/final_original_guard.json`??????????? `native/native56_final_report.json`????? `native/README.md`??????? `native/native56_artifact_manifest.json`??????????????????EDA?????? agent ???????????????????????????
