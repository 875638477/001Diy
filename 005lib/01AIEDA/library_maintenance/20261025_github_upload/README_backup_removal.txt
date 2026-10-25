GitHub上传准备：重复汇总备份ZIP核验与删除记录
日期：2026-10-25

用户指示：查看大文件，若为备份则可以删除。
已删除唯一汇总备份ZIP：D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pad_psm_merge\cadence_library_maintenance_20261025_full.zip
删除大小：375805598字节（约358.4MiB）；文件SHA256：d544cd9d1c1facffd630b03cc915487bf2c5912165e441271be19ef48272d5eb
该ZIP只是两轮维护记录与三套原始恢复目录的重复汇总包，不是实际PAD/PSM/DRA库依赖。
删除前按历史archive_manifest.csv对26476个原始文件共1955833097字节重新读取，大小和SHA256全部一致。
原始记录树、三套原始恢复目录、readable内直接可读记录及所有实际公共库均保留。
旧archive_manifest和verification文件保留为删除前历史证据；旧README、STATUS、总索引与EDA.md已局部修正，不再声称ZIP仍在。

本次核验与删除结果：backup_zip_removal.json
删除前原件全量验证：backup_zip_originals_verification.json
文档修改前后副本：backup_zip_removal_metadata_before/ 与 backup_zip_removal_metadata_after/
本次执行脚本：remove_verified_backup_zip.py（历史脚本，不自动执行）

保留的原件目录：
D:\001DIY\004computer\lga1700\cadence_library_cleanup_20261025
D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025
D:\001DIY\005lib\_library_suffix_backup_20261025
D:\001DIY\005lib\_library_merge_backup_20261025
D:\001DIY\005lib\_library_geometry_backup_20261025
