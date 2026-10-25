from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();report=json.loads((R/'review/b019_native_report.json').read_text(encoding='utf8'));assert all(b['scoped']['zeroNetCount']==65 for b in report['boards'].values())
text='''# b017—b019 原生执行记录（2026-10-22 续作）

本阶段完成 North6 原生精细布线、两层/四层实际 TOP 地铜试验，以及四个右侧 MCU 脚的焊盘内接线规范化。两板各剩 7 个 South GPIO 终端连接；USB 相关原生求解与 whole-board DRC 未通过，不是完整训练板发布。

## 实际入口与状态

当前可供下一批几何规划的工程是 `native_candidates/HI_2L_padentry_normalized_b019_DRC_PENDING.brd` 和 `HI_4L_padentry_normalized_b019_DRC_PENDING.brd`，对应 `inventory/checkpoints/padentry_{2L,4L}_b019_DRC_PENDING/`。权威数值、原板 SHA、原生日志和每网结果在 `review/b019_native_report.json`。没有覆盖旧板或更新 qualified current 别名。

两板均 80 个器件、272 个编号逻辑焊盘（266 带真实网络、6 NC）、69 个真实网。2L 累计 475 个端点证明、772 手工段加 140 生成 thermal 段、160 个过孔、26 个实际 GND 铜形；4L 为 465 个证明、750 手工段加 218 thermal、150 个过孔、22 个铜形。段总数必须与手工/生成角色分开，不把 thermal 计入手工布线工作量。

## North6 与地参考实证

North51 的 39 项操作精确删除 2 旧 PC14 via 和 11 段旧线，新增 17 条分段 path 和 9 via；6 个 U1→J11 真实 pin 对均建立。被重布的旧虚拟 XY 端点仅按冻结合同迁移到真实新 via/终端，不把旧 XY 留作假证明。4L 单独 b017 保存并 fresh；2L 单独 North 施工切割 BOTTOM 地，旧 R28.2→U1.23 共地证明失败，所以拒绝保存，没有一个“通过的 2L b017”。

2L 随后从原 b016 重新执行 North51 并增加实际 TOP 全局动态 GND，4L 从真 b017 增加同样 TOP 动态地。TOP 母形采用实际板内 0.5 mm inset 八角，保机械禁布、铜边规则及全部旧参考平面。永久 quiet 排除区由实际 moat 与 7 条 TOP guard buffer 合并，面积 90.0300125 mm²；27 点中 4 个共线点被原生合并，输入显式化为 23 点，前后几何对称差 0，不是缩小禁布。

官方动态顺序是先创建闭合外形→转 BOUNDARY dynamic→在 BOUNDARY 上创建 permanent void→force fill。不能先给静态 shape 加 void 再转 dynamic；17.2 官方会删除这些 void。真实 quiet 静态铜、唯一 anchor (46.35,29.4)、原 BOTTOM/L2/L3 排除区均保留。

TOP fill 实测把原未接地的 Q1.2、R8.2、R29.2 以及 North 新切割造成的旧地参考问题接回实际公共地。每个阶段均逐一验证 56 个真实 GND pin 和实际 GND via（2L 84，4L 76）都在 C1.2 原生连接图中；所有实际填充 GND shape 也必须共地，不能只凭同网名或颜色。HSE 负测只删除唯一 anchor via，断言 local cap/guard 仍互连但不达 global、case 仍 global；rollback 后全部共地证明恢复。

## 生成孤铜与可撤回阶段 void

首次 4L TOP fill 生成 15 个无实 pin/via 的孤铜，健康门拒绝保存。按本机官方 `algroshapes.html#1035489` 的 Delete Islands 几何语义，取每块实际 `axlPolyFromDB` 含弧 polygon，在新 TOP 母 BOUNDARY 上用 `axlDBCreateVoid` 加 permanent manual void。2L TOP 清理 13 块；North 还在原 application BOTTOM 形成唯一窄岛 bbox (18.6002,49.2599)..(18.8498,54.2404)，面积 1.228451 mm²，额外经 root 明确授权，仅这块无任何真实 pin/via 的含弧岛也加阶段 void。

每个阶段 void 有独立 ID、原 polygon/半径符号、面积、母形、源/保存 SHA：`review/b018_2L_stage_island_void_manifest.json`、`b018_4L_stage_island_void_manifest.json`。没有更改全局 suppress area 阈值，没有 IGNORE_SHAPE_ISLAND，没有删除手工地线或带功能终端参考。没有调用 GUI island_delete，也没有假造 `DYN_DELETED_ISLAND` 属性；使用显式 manifest 区分阶段孤岛 void 与必须保留的 quiet void。

后续 South/最终重布前可仅按 manifest 精确撤阶段孤岛 void，再 refill/重判；不得全删 manual void，更不能撤 quiet 90.0300125 mm² 排除区。所有新增线/via/最终填铜后还须重新做唯一 anchor 负测。这些阶段 void 不是不可变的设计禁区。

## 扩大逐网检查发现真实漏项

b018 保存、独立重开后执行 `axlDRCItem(nil, actual net)`。两板均有 65 项真实返回，其中 61 网为 0、4 网各 2 个 Maximum Neck Length（BOOT0/PA15/PB4/SCL，expected 2.0 mm、actual 2.1414 mm）。只查“当批改动网”漏了旧右侧源段的 effective 实际颈长；不能由之前局部零 DRC 推断整板。

4L 检查在第 66 个网 USB_DP 进入原生 bem2d NoGroundPlane 后未返回；owned 子进程 152.93 s、CPU 152.56 s、OUT 0，经核 executable/start/parent/任务临时路径和板 SHA 后按授权停止，仅终止这次 owned 父/子进程。USB_DM、PA11_SHARED、PA12_SHARED 未执行。保存的 PRE_ALL69 工程 SHA 不变。此前 nil/t 整板重复挂起实证属于 2L；不能泛化成 4L whole Update(t) 已试。本阶段 4L whole t 探针在实际 scoped 同类阻塞后由 root 取消，记录未试。

2L 本阶段只检查 65 个非 USB 网；已知阻塞的 4 USB 网不重复试，也不把缺项当 0。原规则、模式、DP 检查没有为造零而关闭。原生内部求解的非收敛是未完成检查，不是开展了 SI 认证或已满足 90 Ω。

## 正规焊盘内接线规范化（b019）

实际四条 .16 对象从 MCU pin center x44.25 开始，首段到 x45，随后 .141421 斜线加 1.25 mm 直线，原生连续细颈对象长 2.141421 mm。实际 land x43.65..44.85、宽 .30；部分对象位于已有实铜焊盘内。直接提前 .2 flare 会被相邻 tinyvia 形成的窄槽挡住，不能硬挤或放宽间距。

冻结修正各 12 操作：只精删 4 条原首段；加 pin center44.25→44.65 的 normal .20 段（连圆头完全被原 .30 land 覆盖），再44.65→45 保 .16，原外部所有铜不变。原生颈对象改为 1.741421 mm；实际外露 .16 铜长始终 1.541421 mm，没有物理缩短。实际四网 TOP pad+trace 铜并集对称差 0；非目标手工铜/宽/层/归网 Counter 全一致，仅 4 旧段变 8 新段。

为读到原生实际值，四网逐项临时将其现有有限 source CSet 的 TOP necklength_max 从 2.0 收紧为 1.7，原生确报 actual1.7414，然后 unwind 恢复 2.0、整套 TOP 字段严格相同并正常 scoped0。此设置作用于共享 CSet，因此原始严格日志也可能列同 class 其它 1.9914 颈；不能把全部 raw marker 都归给目标网。保完整日志、明确目标 marker，最终 65 网逐项全部返回 0。

b019 fresh 读回再次验证全部物理身份和累计端点；所有 physical/spacing/electrical CSet、net/class/region 映射、嵌入焊盘、机械孔、TOP-L2-L3-BOTTOM 或 TOP-BOTTOM、15/17 Film 及完整参数、所有实际地铜/母框/permanent void、元件姿态和过孔几何相同。只归一进程本地 dbid/pad/propList 地址；不能拿原始内存地址变化当几何变化。

## 这次误报与改进

我在 4L 65 网检查时只看日志尾部 CAN_H/CAN_L 返回 0，把“65 个已返回”误称“65 个零”。完整报告器解析后发现前面 4 网真实非零，已立即向 root 更正；原始日志/停止记录保留，独立勘误在 `review/b018_4L_scoped_summary_correction.json`。之后所有汇总必须先完整解析 begin/result、returned/zero/nonzero/incomplete，不以日志尾部、进程 exit0 或保存的 DRC0 概括通过。报告生成器的错误断言阻止了错误摘要封存。

其他失败完整保留：共线点计数校验误拒→几何对称差归一；无终端孤铜健康拒绝→明确阶段 void；UTF-8 BOM 与全局标签替换误写输入路径均在启动 native 前阻断，改用显式 UTF-8-sig/精确标签；TSV COMPLETE 尾标记不当数据行；进程本地地址不当设计变化。不要把这些解析错误写成 Cadence 设计错误。

自动审批曾将 root 自身“并行只读研究、不启动 native”误当对 native 执行者的暂停命令，拒绝 try04。没有执行被拒动作；root 明确澄清 sole native executor 继续受控试验后重新审核获准，未绕过拒绝。

## 可复现顺序与边界

`prepare_north51_b017_nativeHI.py` / `launch_b017_guardedHI_v1.py` 保留 North 阶段。b018 实际成功脚本为 `prepare_TOP_trial_b018_actual_islands_v4.py` 的 4L try04；2L 在此基础上 `prepare_TOP_trial_b018_bottom_single_v6.py` try06。绝不把未运行的 try01/try05 或拒绝的独立 2L North 当成功入口。

b019 使用 `prepare_padentry_b019HI.py`→`compile_batchHI_v39.py`→`launch_b019_guardedHI_v1.py`（4L 后 2L），每次只从 SHA 锁定源创建全新可写 scratch，固定不存在的新 SaveAs，保护 11 个旧原件与 current。临时关闭在线 DRC 只为批量建铜，unwind 强制恢复 t，在实际 scoped/HSE/保存前检查 master t；没有改永久检查模式。每批 `source/batch_snapshots/<tag>/inputs_manifest.json` 给出真实 helper load order/SHA，不依赖以后变动的 helper。

保存后 `prepare_stored_readbackHI_v4.py`→`launchHI_1800_path.py --readonly`→`extract_checkpointHI_v10.py --stored-state-only --no-alias-update --drc-pending`。fresh 是独立进程几何/连接读回，不冒充 fresh 整板 DRC。报告器 `report_padentry_b019HI_v3.py` 核完整 65 结果、严格挑战、非目标铜、铜并集、所有规则/void/对象和源 SHA；`report_TOP_trial_b017_b018HI_v4.py` 保留前阶段真实失败。

本机官方资料副本在 `source/api_b018_TOP_trial`，原路径/SHA 见 manifest；scoped/full 覆盖区别另见 `review/all_object_scoped_DRC_coverage_proposal.json`。`axlDRCItem` 的 numeric count 不等于 design-wide Update(t)，也不代表 batch-only 检查全部覆盖。当前 native wholeBoardDRC 必须保持 null，rawStoredDRC0 仅 forensic。不能称 EMI、信号/电源完整性已认证，USB 实际参考咬边/未确认 W/S/装配条件仍按工程审查未闭项记录。
'''
(R/'native/b017_b019_execution_notes.md').write_text(text,encoding='utf8');readme=R/'native/README.md';old=readme.read_text(encoding='utf8');append='\n\n## 2026-10-22 b017—b019\n\n最新原生阶段见 [b017_b019_execution_notes.md](b017_b019_execution_notes.md)，事实入口为 `../review/b019_native_report.json`。两板65非USB scoped逐项0、完整真实pin/GND/HSE通过；仍剩South7及USB/wholeDRC pending。b018双板61/65为0及4网8DRC历史不可覆盖；b019仅正规pad内接线规范化，未缩短外露铜或提高预算。\n'
if '## 2026-10-22 b017—b019' not in old:readme.write_text(old+append,encoding='utf8')
S=R/'source/engineering_snapshots/b019_padentry';S.mkdir(exist_ok=False);records=[]
for p in [R/'engineering_power/RIGHT_PADENTRY_NORMALIZE_2L_01.json',R/'engineering_power/RIGHT_PADENTRY_NORMALIZE_4L_01.json',R/'engineering_power/readouts/RIGHT_PADENTRY_NORMALIZE_01_manifest.json']:
 dst=S/p.name;shutil.copyfile(p,dst);records.append({'original':str(p),'snapshot':str(dst),'sha256':sha(dst)})
(S/'manifest.json').write_text(json.dumps(records,indent=2),encoding='utf8');print('WROTE_NATIVE_NOTES_AND_FROZEN_PADENTRY_INPUTS')
