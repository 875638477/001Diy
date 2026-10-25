# 第14课原生工程与库

优先打开 `c14_ready.dsn`。它与 `c14_replace_properties.dsn` 的工程内容相同，已通过独立 Capture 17.2 原生数据库进程重开验证。符号为 QMI8610_C12，U1401、U1402 均关联 `qmi8610_lga16_3d3_p0d5`。这是部分连接的课程练习，继续应用电路前还需完成其余连接与 ERC。

`c14_update_preserve.dsn`、`c14_relocated_preserve.dsn` 是保留属性的对照，U1402 故意保留 `C14_PROP_SENTINEL_NOT_FOR_PCB` 足迹测试值，只供学习对比。它们本轮采用同一已验证的原生受控替换方法；文件名不代表 UpdateCache API 已通过。

`library` 内为最终 OLB、DRA、PSM、PAD。Capture 添加 `c14_qmi8610_v2.olb`；Allegro 的学习用工程将以下路径加入 `psmpath` 与 `padpath`：

`D:/001DIY/005lib/01AIEDA/learning/examples/lesson14_capture/final/library`

本次没有修改用户 env。PCB Footprint 填不带扩展名的 `qmi8610_lga16_3d3_p0d5`。物理脚号是1—16，没有 EP17。

[完整学习记录](../../../notes/lesson14_library_propagation_20261019.md) · [81项检查及SHA](../../../logs/lesson14_capture_20261019/validation.json)
