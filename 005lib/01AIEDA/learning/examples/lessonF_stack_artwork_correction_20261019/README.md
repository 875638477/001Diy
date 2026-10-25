# F 部分层叠与 Artwork 原生纠错记录

本目录为 2026-10-19 对用户指出问题的正式纠正产物；旧 F28/F29 板、旧验收及旧 manifest 均保持历史身份。主板当前入口为 [current/F29_CONSTRAINTS_v4.brd](current/F29_CONSTRAINTS_v4.brd)；两层和四层练习板分别为 current/F28_2L_USERFIX.brd、current/F28_4L_USERFIX.brd。

## 问题与修正

此前脚本自行把阻焊加为 Cross Section 的物理 MASK 层，且只抽取 01env/drill*.txt 的铜 Film 后又额外增加 F28_DESIGN_OUTLINE Film。这不符合用户要求。错误在于只核了铜 Film 子集，没有逐项验收用户完整模板和物理层表；旧 DRC=0、旧通过计数不证明该规范符合。

本次仅在 SHA 备份后的新副本上，按官方 axlXSectionDelete 删除 layerType=MASK 的两项；未删除 PIN/VIA CLASS/PACKAGE GEOMETRY/BOARD GEOMETRY 的 SOLDERMASK_TOP/BOTTOM 绘图类或焊盘开窗。未删除 Through All 孔跨层/钻孔结构。

实际导电层经 axlXSectionGet、ETCH groupMembers、axlSubclassRoute 三路原始读回，均为大写：两层 TOP-BOTTOM，四层 TOP-L2-L3-BOTTOM。旧 API axlGetXSection 同样实际返回大写；不把截图的显示样式推断为数据库已被改名。

删除旧 Film 参数记录后完整原文执行对应不可变 drill2.txt（15 Film）/drill4.txt（17 Film），不添加额外 Film。每项创建均返回 t；全部 Film 的每个显式 Options 与有效 layer 成员已保存并新进程重开读回。mm/3 精度会把模板 0.0025 量化为 0.002，本次使用官方支持的 mm/4，实际保存 0.0025，全部原几何坐标、焊盘与规则数值比较保持不变。

模板 OUTlie 与多项 Film 引用 BOARD GEOMETRY/OUTLINE。本次将原 80×60、C2 板框的 8 个精确直线顶点复制到 legacy OUTLINE；真正 DESIGN_OUTLINE root 不变。新进程对两个形状分别读回，bbox、fill、8 顶点相同，OUTLINE 只为模板输出提供几何。

## 不可隐瞒的原模板事实

01env 模板原文件未修改。原文存在 BOARD GEMETRY 拼写引用，实际 class 不存在，Cadence 会过滤；两层 DisAll 还引用 CONSTRAINT REGION/L2/L3，而实际两层板无这些 subclass，原生也过滤。这些缺项逐 Film 列于 validation.json 的 filteredInvalidTemplateReferences。未创建假 class 或额外铜层来凑齐。重复 layer 项按原生集合语义去重，完整明细亦保留。

所以“完整模板已执行、全部有效成员及全部显式选项已验收”成立；“原模板所有无效字符串在数据库中也已生效”不成立。现有合法非导电绘图 subclass 为模板需要补建；没有改动原模板。SKILTOP/BOTTOM 模板本身不含 REF DES/SILKSCREEN_*，PDFTOP/BOTTOM 使用 REF DES/ASSEMBLY_*。本次不擅改用户模板，也不把 Film 定义通过等同于生产 CAM 位号丝印内容审查通过。

## 保真证据与范围

每板均由原生官方 CLI 打开副本、更新 DRC、保存，然后新进程 readonly 重开；readonly SHA 不变。80 元件、69 网络、272 逻辑 pin-net、5 已放符号、22 个真实物理 pin、1 个唯一真实 through via、机械禁布区及原板框均保留。全部物理 pin 和 via 的导电 pad、阻焊/钢网 aperture figure/bbox 逐项前后相同；不只是检查外部 .pad 文件。

F29 的 27 个单域 net class / 207 个成员关系、3 个差分对、69 net 的类映射与继承、10 physical / 7 spacing / 1 electrical CSet、class-class 间距、GND 与 VDDA 的直接例外、模式开关、唯一许可 via 和实际 via 均前后保真。原挑战的错误类型与恢复证据仍属原 lesson29 历史目录，不重复伪造。

去除物理 MASK 后的铜与介质总厚度：2L=1.5952mm，4L=1.5862mm。生产阻焊为独立工艺资料，不再混入本用户层表；这不构成成品板厚或阻抗认证。四层 L2/L3 连续 GND 仍为后续布局意图，当前尚未铺铜、未完成全板布局布线。

新 F29_RULES_v4.tcf 已由官方 techfile -w 导出并以 -c 对当前 v4 比较，exit0、No objects were updated，BRD SHA 不变。TCF 为技术/CSet 导出，不冒称完整网络对象 DCF；完整 net/class/pair 证据由原生 readback 提供。

## 文件与验收

- input_manifest.json：原始三板和两模板的 SHA 与备份/新副本映射。
- validation.json：PASS_NATIVE_USER_LAYER_ARTWORK_CORRECTION，1133 项、0 失败。
- logs/baseline_* 与 logs/reopen_*：完整基线和新进程真实读回；structure.txt 含三路真实铜名/物理层，films_full.tsv 为全部 Film 原生属性，physical_pad_layers.tsv 为实际开窗与铜 pad。
- logs/outline_*：独立新进程读回 legacy OUTLINE 与 authoritative root 的几何。
- logs/fix_*：每次官方设置返回、全部 Film 创建结果、MASK 删除和 DRC 完成标记。
- exports/F29_RULES_v4.tcf 与 export_result.json：新技术档及官方导出/比较证据。
- scripts：完整源代码，所有 runtime/TMP/TEMP/cwd/ALLEGRO_PCBENV 均受限于本目录。
- review：另一个代理只读独立复核；其状态以 review/review.json 为准。
- artifact_manifest.json：本纠错目录自身文件清单，不锁定仍由主任务更新的上级学习笔记。

验收边界：本次通过的是用户层序、物理 MASK 删除、完整模板重放与有效成员/Options 持久化，以及已有机械/连接/约束的保真。未开展独立 SI/PI 仿真，也未验收 CAM 实产内容、USB 90Ω 几何、全板走线或制造发布。

## 验证器修订

第一次 Python 验证器因模板 input 条目无 key 而异常，失败代码保留为 scripts/validate_correction_v01_failed.py。随后首轮报告仅一项因错误假定 2L 无教学 via 而把 92 条 mask 观察误写应有 88 条，保留 logs/validation_first_report.json。修为实际每板 22pin+1via、每对象4条 aperture 后，1133 项全部通过。原生三板操作没有失败或回滚修改；这些是验收程序自身的输入/计数修正。
