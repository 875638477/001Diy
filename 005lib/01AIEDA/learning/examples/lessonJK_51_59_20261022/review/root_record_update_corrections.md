# 本轮记录脚本的纠错（2026-10-23）

这些是记录工具自身的错误，不是Cadence设计错误，未被记成学习验收通过。

- 首次通过PowerShell管道传含中文文件名的Python源码，编码转换使课程索引备份路径非法，停在备份阶段。改为ASCII JSON转义传递完整UTF-8源码，写到01AIEDA再执行。
- 将完整代码装入JSON后又嵌套Python三单引号，首稿产生SyntaxError，没有执行；移除内部三引号后再编译。
- 初稿把Python编码名写为utf8-sig，实际应为utf-8-sig；在读取课程索引时停止，未改正文，修正后成功更新9行课程状态及EDA开头计划。
- 一次保存视觉复核的自动审批超时，工具明确命令未启动，允许的一次重试成功；没有把超时算作文件已写或安全拒绝。
- consolidate_JK_progress.py含追加/首次断言，不是可随意重跑的日常入口。后续修改以读当前状态、备份、定点更新为准，不能重跑初始化脚本制造重复记录。

已保留更新前EDA/课程索引及主笔记备份。最终核对以实际文件、链接、JSON字段和SHA为准。

- Newstack CAM delta script initially compared lowercase hexdigest to uppercase expected SHA, incorrectly failed one identity check; actual bytes and native before/after SHA were identical. Kept geometry_delta_failed_hash_case.json, normalized case, reran scoped comparison:34/34PASS.

- 一个可变层功能进度JSON曾被旧门槛清单当作不可变输入；更新实际应用状态后出现来源SHA漂移。未改旧sealed；按内容逆转新增进度块并恢复CRLF，重建的原1188字节快照SHA精确匹配旧清单121D0220…，新旧映射单独保存。后续封存使用字节快照，不直接引用可变current入口作为永不变化来源。
