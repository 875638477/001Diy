公共库维护记录统一归档
日期：2026-10-25（Asia/Shanghai）

用户指定的统一入口：D:\001DIY\005lib\01AIEDA\library_maintenance
本次目录：D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pad_psm_merge

本次同时收录两轮公共库工作：
1. 首轮内容/原生定义去重，以及9种数字0402/0603/0805带后缀封装共18个文件的删除。
2. 按实际尺寸和完整几何继续合并：50个PAD、38个PSM、44个DRA、5个SSM、1个FSM；共138条路径。
两轮计数属于顺序操作，部分路径可能重叠，不可直接相加作为唯一文件数。
C/R/L开头封装保持不动；旧名称保留为共享实体的兼容硬链接。

直接查看：readable/ 内的中文执行记录、合并/删除清单、唯一主文件索引、原生验证和完成校验。
汇总备份ZIP：cadence_library_maintenance_20261025_full.zip 已按用户2026-10-25指示删除。删除前逐项核验26476个原始文件的大小与SHA256全部一致；直接可读记录、两轮完整原始记录树及下面三套原始恢复目录继续保留。
完整源文件清单：archive_manifest.csv / archive_manifest.json（含历史原位置、归档内位置、大小、SHA256）。
删除前ZIP收录26476个原始文件、1955833097字节，来自两轮完整记录树和三套恢复备份；ZIP为这些原件的重复汇总副本，不是Cadence库依赖。
archive_manifest.csv/json、archive_verification.json、publication_verification.json是删除前归档的历史清单与验证证据；不表示ZIP目前仍存在。此次重新核验原件及删除结果见 ../20261025_github_upload/backup_zip_removal.json。

原始记录中的绝对路径按历史原文保留；原工程目录中的记录暂留供既有引用读取。统一查阅和今后新增更改记录以本目录和library_maintenance/INDEX.txt为准。
归档的脚本是历史证据，不自动执行。恢复前先核对应备份清单与库当前状态。
现有恢复目录也继续保留：
D:\001DIY\005lib\_library_suffix_backup_20261025
D:\001DIY\005lib\_library_merge_backup_20261025
D:\001DIY\005lib\_library_geometry_backup_20261025
上述三套恢复原件及脚本未删除；此前ZIP中backups/的重复副本随ZIP一并删除。两轮完整记录树仍位于 D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025 与 D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025。

实际公共库仍使用既定01Pad_lib、01Psm_lib、01captureLib等目录，本次仅归档记录与更新入口，不改动CAD库内容、PCB、DSN或网表。
后续所有公共库维护：直接在01AIEDA/library_maintenance下按日期/任务记录工作过程、变更清单、验证与备份，并同步更新EDA.md和总索引。
