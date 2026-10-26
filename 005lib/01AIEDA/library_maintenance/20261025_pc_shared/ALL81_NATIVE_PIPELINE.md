# 现有PCB改用公共封装：批准旋转、连接修复及完整读回

本记录解释项目13剩余50件的工作脚本。工程冻结清单和原生输出在工程 `w/pcb_migration/all81_migration_v7`；通用方法和生成器保留在本学习库。实际最终通过状态以新进程报告为准。

## 输入及批准变化

输入为已经完成34个SOT23迁移和92条焊盘内附着短线的副本，SHA256 `06B8DD73EE20A4C01A0BF36E0BF6CD0FDDFE20CE2F89DA430A2C003414BE9405`。原49AF板的全部84件批准计划包括该34件及余下50件，不重复改已完成的34件。

`project81_final_canonical_plan13/ALL81_PHYSICAL_REF_MIGRATION.tsv` 冻结84件、30种旧封装。`project81_expected_pins13/ALL81_EXPECTED_PINS6521.ilist` 是完整6521个物理焊盘表，不能只校验发生坐标变化的246脚。机械焊盘、空编号、原生nil网络、空字符串NC均保留。

余下50件仅9件批准旋转：U5、AU1为−90°；Q39及PU3/4/5/6/7/9为+90°。器件原点、镜像和全部1066个实例的文字世界坐标不随封装变更移动。转换后的逐脚坐标、焊盘名和网络必须等于冻结表。

## 原生顺序

1. 在替换前，使用 `all81_adjacency_probe.il` 的 `pc13All50Adjacency("source" dir)` 导出余下50件全部964个物理焊盘的真实邻居。按照编号和世界坐标同时定位，不能用同号第一个焊盘代替重复编号机械焊盘。
2. 使用 `pc13_native_replace_v7.il` 的 `pc13All50Apply(dir)`，先守完整源6521脚及1066姿态，再逐件Alt替换。非零旋转使用官方 `axlTransformObject(symbol ?angle delta ?origin originalXY)`；随后恢复完整原文字字段并核批准姿态、引脚、网络、属性。临时ALT_SYMBOLS属性必须还原。
3. 全部实际符号已改名后，以新Capture PST执行 `netrev -y2` 同步逻辑package。直接把新PST导入尚未更名的旧实际符号会取消放置；Always重新重组路径也曾改变源连接，因此不能代替该顺序。
4. 用 `pc13AllRestore(snapshot dir)` 恢复ECO可能重排的全部实例文字。再以新进程、只读加载 `all81_fresh_v8.il`，调用 `pc13AllFresh(snapshot dir)`，核完整6521脚、1066文字/姿态和不滤行的1066个package/symbol/definition名字，并导出全板真实连接、规则和图形。
5. 同一目标副本导出 `pc13All50Adjacency("target" dir)`。根据源真实邻接及完整分区差异，以 `prepare_all81_source_path_stubs.py` 冻结必要的原真实端点候选；原生仅选择完整带宽圆端stroke位于实际新pad铜内的短线。所有候选预检完才写，保留原走线。
6. 保存后再次新进程读回，独立核全部6521物理焊盘的严格类型和网络、完整2020连接分区的成员多重集、1118网络状态、1066姿态/文字、完整CFX/TCFX及实际公共库定义。若源只与shape相连的脚发生分区变化，必须单独查真实铜形接触，不由脚号或网络名自动造铜。

## 合法的超时处理

`axlDBCloak(... 'shape)` 在批函数结束后仍要完成延迟的DRC、connectivity和dynamic shape更新。回调已经写完50行applied不表示已安全保存。首轮源邻接和50个即时检查完成后，在180秒保护时间内未完成cloak收尾，只有临时进程被停止；原输入保持原SHA，失败证据保留。

第二轮复用已完成源邻接，只重跑同一v7 Alt，在600秒保护时间内完成了原生保存和 `PC13_REPLACE_COMPLETE changed=50 original_drc=t final_drc=t`。保存前有一次SPMHUT-48缩放舍入提示，因此仍必须执行新进程完整脚表和几何门，不能因为保存成功忽略舍入。

备用 `pc13_native_replace_batch10_v8.il` 每10件结束一次合法shape cloak，完整核原/批准目标混合状态的全部6521脚和1066姿态后再保存检查点。恢复时只允许每件处于冻结原状态或已批准目标状态；不能任意接收混合状态，也不能通过忽略shape、FIXED或改变DRC状态来加速。该备用分批脚本已生成，尚未用其产生正式设计。

## 原生接口依据

本机17.2文档 `doc/algroskill/06intedt.html#821370` 说明 `axlTransformObject` 的angle/origin参数。`doc/algroskill/17dbtran.html#1065349` 说明 `axlDBCloak` 批处理net-based DRC、connectivity及可选dynamic shape更新。完整附着短线方法及已验证34件案例见 [PCB_PAD_ATTACHMENT_REPAIR.md](PCB_PAD_ATTACHMENT_REPAIR.md)。
