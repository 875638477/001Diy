# 第60课：资料与可迁移操作库

日期：2026-10-23。本轮资料、依赖与同机重定位复现已验；另一台电脑实机与本轮GUI仍未验。

- [完整学习笔记](../../notes/lesson60_20261023.md)
- [迁移/关机恢复手册](MIGRATION.md)
- [最小迁移练习ZIP](eda60-portable-kit.zip)及[包内容与校验](review/portable_kit_validation.json)
- [本地技能源](../../skills/cadence17-learning/SKILL.md)
- [原生操作包及命令](package/README.md)
- [来源学习笔记](../../notes/lesson60_sources_20261023.md)与[实际教程记录](sources/tutorial_records.json)
- [环境依赖笔记](../../notes/lesson60_dependencies_20261023.md)与[迁移清单](inventory/migration_checklist.json)
- [原生复现笔记](../../notes/lesson60_native_replay_20261023.md)
- [独立原始记录复核](review/independent_replay_review.json)：313项通过
- [技能独立评审](review/skill_forward_review.json)、[预检覆盖风险修复](review/preflight_forward_fix_validation.json)
- [异常关机恢复检查](review/recovery_after_shutdown.json)

正式accepted run只有package/runs/final03和native/R Space/runs/move01，各42项通过；它们是同一电脑的两个路径。其他run/失败脚本留作历史，不能混算为最终验收。修正后的932段非空走线读取已核，旧33项缺少实际段的报告不证明走线保真。

ZIP仅含自有fixture、最终源码、示例配置、技能与记录模板，不是完整01AIEDA备份。不含Cadence/许可、Python安装、原书/视频；外部源和目标机安装另核。输入与输出均为训练设计，第60课不关闭H/I或J/K整板/制造/实物待办。

最终清单使用课内冻结快照，EDA、课程索引和技能源的后续更新不改写本课历史。全部文件仍在用户指定01AIEDA内部。
