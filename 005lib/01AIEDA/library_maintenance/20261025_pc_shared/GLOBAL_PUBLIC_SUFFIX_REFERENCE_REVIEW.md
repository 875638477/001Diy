# 公共后缀库引用盘点：本阶段记录

本目录记录全局原生读取、标准公库追加及引用迁移的进展，不是整体发布回执。旧公库资产尚未按退役清单删除，引用更新和 PCB 实际连接验收分别留有独立门。

冻结输入位于 global_suffix_inventory_v1：13361 个受保护文件，941 个候选 PSM、941 个 DRA、868 个 Device TXT，另有 5 个同名 PAD 文件。全部 PSM 字节 SHA 均不同，未依据文件名或二进制片段合并为少量代表。

非 OLB 引用审计位于 global_suffix_reference_audit_v1：

- TEXT_REFERENCE_AUDIT.json / TEXT_REFERENCE_MATCHES.csv：1286 个文本文件、871 个命中文件、6210 个完整名称 token；4340 个 Device 自声明，1736 个旧日志引用，134 个 devices.map,1 的裸数字尺寸描述。当前 env/脚本没有命中候选名称的确认活跃外部引用。二进制容器的未审计边界在报告中逐文件列出。
- PUBLIC_BRD_REFERENCE_AUDIT.json：七个 01brdlib BRD 当前 SHA 全部与原生只读快照吻合；2501 个候选逻辑 package 声明、403 个已放置符号引用。
- PUBLIC_BRD_CONNECTION_SCOPE.json：0010.brd 的候选 403 个 R/C 共 806 个物理脚，806 脚全部有非空网络，涉及 323 个网；全板有 1739 个实际过孔。它是实际电路板模块，不能当作无连接 palette。00012.brd 的裸 0402/0603/0805 共 655 个候选声明全部未放置；006、008 分别有 284、1159 个候选未放置声明。旧快照没有 etch 统计字段，不作“没有走线”的结论。

公共 OLB 字段审计由独立检查任务保存于工程 13/verification/public_olb_footprint_audit13_v4，涵盖当前 37 个 OLB 的 SHA 和 Package/视图默认字段。两份公共 DSN 已另作完整原生 XML 审计，报告位于 13/verification/public_dsn_footprint_audit13/PUBLIC_DSN_FOOTPRINT_REFERENCE_AUDIT.json：Lib.DSN 仅有一个 TP_1/TP 实例，缓存及显式封装均为 TPS-1D00；SCHLIB.DSN 为零实例、零缓存、零 PCB Footprint。两者均无本轮尺寸/AO 旧名引用，原件 SHA 保持不变。

## 原生批处理的失败边界

global_suffix_native_v1 在第一次 axlOpenDesignForBatch 停滞，未取得完整输出。原生单位及范围探针在跳过第一次 reopen 后成功，因此没有依据将其解释为 mils2→3 的单位转换弹窗。

global_alternating_canary_v2 的三个 PSM 通过，但 global_suffix_native_v2 大批处理仍停在第二项打开 blankB，超时仅保留一项输出。A/B 轮换方法未解决间歇 reopen 问题，失败记录保留，不能把短 canary 改写为大批处理成功。

后续 run_global_suffix_psm_native_audit_v3_cold.py 为每个 PSM 启动独立空板进程，每项仅使用启动时的当前空板，不做 reopen；每源核前后 SHA，全局保护在全部开始/结束及每 100 完成项核验。此文写入时 v3 尚未给出全部 941 项的验收结论。

review_global_suffix_native_chunks.py 对已完成项提取完整原生对象、实际脚号、pad/钻孔、相对位置和逐层图形，分别标识普通两端、特殊脚号、穿孔、功能多脚及特殊电容；保留完整 raw SHA 和实际加载 PAD 文件 SHA。它不会把四层派生图形冒充完整外部 PAD XML 的制造证明，也不执行任何删除或改库动作。

通用方法见 learning/notes/public_passive_suffix_consolidation_pc.md；工程数据不应作为通用工具的默认输入。

## 后续已取得的证据：仍非整体发布回执

上述 v3 等待段保留为早期阶段记录。现在独立冷进程批次已结束：原 941 项中 939 项取得完整原生图，两个旧 0603 异常另由原生 DRA 意图证据支持退役到标准；原始批次的 INCOMPLETE 报告没有改成 PASS。13361 个旧公共文件全量保护未变化。后续四十个标准目标独立冷读、完整 source→target 图形比较及 31 个实际 PAD 的全制造 XML 当前 SHA 绑定均通过。

全原公共 3383 个 PSM 已做名称和完整 SHA 盘点。名称/字节候选首批 275 个代表中 274 个完整，增量 51 个中 50 个完整；sot-23、smb 两个失败项保留，没有据失败删除。另为当前工程实际 81 个封装补读十二项候选目标，均有完整原生输出。非 R/C 实际候选中，52 条编号焊盘及完整 PAD 制造等价关系、67 个全字节相同群已形成统一重定向；完整图形差别、功能结构和失败边界单列，未宣称全 3383 个几何均已判重。

nonpassive_additional_aliases13 保存冻结追加映射、KEEP 集、零循环/零多级别名检查和四个语义精确新增目标。它们分别保留单脚 1 的 SOT23、实际 2.54mm 脚距/0.9906mm 孔的两脚穿孔结构及两种不同槽孔/铜 land；没有覆盖已有单脚 3 的 sot23-3，也没有抹平不同槽孔。新增八个 PSM/DRA 的源字节和六项冷读图形全量比较通过，实际七个 PAD 的完整制造 XML 当前 SHA 重算通过；报告在 nonpassive_exact_targets_review13。

本工程最新完整范围固定为原 81 种缓存封装、1066 个已放置器件。一次性迁移计划覆盖 84 个物理位号，包含先前 SOT34 与其余 50；网表对应累计 1031 个显式 FP 字段。另查到七个共享 Package 默认仍引用旧名，需同时更新共享 COMMON_PC 和设计 Cache；capture_cache7_plan13 保存精确七字段计划、失败 v1 wrapper 和修正后的 v2，原始失败证据保留。完整 XML/PST 门和实际 PCB 附着修复分别记录，尚不能据原理图通过宣称 PCB 整体完成。

公共 0010 是有真实布线的模块。public0010_403_endpoint_preflight13 按精确逐位号类别与实际原缓存核 403 个元件/806 pad，检查 12820 个正线宽路端及笔画半宽；159 个候选即使计入半线宽仍未被新 pad 覆盖，涉及 76 个 pin/71 个位号。这只是几何预筛，源几何表缺网络/对象身份，实际附着和短线修复仍必须由原生 GetConnect 门确认。

public_retirement_all_confirmed_plan13 已合并原候选与追加映射为 1067 个待退役别名、3069 个精确文件；runner 支持 dry-run/stage/apply 和复用原 941 完整备份 ZIP，只为未覆盖成员补增量归档。此记录写入时没有执行退役删除；所有引用闭合和最终原生验证必须在 apply 前完成。PAD、共享 SHAPE、用户要求保留的原件、原始大转储和 ZIP 不在删除范围。
