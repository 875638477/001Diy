# 当前装配训练资料入口

J55两板实例整改已实际保存、独立原生重开，并由另一数据审查器各822项/合计1644项通过。当前资料仍为 TRAINING_NOT_FOR_ASSEMBLY；HI走线未完成、USB/整板DRC待验、实际阻焊/字体/选料与工厂坐标映射问题保留。

- [两层当前训练BOM/分组/坐标/SMT与THT-DNP分表](JK55_2L_corrected_TRAINING)
- [两层输入身份](JK55_2L_corrected_TRAINING/source_identity.json)
- [四层当前训练BOM/分组/坐标/SMT与THT-DNP分表](JK55_4L_corrected_TRAINING)
- [四层输入身份](JK55_4L_corrected_TRAINING/source_identity.json)

两个目录的coordinates_all80保留原生CAD符号原点/角度，不能直接作为已核准的吸取中心/机台角度；factory旋转列有意为空。65件SMT候选包含J2混装，13件THT+2件DNP显式另列；6个NPTH不算物料。主BOM始终保全部80件，原采购MPN只12件，68件待定。

4L仍为历史L3_GND栈的文字/高度练习，不表示新TOP/L2完整GND/L3电源/BOTTOM推荐已实现。原80位置、272电气针、路由与pad/stack/Film保持；新增72个1MM高度只为用户默认占位，不是实物高度认证。8个原显式高度与4个遗留PlaceBound path保留。

本目录根部带b019的BOM/坐标/装配审核PNG/SVG/开口表均保留为真实输入基线；审核图依据真实物理位置，字是独立callout而非Cadence字体Artwork。当前原生补充丝印/REF装配/VALUE核对制造文件另由唯一执行者输出，不用根部b019审核图冒充。

完整记录：[第55/57课学习笔记](../../../notes/lessonJK_55_57_20261022.md)。审查结果：[1644项](../audits/j55_corrected_independent_summary.json)、[问题登记](../audits/j55_57_issue_registry.json)、[哈希清单](../audits/j55_57_artifact_manifest.json)。
