> 2026-10-24更新：本历史归档已再次按用户授权清理。当前正式工程为上级项目根的09shape_power_fixed_20261024。下文早期06入口及历史完整迁移清单为当时记录，当前删除范围以本页末尾新清理记录为准。
# 从01AIEDA迁入的LGA1700工程归档

此目录保留本工程转换、修复及封装合并全过程资料。当前可使用工程在项目根06package_merged_20261023，见 [归档说明](../../工程文件归档说明.md) 和 [转换记录](../../转换记录.md)。

- capture/：原examples/lga1700_capture_migration_20261022。
- translator/：原staging/lga1700_migration_20261022。
- pcb_repair/：原staging/lga1700_pcb_repair_20261023。
- project_scripts/：原learning/scripts的五份LGA1700专用脚本。
- project_notes/：原learning/notes的四份本工程案例笔记。
- relocation_audit/：迁移前后路径、大小及SHA256清单、完整复核、06证书脚本备份和独立复算。

14692个原文件迁移前后字节和SHA256相同，见 [校验报告](relocation_audit/move_validation.json)、[路径映射](relocation_audit/path_mapping.json) 及 [文件清单](relocation_audit/final_locations_sha256.csv)。

历史日志、XML、脚本和旧ZIP保留当时路径，没有批量改写证据。旧脚本含固定输入、旧输出和部分失败试验，重新使用时先复制到工程新工作目录、核对映射并配置路径。现有工程使用06入口；后续中间文件继续写本工程。

06证书脚本已改为读取06内配套快照。复算在relocation_audit/certificate_recheck，原脚本在relocation_audit/active06_before，CAD设计及原证书保持原字节。

## 清理后的当前状态（2026-10-23）

已按用户授权删除160个可再生成/重复文件，共2161966302字节。此前完整迁移清单为清理前历史快照，保留原文追溯；当前删除范围、剩余文件和重建方法见 [清理执行记录](../../清理执行记录_20261023.md)。现用06与原始AD完整保留。

## 2026-10-24 保留脚本与关键证据的再次清理

本轮删除160项经逐路径、大小、mtime与SHA核验的大文件，共1,733,712,882字节。归档由2,176,682,913字节降至约442,970,031字节（约443MB，另加本说明更新）。删除内容为重复CAD/旧工程包、已弃用的试验板与大几何转储、可再导出的缓存，以及已保存执行摘要的成功XMATIC流水日志。

保留全部小于等于1MiB的原文件、240份脚本、49份Markdown/PDF、280项指定保护资料和6份必要原始/重建输入；原AD编译pin/net数据、NC/USB缺脚证据、真实封装差异、源线映射、旧DRC几何副作用结论和关键验收证书保留。14,400份剩余原文件已逐SHA核对不变，正式原AD/08/09和09工程包哈希不变。

历史报告和清单仍是执行当时快照；部分旧中间文件链接已删除。两个旧校验输入已有工程外相同SHA替代位置，第三个唯一输入仍保留。57个弃用CAD版本和26个试验大转储属用户授权舍弃历史中间件，不宣称能逐字重建。重跑旧脚本须按本次映射使用保留输入和新的输出目录。

本轮记录与完整清单：[清理说明](../../archive_cleanup_20261024/README.md)、[删除文件清单](../../archive_cleanup_20261024/DELETED_FILES.csv)、[保留资料核验](../../archive_cleanup_20261024/RETAINED_VERIFY_RESULT.json)、[旧输入替代映射](../../archive_cleanup_20261024/cad_rebuild_input_path_replacements.csv)。